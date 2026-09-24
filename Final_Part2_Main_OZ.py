# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:48:50 2024

@author: geode
"""
#main program
import pandas as pd
from Final_Part2_Functions import herons, triangle_type

# Define the file paths
file_path = r"C:\Users\geode\Downloads\Triangle_Sides.xlsx"
output_file_path = r"C:\Users\geode\Downloads\Triangle_Sides_Complete.csv"

# Load the Excel file
data = pd.read_excel(file_path)

# Step 1: Replace negative side lengths with their absolute values
data[['s1', 's2', 's3']] = data[['s1', 's2', 's3']].abs()

# Step 2: Calculate the perimeter
data['perimeter'] = data['s1'] + data['s2'] + data['s3']

# Step 3: Calculate the area using Heron's formula
data['area'] = data.apply(lambda row: herons(row['s1'], row['s2'], row['s3']), axis=1)

# Step 4: Determine the triangle type
data['type'] = data.apply(lambda row: triangle_type(row['s1'], row['s2'], row['s3']), axis=1)

# Step 5: Save the updated DataFrame into a new CSV file
data.to_csv(output_file_path, index=False)

# Display a confirmation message
print(f"Processed data has been saved to: {output_file_path}")
