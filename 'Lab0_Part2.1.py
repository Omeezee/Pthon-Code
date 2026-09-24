# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:52:48 2024

@author: geode
"""
# use of variables to assigne different numbers to the variables by prompting a user a question 
# allows user to input value for a
a= float(input('number value for a'))
# allows user to input value for b
b= float(input('number value for b'))
# allows user to input value for c
c= float(input('number value for c'))
# printing the values assigned by the user.
# prints inputed value by user for a
print(f'Enter a (a number) : {a}')
# prints inputed value by user for b
print(f'Enter b (b number) : {b}')
# prints inputed value by user for c
print(f'Enter c (c number) : {c}')
# providing the coffecients in a printed form 
print(f'The coefficients provided are: a= {a}, b= {b}, c= {c}')
#equation for the quadratic formula as a variable to input numbers and get answers
#equation for the added quadratic formula 
r1 = (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a)
#equation for the subtracted quadratic formula 
r2 = (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)
# printing the roots calcualted by the quadratic formula 
print(f'The roots are x1= {r1}, x2= {r2}')


