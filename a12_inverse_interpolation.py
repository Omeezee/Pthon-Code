# -*- coding: utf-8 -*-
"""
Created on March 29 21:23:07 2025

@author: geode
"""

# a12_inverse_interpolation source used to view latter to make into matlab https://www.geeksforgeeks.org/newtons-divided-difference-interpolation-formula/?utm_source
x_vals = [0.12, 0.22, 0.45, 0.56]
y_vals = [15,   30,   45,   60]

# reuse the same Newton stuff from a12_enzyme_interpolation to make my life easier 
def get_coeffs(xs, ys):
    c = ys.copy()               # make a working copy of y-values so that if it goes wrong doesnt rune og data
    n = len(xs)
    for order in range(1, n):
        for i in range(n - order): # computes the next divded difference in place
            c[i] = (c[i+1] - c[i]) / (xs[i+order] - xs[i])
    return c[:n]                # first n entries are going to be the coeff we need 

# this will evaluate the Newton polynomial idk but it works 
def interp(xs, coeffs, x):
    res = coeffs[0]             # start from the first coeff
    # accumulate each term: (x - xi) * previous + next coeff
    for i in range(1, len(coeffs)):
        res = coeffs[i] + (x - xs[i-1]) * res
    return res

#build the inverse interpolation model 
coeffs_inv = get_coeffs(x_vals, y_vals)

# estimate time for a new OD reading
target = 0.50
estimate = interp(x_vals, coeffs_inv, target) 
# prints the newly calculated invers coeff
print("Inverse interp coeffs:", coeffs_inv)
# prints the estimated time OD
print("estimated time for od =", target, " about", f"{estimate:.2f}", "minutes")