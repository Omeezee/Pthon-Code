# -*- coding: utf-8 -*-
"""
Created on March 29 23:09:36 2025

@author: geode
"""

# a12_root_finding  this was used as source https://www.geeksforgeeks.org/newton-raphson-method/ to later convert 
import numpy as np #standard array and number library 
import sympy as sp #  symbolic math library

# data
xs = [15, 30, 45, 60]
ys = [0.12, 0.22, 0.45, 0.56]
# Newton interpolation funcs same as before copy basically tweaked slighlty 
def get_coeffs(x, y):
    n = len(x)
    table = [[0]*n for _ in range(n)]
    for i in range(n):
        table[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i+1][j-1] - table[i][j-1]) / (x[i+j] - x[i])
    return [table[0][j] for j in range(n)]

# get the coeffs
coefs = get_coeffs(xs, ys)

# build symbolic poly for derivative 
t = sp.symbols('t')
poly = coefs[-1]
for k in range(len(coefs)-2, -1, -1):
    poly = coefs[k] + (t - xs[k]) * poly
# nprepare functions for symbolic polynomial-0.5 and its derivative
f = poly - 0.5
df = sp.diff(poly, t)
f_num  = sp.lambdify(t, f,  'numpy')
df_num = sp.lambdify(t, df, 'numpy')
# Newton Raphson loop NR to solve its derivative at 0
guess = 40.0
for i in range(50):
    next_guess = guess - f_num(guess)/df_num(guess)
    if abs(next_guess - guess) < 1e-5:
        guess = next_guess
        break
    guess = next_guess
#prints teh esitmated at od at 1/2 adn the guess and minuets after
print(f"estimate for OD at 0.50 is {guess:} min after {i+1} ")
