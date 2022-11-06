from vpython import *
import numpy as np
import math, sys

# Displays the n-th iteration of Antoine's Necklace - T_n specified in the Assignment

# K should probably be an even number
K = 16
c = 5
radius = 2.0*c
thickness = 0.5*c
# The scales for changing radius and thickness of the torus
scale_r = 1/6
scale_t = scale_r
# scale_t = 1/18
t_list = []

def radial_poistion(index, r):
    radian = 2*math.pi*index/K
    x_pos = r*math.cos(radian)
    y_pos = r*math.sin(radian)
    
    return vector(x_pos, y_pos, 0)

def np_to_vec(input):
    return vector(input[0], input[1], input[2])
    
def vec_to_np(input):
    return np.array([input.x, input.y, input.z])

def scale_vector(vector, length):
    """ Scales the vector to a specified length """
    np_vector = vec_to_np(vector)
    result = (length * np_vector) / np.linalg.norm(np_vector)
    return np_to_vec(result)

def cross_product(vector_1, vector_2):
    np_vector_1 = vec_to_np(vector_1)
    np_vector_2 = vec_to_np(vector_2)
    result = np.cross(np_vector_1, np_vector_2);
    return np_to_vec(result)

def plane_vector(normal, r):
    """ Given a normal vector and some radius r, find its two perpendicular vector of that size"""
    if normal.z != 0:
        vec_1 = vector(1, 1, -(normal.x + normal.y) / normal.z)
    elif normal.y != 0:
        vec_1 = vector(1, -(normal.x + normal.z) / normal.y, 1)
    else:
        vec_1 = vector(-(normal.z + normal.y) / normal.x, 1, 1)
    
    vec_2 = cross_product(vec_1, normal)
    
    vec_1 = scale_vector(vec_1, r)
    vec_2 = scale_vector(vec_2, r)
    
    return vec_1, vec_2

# This is not good coding practice but~ will fix it later

# Given a plane with normal vector and some center, find the K
# points around the center of distance r that form a regular K-gon

def radial_poistion_extend(center, normal, r):
    vec_1, vec_2 = plane_vector(normal, r)
    np_vec_1 = vec_to_np(vec_1)
    np_vec_2 = vec_to_np(vec_2)
    np_normal = vec_to_np(normal)
    
    matrix = np.column_stack((np_vec_1, np_vec_2, np_normal))
    result = []
    
    for index in range(0, K):
        radian = 2*math.pi*index/K
        x_pos = math.cos(radian)
        y_pos = math.sin(radian)
        vec = np.array([[x_pos, y_pos, 0]])
        transformed_vec = np.matmul(matrix, np.transpose(vec))
        result_vec = center + vector(transformed_vec[0][0], transformed_vec[1][0], transformed_vec[2][0])
        # sphere(pos=result_vec, radius=0.1)
        result.append(result_vec)
    
    return result
    # return vector(x_pos, y_pos, 0)

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
            current_torus = ring(
            pos=radial_poistion(i, radius),
            axis=vector(0,0,1),
            radius=scale_r*radius, thickness=scale_t*thickness, color=vector(1, 0, 0))
            tori_list.append(current_torus)
        else:
        # Odd position
            current_torus = ring(
            pos=radial_poistion(i, radius),
            axis=perpendicular(i, vector(0, 0, 0), radius),
            radius=scale_r*radius, thickness=scale_t*thickness, color=vector(0, 0, 1))
            
            tori_list.append(current_torus)
            
    return tori_list

def change_radius(s):
    global radius
    radius = s.number

def change_thickness(s):
    global thickness
    thickness = s.number

# The main body of the code:
if __name__ == "__main__":
    recursive = canvas(title=f"<h1>Antoine's Necklace - Initial Setup:</h1>",
        width=1000, height=1000,
        center=vector(0,0,0),
        background=color.white)
    
    t_list = init(K)
    original = ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius = radius, thickness = thickness, color=color.black, opacity=0.2)
    # button( bind=click, text='Show Setup' )
    # scene.append_to_caption('\n\n')
    wtext(text='Radius: ')
    winput( bind=change_radius, type='numeric')
    scene.append_to_caption('\n\n')
    wtext(text='Thickness: ')
    winput( bind=change_thickness, type='numeric')
    scene.append_to_caption('\n\n')
    
    def click(b):
        for torus in t_list:
            torus.radius = scale_r*radius
            torus.thickness = scale_t*thickness
        original.radius = radius
        original.thickness = thickness
    button(bind=click, text='Change Torus') 