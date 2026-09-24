#Exam 2 BIOE 3020
import numpy as v
#inout section of vlaues that are given 
units=print("ensure all units are the same for each section")
L=input(int("What is the lenght of the element Li = ")) #total lenght will be given 
A=input(int("What is the cross sectional area = "))     #are may be given or may need to be calcualted this will be a list 
E=input(int("What is the modulus of elasticity = "))  #this value will be given to us 
P=input(int("What is the external load applied at the right end of element i = "))  #force mutliple loads this value will be give to us and is the force pushing from the right side 
n= input(int("What is the total number of iterations"))      #this value will be the number of cuts of the bar
#geneartes lists/arrays of the values for the cross sectional areas, teh youngs modulus and the lengths although length is consisten for eferything but to calcualte later an array will beeasy 
Li=v.full(n,L/n) 
Ai=v.full(n,A)
Ei=v.full(n,E)
#zero out the force to start and find forces/loads on the right side
Pi = v.zeros(n)
Pi[-1] = P
#find the total loads on the left side of each section
S=v.zeros(n+1)
for f in range(1,n+1):
    S[f]=S[f-1]+Pi[f-1]
    
#solving for first section of force pressing and finding equalibrium equaiton then latter turn ot for loop
#all intneral loads solved using this funciton 

#equations to calcualte 
#equilbirum check 
#total equiliibrium 
#stress
#deformation
#Reaction at A
#Reaction at B 

     
