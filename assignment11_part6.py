# -*- coding: utf-8 -*-
"""
Created on Mar 23 21:56:50 2025

@author: geode
"""

# assignment11_part6 same source as before 

#get libraries 
import numpy as np
import matplotlib.pyplot as plt

# data: substrate x mM vs activity idk the unit y
x = np.array([0.00, 0.34, 0.69, 1.03, 1.38, 1.72, 2.07, 2.41, 2.76, 3.10,
              3.45, 3.79, 4.14, 4.48, 4.83, 5.17, 5.52, 5.86, 6.21, 6.55,
              6.90, 7.24, 7.59, 7.93, 8.28, 8.62, 8.97, 9.31, 9.66, 10.00])
y = np.array([-0.48, 2.48, 4.03, 6.22, 10.33, 11.19, 12.39, 13.54, 15.29, 16.44,
              17.39, 18.68, 18.68, 19.64, 19.44, 19.74, 20.46, 20.53, 20.28,
              18.83, 19.22, 17.35, 15.80, 13.78, 12.59, 10.39, 8.27, 5.73,
              4.24, 2.82])

# polyfit degree=2 to make it find the degree of best fit for the graph of the data 
a, b, c = np.polyfit(x, y, 2)
y_fit = a*x**2 + b*x + c
# R^2 value and also find the line of best fit for the data
ss_res = np.sum((y - y_fit)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
#print the line of best fit equation and the R62 values 
print(f"fit: {a:}x² + {b:}x + {c:}")
print(f"r² = {r2:}")

# plot it
plt.scatter(x, y, label='data')
plt.plot(x, y_fit, label='quadratic fit')
plt.xlabel('substrate (mM)')
plt.ylabel('activity')
plt.title('substrate vs enzyme activity')
plt.legend()
plt.grid(True)
plt.show()