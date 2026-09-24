# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:59:19 2025

@author: geode
"""

from exam2_solver import solve_bar, BarInput
import scipy.io as sio
import numpy as np

temp = sio.loadmat('Prob2.04.mat', struct_as_record=False, squeeze_me=True)
b = temp['bar']

# manually convert the matlab object into BarInput
bar = BarInput(
    NElem=int(b.NElem),
    initT=float(getattr(b, "initT", 0.0)),
    Nistp=int(getattr(b, "Nistp", 8)),
    Leng=np.atleast_1d(np.array(b.Leng, dtype=float)),
    Area1=np.atleast_1d(np.array(b.Area1, dtype=float)),
    Area2=np.atleast_1d(np.array(b.Area2, dtype=float)),
    Modu1=np.atleast_1d(np.array(b.Modu1, dtype=float)),
    Modu2=np.atleast_1d(np.array(b.Modu2, dtype=float)),
    Alph=np.atleast_1d(np.array(b.Alph, dtype=float)),
    DeltT=np.atleast_1d(np.array(b.DeltT, dtype=float)),
    EndGap=float(getattr(b, "EndGap", 0.0)),
    EndLoad=np.atleast_1d(np.array(b.EndLoad, dtype=float)),
)

out = solve_bar(bar)   # run the solver using your bar struct
print(out)
