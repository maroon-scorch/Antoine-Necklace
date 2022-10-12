from vpython import *
from copy import deepcopy
import math

# Displays the initial setup of Antoine's Necklace - T_0 specified in the Assignment

# K should probably be an even number
K = 20
radius = 2
thickness = 0.5
iter = 1

initial = canvas(title="""<h1>Antoine's Necklace - Initial Setup</h1>""",
        width=1000, height=1000,
        center=vector(0,0,0))

def original(r, t):
    """The original torus that the necklace should be bounded in"""
    ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius = r, thickness = t)

def radial_poistion(index):
    radian = 2*math.pi*index/K
    x_pos = radius*math.cos(radian)
    y_pos = radius*math.sin(radian)
    
    return vector(x_pos, y_pos, 0)

def perpendicular(index):
    """ Index is guaranteed to be odd """
    vec_1 = radial_poistion(index - 1);
    vec_2 = radial_poistion(index);
    
    edge = vec_2 - vec_1;
    result = vec_1 + 0.5*edge;
    
    return result
    
def init(n):
    """ Given a positive number n, constructs the initial
    setup of Antoine's Necklace """
    print("This setup contains " + str(n) + " tori.")
    
    tori_list = []
    
    for i in range(0, n):
        print(i)
        if i % 2 == 0:
        # Even position
            current_torus = ring(canvas=initial,
            pos=radial_poistion(i),
            axis=vector(0,0,1),
            radius=0.5, thickness=0.1, color=vector(1, 0, 0))
            
            tori_list.append(current_torus)
        else:
        # Odd position
            current_torus = ring(canvas=initial,
            pos=radial_poistion(i),
            axis=perpendicular(i),
            radius=0.5, thickness=0.1, color=vector(0, 0, 1))
            
            tori_list.append(current_torus)
            
    return tori_list


# The main body of the code:
if __name__ == "__main__":
    init(K);