# version: 0.0.6
# author: picklez

# authors notes:
# !=========================!
# PLEASE SEE BOTTOM OF FILE BEFORE RUNNING

import numpy
import random
import math
import time
import tkinter
from PIL import Image,ImageTk
import os
import copy

cwd = os.getcwd()
start_time = time.time()

# TODO: create saves state; create restart start; also create arguments; also reduce memory

height = 900
width = 1600
dots_defined = 1000

def draw_black(array):
    for col in range(len(array)):
        for row in range(len(array[-1])):
            array[col][row][0] = 0
            array[col][row][1] = 0
            array[col][row][2] = 0
    return array

def create_random_dots(array):
    amt_of_dots = dots_defined
    dot_array = []
    while amt_of_dots != 0:
        new_dot = []
        new_dot.append(random.randrange(1,height-1))
        new_dot.append(random.randrange(1,width-1))
        dot_array.append(new_dot)
        amt_of_dots -= 1
    return sorted(dot_array)

def find_distance(dot1, dot2):
    d_x = abs(dot2[0]) - abs(dot1[0])
    d_y = abs(dot2[1]) - abs(dot1[1])
    distance = math.sqrt((d_x*d_x)+(d_y*d_y))
    return round(distance, 2)
    
def nearest(dot_array): # returns the 10 nearest dot to a given dot
    nearest = {}
    for dot in dot_array:
        sub_nearest = {}
        distance_array = []
        sub_dot_array = dot_array.copy()
        sub_dot_array.remove(dot)
        for dot2 in sub_dot_array:
            distance = find_distance(dot, dot2)
            sub_nearest[str(distance)] = dot2
            distance_array.append(distance)
        distance_array=sorted(distance_array)
        to_add = []
        for i in range(10):
            to_add.append(sub_nearest[str(distance_array[i])])
        nearest[str(dot)] = to_add
    return nearest

