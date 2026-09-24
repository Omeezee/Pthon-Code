# exam2_solver_matched.py — same names as your drafts but cleaned up + complete
# comments are chill, lowercase, and short like your style

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Iterable, Union
import numpy as np

try:
    import scipy.io as sio  # for .mat i/o
except Exception:
    sio = None


# ========= data class to mirror "bar" =========

@dataclass
class BarInput:
    NElem: int
    initT: float
    Nistp: int
    Leng:  np.ndarray      # L
    Area1: np.ndarray      # A at left
    Area2: np.ndarray      # A at right (can equal Area1)
    Modu1: np.ndarray      # E at left
    Modu2: np.ndarray      # E at right (can equal Modu1)
    Alph:  np.ndarray      # alpha
    DeltT: np.ndarray      # delta T per element
    EndGap: float          # gap at right end
    EndLoad: np.ndarray    # nodal loads (size n+1)


# ========= helpers to read/normalize inputs =========

def _to_1d_float(x) -> np.ndarray:
    a = np.atleast_1d(np.array(x, dtype=float))
    return a.reshape(-1)

def bar_from_struct(b) -> BarInput:
    # takes temp['bar'][0,0] or squeezed version and cleans it up
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
    if sio is None:
        raise RuntimeError("need scipy to read .mat files (pip install scipy)")
    m = sio.loadmat(path, struct_as_record=False, squeeze_me=True)
    return bar_from_struct(m["bar"])


# ========= math bits (names kept) =========

def _validate_shapes(L, A, E, EndLoad) -> int:
    # quick sanity checks so nothing explodes later
    n = len(L)
    if len(A) != n or len(E) != n:
        raise ValueError("A and E length must match L.")
    if len(EndLoad) != n + 1:
        raise ValueError("EndLoad must have n+1 values (one per node).")
    return n

def cumulative_right_loads(EndLoad: np.ndarray) -> np.ndarray:
    # fr[i] = sum of nodal loads to the right of element i
    c = np.flip(np.cumsum(np.flip(EndLoad)))
    return c[1:]

def element_compliance_trap(Li, A1, A2, E1, E2, nsub):
    # ∫ 0..L 1/(A(x)E(x)) dx, with A,E linear across the element
    if A1 <= 0 or A2 <= 0 or E1 <= 0 or E2 <= 0:
        raise ValueError("area and modulus must be positive along the element")
    if A1 == A2 and E1 == E2:
        return Li / (A1 * E1)  # constant props, closed form

    nsub = max(2, int(nsub))   # at least two panels
    x = np.linspace(0.0, Li, nsub)
    t = x / Li if Li > 0 else x
    A = A1 + (A2 - A1) * t
    E = E1 + (E2 - E1) * t
    return np.trapz(1.0 / (A * E), x)

def trap_S_converged(Li, A1, A2, E1, E2, n0=8, tol=1e-6, nmax=1 << 17) -> Tuple[float, int]:
    # doubles panels until change is tiny
    n = max(2, int(n0))
    s0 = element_compliance_trap(Li, A1, A2, E1, E2, n)
    while True:
        n2 = min(2 * n, nmax)
        s1 = element_compliance_trap(Li, A1, A2, E1, E2, n2)
        if abs(s1 - s0) <= tol * max(1.0, abs(s1)) or n2 == nmax:
            return s1, n2
        s0, n = s1, n2

def build_compliances_trap(L, Area1, Area2, Modu1, Modu2, nsub_or_seed, tol=1e-6):
    # builds s[i] for each element, also returns how many panels were used
    n = len(L)
    s = np.zeros(n)
    used = np.zeros(n, dtype=int)
    for i in range(n):
        s[i], used[i] = trap_S_converged(L[i], Area1[i], Area2[i], Modu1[i], Modu2[i],
                                         n0=nsub_or_seed, tol=tol)
    return s, used

