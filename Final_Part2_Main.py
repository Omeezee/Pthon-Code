import pandas as pd
import numpy as np

# Define the file path
file_path = r"C:\Users\geode\Downloads\Triangle_Sides.xlsx"
output_file_path = r"C:\Users\geode\Downloads\Triangle_Sides_Complete.csv"

# Load the Excel file
data = pd.read_excel(file_path)

# Step 1: Replace negative side lengths with their absolute values
data[['s1', 's2', 's3']] = data[['s1', 's2', 's3']].abs()

# Step 2: Calculate the perimeter
data['perimeter'] = data['s1'] + data['s2'] + data['s3']

# Step 3: Calculate the area using Heron's formula
s = data['perimeter'] / 2  # Semi-perimeter
data['area'] = np.sqrt(s * (s - data['s1']) * (s - data['s2']) * (s - data['s3']))

# Step 4: Determine the triangle type
def determine_triangle_type(row):
    a, b, c = sorted([row['s1'], row['s2'], row['s3']])  # Sort sides to simplify comparisons
    if a == b == c:
        return 'Equilateral'
    elif a == b or b == c:
        if a**2 + b**2 == c**2:
            return 'Right'
        return 'Isosceles'
    elif a**2 + b**2 == c**2:
        return 'Right'
    return 'Ordinary'

data['type'] = data.apply(determine_triangle_type, axis=1)

# Step 5: Save the updated DataFrame into a new CSV file
data.to_csv(output_file_path, index=False)

# Display a confirmation message
print(f"Processed data has been saved to: {output_file_path}")
