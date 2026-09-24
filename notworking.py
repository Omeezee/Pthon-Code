# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 23:34:44 2025

@author: geode
"""
#UHMMM idk why it wont work but ya here is my bs work 
import numpy as np

L = np.array([1.0, 0.5, 0.75], dtype=float)    #given lengths per section 
A = np.array([0.002, 0.002, 0.002], dtype=float) #given areas per section
E = np.array([200e9, 200e9, 200e9], dtype=float)  #modulus per section 
# external force positive is force put on the right side left side is negative 
Force_e_known = np.array([0.0, 0.0, 5e3, -2e3], dtype=float) #known external forces 
n=L.size 

#solving the reaction forces force balance is force left+force righ + sum of external forces = 0 
sumf =float(Force_e_known.sum())
Li_over_AEi=L/(A*E)
Forces_R=np.array([float(Force_e_known[i+1:].sum()) for i in range(n)], dtype=float)
S = float(Li_over_AEi.sum())
C = float(np.dot(Forces_R, Li_over_AEi))
F_right = -C / S
F_left  = -F_right - sumf
#getting internal forces in each section from the right side down 
N_int = -(F_right +Forces_R)
#solving deformation for each section
delta =N_int*Li_over_AEi
#stress for each section
sigma = N_int/A
#nodes displacment/ movement 
u=np.zeros(n+1,dtype=float)
u[1]=np.cumsum(delta)

#output for this bs
#given probably 
print("Given Data:")
print(f"  lengths (L): {L} m")
print(f"  areas (A): {A} m²")
print(f"  material moudlus (E): {E} Pa")
print(f"  External Loads (Force_e_known): {Force_e_known} N\n")
#reacctions
print("Reactions:")
print(f"  Left Reaction  = {F_left:} N")
print(f"  Right Reaction = {F_right:} N\n")
#results of the sections that where calcualted 
print("Section Results:")
for i in range(n):
    print(f"\nPart {i+1}:") #for each calcuatlated part
    print("intneral force(N):", N_int[i]) #for the interanl forces
    print("deformation(m):",delta[i])
    print("stress(Pa):", sigma[i])
    if N_int[i] > 0: #to see if the force is tensile
        print("type: tension (+)")
    elif N_int[i] < 0: #to see if force is compression 
        print("type: compression (-)")
    else: #to see if there even is a force 
        print("type: none")

# also internal displacment to print it out still
#idk if this will work for different problems or not also btw idk if it even works right for this one 
# to check the work (idk )

