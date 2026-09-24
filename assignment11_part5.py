# -*- coding: utf-8 -*-
"""
Created on Mar 23 21:12:06 2025

@author: geode
"""
# assignment11_part5  https://www.geeksforgeeks.org/how-to-do-exponential-and-logarithmic-curve-fitting-in-python/?utm_source use this to refrence and help convert later 

import numpy as np
import matplotlib.pyplot as plt

# data (d = dosage in mg, resp = response %)
d = np.array([1.00, 2.69, 4.38, 6.07, 7.76, 9.45, 11.14, 12.83, 14.52, 16.21,
              17.90, 19.59, 21.28, 22.97, 24.66, 26.34, 28.03, 29.72, 31.41,
              33.10, 34.79, 36.48, 38.17, 39.86, 41.55, 43.24, 44.93, 46.62,
              48.31, 50.00])
resp = np.array([15.10, 25.86, 29.07, 32.70, 35.10, 36.44, 38.85, 40.35, 41.99,
                 42.87, 44.16, 45.13, 46.26, 46.70, 47.68, 48.25, 48.49, 48.92,
                 49.83, 49.60, 50.21, 50.81, 50.79, 51.38, 51.86, 52.15, 52.81,
                 52.72, 53.43, 54.16])

# take ln of dosage for the function  do linear fit: response = m*x + c natruatlized uisng ln 
x = np.log(d)
m, c = np.polyfit(x, resp, 1)
y_fit = m*x + c

# compute R^2 to see if closley follows line or not
ss_res = np.sum((resp - y_fit)**2)
ss_tot = np.sum((resp - resp.mean())**2)
r2 = 1 - ss_res/ss_tot
#print function of best fit and the R62 valuse
print(f"fit: {c:} + {m:} * ln(d)")
print(f"r² = {r2:}")

# plot
plt.scatter(d, resp, label='data')
plt.plot(d, y_fit, label='log fit')
plt.xlabel('dosage (mg)')
plt.ylabel('response (%)')
plt.title('drug dosage vs response')
plt.legend()
plt.grid(True)
plt.show()