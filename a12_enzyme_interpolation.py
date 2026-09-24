# -*- coding: utf-8 -*-
"""
Created on March 29 20:30:43 2025

@author: geode
"""

# a12_enzyme_interpolation

#data values 
x_vals = [1.0, 1.5, 2.0, 3.0]
y_vals = [2.0, 2.7, 3.8, 4.1]

#Builds a divided difference table basically will compute the differences between the points and tehen computes newton interpolating  poly
def get_coeffs(xs, ys):
    n = len(xs)
    table = [[0]*n for _ in range(n)]
    for i in range(n):
        table[i][0] = ys[i]
    for order in range(1, n):
        for i in range(n - order):
            diff = table[i+1][order-1] - table[i][order-1]
            span = xs[i+order] - xs[i]
            table[i][order] = diff / span
    return [table[0][i] for i in range(n)]

# this uses horns nested method and evaluate the newton poly this will and will start at x is 0 stimate the polynomial value at a new x point 
def interp(xs, coeffs, x0):
    result = coeffs[-1]
    for i in range(len(coeffs)-2, -1, -1):
        result = coeffs[i] + (x0 - xs[i]) * result
    return result
# get coeffs and make a little function to plot values 
coeffs = get_coeffs(x_vals, y_vals)
test_x = 2.5
estimate = interp(x_vals, coeffs, test_x)   
# shows the divided difference coefficients
print(f"divided difference coeffs: {coeffs}")
# prints the estimated enzyme activity
print(f"estimated activity at [S]={test_x} mM: {estimate:} µmol/min")
