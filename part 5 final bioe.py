# -*- coding: utf-8 -*-
"""
Created on Mon May 12 19:57:47 2025

@author: geode
"""
# part 5
import numpy as np
import matplotlib.pyplot as plt

# the arrays of the data of days and cocnetration 
t_data = np.array([0, 5, 10, 15, 20, 25, 30])
C_data = np.array([100, 60, 36, 22, 14, 9, 6])

# calcaujted things from from earlier parts
kd = 0.09413244# decay rate day
C0 = 100.0# initial implant concentration mg/ml
D  = 0.01# diffusion coefficient cm oer day
kc = 0.05  # clearance rate per day 

# using the factor of  x=0.5 cm the concentration at distance x from the implant is scaled by .5cm this was calcualted manually and seen on the document 
lambda_ = np.sqrt(kc / D)
phi_x0  = np.sinh(lambda_ * 0.5) / np.sinh(lambda_)

# predicted concentrations at each data time using the eqaution calcauted before to find the predicted 
C_predictaed = C0 * np.exp(-kd * t_data) * phi_x0

# calcaute the  mean squared error eqaution to solve for MSE
MSE = np.mean((C_predictaed - C_data)**2)

# Print results of the data 
print("time in days:      ", t_data)
print("measured mg/ml: ", C_data)
print("predicted mg/ml:", np.round(C_predictaed, 2))
print(f"\nMSE = {MSE:} (mg/mL)^2")

# graph of the  measured vs predicted
plt.figure(figsize=(8,5))
plt.plot(t_data, C_data, 'ro-', label='measured date')
plt.plot(t_data, C_predictaed, 'bs--', label='model prediction')
plt.xlabel('time days')
plt.ylabel('concetration at x=0.5 cm mg/ml')
plt.title(' prediction of concetnration vs. acutal colceted conentration data')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
