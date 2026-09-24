# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 13:14:52 2025
=
"""
import numpy as np
#inout section of vlaues that are given 
units=print("ensure all units are the same for each section")
L=20 #total lenght will be given 
A=[.001,.0001,1]  #are may be given or may need to be calcualted this will be a list 
E= 200 #this value will be given to us 
P=[100,-100]  #force mutliple loads this value will be give to us and is the force pushing from the right side 
n= input(int("What is the total number of iterations n = "))      #this value will be the number of cuts of the bar
#find lengths for each section first 
li=L/n
#to start calcualting internal loads will assume that based
#need to find pi,li,ai,ei for each sectional area of the road then calcualte it all 

def mech_main(bar=None):
    """
    Combined mechanical/thermal axial loading analysis (Python version).
    """

    print("**** COMBINED MECHANICAL/THERMAL AXIAL LOADING ANALYSIS ****")

    if bar is None:
        print("Reading in new bar model")
        bar = model_input()
    else:
        print("Using bar model provided in call")

    # =========================================================
    # >>> DO WORK HERE <<<
    # (Insert your calculations for reactions, deformation, stress, etc.)
    # =========================================================

    # Example output structure
    out = {
        "React0": None,       # Reaction at right side
        "React1": None,       # Reaction at left side
        "TotLoad": np.zeros(bar["NElem"]),
        "TotDef": np.zeros(bar["NElem"]),
        "Stress": np.zeros(bar["NElem"]),
        # Optional outputs:
        "UncLoad": np.zeros(bar["NElem"]),
        "UncMDef": np.zeros(bar["NElem"]),
        "UncTDef": np.zeros(bar["NElem"]),
        "MecDef": np.zeros(bar["NElem"]),
    }

    return out


def model_input():
    """
    Collect bar mechanical/thermal information from user input.
    """

    bar = {}
    bar["NElem"] = int(input("Total # of elements? "))
    bar["initT"] = float(input("Initial Temperature? "))
    bar["Nistp"] = int(input("Number of integration steps? "))

    bar["Area1"] = np.zeros(bar["NElem"])
    bar["Area2"] = np.zeros(bar["NElem"])
    bar["Leng"] = np.zeros(bar["NElem"])
    bar["Modu1"] = np.zeros(bar["NElem"])
    bar["Modu2"] = np.zeros(bar["NElem"])
    bar["Alph"] = np.zeros(bar["NElem"])
    bar["DeltT"] = np.zeros(bar["NElem"])
    bar["EndLoad"] = np.zeros(bar["NElem"])
    bar["EndGap"] = 0.0

    for i in range(bar["NElem"]):
        print(f"\nBar Element #{i+1}")
        bar["Area1"][i] = float(input("  Area near end = "))
        bar["Area2"][i] = float(input("  Area far end = "))
        bar["Leng"][i] = float(input("  Length = "))
        bar["Modu1"][i] = float(input("  Modulus near end = "))
        bar["Modu2"][i] = float(input("  Modulus far end = "))
        bar["Alph"][i] = float(input("  Alpha = "))
        bar["DeltT"][i] = float(input("  Final Temperature = "))

        if i == 0:
            bar["EndGap"] = float(input("  End gap = "))
            bar["EndLoad"][i] = 0.0
        else:
            bar["EndLoad"][i] = float(input("  End load = "))

    yn = input("Save model to .npz file? (y/n) ").strip().lower()
    if yn == "y":
        name = input("Input model name (no extension): ").strip()
        np.savez(name + ".npz", **bar)
        print(f"Model saved to {name}.npz")

    return bar


# =========================================================
# Optional: Example subfunction for integration


# =========================================================
def int_def(P, A, E, x):
    """
    Example: Numerically integrate [P / (A(x) * E(x))] dx.
    You can customize based on your model.
    """
    integrand = P / (A * E)
    return np.trapz(integrand, x)