def thermal_free_def(Alph, DeltT, initT, L):
    # δ_th[i] = alpha * (ΔT - initT) * L
    dT = np.asarray(DeltT, float) - float(initT)
    return np.asarray(Alph, float) * dT * np.asarray(L, float)

def compute_F_right_with_thermal(s, EndLoad, EndGap, th):
    # compatibility w/ thermal + gap → solve for right reaction
    FR = cumulative_right_loads(EndLoad)
    S  = float(np.sum(s))
    C  = float(np.dot(FR, s))
    TH = float(np.sum(th))
    if abs(S) < 1e-18:
        raise ZeroDivisionError("total compliance is ~0, check A/E")
    return (TH - EndGap - C) / S

def combine_mech_and_thermal(delta_mech, delta_th):
    # δ_tot = δ_mech + δ_th
    return np.asarray(delta_mech, float) + np.asarray(delta_th, float)


# ========= solvers (names kept) =========

def solve_series_bar(L, A, E, EndLoad, EndGap):
    # constant A/E, no thermal — mechanical only + end gap
    n = _validate_shapes(L, A, E, EndLoad)
    L = np.asarray(L, float); A = np.asarray(A, float); E = np.asarray(E, float)
    s = L / (A * E)                         # compliance per element
    S = float(np.sum(s));  FR = cumulative_right_loads(EndLoad)
    C = float(np.dot(FR, s))                # sum(FR_i * s_i)
    F_right = -(EndGap + C) / S             # from compatibility (gap only)
    F_left  = -F_right - float(np.sum(EndLoad))  # equilibrium
    N_int   = -(F_right + FR)               # internal force in each element
    delta   = N_int * s                     # mech deformation per element
    u = np.zeros(n + 1);  u[1:] = np.cumsum(delta)  # nodal displacements
    sigma   = N_int / A                     # stress

    TotLoad = np.array(EndLoad, float)      # include reactions for a check
    TotLoad[0]  += F_left
    TotLoad[-1] += F_right
    eq_residual  = abs(np.sum(TotLoad))
    comp_balance = float(np.sum(delta) - EndGap)

    return {
        "F_left": F_left, "F_right": F_right, "N_int": N_int.tolist(),
        "delta": delta.tolist(), "u": u.tolist(), "sigma": sigma.tolist(),
        "TotLoad": TotLoad.tolist(), "eq_residual": float(eq_residual),
        "comp_balance": float(comp_balance), "s": s.tolist()
    }

