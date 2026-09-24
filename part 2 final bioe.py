# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:11:19 2025

@author: geode
"""
#part 2
import numpy as np
import matplotlib.pyplot as plt
# Solve dC/dt = -kd·C numerically and compare to analytical
#numbers from part 1 
kd = 0.09413244 # decay constant in days 
C0 = 100.0 # initial concentration 
t_end = 30 # simulate from t=0 to t=30 days inital minus final 
#step size 
dt = 1.0# time‐step of 1 day
t = np.arange(0, t_end + dt, dt)# array [0,1,2,…,30] geneart an array for the step size to calculate later
# arrays that will hold the solutions
C_euler   = np.zeros_like(t)#forward Euler solution
C_mid     = np.zeros_like(t)#midpoint solution
C_analyt  = np.zeros_like(t)#exact solution
# set them to 0 intialization
C_euler[0]  = C0
C_mid[0]    = C0
C_analyt[0] = C0
#calcualting using step size
for i in range(len(t)-1):
    # slope at current point: dC/dt = -kd * C
    slope = -kd * C_euler[i]
    # forward method C_{n+1} = C_n + slope * dt
    C_euler[i+1] = C_euler[i] + slope * dt
    #midpoint method
    C_half = C_mid[i] + (-kd * C_mid[i]) * (dt/2)
    #slope at the midpoint method
    slope_mid = -kd * C_half
    #midpoint method caclulated
    C_mid[i+1] = C_mid[i] + slope_mid * dt
    #exact solution at next time
    C_analyt[i+1] = C0 * np.exp(-kd * t[i+1])
#graph the plot
plt.figure(figsize=(8,5))
plt.plot(t, C_analyt, 'k-',  label='Analytical')
plt.plot(t, C_euler,  'ro--', label='forward method')
plt.plot(t, C_mid,    'bs--', label='midpoint method')
plt.xlabel('time (days)')
plt.ylabel('drug concentration (mg/mL)')
plt.title('solve the implant ODE' )
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
#compare the answers and print values
error_forward = abs(C_euler[-1] - C_analyt[-1])
error_midppint= abs(C_mid[-1]   - C_analyt[-1])
print(f"At t = {t_end} days:")
print(f"  forward method error = {error_forward:} mg/mL")
print(f"  midpoint method error = {error_midppint:} mg/mL")
