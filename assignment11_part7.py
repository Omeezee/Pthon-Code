# -*- coding: utf-8 -*-
"""
Created on Mar 23 22:17:56 2025

@author: geode
"""
# assignment11_part7 same source as before 

# import libraries 
import numpy as np
import matplotlib.pyplot as plt

# data for the enzyme concentratio (mg/mL) vs reaction rate (µmol/min) e is enzyme concentraiton and r is the reactionr ate
e = np.arange(0.1, 3.1, 0.1)
r = np.array([0.83, 0.82, 1.23, 1.68, 1.33, 1.72, 2.09, 1.74, 1.91, 2.40,
              2.58, 2.94, 2.87, 2.70, 3.15, 3.35, 3.71, 3.74, 3.62, 3.91,
              4.26, 4.50, 4.48, 4.85, 4.81, 5.10, 5.21, 5.46, 5.59, 5.92])
# simple linear fit 
m, c = np.polyfit(e, r, 1)
fit = m*e + c
#  R^2 value and also find the line of best fit for the data
ss_res = np.sum((r - fit)**2)
ss_tot = np.sum((r - r.mean())**2)
r2 = 1 - ss_res/ss_tot
#print the fit equation and the R62 values 
print(f"fit: {m:}x + {c:}")
print(f"r² = {r2:}")
# plot
plt.scatter(e, r, label='data')
plt.plot(e, fit, label='linear fit')
plt.xlabel('enzyme conc (mg/mL)')
plt.ylabel('reaction rate (µmol/min)')
plt.title('enzyme conc vs rate')
plt.legend()
plt.grid(True)
plt.show()
