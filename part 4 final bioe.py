# -*- coding: utf-8 -*-
"""
Created on Mon May 12 19:43:07 2025

@author: geode
"""

#part 4
import numpy as np

# the constants to calcaute when the drug concentration is below 10
kd = 0.09413244 # first-order decay rate 
C0 = 100.0  # initial implant concentration mg/ml
D  = 0.01 # diffusion coefficient cm/day
kc = 0.05  # tissue clearance rate per day 

# using the factor of  x=0.5 cm the concentration at distance x from the implant is scaled by .5cm this was calcualted manually and seen on the document 
lambda_ = np.sqrt(kc / D)
phi_x0  = np.sinh(lambda_ * 0.5) / np.sinh(lambda_)

# the function shows  the difference between the predicted concentration at x=0.5 cm and the lowest threshold 10  
def f(t):
    # concentration at x=0.5 minus threshold 10 mg/mL
    return C0 * np.exp(-kd * t) * phi_x0 - 10

# to calcualte the secant method 
t0, t1 = 5.0, 15.0 # two initial time guesses in days
tol     = 1e-6 # the tolerance
max_it  = 50 # maximum iterations to calcualte 

# loop to calacualte the itteratiosn
for _ in range(max_it):
    f0, f1 = f(t0), f(t1)
    # secant formula the t_next = t1 - f1*(t1 - t0)/(f1 - f0)
    t2 = t1 - f1 * (t1 - t0) / (f1 - f0)
    if abs(t2 - t1) < tol:
        break
    t0, t1 = t1, t2   # shift guesses

t_star = t2
print(f"the time t* (Secant method) = {t_star:} days")
