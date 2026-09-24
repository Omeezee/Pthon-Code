# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:00:59 2025

@author: geode
"""
# exam2_solver.py — general axial bar solver for your take-home
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Tuple, Union
import sys
import numpy as np

# try scipy for .mat i/o. only needed if you pass a .mat path.
try:
    import scipy.io as sio
except Exception:
    sio = None


# ====================== data containers ======================

@dataclass
class BarInput:
    # cleaned version of the matlab “bar” struct
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
    # everything the grader will look for
    IntLoad: np.ndarray
    UncMDef: np.ndarray
    UncTDef: np.ndarray
    React0: float
    React1: float
    TotLoad: np.ndarray
    MecDef: np.ndarray
    TotDef: np.ndarray
    Stress: np.ndarray
    # extras that help show correctness
    comp_residual: float
    force_residual: float
    trap_panels_used: np.ndarray  # how many subpanels each element needed to converge


# ====================== i/o helpers ======================

def _to_1d_float(x) -> np.ndarray:
    # normalize whatever matlab gives into a flat float array
    a = np.atleast_1d(np.array(x, dtype=float))
    return a.reshape(-1)

def _barinput_from_mat_struct(b) -> BarInput:
    # builds our dataclass from the raw matlab object (temp['bar'][0,0])
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
    # reads the .mat and converts to BarInput
    if sio is None:
        raise RuntimeError("need scipy to read .mat files (pip install scipy)")
    m = sio.loadmat(path, struct_as_record=False, squeeze_me=True)
    b = m["bar"]
    return _barinput_from_mat_struct(b)


# ====================== numerics ======================

def cumulative_right_loads(endload: np.ndarray) -> np.ndarray:
    # fr[i] = sum of nodal loads to the right of element i
    c = np.flip(np.cumsum(np.flip(endload)))
    return c[1:]

def trap_S(L, A1, A2, E1, E2, n_sub):
    # trapezoid for ∫ 1/(a(x)*e(x)) dx with linear a and e along the element
    if A1 <= 0 or A2 <= 0 or E1 <= 0 or E2 <= 0:
        raise ValueError("area/modulus must stay positive within each element")
    if A1 == A2 and E1 == E2:
        # constant props: closed form, no need to integrate
        return L / (A1 * E1)
    n_sub = max(2, int(n_sub))
    x = np.linspace(0.0, L, n_sub)
    t = x / L if L > 0 else x
    A = A1 + (A2 - A1) * t
    E = E1 + (E2 - E1) * t
    return np.trapz(1.0 / (A * E), x)

def trap_S_converged(L, A1, A2, E1, E2, n0=8, tol=1e-6, nmax=1 << 17):
    # doubles panels until the change is tiny; returns s and panels used
    n = max(2, int(n0))
    s0 = trap_S(L, A1, A2, E1, E2, n)
    while True:
        n2 = min(2 * n, nmax)
        s1 = trap_S(L, A1, A2, E1, E2, n2)
        if abs(s1 - s0) <= tol * max(1.0, abs(s1)) or n2 == nmax:
            return s1, n2
        s0, n = s1, n2

def build_compliances(L, A1, A2, E1, E2, n0, tol):
    # computes s_i and keeps track of panel counts for your convergence write-up
    n = len(L)
    S = np.zeros(n)
    used = np.zeros(n, dtype=int)
    for i in range(n):
        S[i], used[i] = trap_S_converged(L[i], A1[i], A2[i], E1[i], E2[i], n0=n0, tol=tol)
    return S, used


# ====================== core solver ======================

def solve_bar(
    bar: BarInput,
    constraint: str = "both",
    conv_tol: float = 1e-6,
    integrate_variable_props: bool = True,
) -> BarResult:
    """
    general solver: mechanical + thermal + end gap + static indeterminacy
    constraint: "both" (fixed-fixed), "left", "right", or "none"
    integrate_variable_props: if false, just uses area1/modu1 (no extra credit)
    """
    n = bar.NElem
    L, A1, A2 = bar.Leng, bar.Area1, bar.Area2
    E1, E2    = bar.Modu1, bar.Modu2
    alpha, dT = bar.Alph, bar.DeltT
    P_end     = bar.EndLoad

    if len(P_end) != n + 1:
        raise ValueError("EndLoad must have n+1 values (one per node)")

    # internal force from nodal loads only (right cumulative)
    FR = cumulative_right_loads(P_end)
    IntLoad = np.flip(np.cumsum(np.flip(P_end)))[1:]

    # element compliances
    if integrate_variable_props:
        S, used = build_compliances(L, A1, A2, E1, E2, n0=max(2, bar.Nistp), tol=conv_tol)
    else:
        # no integration path (area and modulus taken at left side)
        S = L / (A1 * E1)
        used = np.full(n, 1, dtype=int)  # just to keep the field present

    # unconstrained deflections (mechanical from IntLoad, thermal from alpha*Δt*l)
    UncMDef = IntLoad * S
    UncTDef = alpha * (dT - bar.initT) * L

    # solve the uniform shift r from compatibility + equilibrium based on bc
    if constraint == "both":
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

    # final forces and deflections
    TotLoad = IntLoad + R
    MecDef  = UncMDef + R * S
    TotDef  = MecDef + UncTDef

    # stress (average area is solid for linear a(x))
    Aavg   = 0.5 * (A1 + A2)
    Stress = TotLoad / Aavg

    # residual checks for your printout
    force_residual = abs(React0 + React1 + np.sum(P_end))
    comp_residual  = abs(np.sum(TotDef) - bar.EndGap) if constraint == "both" else np.nan

    return BarResult(
        IntLoad=IntLoad, UncMDef=UncMDef, UncTDef=UncTDef,
        React0=float(React0), React1=float(React1),
        TotLoad=TotLoad, MecDef=MecDef, TotDef=TotDef, Stress=Stress,
        comp_residual=float(comp_residual), force_residual=float(force_residual),
        trap_panels_used=used,
    )


# ====================== simple drivers ======================

def quick_solve(x: Union[str, Any], **kwargs) -> Dict[str, Any]:
    """
    super simple wrapper:
    - if x is a str path like 'Prob2.04.mat', it loads and solves it
    - if x is a raw matlab struct (temp['bar'][0,0]), it converts and solves it
    returns a plain dict ready to display or export
    """
    if isinstance(x, str):
        bar = load_bar_mat(x)
        tag = x
    else:
        bar = _barinput_from_mat_struct(x)
        tag = "<matlab struct>"
    out = solve_bar(bar, **kwargs)
    return {
        "tag": tag,
        "React0": out.React0, "React1": out.React1,
        "IntLoad": out.IntLoad, "TotLoad": out.TotLoad,
        "UncMDef": out.UncMDef, "UncTDef": out.UncTDef,
        "MecDef": out.MecDef, "TotDef": out.TotDef,
        "Stress": out.Stress,
        "force_residual": out.force_residual,
        "comp_residual": out.comp_residual,
        "trap_panels_used": out.trap_panels_used,
    }

def print_result(d: Dict[str, Any]):
    # clean console print that matches what profs like to see
    print(f"\n=== {d['tag']} ===")
    print(f"reactions -> left: {d['React0']:.6g}   right: {d['React1']:.6g}")
    print(f"residuals -> force: {d['force_residual']:.3e}   compat: {d['comp_residual']:.3e}")
    print("\ni :   IntLoad         TotLoad         Stress[Pa]         TotDef[m]")
    n = len(d["IntLoad"])
    for i in range(n):
        print(
            f"{i+1:2d}: {d['IntLoad'][i]: .6g}   {d['TotLoad'][i]: .6g}   "
            f"{d['Stress'][i]: .6g}   {d['TotDef'][i]: .6g}"
        )

def print_convergence(d: Dict[str, Any]):
    # shows how many trap panels each element needed → perfect for your convergence note
    used = d["trap_panels_used"]
    if used is None or np.size(used) == 0:
        print("\nconvergence: not applicable (integration disabled)")
        return
    print("\nconvergence (trap panels used per element):")
    for i, k in enumerate(used, start=1):
        print(f"  elem {i:2d}: {int(k)} panels")

def run_many(paths: Iterable[str], **kwargs):
    # batch runner for the graded files
    for p in paths:
        try:
            d = quick_solve(p, **kwargs)
            print_result(d)
            print_convergence(d)
        except Exception as e:
            print(f"{p}: error — {e}")


# ====================== cli entry (so you can just run it) ======================

if __name__ == "__main__":
    # usage:
    #   python exam2_solver.py Prob2.04.mat
    #   python exam2_solver.py Prob2.05.mat --no-var
    # flags:
    #   --no-var   -> turn off variable A/E integration (just use area1, modu1)
    use_var = True
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if any(a in ("--no-var", "--novar", "--const") for a in sys.argv[1:]):
        use_var = False

    if len(args) >= 1:
        path = args[0]
        d = quick_solve(path, constraint="both", conv_tol=1e-6, integrate_variable_props=use_var)
        print_result(d)
        print_convergence(d)
    else:
        print("usage: python exam2_solver.py <matfile> [--no-var]")
        print("tip: pass --no-var to skip a(x), e(x) integration and just use area1/modu1")
        print("you can also import quick_solve / run_many from python and batch the graded files")

