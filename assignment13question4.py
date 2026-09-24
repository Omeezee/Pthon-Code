# -*- coding: utf-8 -*-
"""
Created on Tue May  6 11:07:53 2025

@author: geode
"""

import numpy as np
import matplotlib.pyplot as plt

# inforamtion
k  = 0.5         # rate constant
h  = 0.1         # step size
t  = np.arange(0, 1 + h, h)  # makes an array for the values using the step size 
O  = np.zeros_like(t)        # makes a new array for the eulers method 
O[0] = 1.0                    # initial condition which is at 0 it is 1
#for loop to calculate the forward euler steps
for n in range(len(t)-1):
    O[n+1] = O[n] + h * (-k * O[n])

#prints a table for t vs o table so step size vs the calcualted eulers method x vs y 
print(f"{'n':} | {'t':} | {'O(t) using the euler method':}")
for n, (tn, On) in enumerate(zip(t, O)):
    print(f"{n:2d} | {tn:f} | {On:f}")   
 # now to geenrate the exponential fit using the linearized equation ln(O) = ln(A) + B t   so thta tline of best fit si O_fit = A e^{B t}
p = np.polyfit(t, np.log(O), 1)   # p[0]=B, p[1]=ln(A)
O_fit = np.exp(np.polyval(p, t))  # A * exp(B t)
#print p[0],vsp[1]
print("\the fit model: O(t) = exp({:f} t + {:f})".format(p[0], p[1]))
#making the plot 
plt.figure(figsize=(8,5))
plt.plot(t, O,    'bo-', label='euler approximation O')
plt.plot(t, O_fit,'r--', label='exponential fit approximation using ln')
plt.title("O concentration with euler's method vs the exponential fit ln")
plt.xlabel("t (s)")
plt.ylabel("O(t)")
plt.grid(True)
plt.legend()
plt.show()