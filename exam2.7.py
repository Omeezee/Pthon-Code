# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:00:42 2025

@author: geode
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Iterable, Union
import sys
import numpy as np


try:
    import scipy.io as sio
except Exception:
    sio = None  # we only complain if you call a function that needs it


# ============== data containers ==============

@dataclass
class BarInput:
    NElem: int
    initT: float
    Nistp: int
    Leng:  np.ndarray
    Area1: np.ndarray
    Area2: np.ndarray
    Modu1: np.ndarray
    Modu2: np.ndarray
    Alph:  np.ndarray
    DeltT: np.ndarray
    EndGap: float
    EndLoad: np.ndarray

@dataclass
class BarResult:
    IntLoad: np.ndarray
    UncMDef: np.ndarray
    UncTDef: np.ndarray
    React0: float
    React1: float
    TotLoad: np.ndarray
    MecDef: np.ndarray
    TotDef: np.ndarray
    Stress: np.ndarray
    comp_residual: float
    force_residual: float


# ============== small utils ==============

def _to_1d_float(x) -> np.ndarray:
    # make sure it’s a flat 1d float array
    a = np.atleast_1d(np.array(x, dtype=float))
    return a.reshape(-1)

def _barinput_from_mat_struct(b) -> BarInput:
    # take raw matlab struct object (like temp['bar'][0,0]) and normalize it
    return BarInput(
        NElem  = int(b.NElem),
        initT  = float(getattr(b, "initT", 0.0)),
        Nistp  = int(getattr(b, "Nistp", 8)),
        Leng   = _to_1d_float(b.Leng),
        Area1  = _to_1d_float(getattr(b, "Area1", b.Area)),
        Area2  = _to_1d_float(getattr(b, "Area2", b.Area1)),
        Modu1  = _to_1d_float(getattr(b, "Modu1", b.Modu)),
        Modu2  = _to_1d_float(getattr(b, "Modu2", b.Modu1)),
        Alph   = _to_1d_float(getattr(b, "Alph", 0.0)),
        DeltT  = _to_1d_float(getattr(b, "DeltT", 0.0)),
        EndGap = float(getattr(b, "EndGap", 0.0)),
        EndLoad= _to_1d_float(getattr(b, "EndLoad", b.P if hasattr(b, "P") else 0.0)),
    )

def load_bar_mat(path: str) -> BarInput:
    # read the matlab file that has a struct named 'bar' and convert it
    if sio is None:
        raise RuntimeError("need scipy to read .mat files (pip install scipy)")
    m = sio.loadmat(path, struct_as_record=False, squeeze_me=True)
    b = m["bar"]
    return _barinput_from_mat_struct(b)


# ============== numerics ==============

def cumulative_right_loads(endload: np.ndarray) -> np.ndarray:
    # sum of nodal loads to the right of each element
    c = np.flip(np.cumsum(np.flip(endload)))
    return c[1:]

def trap_S(L, A1, A2, E1, E2, n_sub):
    # trapezoid for ∫ 1/(a(x)*e(x)) dx with a,e linear across the element
    if A1 <= 0 or E1 <= 0 or A2 <= 0 or E2 <= 0:
        raise ValueError("area/modulus must stay positive across the element")
    if A1 == A2 and E1 == E2:
        return L / (A1 * E1)
    n_sub = max(2, int(n_sub))
    x = np.linspace(0.0, L, n_sub)
    t = x / L if L > 0 else x
    A = A1 + (A2 - A1) * t
    E = E1 + (E2 - E1) * t
    return np.trapz(1.0 / (A * E), x)

def trap_S_converged(L, A1, A2, E1, E2, n0=8, tol=1e-6, nmax=1 << 17):
    # double panels until the answer stops changing much
    n = max(2, int(n0))
    s0 = trap_S(L, A1, A2, E1, E2, n)
    while True:
        n2 = min(2 * n, nmax)
        s1 = trap_S(L, A1, A2, E1, E2, n2)
        if abs(s1 - s0) <= tol * max(1.0, abs(s1)) or n2 == nmax:
            return s1, n2
        s0, n = s1, n2

def build_compliances(L, A1, A2, E1, E2, n0, tol):
    # compute s_i for every element and track how many panels we used (for your write-up)
    n = len(L)
    S = np.zeros(n)
    used = np.zeros(n, dtype=int)
    for i in range(n):
        S[i], used[i] = trap_S_converged(L[i], A1[i], A2[i], E1[i], E2[i], n0=n0, tol=tol)
    return S, used


# ============== core solver ==============

