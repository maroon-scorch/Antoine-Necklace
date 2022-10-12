from vpython import *
from copy import deepcopy
import math

# Displays the n-th iteration of Antoine's Necklace - T_n specified in the Assignment

# K should probably be an even number
K = 20
c = 5
radius = 2*c
thickness = 0.5*c
iter = 1

recursive = canvas(title="""<h1>Antoine's Necklace - Recursive Steps</h1>""",
        width=1000, height=1000,
        center=vector(0,0,0))

def radial_poistion(index, r):
    radian = 2*math.pi*index/K
    x_pos = r*math.cos(radian)
    y_pos = r*math.sin(radian)
    
    return vector(x_pos, y_pos, 0)

def perpendicular(index, center, r):
    """ Index is guaranteed to be odd """
    vec_1 = center + radial_poistion(index - 1, r);
    vec_2 = center + radial_poistion(index, r);
    
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
            current_torus = ring(canvas=recursive,
            pos=radial_poistion(i, radius),
            axis=vector(0,0,1),
            radius=1/4*radius, thickness=1/20*radius, color=vector(1, 0, 0))
            tori_list.append(current_torus)
        else:
        # Odd position
            current_torus = ring(canvas=recursive,
            pos=radial_poistion(i, radius),
            axis=perpendicular(i, vector(0, 0, 0), radius),
            radius=1/4*radius, thickness=1/20*radius, color=vector(0, 0, 1))
            
            tori_list.append(current_torus)
            
    return tori_list

def recursive_steps(torus_list, iter):
    if iter > 0:
        necklace = compound(torus_list);
        for torus in tori_list:
            current_necklace = necklace.clone(pos = torus.pos,
                                              axis = torus.axis,
                                              radius = torus.radius
                                              ,thickness=torus.thickness)
        iter = iter - 1;
        result = [];
        recursive_steps(result, iter);
        
    print("Exiting the recursion!")


# The main body of the code:
if __name__ == "__main__":
    tori_list = init(K);
    
    # necklace = compound(tori_list);
    
    for torus in tori_list:
        torus.visible = False        
        for i in range(0, K):
            if i % 2 == 0:
            # Even position
                current_torus = ring(canvas=recursive,
                pos=torus.pos + radial_poistion(i, torus.radius),
                axis=torus.axis,
                radius=1/4*torus.radius, thickness=1/20*torus.thickness, color=vector(1, 0, 0))
            else:
        # Odd position
                current_torus = ring(canvas=recursive,
                pos=torus.pos + radial_poistion(i, torus.radius),
                radius=1/4*torus.radius, thickness=1/20*torus.thickness, color=vector(0, 0, 1))
                
                current_torus.axis = perpendicular(i, current_torus.pos, torus.radius)
    
    # necklace.axis = vector(1.95106, 0.309017, 0);
    # necklace.axis = vector(0, 1.95106, 0.309017) 
    # print(necklace.axis);
    # size = vector(necklace.size.x, necklace.size.y, necklace.size.z);
    # necklace.visible = False;
    # for torus in tori_list:
    #     torus.visible = False;
    #     current_necklace = necklace.clone(pos = torus.pos,
    #                                     radius = torus.radius)
    #     current_necklace.axis = torus.axis;
    #     current_necklace.size = 1/4*size;
    #     print(torus.axis);
    #     print(current_necklace.axis);
    #     print("-------------")
        
    # iter = iter - 1;
    # recursive_steps(torus_list, iter);