def line(point1, point2):
    point1 = point1.replace("[","").replace("]","").split(", ")
    for i in range(len(point1)):
        point1[i] = int(point1[i])
    all_points_between = []
    # y = mx + b
    dtop = point2[0] - point1[0]
    dbot = point2[1] - point1[1]
    m = (dtop + 0.001) / (dbot + 0.001)
    b = point1[0] - (m * point1[1])
    if point1[1] < point2[1]:
        for i in range(point1[1],point2[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    if point1[1] > point2[1]:
        for i in range(point2[1],point1[1]):
            hy = (m*i)+b
            hy = math.trunc(hy)
            hold = [int(hy), int(i)]
            all_points_between.append(hold)
    return all_points_between

def draw_lines(new_image, nearest):
    for key in nearest:
        for point in nearest[key]:
            line_array = line(key, point)
            r_or_b = random.randrange(0,2)
            for point2 in line_array:
                if point2[0] != 0 and point2[0] <= height and point2[1] != 0 and point2[1] <= width:
                    if r_or_b == 0:
                        new_image[point2[0]][point2[1]][0] = 255
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 0
                    if r_or_b == 1:
                        new_image[point2[0]][point2[1]][0] = 0
                        new_image[point2[0]][point2[1]][1] = 0
                        new_image[point2[0]][point2[1]][2] = 255
    return new_image

def apply_dots(new_image, dot_array):
    for dot in dot_array:
        # center of dot
        if dot[0] != 0 and dot[0] <= height-1 and dot[1] != 0 and dot[1] <= width-1:
            new_image[dot[0]][dot[1]][0] = 255
            new_image[dot[0]][dot[1]][1] = 255
            new_image[dot[0]][dot[1]][2] = 255
    return new_image

def get_random_dot_movement_dict(dot_array):
    direction_dict = {}
    for i in range(len(dot_array)):
        direction_dict[i] = random.randrange(0,8)
    return direction_dict

def next_step(direction_value):
    if direction_value == 0:
        return -1, -1
    if direction_value == 1:
        return -1, 0
    if direction_value == 2:
        return -1, 1
    if direction_value == 3:
        return 0, -1
    if direction_value == 4:
        return 0, 1
    if direction_value == 5:
        return 1, -1
    if direction_value == 6:
        return 1, 0
    if direction_value == 7:
        return 1, 1

def next_step_new_array(dot_array, direction_dict):
    for i in range(len(dot_array)):
        direction = direction_dict[i]
        current_dot = dot_array[i]
        next_move = next_step(direction)
        if current_dot[0]+1 != 0 and current_dot[0]+1 != height and current_dot[1]+1 != 0 and current_dot[1]+1 != width:
            current_dot[0] = current_dot[0] + next_move[0]
            current_dot[1] = current_dot[1] + next_move[1]
        dot_array[i] = current_dot
    return dot_array

def create_image(ni):
    da = create_random_dots(ni)
    ni = apply_dots(ni, da)
    ndm = nearest(da)
    ni = draw_lines(ni, ndm)
    dd = get_random_dot_movement_dict(da)
    dans = next_step_new_array(da, dd)
    return ni, dd, dans

def move_image(bi, da, dd):
    bi = apply_dots(bi, da)
    ndm = nearest(da)
    bi = draw_lines(bi, ndm)
    dans = next_step_new_array(da, dd)
    return bi, dd, dans
    
def get_image(bi, da, dd):
    bi = apply_dots(bi, da)
    ndm = nearest(da)
    bi = draw_lines(bi, ndm)
    return bi

def run_new(num_wanted):    
    all_images = []
    all_next = []
    # define our image array
    new_image = numpy.empty((height,width,3))
    new_image = draw_black(new_image)
    blank_image = new_image.copy()

    new_image, direction_dict, dot_array_next_step = create_image(new_image)
    all_images.append(new_image)
    all_next.append(copy.deepcopy(dot_array_next_step))
    
    save_directions(direction_dict)
    
    delta_create_len = 0
    for i in range(1,num_wanted):
        new_image_2, direction_dict, dot_array_next_step = move_image(blank_image.copy(), dot_array_next_step, direction_dict)
        all_images.append(new_image_2.copy().astype(numpy.uint8))
        all_next.append(copy.deepcopy(dot_array_next_step))
        time2 = time.time()
        delta_create_len = round(time2 - start_time, 2)
        print("Creating: " + str(i) + " Elapsed: " + str(delta_create_len) + "s")
        
    save_steps(all_next)
    window_on_run(all_images)

def save_directions(direct_dict): # wont save with a unique ID (yet)
    w = open("directions.csv", "w")
    for key in direct_dict:
        w.write(str(direct_dict[key]) + "\n")
    w.close()
    
def read_directions_dict():
    fn = cwd + "\\directions.csv"
    r = open(fn, "r")
    re = r.read().split("\n")
    re.pop()
    h = {}
    for i in range(len(re)):
        h[i] = int(re[i])
    return h

def save_steps(all_next_array):
    w = open("nexts.csv", "w")
    for i in range(len(all_next_array)):
        for ii in range(len(all_next_array[i])):
            w.write(str(i) + "," + str(all_next_array[i][ii][0]) + "," + str(all_next_array[i][ii][1]) + "\n")
    w.close()
    
def read_steps():
    fn = cwd + "\\nexts.csv"
    r = open(fn, "r")
    re = r.read().split("\n")
    re.pop()
    h = []
    tot_frames = int(len(re)/dots_defined)
    for i in range(tot_frames):
        sh = []
        for ii in range(dots_defined):
            ssh = re.pop(0)
            ssh = ssh.split(",")
            sssh = [int(ssh[1]), int(ssh[2])]
            sh.append(sssh)
        h.append(sh)
    return h
    
def append_steps(dans, sh):
    a = open("nexts.csv", "a")
    front = len(sh)-1
    for i in range(len(dans)):
        a.write(str(front) + "," + str(dans[i][0]) + "," + str(dans[i][1]) + "\n")
    a.close()

def resume_from(num_wanted):
    new_image = numpy.empty((height,width,3))
    new_image = draw_black(new_image)
    blank_image = new_image.copy()
    dh = read_directions_dict()
    sh = read_steps()
    all_images_2 = []
    for i in range(len(sh)):
        all_images_2.append(get_image(blank_image.copy(), sh[i], dh))
    
    if num_wanted == 0:
        window_on_run(all_images_2)
        exit()
    
    for i in range(num_wanted):
        new_image_2, direction_dict, dot_array_next_step = move_image(blank_image.copy(), sh[len(sh)-1], dh)
        all_images_2.append(new_image_2.copy().astype(numpy.uint8))
        sh.append(copy.deepcopy(dot_array_next_step))
        append_steps(dot_array_next_step, sh)
        time2 = time.time()
        delta_create_len = round(time2 - start_time, 2)
        print("Creating: " + str(i) + " Elapsed: " + str(delta_create_len) + "s")
    
    window_on_run(all_images_2)
    
def window_on_run(imgs):
    window = tkinter.Tk()
    window.title("Python GUI APP")
    window.configure(width=width,height=height)
    window.configure(bg='black')
    winWidth = window.winfo_reqwidth()
    winHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth /2)
    posDown = int(window.winfo_screenheight() / 2 - winHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    canvas = tkinter.Canvas(window)
    canvas = tkinter.Canvas(window, width=width, height=height)
    canvas.pack()
    
    while True:
        for i in range(len(imgs)):
            img2 = ImageTk.PhotoImage(image=Image.fromarray((imgs[i].copy()).astype(numpy.uint8)))
            print(type(img2))
            canvas.create_image(0, 0, anchor=tkinter.NW, image=img2)
            canvas.update()
            time.sleep(.1)
    
    window.mainloop()
    
# !======================!
# Before running please comment out all but 1 of the commands below!!
# Otherwise you will be sitting there for a long time. What the commands do
# is explained below.
    
# run this part if you would like to start the progrm without generating new frames
resume_from(0)
# run this to start the program from last frame and add 10 frames
# the argument given is how many frames you would like to generate in addition to
resume_from(10)
# run this if you would like to generate frames fresh from start
run_new(10)