def solve_bar(bar: BarInput, constraint="both", conv_tol=1e-6) -> BarResult:
    # general solver: handles constant/variable a,e and thermal
    n = bar.NElem
    L, A1, A2 = bar.Leng, bar.Area1, bar.Area2
    E1, E2    = bar.Modu1, bar.Modu2
    alpha, dT = bar.Alph, bar.DeltT
    P_end     = bar.EndLoad

    if len(P_end) != n + 1:
        raise ValueError("EndLoad should be length n+1 (one value per node)")

    # internal force from nodal loads (right cumulative)
    FR = cumulative_right_loads(P_end)
    IntLoad = np.flip(np.cumsum(np.flip(P_end)))[1:]

    # element compliances with convergence check
    S, _used = build_compliances(L, A1, A2, E1, E2, n0=max(2, bar.Nistp), tol=conv_tol)

    # free mechanical and thermal deflections
    UncMDef = IntLoad * S
    UncTDef = alpha * (dT - bar.initT) * L

    # pick reactions based on end condition
    if constraint == "both":
        # compatibility with gap gives uniform shift r
        R = (np.sum(UncTDef) - bar.EndGap - np.sum(FR * S)) / np.sum(S)
        React1 = -R
        React0 = -np.sum(P_end) - React1
    elif constraint == "left":
        React1 = 0.0
        React0 = -np.sum(P_end)
        R = -React1
    elif constraint == "right":
        React0 = 0.0
        React1 = -np.sum(P_end)
        R = -React1
    elif constraint == "none":
        React0 = 0.0
        React1 = 0.0
        R = 0.0
    else:
        raise ValueError("constraint must be 'both', 'left', 'right', or 'none'")

    # final internal forces/deflections
    TotLoad = IntLoad + R
    MecDef  = UncMDef + R * S
    TotDef  = MecDef + UncTDef

    # stress using average area (solid for linear a(x))
    Aavg   = 0.5 * (A1 + A2)
    Stress = TotLoad / Aavg

    # quick sanity checks
    force_residual = abs(React0 + React1 + np.sum(P_end))
    comp_residual  = abs(np.sum(TotDef) - bar.EndGap) if constraint == "both" else np.nan

    return BarResult(
        IntLoad=IntLoad, UncMDef=UncMDef, UncTDef=UncTDef,
        React0=float(React0), React1=float(React1),
        TotLoad=TotLoad, MecDef=MecDef, TotDef=TotDef, Stress=Stress,
        comp_residual=float(comp_residual), force_residual=float(force_residual),
    )


# ============== super-simple entry points you asked for ==============

def quick_solve(x: Union[str, Any], constraint="both", conv_tol=1e-6) -> Dict[str, Any]:
    """
    super chill wrapper:
    - if x is a string path like 'Prob2.04.mat', we load and solve it
    - if x is a raw matlab struct (temp['bar'][0,0]), we coerce and solve it
    returns a plain dict you can print or inspect
    """
    if isinstance(x, str):
        bar = load_bar_mat(x)
    else:
        bar = _barinput_from_mat_struct(x)
    out = solve_bar(bar, constraint=constraint, conv_tol=conv_tol)
    return {
        "React0": out.React0, "React1": out.React1,
        "IntLoad": out.IntLoad, "TotLoad": out.TotLoad,
        "UncMDef": out.UncMDef, "UncTDef": out.UncTDef,
        "MecDef": out.MecDef, "TotDef": out.TotDef,
        "Stress": out.Stress,
        "force_residual": out.force_residual,
        "comp_residual": out.comp_residual,
    }

def run_and_print(x: Union[str, Any], constraint="both", conv_tol=1e-6) -> Dict[str, Any]:
    # same as quick_solve but prints a compact table for you
    d = quick_solve(x, constraint=constraint, conv_tol=conv_tol)
    print("\n=== result ===")
    print(f"reactions -> left: {d['React0']:.6g}  right: {d['React1']:.6g}")
    print(f"residuals -> force: {d['force_residual']:.3e}  compat: {d['comp_residual']:.3e}")
    print("i :   IntLoad        TotLoad        Stress[Pa]        TotDef[m]")
    n = len(d["IntLoad"])
    for i in range(n):
        print(f"{i+1:2d}: {d['IntLoad'][i]: .6g}  {d['TotLoad'][i]: .6g}  {d['Stress'][i]: .6g}  {d['TotDef'][i]: .6g}")
    return d


# ============== cli mode (so you can just: python exam2_solver.py Prob2.04.mat) ==============

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        path = sys.argv[1]            # first arg is the .mat file path
        run_and_print(path)           # load+solve+print
    else:
        print("usage: python exam2_solver.py <matfile>")
        print("or from python:")
        print("  from exam2_solver import run_and_print, quick_solve")
        print("  run_and_print('Prob2.04.mat')")
        print("  # or with your raw matlab struct style:")
        print("  import scipy.io as sio")
        print("  temp = sio.loadmat('Prob2.04.mat', struct_as_record=False)")
        print("  bar = temp['bar'][0,0]")
        print("  run_and_print(bar)")
