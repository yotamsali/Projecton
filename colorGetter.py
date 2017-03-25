import cv2
from PIL import Image, ImageStat
import numpy
import matplotlib

HEIGHT_WIDTH_RATIO = 2.2
THRESHOLD = 30

#states of the traffic light
GREEN = "Green"
ORANGE = "Orange"
RED_ORANGE = "Red-Orange"
RED = "Red"
OFF = "Off"
ERROR = -1


#receives an image of a traffic light and returns the cropped image of only the black part
#(without blue circle above)
#assumes that image is well cropped beforehand

def getBlackBox(im):
    height, width, temp = im.shape
    new_height = int(width * HEIGHT_WIDTH_RATIO)
    crop_img = im[height - new_height: height, 0: width]
    return crop_img


#revieces image of traffic light black box
#returns tuple containing three images
#top, middle, and bottom of the traffic light

def getTopMiddleBottom(im):
    height, width, temp = im.shape
    cut_1 = height // 3
    cut_2 = 2 * height // 3
    top = im[0: cut_1, 0: width]
    middle = im[cut_1: cut_2, 0: width]
    bottom = im[cut_2: height, 0: width]
    print("top" + str(top.shape))
    return top, middle, bottom


#calculates average brightness of image

def brightness(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    average_color_per_row = numpy.average(gray, axis=0)
    average_color = numpy.average(average_color_per_row, axis=0)
    return average_color







# TODO make sure that img is cropped image of traffic light
#returns the current state of the traffic light
#returns -1 in case of error

def getColor(img):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2
    # black = getBlackBox(img) todo: fix this function
    top, middle, bottom = getTopMiddleBottom(img)


    #get brightness
    brght_arr = [brightness(top), brightness(middle), brightness(bottom)]
    brght_arr = brght_arr - min(brght_arr)

    #check if lights are on
    light_on = lambda x: x > THRESHOLD
    light_arr = [light_on(x) for x in brght_arr]



    if (light_arr[BOTTOM] & (not light_arr[MIDDLE]) & (not light_arr[TOP])):
        return GREEN
    elif (light_arr[TOP] & light_arr[MIDDLE] & (not light_arr[BOTTOM])):
        return RED_ORANGE
    elif (light_arr[TOP] & (not light_arr[MIDDLE]) & (not light_arr[BOTTOM])):
        return RED
    elif (light_arr[MIDDLE] & (not light_arr[BOTTOM]) & (not light_arr[TOP])):
        return ORANGE
    elif ((not light_arr[BOTTOM]) & (not light_arr[MIDDLE]) & (not light_arr[TOP])):
        return OFF
    else:
        return ERROR