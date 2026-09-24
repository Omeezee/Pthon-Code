# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:45:11 2025

@author: geode
"""
#load the libraries to read matlab files to use numbers and to plot 
#source used https://zerowithdot.com/polynomial-regression-in-python/?utm_source and https://www.askpython.com/python/examples/rmse-root-mean-square-error?utm_source to refrence for switch 
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
#to open up .mat data 
mat = sio.loadmat(r'C:\Users\geode\Downloads\ECG_Data.mat')  
trace = mat['ECG'][0]         # first row of ECG matrix and pull 
n = trace.size
t = np.linspace(0, 1, n)      # normalize the  time axis
orders = [3, 5, 9] #the roder wanted to see 
errors = []

#plot normal ecg data 
plt.plot(t, trace, label='original ECG')
#plot normal ecg data it will try and fit to plot pthe polynomial approximations for each specified order
for i in orders:
    coeffs = np.polyfit(t, trace, i)         # ind best-fit coefficients for  a blank degree poly
    pred   = np.polyval(coeffs, t)           # eevaluate the polynomial at all time points
    rmse   = np.sqrt(np.mean((trace - pred)**2))  # compute RMSE for fit basically points from line 
    errors.append(rmse)             # apperantly can store the error for later reporting
    plt.plot(t, pred, label=f'{i}° (RMSE={rmse:})') #add the add the polynomial curve to the plot
    
 #plot the new data 
plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('Polynomial Approximation of ECG')
plt.legend()
plt.grid(True)
plt.show()
#print the degree and error for each order for loop 
for order, rmse in zip(orders, errors):
    print(f'{order}th degree RMSE: {rmse:}')
