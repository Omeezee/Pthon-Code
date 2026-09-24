# -*- coding: utf-8 -*-
"""
Created on Tue May  6 11:29:46 2025

@author: geode
"""
#part 1 final bioe
import numpy as np
import matplotlib.pyplot as plt
#array of the data given 
t = np.array([0, 5, 10, 15, 20, 25, 30]) # tme points
C = np.array([100, 60, 36, 22, 14, 9, 6]) # measred concentration 
# calcualting the sums and means for the regression formula 
n = len(t)  # finds the number of data points
lnC = np.log(C)  # natural log of each concentration value needed varaible to calcule this 
sum_t    = np.sum(t) # sumation of t
sum_lnC  = np.sum(lnC) # sumation of ln(C)
sum_t2   = np.sum(t * t)# sumation of t^2
sum_tlnC = np.sum(t * lnC) # sum of t * ln(C)
mean_t   = sum_t    / n  # average of t
mean_lnC = sum_lnC  / n # average of ln(C)
mean_t2  = sum_t2   / n # average of t^2
mean_tlnC= sum_tlnC / n # average of t * ln(C)
# calcaution of the  slope (b) and intercept (a) of the line lnC = a + b * t 
b = (mean_tlnC - mean_t * mean_lnC) / (mean_t2 - mean_t**2)# slope calcaution
a = mean_lnC - b * mean_t # finding intercept

# finding the k_d and initial ln concentration 
kd = -b  # decay constant (day)
lnC0 = a  # the calcualtion fo ln(C), intercept corresponds for the og starting concetntration

#finding r^2
#predicting the lnC values at each time
lnC_pred = a + b * t
# total sum of squareses of lnC around the mean
SS_tot = np.sum((lnC - mean_lnC)**2)

# the sum of squares between the actual value and predicted lnC 
SS_res = np.sum((lnC - lnC_pred)**2)

R2 = 1 - (SS_res / SS_tot)    # coefficient of determination

#printing values
print(f"a (intercept)     = {a:}")  # print the  intercept
print(f"b (slope)         = {b:}")# print slope b
print(f"k_d (decay rate)  = {kd:} day")  # print decay constant a 
print(f"R^2 (the scale of fit)= {R2:}")# print goodness ffit
#graphing the things
plt.figure()                               
plt.scatter(t, lnC, label='the seen ln(C)')  
plt.plot(t, lnC_pred, label='the line of best fit')   
plt.xlabel('time (days)')                  
plt.ylabel('ln(concentration)')              
plt.title('linear regression fit')
plt.legend()                                  
plt.grid(True)                             
plt.show()