# -*- coding: utf-8 -*-
"""
Created on Tue March 15 22:13:44 2025

@author: geode
"""
# assignment10_part2

# clustering MRI intensity vs lesion diameter: first get teh necessary folders to see
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# put the numbers in arrays
mri_intensity = np.array([180, 200, 150, 220, 210, 250])
lesion_diameter = np.array([30, 35, 25, 40, 38, 45])

# combine the array into a single one from 3d to 2d
mri_data = np.column_stack((mri_intensity, lesion_diameter))

# do K-Means++ with 2 clusters maybe try a few more just to test for now
kmeans = KMeans(n_clusters=2, init='k-means++', random_state=0)
labels = kmeans.fit_predict(mri_data)
centroids = kmeans.cluster_centers_

#show the centers of the clutsters in number formate
print(centroids)

# plot it out with different colors to show teh different clustures 
colors = ['red','blue']
for i in range(2):
    plt.scatter(mri_data[labels==i,0], mri_data[labels==i,1],
                c=colors[i], label=f'Cluster {i+1}', s=50)
    #show the sentroids in the cluster and make them black can change size and other variables for fomating later
plt.scatter(centroids[:,0], centroids[:,1],
            c='black', marker='x', s=100, linewidths=3, label='Centroids')
plt.xlabel('MRI Intensity')
plt.ylabel('Lesion Diameter (mm)')
plt.title('K-Means++ Clustering of MRI & Lesion Data')
plt.legend()
plt.grid(True)
plt.show()

