# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:48:43 2024

@author: geode
"""
#module 2
import numpy as np

def herons(s1, s2, s3):
    perimeter = s1 + s2 + s3
    s = perimeter / 2  # Semi-perimeter
    area = np.sqrt(s * (s - s1) * (s - s2) * (s - s3))
    return area

def triangle_type(s1, s2, s3):
    a, b, c = sorted([s1, s2, s3])  # Sort sides for comparison
    if a == b == c:
        return 'Equilateral'
    elif a == b or b == c:
        if a**2 + b**2 == c**2:
            return 'Right'
        return 'Isosceles'
    elif a**2 + b**2 == c**2:
        return 'Right'
    return 'Ordinary'
