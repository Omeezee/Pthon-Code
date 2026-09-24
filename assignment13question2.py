# -*- coding: utf-8 -*-
"""
Created on Tue May  6 09:41:36 2025

@author: geode
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy #to calcualte the derivative 
#approximatin of the integral 
#2 interavals
x = [0, 1, 2]  # 2 intervals x values becasue step size is 1
f = [4 * x**2 for x in x]   # calcualtes the values for f(x) = 4x² from data
#4 intervals 
x2 = [0, 0.5, 1.0, 1.5, 2.0] # 4 intervals x values because step size si .5 
f2= [4 * x**2 for x in x2]  # compute f(x) = 4x² from data
#using the true value wich was calculated manually before 
tv= 32 / 3 #true value
#trapazoidal aprroximation for interval 2 
h1 = np.diff(x)
approximation2 = 0
for i in range(len(h1)):
    approximation2 += (h1[i] / 2) * (f[i] + f[i+1])
#trapazoidal approximation for interval 4 
h2 = np.diff(x2)
approximation4 = 0
for i in range(len(h2)):
    approximation4 += (h2[i] / 2) * (f2[i] + f2[i+1])
#calculating the error absolute and relative for both aprroximations 
abserror_2 = abs(tv - approximation2)
relerror_2 = abserror_2 / tv * 100

abserror_4 = abs(tv - approximation4)
relerror_4 = abserror_4 / tv * 100
#pritn results
print("intgral of 4x² from 0 to 2")
print(f"true value is :          {tv:}\n")

print(" for the 2 intervals:")
print(f"approximation:     {approximation2:}")
print(f" absolute error:    {abserror_2:}")
print(f"relative error:    {relerror_2:}%\n")

print(" for 4 intervals:")
print(f"approximation:{approximation4:}")
print(f"absolute error:{abserror_4:}")
print(f"relative error:{relerror_4:}%")


#plot it for fun 
intervals = [2, 4]
errors      = [abserror_2, abserror_4]

plt.figure()
plt.plot(intervals, errors, marker='o')
plt.title("abs eror of trapezoidal rule")
plt.xlabel("#of intervals")
plt.ylabel("absolute error")
plt.grid(True)
plt.show()