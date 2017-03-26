import cv2
from PIL import Image, ImageStat
import numpy
import matplotlib.pyplot

HEIGHT_WIDTH_RATIO = 2.2
THRESHOLD = 20

#states of the traffic light
GREEN = "Green"
ORANGE = "Orange"
RED_ORANGE = "Red-Orange"
RED = "Red"
OFF = "Off"
ERROR = -1

RED_LOW = [0,40,100]
RED_UP = [20,255,255]

ORANGE_LOW = [10,40,100]
ORANGE_UP = [30,255,255]

GREEN_LOW = [85,90,100]
GREEN_UP = [105,255,255]

BRIGHT_LOW = [160, 40, 100]
BRIGHT_UP = [180, 255, 255]

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
    height, width = im.shape
    cut_1 = height // 3
    cut_2 = 2 * height // 3
    top = im[0: cut_1, 0: width]
    middle = im[cut_1: cut_2, 0: width]
    bottom = im[cut_2: height, 0: width]
    return top, middle, bottom


#calculates average brightness of image

def brightness(im):
    gray = im
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
    ''''
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(img, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    cv2.imwrite("/home/yovelrom/PycharmProjects/Projecton/color_examples/orange/3/image.jpg", cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(hsv, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    '''
    lower_red1 = numpy.array(RED_LOW)
    upper_red1 = numpy.array(RED_UP)
    lower_orange1 = numpy.array(ORANGE_LOW)
    upper_orange1 = numpy.array(ORANGE_UP)
    lower_green = numpy.array(GREEN_LOW)
    upper_green = numpy.array(GREEN_UP)

    mask_bright = cv2.inRange(hsv, numpy.array(BRIGHT_LOW), numpy.array(BRIGHT_UP))
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    ''''
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(mask_bright, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(mask1, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    '''
    mask_red = cv2.bitwise_or(mask1, mask_bright)
    '''
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(mask_red, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    '''
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    #mask_green = cv2.bitwise_or(mask2, mask_bright)
    mask3 = cv2.inRange(hsv, lower_orange1, upper_orange1)
    mask_orange = cv2.bitwise_or(mask3, mask_bright)
    '''
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(img, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    '''
    # black = getBlackBox(img) todo: fix this function
    #top, middle, bottom = getTopMiddleBottom(img)
    top , temp1, temp2 = getTopMiddleBottom(mask_red)
    temp1, middle, temp2 = getTopMiddleBottom(mask_orange)
    temp1, temp2, bottom = getTopMiddleBottom(mask_green)
    #get brightness
    brght_arr = [brightness(top), brightness(middle), brightness(bottom)]
    brght_arr = brght_arr - min(brght_arr)

    #check if lights are on
    light_on = lambda x: x > THRESHOLD
    light_arr = [light_on(x) for x in brght_arr]

    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(top, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    # cv2.imwrite("/home/yovelrom/PycharmProjects/Projecton/color_examples/orange/3/top.jpg", top)
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(middle, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    #cv2.imwrite("/home/yovelrom/PycharmProjects/Projecton/color_examples/orange/3/middle.jpg", middle)
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(bottom, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    #cv2.imwrite("/home/yovelrom/PycharmProjects/Projecton/color_examples/orange/3/bottom.jpg", bottom)


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
'''''
image = cv2.cvtColor(cv2.imread("./my/frame2535.jpg"), cv2.COLOR_BGR2RGB)
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(image, cmap='gray', interpolation='nearest')
matplotlib.pyplot.show()
print(getColor(image[296:364, 640:672]))
#print(getColor(image[227:324, 475:522]))
'''