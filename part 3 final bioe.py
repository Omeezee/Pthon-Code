# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:42:57 2025

@author: geode
"""

#part 3
import numpy as np 
import matplotlib.pyplot as plt
D  = 0.01 # diffusion coefficient cm per day
kc = 0.05 # clearance rate of 1 day
kd = 0.09413244 # degradation rate from Part 1 
C0 = 100.0 # initial concentration
t15 = 15.0 # the value at day the 15

#concentration equation at x =0 
C15 = C0 * np.exp(-kd * t15)

L = 1.0 # domain length in cm 
N = 21 # number of grid points maybe more or less idk
dx = L / (N - 1) # spacing between points
x = np.linspace(0, L, N) # x coordinates

# --- 3) Build finite-difference matrix A and RHS vector b ---
A = np.zeros((N, N))    # coefficient matrix
b = np.zeros(N)         # right-hand side

# so that at x=0 c=15
A[0, 0] = 1.0
b[0]    = C15

# other  points tkae the second derivative minus (kc/D)*c = 0
# about  d2c/dx2 = (c[i-1] - 2c[i] + c[i+1]) / dx^2
# times the dx^2 is = c[i-1] - (2 + (kc/D)*dx^2)*c[i] + c[i+1] = 0
coeff = 2.0 + (kc / D) * dx**2
for i in range(1, N-1):
    A[i, i-1] = 1.0
    A[i, i]   = -coeff
    A[i, i+1] = 1.0
    b[i]      = 0.0

# right boundry at x=1 c= 0
A[N-1, N-1] = 1.0
b[N-1]      = 0.0

# solving for c at A and b 
c = np.linalg.solve(A, b)

# plots the concentration vs time grpah 
plt.figure(figsize=(8,5))
plt.plot(x, c, 'o-', label='c(x) grph')
plt.xlabel('distance x (cm)')
plt.ylabel('concentration c(x) (mg/mL)')
plt.title('Compute Tissue Concentration Profile')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()  