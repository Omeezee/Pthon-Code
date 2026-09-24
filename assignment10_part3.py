# -*- coding: utf-8 -*-
"""
Created on Tue March 15 23:15:56 2025

@author: geode
"""
# assignment10_part3

# clustering prosthetic designs graph stuff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# load the CSV (change path as needed)
df = pd.read_csv(r"C:\Users\geode\Downloads\prosthetics_optimization_dataset.csv")  # assumes columns: force, battery

# pick out the columns to use and graph
force_output = df.iloc[:,0].values
battery_consumption = df.iloc[:,1].values

# stack into a signle data stack not multiple
prosthetic_data = np.column_stack((force_output, battery_consumption))

# cluster into 3 groupsusing kmeans++ so that it selects the best cluster groups avaible 
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
labels = kmeans.fit_predict(prosthetic_data)
centroids = kmeans.cluster_centers_

#show the centroids values
print(centroids)

# visualize the graph to show teh different color for each cluster adn also the centroids so that user can see the centroids selected by kmeans ++ an
colors = ['red', 'green', 'blue']
for i in range(3):
    plt.scatter(prosthetic_data[labels==i,0], prosthetic_data[labels==i,1],
                c=colors[i], label=f'Cluster {i+1}', s=50)
plt.scatter(centroids[:,0], centroids[:,1],
            c='black', marker='x', s=100, linewidths=3, label='Centroids')
plt.xlabel('Force Output')
plt.ylabel('Battery Consumption')
plt.title('K-Means++ Clustering of Prosthetic Designs')
plt.legend()
plt.grid(True)
plt.show()