def solve_with_constraints(L, A1, E1, EndLoad, EndGap,
                           constraint="both",
                           Alph=None, DeltT=None, initT=0.0,
                           Area2=None, Modu2=None, nsub=8, tol=1e-6):
    # full solver: variable A/E (linear), thermal, gap, end constraints
    n = _validate_shapes(L, A1, E1, EndLoad)
    L  = np.asarray(L,  float)
    A1 = np.asarray(A1, float); E1 = np.asarray(E1, float)
    Area2 = A1 if Area2 is None else np.asarray(Area2, float)
    Modu2 = E1 if Modu2 is None else np.asarray(Modu2, float)
    Alph  = np.zeros(n) if Alph  is None else np.asarray(Alph,  float)
    DeltT = np.zeros(n) if DeltT is None else np.asarray(DeltT, float)

    # compliances via trap rule (with convergence)
    s, used = build_compliances_trap(L, A1, Area2, E1, Modu2, nsub_or_seed=nsub, tol=tol)

    # free thermal elongations
    th = thermal_free_def(Alph, DeltT, initT, L)

    # pick reactions based on constraint
    sumP = float(np.sum(EndLoad))
    if constraint == "both":
        F_right = compute_F_right_with_thermal(s, EndLoad, EndGap, th)
        F_left  = -F_right - sumP
    elif constraint == "left":
        F_right = 0.0; F_left = -sumP
    elif constraint == "right":
        F_left = 0.0;  F_right = -sumP
    elif constraint == "none":
        F_left = 0.0;  F_right = 0.0
    else:
        raise ValueError("constraint must be 'both','left','right','none'")

    # internal loads + deformations
    FR        = cumulative_right_loads(EndLoad)
    N_int     = -(F_right + FR)
    delta_mech= N_int * s
    delta_tot = combine_mech_and_thermal(delta_mech, th)

    # nodal displacements (start at 0)
    u = np.zeros(n + 1); u[1:] = np.cumsum(delta_tot)

    # loads including reactions, for residual check
    TotLoad = np.array(EndLoad, float)
    TotLoad[0]  += F_left
    TotLoad[-1] += F_right
    eq_residual = abs(np.sum(TotLoad))
    comp_res    = abs(np.sum(delta_tot) - EndGap) if constraint == "both" else np.nan

    # section stress using average area (good for linear a(x))
    Aavg  = 0.5 * (A1 + Area2)
    sigma = N_int / Aavg

    return {
        "F_left": F_left, "F_right": F_right,
        "N_int": N_int.tolist(),
        "delta_mech": delta_mech.tolist(),
        "delta_th": th.tolist(),
        "delta": delta_tot.tolist(),
        "u": u.tolist(),
        "TotLoad": TotLoad.tolist(),
        "eq_residual": float(eq_residual),
        "comp_balance": float(comp_res) if np.isfinite(comp_res) else None,
        "s": s.tolist(),
        "sigma": sigma.tolist(),
        "trap_panels_used": used.tolist(),
    }


# ========= small runners, same vibe as yours =========

def print_results(L, A, E, EndLoad, EndGap, res):
    n = len(L)
    print("given data:")
    print("L:", L); print("A:", A); print("E:", E)
    print("EndLoad:", EndLoad); print("EndGap:", EndGap); print()

    print("reactions:")
    print("left:", res["F_left"], "N")
    print("right:", res["F_right"], "N")
    print("force balance residual:", res.get("eq_residual", 0.0))
    if "comp_balance" in res and res["comp_balance"] is not None:
        print("compatibility residual:", res["comp_balance"])
    print()

    print("section results:")
    if "sigma" in res:
        sigma = res["sigma"]
    else:
        sigma = [res["N_int"][i] / A[i] for i in range(n)]
    delta = res["delta"] if "delta" in res else res["delta_mech"]
    for i in range(n):
        print(f"section {i+1}")
        print("  N:", res["N_int"][i], "N")
        print("  stress:", sigma[i], "Pa")
        print("  deformation:", delta[i], "m")
    print()

    print("nodal displacements:")
    for j, uj in enumerate(res["u"]):
        print(f"  node {j}: u = {uj} m")

def mech_main(bar: Union[BarInput, Dict[str, Any], None] = None,
              use_variable_props: bool = True,
              constraint: str = "both",
              nsub: int = 8, tol: float = 1e-6) -> Dict[str, Any]:
    # quick front door, mirrors the matlab vibe
    if bar is None:
        raise ValueError("pass a BarInput or use load_bar_mat(path) first")
    if isinstance(bar, dict) or not hasattr(bar, "NElem"):
        # assume matlab struct
        bar = bar_from_struct(bar)

    if use_variable_props:
        res = solve_with_constraints(
            L=bar.Leng, A1=bar.Area1, E1=bar.Modu1, EndLoad=bar.EndLoad, EndGap=bar.EndGap,
            constraint=constraint, Alph=bar.Alph, DeltT=bar.DeltT, initT=bar.initT,
            Area2=bar.Area2, Modu2=bar.Modu2, nsub=max(2, bar.Nistp), tol=tol
        )
    else:
        res = solve_series_bar(
            L=bar.Leng, A=bar.Area1, E=bar.Modu1, EndLoad=bar.EndLoad, EndGap=bar.EndGap
        )
    return res
