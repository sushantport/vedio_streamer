import cv2
import numpy as np


def convert_gray_scale(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

    # define range of red color in HSV 
    lower_red = np.array([30,150,50]) 
    upper_red = np.array([255,255,180]) 

    # create a red HSV colour boundary and  
    # threshold HSV image 
    mask = cv2.inRange(hsv, lower_red, upper_red) 

    # Bitwise-AND mask and original image 
    res = cv2.bitwise_and(frame,frame, mask= mask) 

    # finds edges in the input image image and 
    # marks them in the output map edges 
    edges = cv2.Canny(frame,100,200)

    return edges
