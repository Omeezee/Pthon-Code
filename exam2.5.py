# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 20:00:00 2025

@author: geode
"""
from typing import Dict, Any, List            # for type hints on plain dicts and lists
import numpy as np                            # for arrays and math

# Try to import scipy.io.loadmat for .mat file reading (used by read_bar_mat)
try:
    from scipy.io import loadmat             # MATLAB .mat reader
    SCIPY_OK = True                          # flag to know if scipy is available
except Exception:
    SCIPY_OK = False                         # if import fails, we keep going but .mat reading will not work


# ----------------------------- I/O HELPERS -----------------------------

def _to_1d(arr) -> np.ndarray:
    """Convert input (possibly MATLAB-shaped) to a 1D float numpy array."""
    return np.array(arr, dtype=float).squeeze()   # make an array of floats and remove extra dimensions


def read_bar_mat(path: str) -> Dict[str, Any]:
    """
    Read a .mat file that contains a single struct named 'bar'.
    Return its fields as a plain Python dict of numpy arrays and numbers.
    """
    if not SCIPY_OK:
        # If scipy is not installed, we explain what to do
        raise RuntimeError("scipy is required to read .mat files. Please `pip install scipy` and retry.")

    md = loadmat(path, squeeze_me=True, struct_as_record=False)  # load the .mat into a Python dict-like object
    bar = md.get('bar', None)                                    # try to fetch the 'bar' struct
    if bar is None:
        # If the file uses a different top-level name, try to guess it
        keys = [k for k in md.keys() if not k.startswith('__')]  # filter out meta keys like __header__
        if len(keys) == 1:
            bar = md[keys[0]]                                    # take the only non-meta key as the struct
        else:
            # If we still cannot find it, raise a helpful error
            raise ValueError(f"No 'bar' struct in {path}. Found keys: {list(md.keys())}")

    # Tiny helper to safely get a field from the MATLAB struct, with a default when missing
    def fget(name, default=None):
        return getattr(bar, name, default)                       # getattr works on scipy-loaded MATLAB structs

    # Pull mandatory scalar/array fields and convert to the right shapes
    NElem = int(fget('NElem'))                                   # number of elements (scalar int)
    Leng  = _to_1d(fget('Leng'))                                 # element lengths (size n)
    Area1 = _to_1d(fget('Area1'))                                # left-end areas (size n)
    Area2 = _to_1d(fget('Area2', Area1))                         # right-end areas (size n), default to Area1 if missing
    Modu1 = _to_1d(fget('Modu1'))                                # left-end modulus (size n)
    Modu2 = _to_1d(fget('Modu2', Modu1))                         # right-end modulus (size n), default to Modu1
    Alph  = _to_1d(fget('Alph'))                                 # thermal expansion coeffs α (size n)
    DeltT = _to_1d(fget('DeltT'))                                # per-element final temperature (or ΔT) (size n)
    initT = float(fget('initT', 0.0))                            # initial uniform temperature (scalar), default 0.0
    EndGap= float(fget('EndGap', 0.0))                           # initial end gap (scalar), default 0.0
    EndLoad = _to_1d(fget('EndLoad'))                            # nodal loads (size n+1)
    Nistp = int(fget('Nistp', 64))                               # subdivisions for integration (scalar), default 64

    # Quick validation to catch shape mistakes early
    assert Leng.size == NElem                                    # lengths must match number of elements
    assert Area1.size == NElem and Modu1.size == NElem           # area/modulus left arrays must be size n
    assert Alph.size  == NElem and DeltT.size == NElem           # α and temperature arrays must be size n
    assert EndLoad.size == NElem + 1                             # nodal loads must have n+1 entries (nodes)

    # Return a plain dict representing the entire model input
    return dict(
        NElem=NElem, Leng=Leng,
        Area1=Area1, Area2=Area2,
        Modu1=Modu1, Modu2=Modu2,
        Alph=Alph, DeltT=DeltT,
        initT=initT, EndGap=EndGap,
        EndLoad=EndLoad, Nistp=Nistp
    )


# ----------------------------- CORE MATH -----------------------------

def element_compliance(L: float, A1: float, A2: float, E1: float, E2: float, nsub: int) -> float:
    """
    Compute the axial compliance of a single element:
        s = ∫(0→L) [1 / (A(x) * E(x))] dx
    where A(x) and E(x) can vary linearly from (A1,E1) at x=0 to (A2,E2) at x=L.
    We use the trapezoidal rule with 'nsub' subdivisions for numerical integration.
    If A and E are constant across the element, we use the simple closed-form: s = L / (A * E).
    """
    if A1 <= 0 or A2 <= 0 or E1 <= 0 or E2 <= 0:                 # guard against invalid inputs
        raise ValueError("Area and Modulus must be positive.")

    # If both A and E are effectively constant, return the simple formula
    if abs(A1 - A2) < 1e-16 and abs(E1 - E2) < 1e-16:
        return L / (A1 * E1)

    nsub = max(2, int(nsub))                                     # ensure at least 2 points for trapezoid
    xs = np.linspace(0.0, L, nsub)                               # nsub points from 0 to L
    t  = xs / L if L > 0 else np.zeros_like(xs)                  # normalized position (0 at left, 1 at right)
    A  = A1 + t * (A2 - A1)                                      # linear interpolation of area along the element
    E  = E1 + t * (E2 - E1)                                      # linear interpolation of modulus along the element
    integrand = 1.0 / (A * E)                                    # value of 1/(A*E) at each x
    s = np.trapz(integrand, xs)                                  # trapezoidal integration over x
    return float(s)                                              # return as a plain float


def build_compliances(bar: Dict[str, Any]) -> np.ndarray:
    """
    Build a vector of element compliances s_i for i=0..n-1 using element_compliance().
    """
    n = bar["NElem"]                                             # number of elements
    s = np.zeros(n, dtype=float)                                 # allocate array for n compliances
    for i in range(n):                                           # loop over elements
        # compute s_i with possibly varying A/E, using bar["Nistp"] subdivisions
        s[i] = element_compliance(
            bar["Leng"][i], bar["Area1"][i], bar["Area2"][i],
            bar["Modu1"][i], bar["Modu2"][i], bar["Nistp"]
        )
    return s                                                     # return the vector of compliances


def thermal_free_def(bar: Dict[str, Any]) -> np.ndarray:
    """
    Compute the free thermal deformation per element:
        δ_th_i = α_i * (T_final_i - T_init) * L_i
    If your input DeltT is already ΔT (not final temperature), set initT = 0 in the input.
    """
    dT = bar["DeltT"] - bar["initT"]                              # convert final T to ΔT relative to initial T
    return bar["Alph"] * dT * bar["Leng"]                         # α * ΔT * L for each element


def cumulative_right_loads(EndLoad: np.ndarray) -> np.ndarray:
    """
    For each element i (between nodes i and i+1), compute the sum of all nodal loads
    to the RIGHT of that element: nodes i+1, i+2, ..., n.
    This is used to express internal force N_i in terms of the right reaction R1.
    """
    n = EndLoad.size - 1                                          # number of elements inferred from nodal loads
    FR = np.zeros(n, dtype=float)                                 # allocate FR vector
    for i in range(n):                                            # loop elements
        FR[i] = float(np.sum(EndLoad[i+1:]))                      # sum of loads on nodes right of element i
    return FR                                                     # return the right-side sums


# ----------------------------- SOLVER -----------------------------

def solve_bar(bar: Dict[str, Any]) -> Dict[str, Any]:
    """
    Solve the 1D bar problem with thermal effects and an initial end gap.

    Unknowns:
      - Right reaction R1 (we solve this from compatibility)
      - Left  reaction R0 (we get this from equilibrium once R1 is known)

    Key equations:
      - Internal force in element i:  N_i = -(R1 + FR_i), where FR_i = sum of nodal loads to the right of element i
      - Compatibility: sum_i (N_i * s_i) + sum_i (δ_th_i) = EndGap
      - Equilibrium:  R0 + R1 + sum(EndLoad) = 0
    """
    n   = bar["NElem"]                                            # number of elements
    s   = build_compliances(bar)                                  # element compliances s_i
    S   = float(np.sum(s))                                        # total compliance (sum s_i)
    th  = thermal_free_def(bar)                                   # thermal free def per element δ_th_i
    TH  = float(np.sum(th))                                       # total thermal free def
    FR  = cumulative_right_loads(bar["EndLoad"])                  # right-side nodal load sums FR_i

    if abs(S) < 1e-18:                                            # safety: avoid division by ~zero
        raise ZeroDivisionError("Total compliance is ~0. Check areas/moduli.")

    # Compatibility:
    #   sum_i [-(R1 + FR_i) * s_i] + TH = EndGap
    #   -R1 * sum_i s_i - sum_i(FR_i s_i) + TH = EndGap
    #   R1 = (TH - EndGap - sum_i(FR_i s_i)) / sum_i s_i
    C = float(np.dot(FR, s))                                      # sum of (FR_i * s_i)
    R1 = (TH - bar["EndGap"] - C) / S                             # compute right reaction from compatibility

    # Equilibrium:
    #   R0 + R1 + sum(EndLoad) = 0  ->  R0 = -R1 - sum(EndLoad)
    sumF = float(np.sum(bar["EndLoad"]))                          # sum of all given nodal loads
    R0 = -R1 - sumF                                               # compute left reaction

    # Internal forces per element:
    #   N_i = -(R1 + FR_i)
    N_int = -(R1 + FR)                                            # vector of internal forces (positive = tension)

    # Mechanical deformation piece per element (from forces only):
    #   δ_mech_i = N_i * s_i
    unc_mech = N_int * s                                          # vector of mechanical deformations

    # Total element deformation:
    #   δ_tot_i = δ_mech_i + δ_th_i
    tot_def  = unc_mech + th                                      # vector of total deformations

    # Nodal displacements (u0 = 0 reference, then cumulative sum of δ_tot to the right)
    u = np.zeros(n+1, dtype=float)                                # allocate displacements (n+1 nodes)
    u[1:] = np.cumsum(tot_def)                                    # cumulative displacements from left to right

    # Element stress (using average area; switch to Area1 if your grader expects left-end stress)
    A_avg  = 0.5 * (bar["Area1"] + bar["Area2"])                  # per-element average area
    stress = N_int / A_avg                                        # average stress per element

    # Nodal loads including the reactions, to verify equilibrium
    TotLoad = bar["EndLoad"].copy()                               # start from the given nodal loads
    TotLoad[0]  += R0                                             # add left reaction at node 0
    TotLoad[-1] += R1                                             # add right reaction at last node

    # Diagnostic checks: overall force balance and compatibility balance
    eq_res    = abs(np.sum(TotLoad))                              # should be ~0 if equilibrium is satisfied
    comp_bal  = float(np.sum(tot_def) - bar["EndGap"])            # should be ~0 if compatibility is satisfied

    # Return everything in a plain dictionary
    return dict(
        React0=R0,                 # left reaction
        React1=R1,                 # right reaction
        IntLoad=N_int,             # internal force per element
        Stress=stress,             # stress per element (avg area)
        UncMDef=unc_mech,          # mechanical deformation per element (from forces)
        UncTDef=th,                # thermal free deformation per element
        MecDef=unc_mech,           # alias for clarity (matches some MATLAB stubs)
        TotDef=tot_def,            # total deformation per element
        NodalDisp=u,               # nodal displacements (u0=0)
        TotLoad=TotLoad,           # nodal loads including reactions
        eq_residual=eq_res,        # |sum TotLoad| (equilibrium residual)
        comp_balance=comp_bal      # sum(TotDef) - EndGap (compatibility balance)
    )


# ----------------------------- PRETTY PRINTER -----------------------------

def print_result(bar: Dict[str, Any], res: Dict[str, Any]) -> None:
    """
    Print reactions, a per-element table, and nodal displacements in a tidy way.
    This matches the “published run” style expected in your assignment.
    """
    n = bar["NElem"]                                              # number of elements for loops

    # Print reaction forces and diagnostic residuals
    print("\n=== Reactions ===")
    print(f"Left Reaction (React0): {res['React0']:.6e} N")
    print(f"Right Reaction(React1): {res['React1']:.6e} N")
    print(f"Equilibrium residual  : {res['eq_residual']:.3e} N (should be ~0)")
    print(f"Compatibility balance : {res['comp_balance']:.3e} m (sum TotDef - EndGap)")

    # Build a header for the element table with aligned columns
    header = (f"\n{'Elem':>4} | {'L [m]':>8} {'A1 [m^2]':>10} {'A2 [m^2]':>10} "
              f"{'E1 [Pa]':>12} {'E2 [Pa]':>12} {'N [N]':>14} {'σ_avg [Pa]':>14} "
              f"{'δ_mech [m]':>14} {'δ_th [m]':>12} {'δ_tot [m]':>12}")
    print(header)                                                 # print the header line
    print("-"*len(header))                                       # underline

    # Print one row per element with key values
    for i in range(n):
        print(f"{i+1:4d} | "                                     # element number (1-based for readability)
              f"{bar['Leng'][i]:8.4f} "                          # element length
              f"{bar['Area1'][i]:10.6e} {bar['Area2'][i]:10.6e} "  # left/right areas
              f"{bar['Modu1'][i]:12.4e} {bar['Modu2'][i]:12.4e} "  # left/right moduli
              f"{res['IntLoad'][i]:14.6e} "                      # internal force
              f"{res['Stress'][i]:14.6e} "                       # stress (avg area)
              f"{res['UncMDef'][i]:14.6e} "                      # mechanical deformation
              f"{res['UncTDef'][i]:12.6e} "                      # thermal deformation
              f"{res['TotDef'][i]:12.6e}")                       # total deformation

    # Print nodal displacements after the table
    print("\nNodal Displacements (u):")
    for j, uj in enumerate(res["NodalDisp"]):                     # loop over nodes
        print(f"  Node {j}: u = {uj:.6e} m")                      # displacement at node j

    # Print simple totals to show sum of element deformations vs EndGap
    print("\nTotals:")
    print(f"  Sum element δ_tot = {np.sum(res['TotDef']):.6e} m   (EndGap = {bar['EndGap']:.6e} m)")


# ----------------------------- CONVERGENCE (OPTIONAL) -----------------------------

def convergence_study(bar: Dict[str, Any], nsub_list: List[int], key: str = "React1") -> np.ndarray:
    """
    Sweep different trapezoid subdivisions (Nistp) to show numerical convergence.
    Returns a 2D numpy array with columns: [Nistp, value, abs(diff from previous)].

    - bar: your input dict
    - nsub_list: e.g., [4, 8, 16, 32, 64]
    - key: which quantity to watch for convergence (default 'React1')
    """
    out_rows = []                                                 # list to collect rows
    prev_val = None                                               # remember previous value to compute differences
    for nsub in nsub_list:                                        # loop over requested subdivisions
        bar2 = dict(bar)                                          # make a shallow copy of the input dict
        bar2["Nistp"] = int(nsub)                                 # set a new integration density
        res = solve_bar(bar2)                                     # solve with this Nistp
        val = res[key]                                            # take the requested quantity
        # If the quantity is an array (rare for this key), summarize by sum to keep it scalar
        if isinstance(val, np.ndarray):
            val = float(np.sum(val))                              # reduce arrays to a single number
        else:
            val = float(val)                                      # ensure type is a plain float

        diff = np.nan if prev_val is None else abs(val - prev_val)  # change from previous
        out_rows.append([float(nsub), val, diff])                 # store row: [Nistp, value, |Δ|]
        prev_val = val                                           # update previous value
    return np.array(out_rows, dtype=float)                        # return as a 2D numpy array
