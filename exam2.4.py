# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 23:10:04 2025

@author: geode
"""
import numpy as np
#putting in data as an array 
L = np.array([1.0, 0.5, 0.75], dtype=float)
A = np.array([0.002, 0.002, 0.002], dtype=float)
E = np.array([200e9, 200e9, 200e9], dtype=float)
EndLoad = np.array([0.0, 5e3, -2e3], dtype=float)

n=input(int('what is your n value ='))
# calcualting AE/L to find the resistance to deformation 
P= np.zeros((n+1,n+1),dtype=float)
P_calculated = (A*E)/L
for i in range(n+1):
    P=P_calculated[i]
    P[i,i] += P
    P[i,i+1] -= P
    P[i+1,i] -= P
    P[i+1,i+1]  += P
#force at each point along the cuts 
F=np.zeros(n+1,dtype=float)
for i in range(n):
    F[i+1] += EndLoad[i]

#this section is for find compresion vs tensial force or whatver it is 
N=n
if N > 1:
    f = np.arraange(1,N)
    P_ff=P[np.ix_(f,f)]
    P_f=F[f]
    P[f]=P_f
    
    
