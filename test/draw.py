# Woddpecker writing machine
# Author: ToddZhouFeng, aka Todd Zhou
# Date: 2021/01/25

import ctypes
import math
#import threading

import cv2
import numpy as np
import RPi.GPIO as GPIO

libc = ctypes.CDLL("libc.so.6")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 步进电机驱动
class Motor_28byj48:
    stride_angle = 5.625 # in degree
    gear_ratios = 64 # or 64
    step_pattern = [
        [1,0,0,0], # pattern 0
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]  # pattern 7
    ]
    delay=900 # in us

    def __init__(self, r, step_length, pins, direction=1):
        self.stride_length = 2*math.pi*r*self.stride_angle/360/self.gear_ratios
        self.step_length = step_length
        self.pins = pins
        self.steps_now = -1
        self.direction = direction
        GPIO.setwarnings(False)
        for i in pins:
            GPIO.setup(i, GPIO.OUT)

        print("A motor class is created. Please initialize it.")

    def initialize(self, init_thread_length):
        self.steps_now = int(init_thread_length / (self.step_length * self.stride_length))
        self.steps_now -= self.steps_now%8
        print("The motor has been initialized.")

    def rotate(self, steps):
        if steps>0:
            clockwise=-1*self.direction
        elif steps<0:
            clockwise=1*self.direction
        else:
            return

        if self.steps_now==-1:
            #if clockwise, then pattern start from 1 to 7 to 0
            #else then pattern start from 7 to 0
            start = int(4-clockwise*3)
            stop = int(4+clockwise*5)
            for i in range(abs(steps)):
                for j in range(start, stop, clockwise):
                    for k in range(4):
                        GPIO.output(self.pins[k], self.step_pattern[j%8][k])
                    libc.usleep(self.delay)
        else:
            for i in range(abs(steps)):
                self.steps_now-=clockwise
                for k in range(4):
                    GPIO.output(self.pins[k], self.step_pattern[self.steps_now%8][k])
                libc.usleep(self.delay)
                
        for k in range(4):
            GPIO.output(self.pins[k], 0)

    def move(self, thread_length):
        steps_next = int(thread_length/(self.step_length*self.stride_length))
        steps = (steps_next - self.steps_now)
        print("move to", steps_next, "from", self.steps_now)
        self.rotate(steps)

#查找最近点
def search(image, index_now):
    distance=0
    height=image.shape[0]
    width=image.shape[1]
    no_result=4
    while no_result != 0:
        distance+=1
        no_result=4
        k=0
        l=0
        if index_now[1]-distance>=0:
            #print(1, end='')
            for i in range(distance-1,-distance,-1):
                k=index_now[0]+i
                l=index_now[1]-distance
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[0]-distance>=0:
                k-=1
                if k>=0 and l>=0 and k<width and l < height and image[l,k]==1:
                    return [l, k]
        else:
            no_result-=1
        if index_now[0]-distance>=0:
            #print(2, end='')
            for i in range(-distance+1,distance):
                k=index_now[0]-distance
                l=index_now[1]+i
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[1]+distance<height:
                l+=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
        if index_now[1]+distance<height:
            #print(3, end='')
            for i in range(-distance+1,distance):
                k=index_now[0]+i
                l=index_now[1]+distance
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[0]+distance<width:
                k+=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
        if index_now[0]+distance<width:
            #print(4)
            for i in range(distance-1,-distance,-1):
                k=index_now[0]+distance
                l=index_now[1]+i
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
            if index_now[1]-distance>=0:
                l-=1
                if k>=0 and l>=0 and k<width and l < height and image[l, k]==1:
                    return [k, l]
        else:
            no_result-=1
    return None

#判断是否相邻
def is_next_to(index_a, index_b):
    if abs(index_a[0]-index_b[0])<=1 and \
        abs(index_a[1]-index_b[1])<=1:
        return True
    else:
        return False

#像素转线长
def index2length(index, step_length, oval=1, w=0):
    a_A = index[0]*step_length
    a_B = index[1]*step_length
    if oval==1:
        return [a_A, a_B]
    elif oval>1 and w>0:
        x = (a_A**2-a_B**2)/(2*w*oval**2)+w/2
        y = math.sqrt(a_A**2-(x**2)*(oval**2))
        a = math.sqrt(x**2+y**2)
        b = math.sqrt((w-x)**2+y**2)
        return [a, b]
    else:
        print("c2o error")
        return False

is_drop=0
#下笔
def drop():
    print("下笔")
    global is_drop
    is_drop=1
    
#抬笔
def lift():
    print("    抬笔")
    global is_drop
    is_drop=0

def main():
    image = 1-cv2.imread("final.png", cv2.IMREAD_GRAYSCALE)/255
    image = image.astype(np.uint8)
    motor_a = Motor_28byj48(r=2.1, step_length=1, pins=[4,18,23,24], direction=1)
    motor_b = Motor_28byj48(r=2.1, step_length=1, pins=[5,6,13,19], direction=1)
    motor_a.initialize(68)
    motor_b.initialize(158)
    global is_drop
    index_now=[0,0]
    while True:
        index_next=search(image, index_now)
        print(index_next)
        if index_next == None:
            break
        if not is_next_to(index_next, index_now) and is_drop:
            lift()
        thread_length_a, thread_length_b = index2length(index_next, 0.0046*25)
        print(thread_length_a, thread_length_b)
        motor_a.move(thread_length_a)
        motor_b.move(thread_length_b)
        if not is_drop:
            drop()
        image[index_now[1], index_now[0]] = 0
#         try:
#             for i in (-1, 0, 1):
#                 for j in (-1, 0, 1):
#                     image[index_now[1]+i, index_now[0]+j] = 0
#         except:
#             pass
        index_now[0]=index_next[0]
        index_now[1]=index_next[1]
        

main()