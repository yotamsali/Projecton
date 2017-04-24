"""
module for tracking the traffic light
"""

import math

import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import feature
import cv2
from time import sleep

TEMPS_SIZES = [1,1.02,1.05] #The image is half from its original size
MATCH_RATE = 0
PIXEL_INDEX = 1
TEMPLATE_INDEX = 2
HEIGHT = 0
WIDTH = 1

DECREACE_UPPER_BOUND = 40
INCREACE_LOWER_BOUND = 1.5

OLD_TO_NEW_RATIO = 0.6

def my_imresize(im, size):
    im = imresize(im, size)
    im = np.multiply(im, 1/256)
    return im


# gets the traffic light from a moment age
# returns possible relevant templates for the recent image
def templates(template):

    templates_list = []
    height = template.shape[HEIGHT]
    width = template.shape[WIDTH]

    for factor in TEMPS_SIZES:
        template_size = np.array([(int)(height * factor) ,(int)(np.ceil(width * factor))])
        x = imresize(template,template_size)
        templates_list.append(x)

    return templates_list

# gets List of template matched images
# returns the best matched pixel, the match rate and the right template
def max_spot(arr):

    best_match = 0
    best_match_index = 0
    best_template= 0

    for a in arr:
        new_candidate = np.max(a)
        if new_candidate > best_match:
            best_match = new_candidate
            best_match_index = np.unravel_index(a.argmax(), a.shape)
            best_template = arr.index(a)

    return best_match, best_match_index, best_template

# gets image, a traffic light template (from a moment ago), it's location and the difference between the last two
# traffic lights.
# returns new relevant template, the location of the traffic light right now, the relevant temaplate
# (merged with old images) and the difference between the locations of the traffic light now and the previous image.
def Track(im, template, xy, diff = 0):

    # bounds of the template to be found, min/max to keep the bound legal

    size = template.shape
    up = max(xy[HEIGHT] - int(0.5*size[HEIGHT])-1, 0)
    down = min(xy[HEIGHT] + int(size[HEIGHT]*INCREACE_LOWER_BOUND), im.shape[HEIGHT]-1)
    left = max(int(xy[WIDTH] - size[WIDTH]-1) , 0) #- math.ceil(size[1]*(-im.shape[1]/2 + xy[1])/150)
    right = min(int( xy[WIDTH] + 2*size[WIDTH])+1 , im.shape[WIDTH]-1) #math.ceil(size[1]*(-im.shape[1]/2 + xy[1])/150)

    if diff[WIDTH] < 0:
        left = max(left + diff[WIDTH],0)
    if diff[WIDTH] > 0:
        right =  min(diff[WIDTH] + right,im.shape[WIDTH]-1)
    if diff[HEIGHT] < 0:
        up = max(int(1.5*diff[HEIGHT])+up, 0)
    if diff[HEIGHT] > 0:
        down = min( diff[HEIGHT] + down, im.shape[HEIGHT]-1)

    imNew = im[up:down, left:right]

    possible_templates_list = templates(template)
    filters = []
    i = 0;

    # match the templates
    for t in possible_templates_list:
        filters.append(feature.match_template(imNew, t, pad_input=False))
        i+=1

        #f, arr = matplotlib.pyplot.subplots(1, 1)
        #arr.imshow(feature.match_template(imNew, t, pad_input=False), cmap='gray', interpolation='nearest')
        #matplotlib.pyplot.show()

    # find best match
    traffic_light = max_spot(filters)

    # get the properties of the new template - first - size, second - location on the screen
    new_template_size = possible_templates_list[traffic_light[TEMPLATE_INDEX]].shape
    new_template_index = (traffic_light[PIXEL_INDEX][HEIGHT]
                          +up, traffic_light[PIXEL_INDEX][WIDTH]+left)


    startH = new_template_index[HEIGHT]
    endH = new_template_index[HEIGHT] + new_template_size[HEIGHT]
    startW = new_template_index[WIDTH]
    endW = new_template_index[WIDTH] + new_template_size[WIDTH]

    new_template = im[startH: endH, startW: endW]

    # merge old with new
    template = imresize(template, new_template_size)
    template_merged_with_past = np.multiply(new_template,OLD_TO_NEW_RATIO)+\
                  np.multiply(np.reshape(template,new_template.shape),1-OLD_TO_NEW_RATIO)
    return new_template, new_template_index, template_merged_with_past, (-xy[HEIGHT]+new_template_index[HEIGHT],
                                                                         -xy[WIDTH]+new_template_index[WIDTH])

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc

def string(i):
    new = ''
    if i==0:
        return "00000"
    inte = 10000
    while i/inte == 0:
        new += '0'
        inte /= 10
    new += str(i)
    return new
