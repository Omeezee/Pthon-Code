# -*- coding: utf-8 -*-
"""
Created on March 29 22:49:28 2025

@author: geode
"""

# a12_polyfit_interpolation source used for this and past idk if i put it in https://www.geeksforgeeks.org/numpys-polyfit-function-a-comprehensive-guide/?utm_source

import numpy as np

# given data in array foramt
t_vals = np.array([15, 30, 45, 60])
od_vals = np.array([0.12, 0.22, 0.45, 0.56])

#makes it fit into a 3rd power poly 
coeffs = np.polyfit(t_vals, od_vals, 3)
# get cubic fit: p(t) = a*t^3 + b*t^2 + c*t + d
p = [coeffs[0], coeffs[1], coeffs[2], coeffs[3] - 0.50]
roots = np.roots(p)              # 

# find roots of poly(t) - 0.50 = 0
roots = np.roots(coeffs - [0,0,0,0.50])  # subtract 0.50 from constant term

# pick the real root in between 15 and 60  https://stackoverflow.com/questions/3013449/list-comprehension-vs-lambda-filter?utm_source
t_est = next(
    (r.real for r in roots 
     if abs(r.imag) < 1e-6 and 15 <= r.real <= 60),
    None
)
#essentially it checks the root is real or not then it checks the time in a range between 15 adn 60 to make sure it fits 
#print valyes of the coeffetiont root and the estimated time for OD
print("cubic coeffs:", coeffs)
print("roots:", roots)
print(f"the estimated time for OD at .5 is: {t_est:}")
