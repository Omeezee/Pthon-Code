# -*- coding: utf-8 -*-
"""
Created on Tue May  6 10:38:56 2025

@author: geode
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters for the ODE dC/dt = -60 Cn, and intial is C(0)=10
h = 0.05 #thestep size
t = np.arange(0, 0.2 + h, h) #make the gird
c0 = 10.0 #intial condition
k = 60.0  #the constant in this case is 60 

# maeke the arrays for the forward and the backward euler plots and to calculate 
cf = np.zeros(len(t)) #foward euler array
cb = np.zeros(len(t)) #backward euler arry 
cf[0] = c0  #intalize with f(o) for each array
cb[0] = c0 #intalize with f(o) for each array

# forward and backwardeuler loops to calculate the data to plot and find values
for i in range(len(t) - 1):
    cf[i + 1] = cf[i] + h * (-k * cf[i])  #equation for forward euler
    cb[i + 1] = cb[i] / (1 + k * h)  #equation for backward euler 

# the exact solution so that we can refrence eaitehr values geenrated by the forward and backward 
ce = c0 * np.exp(-k * t)
#printing out the generated values by the for loop will print out a table with t forward euler and backward euelr and the exact value for comparison
print(f"{'t':>5} | {'forward euler':>14} | {'bakcward euler':>15} | {'the exact value is':>10}")
print("-" * 57)
#for ti, cf, cb, ce in zip(t, cf, cb, ce):
 #   print(f"{ti:5.2f} | {cf:14.6f} | {cb:15.6f} | {ce:10.6f}")
#new for loop becasue plotting problems with array 
for ti, fwd, bwd, exact in zip(t, cf, cb, ce):
    print(f"{ti:5.2f} | {fwd:14.6f} | {bwd:15.6f} | {exact:10.6f}")
# plot it 
plt.figure(figsize=(12, 8))
plt.plot(t, cf, 'ro--', label='forward Euler')
plt.plot(t, cb, 'bo--', label='backward Euler')
plt.plot(t, ce, 'g-',  label='exact')
plt.title('Forward vs. Backward Euler and Exact Solution\nfor dC/dt = -60 C, C(0)=10')
plt.xlabel('t')
plt.ylabel('C(t)')
plt.grid(True)
plt.legend(loc='upper right')
plt.show()
