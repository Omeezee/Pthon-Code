# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 09:12:09 2025

@author: geode
"""
#source https://www.geeksforgeeks.org/principal-component-analysis-pca/
import scipy.io as sio # to read matlab files 
import numpy as np #standard number library 
from sklearn.decomposition import PCA # to use the pca calcualtion and not make it manual library 
import matplotlib.pyplot as plt #plotting library 
#to open up .mat data and load ECG matrix took too long 
raw  = sio.loadmat(r'C:\Users\geode\Downloads\ECG_Data.mat')
data = raw['ECG']                 #to get actual ecg array 
# standardization get teh zero mean and unit variance for data 
means = data.mean(axis=0)         
stds  = data.std(axis=0)
scaled = (data - means) / stds
# calcuate the PCA and total  variance
pca = PCA()
scores = pca.fit_transform(scaled)
cumilative_var= np.cumsum(pca.explained_variance_ratio_) * 100
#plotting the values and total variances
plt.plot(range(1, len(cumilative_var)+1), cumilative_var, '.-', linewidth=1.5)
plt.axhline(95, linestyle='--')  # 95% cutoff
plt.xlabel('components')
plt.ylabel('cumulative variance (%)')
plt.grid(True)
plt.show()

# show how many of the values reach over 95%
n = np.argmax(cumilative_var >= 95) + 1
print(f"components for 95% variance: {n}")

compressed = scores[:, :n]
