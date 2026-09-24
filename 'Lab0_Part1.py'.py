# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
X=int(input("Enter x for which the polynomial will be calculated"))
print(type(X))
# the polynomial 
P0=3.0
P1=-.5
P2=5
P3=2/3
P4=-2.3
P5=7



PX=(P5*X**5)+(P4*X**4)+(P3*X**3)+(P2*X**2)+(P1*X**1)+(P0*X**0)
sum_p =  P5+P4+P3+P2+P1+P0
# prints 
print(f'The  vale of X is {X}')
print(f'\n\t The value of P(X) is {PX}')
print(f'sum_p {sum_p}')
