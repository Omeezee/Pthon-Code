# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 16:02:44 2024

@author: geode
"""
#inputs the angle 
import math
n=int(input('Enter an angle between 0 to 180 degrees'))
if n > 180 :
    print(f'WARNING your angle must be between 0 to 180 degrees try again')
else: # converts the angle to radians using math.pi from google for numbers of pi 3.1415
    b= round(n*(math.pi/180), 5) 
    # print(f'your degrees in radians is {b}')
#calcualtes sinx with the math function 
sinx = round(math.sin(b),10) 
# print(f"The sin of your angle is {sinx}")
# cacluating sinx using factorial 
sinx4 = b - (b**3 / math.factorial(3)) + (b**5 / math.factorial(5)) - (b**7 / math.factorial(7))
#step 2: adding the 5th term 
sinx5 = sinx4 + (b**9 / math.factorial(9))
# Use Equation (3) to get cos(x) based on the sin values
cosx4 = math.sqrt(1 - sinx4**2)
cosx5 = math.sqrt(1 - sinx5**2)
cosx_exact = round(math.cos(b), 10)

# Adjust cos(x) signs depending on the angle range (0 to pi)
if math.pi / 2 <= b <= math.pi:
    cosx4 = -cosx4
    cosx5 = -cosx5
# rounding all the values 
sinx4 = round(sinx4, 10)
sinx5 = round(sinx5, 10)
cosx4 = round(cosx4, 10)
cosx5 = round(cosx5, 10)

#printing all the results with the right formatting 

print(f"Results for an angle of {n} degrees (radians: {b}):")
print(f"sin(x) using 4 terms of expansion: {sinx4}")
print(f"sin(x) using 5 terms of expansion: {sinx5}")
print(f"sin(x) exact: {sinx}")
print(f"cos(x) using 4 terms of expansion: {cosx4}")
print(f"cos(x) using 5 terms of expansion: {cosx5}")
print(f"cos(x) exact: {cosx_exact}")
