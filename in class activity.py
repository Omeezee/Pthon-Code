# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:26:47 2024

@author: geode
"""
s = input('enter a positive integer :')
N = int(s)
sum_g = N * (N+1)/ 2
print(f'Gauss formula sum is {sum_g}')

sum_f = 0
the_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
for n in the_numbers:
    sum_f = sum_f + n

print(f'The sum using for loop is {sum_f}')

iterator = range(100)
print(iterator)
