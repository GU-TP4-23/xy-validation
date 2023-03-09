"""
Machine Vision for quality checks in terms of allgining the x-y values of the arm to the PCB
in a cartesian robot used in PCB manufacturing
"""

# from smbus import SMBus
import cv2 as cv
import numpy as np
import os
from rasp_I2C_comms import *

    

# get the centre of the image
def get_centre(img, width, length, offset_x=0, offset_y=0):
    dim = img.shape
    start_x = int((dim[1]-width)/2 + offset_x)
    start_y = int((dim[0]-length)/2 + offset_y)
    return img[start_y:start_y+length, start_x:start_x+width]

# find correlation of 2 images
def cosine_similarity(img1, img2):
    s = np.sum(np.multiply(img1,img2))
    s1 = np.sum(np.power(img1, 2))
    s2 = np.sum(np.power(img2, 2))
    
    return s/((s1**0.5)*(s2**0.5))

#  flatten image from 225 possible values to 5 values
def flatten_colors(img):
    for index, i in enumerate(img):
        for index_j, j in enumerate(i):
            if j <= 100:
                img[index, index_j] = 0
            elif 100 < j <= 150:
                img[index, index_j] = 115
            elif 150 < j <= 160:
                img[index, index_j] = 150
            elif 160 < j <= 210:
                img[index, index_j] = 170
            else:
                img[index, index_j] = 255
    return img
    
# get the top, bottom, left, right values
# flattens and centers
def get_surrounding(pcb, width, height):
    iter = 2
    top = flatten_colors(get_centre(pcb, width, height, 0, 0 + iter))
    bottom = flatten_colors(get_centre(pcb, width, height, 0, 0 - iter))
    right = flatten_colors(get_centre(pcb, width, height, 0 + iter, 0))
    left = flatten_colors(get_centre(pcb, width, height, 0 - iter, 0))
    return [top, bottom, left, right]


def main():
    # to be changed, needs to fit the calibration
    image_width = 200
    image_height = 200

    max_team_id = len(os.listdir(saved_dir))
    max_team_components = [len(os.listdir(f"{saved_dir}//{t}")) for t in os.listdir(saved_dir)]
    saved_dir = ""
    # initiate the camera
    current_team = 0
    current_team_component = 0 
    cam = cv.VideoCapture(0)

    # refer to rasp_I2C_comms to implement I2C calls to Team 5 pico
    cartesian_movement_I2C = [XY_up(), XY_down(), XY_left(), XY_right()]


    while (current_team<max_team_id and current_team_component<max_team_components[current_team]):
        # [to implement: wait for interrupt]


        # reads image shown on raspi camera and process it
        ret, frame = cam.read()
        compared_image = cv.imread(f"{current_team}//{current_team_component}")[:,:,1]
        current_ret, current_image = cam.read()
        current_image = current_image[:,:,1]
        current_image = get_centre(current_image, image_width, image_height)

        # note: save the compared image as sliced, and color flattened
        similarity = cosine_similarity(current_image.flatten(),compared_image.flatten())
        if similarity < 0.9:
            current_ret, current_image = cam.read()
            current_image = current_image[:,:,1]
            windows = get_surrounding(current_image)
            chosen = np.argmax([cosine_similarity(w, compared_image) for w in windows])
            cartesian_movement_I2C[chosen]()
        else:
            # [to implement: send acknowledge]
            
            # move on to next component/ team component
            if current_team_component >= max_team_components[current_team] -1:
                current_team_component = 0
                current_team += 1
            else:
                current_team_component += 1




main()