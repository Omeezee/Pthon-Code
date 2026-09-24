# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 18:35:01 2024

@author: ridva
"""

# IMPORT the libraries that you need sin, cos,pi, and plotting

import math
import matplotlib.pyplot as plt

# FUNCTIONS START HERE

#==============================================================================
def Create_Theta(P):
    theta = [i * (2 * math.pi / (P - 1)) for i in range(P)]
    return theta
#==============================================================================
def Make_List_Circles(N, mode):
   
    list_circles = []
    
    for i in range(N):
        r    = i
        x0   = r
        P    = 50*r
        
        # Match case for setting the y-coordinate of the origin
        match mode:
            case 0:
                y0=x0
            case 1:
                y0=2*x0
            case 2:
                y0=-x0
            case _ :
                y0=x0**2
        
        d_circle = {
            'r':  r,
            'x0': x0,
            'y0': y0,
            'P':  P
            }
        
        list_circles.append(d_circle)
    
    return list_circles





#==============================================================================
def Create_XY_Coords(d_dict):
    
    x0 = d_dict['x0']
    y0 = d_dict['y0']
    r = d_dict['r']
    theta = d_dict['theta']
    
    xCoor = []
    yCoor = []
    
    for angle in theta:
        x = x0 + r * math.cos(angle)
        y = y0 + r * math.sin(angle)
        xCoor.append(x)
        yCoor.append(y)
        
    return xCoor, yCoor


#..............................................................................
# Main starts here, complete the expressions (the dotted parts)

s    = input('Enter N and mode: ')
temp = s.split()
N    = int(temp[0])
mode = int(temp[1])




################################################################################
#	DO NOT CHANGE  THE PART BELOW 
################################################################################

# CREATING the list that contains N dictionaries, one for each circle
list_circles = Make_List_Circles(N, mode)

# CREATING THE PLOT OBJECTS
plt.figure(figsize=(5,5))


# FOR LOOP for drawing the circles
for d_circle in list_circles:
    theta              = Create_Theta(d_circle['P'])
    d_circle['theta']  = theta
    xCoor,yCoor        = Create_XY_Coords(d_circle)
    
    # This will plot the circle for each loop - DO NOT CHANGE IT
    plt.plot(xCoor, yCoor) 


# THESE LINES WILL add a grid and labels to the plot created in the loop.
plt.grid()
plt.xlabel('x coord')
plt.ylabel('y coord')
plt.show()

