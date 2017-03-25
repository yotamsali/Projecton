import cv2
from PIL import Image, ImageStat
import numpy
import matplotlib.pyplot

HEIGHT_WIDTH_RATIO = 2.2
THRESHOLD = 5

#states of the traffic light
GREEN = "Green"
ORANGE = "Orange"
RED_ORANGE = "Red-Orange"
RED = "Red"
OFF = "Off"
ERROR = -1

RED_LOW = [0,0,170]
RED_UP = [30,255,255]
GREEN_LOW = [85,90,90]
GREEN_UP = [95,255,255]

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
    return top, middle, bottom


#calculates average brightness of image

def brightness(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    average_color_per_row = numpy.average(gray, axis=0)
    average_color = numpy.average(average_color_per_row, axis=0)
    print(average_color)
    return average_color







# TODO make sure that img is cropped image of traffic light
#returns the current state of the traffic light
#returns -1 in case of error

def getColor(img):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(img, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()

    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(hsv, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()

    lower_red1 = numpy.array(RED_LOW)
    upper_red1 = numpy.array(RED_UP)
    lower_green = numpy.array(GREEN_LOW)
    upper_green = numpy.array(GREEN_UP)

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.bitwise_or(mask1, mask2)
    img = cv2.bitwise_and(img, img, mask=mask)
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(img, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    # black = getBlackBox(img) todo: fix this function
    top, middle, bottom = getTopMiddleBottom(img)
    #get brightness
    brght_arr = [brightness(top), brightness(middle), brightness(bottom)]
    brght_arr = brght_arr - min(brght_arr)

    #check if lights are on
    light_on = lambda x: x > THRESHOLD
    light_arr = [light_on(x) for x in brght_arr]

    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(middle, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(bottom, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(top, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()

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

image = cv2.cvtColor(cv2.imread("./my/frame237.jpg"), cv2.COLOR_BGR2RGB)
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(image, cmap='gray', interpolation='nearest')
matplotlib.pyplot.show()
print(getColor(image[298:336, 921:937]))
#print(getColor(image[227:324, 475:522]))