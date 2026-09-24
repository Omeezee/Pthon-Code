# -*- coding: utf-8 -*-
"""
Created on Mar 23 20:15:05 2025

@author: geode
"""
# assignment11_part4 https://www.geeksforgeeks.org/how-to-do-exponential-and-logarithmic-curve-fitting-in-python/?utm_source source for later to convert 

import numpy as np #number library 
import matplotlib.pyplot as plt #plotting library 

# data  the time in hours for the population in thousands
t = np.array([0, 0.21, 0.41, 0.62, 0.83, 1.03, 1.24, 1.45, 1.66, 1.86,
              2.07, 2.28, 2.48, 2.69, 2.90, 3.10, 3.31, 3.52, 3.72, 3.93,
              4.14, 4.34, 4.55, 4.76, 4.97, 5.17, 5.38, 5.59, 5.79, 6.00])
p = np.array([-3.02, 21.99, 3.87, -5.94, 13.58, 28.07, 52.56, 63.69, 74.90, 105.92,
              130.39, 177.35, 210.67, 268.66, 319.96, 401.92, 486.04, 578.65, 698.98,
              844.17, 1005.58, 1211.93, 1475.16, 1795.48, 2201.16, 2692.78, 3287.16,
              4031.50, 4938.22, 6034.13])

# only keep positive ones so log function works when calculating the log made making it linear basically
mask = p > 0
x = t[mask]
y = np.log(p[mask])
b, loga = np.polyfit(x, y, 1)
a = np.exp(loga)

# fit a line to the log-data values so that graph is showing the growth for the function
b, loga = np.polyfit(x, y, 1)  # y = b*x + loga
a = np.exp(loga)

# predictions and R^2 statistics values to ensure how well the data follows the line of best fit makes the calcaultion gor r62 
p_fit = a * np.exp(b * t)
ss_res = ((p - p_fit)**2).sum()
ss_tot = ((p - p.mean())**2).sum()
r2 = 1 - ss_res/ss_tot
#print the calcualted values for the r^2 and the equation for the best fit line
print(f"fit: {a:.2f} * exp({b:} * t)")
print(f"r² = {r2:}")
# plot it and show the data and exp fit line
plt.scatter(t, p, label='data')
plt.plot(t, p_fit, label='exp fit')
plt.xlabel('time (h)')
plt.ylabel('population (×1000)')
plt.title('bacterial growth')
plt.legend()
plt.grid(True)
plt.show()

