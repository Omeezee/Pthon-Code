# -*- coding: utf-8 -*-
"""
Created on Tue March 15 20:18:04 2025
@author: geode
"""
# assignment10_part1

# Importing the important python folders to do ploting and kmeans  https://www.geeksforgeeks.org/k-means-clustering-on-the-handwritten-digits-data-using-scikit-learn-in-python/?utm_source for later to convert 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Step 1: Initiate the data put into an array just to make the code quicker 
cell_size = np.array([15, 16, 14, 22, 21, 20, 8, 9, 7, 25, 26, 24])
protein_expression = np.array([200, 190, 210, 400, 410, 390, 120, 130, 110, 500, 520, 510])

# Step 2: combine the array into a single one
data = np.column_stack((cell_size, protein_expression))

# Step 3: plot it to see how it looks and  se if ploted propeyly 
plt.scatter(cell_size, protein_expression, c='blue', s=50)
plt.xlabel('Cell Size (μm)')
plt.ylabel('Protein Expression (units)')
plt.title('Cell Measurements Clustering')
plt.grid(True)
plt.show()

# Step 4: pick number of clusters
k = 3  # 3 and  try 4 to see which is closest  from the plot

# Step 5: run K-Means++
kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0)
labels = kmeans.fit_predict(data)
centroids = kmeans.cluster_centers_
#show the centers of the clutsters
print(centroids)

# Step 6: show clusters with colors to show different clustures 
colors = ['red', 'green', 'purple']
for i in range(k):
    plt.scatter(data[labels==i,0], data[labels==i,1], 
                c=colors[i], label=f'Cluster {i+1}', s=50)
# mark centroids to show where they would be for each cluster type
plt.scatter(centroids[:,0], centroids[:,1], 
            c='black', marker='x', s=100, linewidths=3, label='Centroids')
plt.xlabel('Cell Size (μm)')
plt.ylabel('Protein Expression (units)')
plt.title('K-Means++ Clustering of Cell Measurements')
plt.legend()
plt.grid(True)
plt.show()


