# -*- coding: utf-8 -*-
"""
Created on Sat May  3 11:51:07 2025

@author: geode
"""
import numpy as np
import matplotlib.pyplot as plt
import sympy #to calcualte the derivative 

t_vals = [0.0, 0.1, 0.2, 0.3] #value of the table for seconds 
a= c_vals = [0.0, 2.1, 3.7, 4.8]  #value of table for Current (µA)
s=.0476190476 #slope
h = 0.1  # Step size
i = 1    # Index for t = 0.1
 
#def function_original (x):
    #return 0.0476190476*x

#equation of forward method with index of .1 and step size of .1 forward_method_function(f(a + h) - f(a)) / h
forward_diff = (c_vals[i + 1] - c_vals[i]) / h

  
# equation to calcualte teh central_method_equation=(f(a + h) - f(a - h))/(2*h) 
central_diff = (c_vals[i + 1] - c_vals[i - 1]) / (2 * h)
#Print out the results of what is given 
print(f"time point: t = {t_vals[i]} s")
print(f"The forward difference estimate is: {forward_diff:} µA/s")
print(f"The central difference estimate is: {central_diff:} µA/s")

#plot it just to visualize it 
plt.figure(figsize=(8, 5))
plt.plot(t_vals, c_vals, 'bo-', label='Current Data (µA)')
plt.plot([t_vals[i], t_vals[i+1]], [c_vals[i], c_vals[i+1]], 'r--', label='Forward Slope') #line to show the FD
plt.plot([t_vals[i-1], t_vals[i+1]], [c_vals[i-1], c_vals[i+1]], 'g--', label='Central Slope') #line to show the CD
#plot information and lables 
plt.title("glucose biosensor measures vs time")
plt.xlabel("time (s)")
plt.ylabel("crrent (µA)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

