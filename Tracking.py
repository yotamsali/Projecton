import math

import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import feature
import cv2

TEMPS_SIZES = [1,1.1,1.2] #The image is half from its original size
MATCH_RATE = 0
PIXEL_INDEX = 1
TEMPLATE_INDEX = 2
HEIGHT = 0
WIDTH = 1

DECREACE_UPPER_BOUND = 40
INCREACE_LOWER_BOUND = 1.1

OLD_TO_NEW_RATIO = 0.7

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

# gets image and a traffic light template (from a moment ago)
# returns new relevant template and the location of the traffic light right now
def Track(im, template, xy):

    # bounds of the template to be found, min/max to keep the bound legal
    size = template.shape
    up = max(xy[HEIGHT] - int(size[HEIGHT] * size[HEIGHT] / DECREACE_UPPER_BOUND), 0)
    down = min(xy[HEIGHT] + int(size[HEIGHT]*INCREACE_LOWER_BOUND), im.shape[HEIGHT]-1)
    left = max(int(xy[WIDTH] - 2*size[WIDTH]), 0)# - math.ceil(math.pow(2,size[1]*(im.shape[1]/2 - xy[1])/1920)))
    right = min(int( xy[WIDTH] + 2*size[WIDTH]), im.shape[WIDTH]-1) # + math.ceil(math.pow(2,size[1]*(-im.shape[1]/2 + xy[1])/700)))
    imNew = im[up:down, left:right]

    # get new templates
    possible_templates_list = templates(template)
    filters = []
    i = 0;

    # match the templates
    for t in possible_templates_list:
        filters.append(feature.match_template(imNew, t, pad_input=False))
        i+=1
        """""
        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(feature.match_template(imNew, t, pad_input=False), cmap='gray', interpolation='nearest')
        matplotlib.pyplot.show()
        """
    # find best match
    traffic_light = max_spot(filters)

    # get the properties of the new template - first - size, second - location on the screen
    new_template_size = possible_templates_list[traffic_light[TEMPLATE_INDEX]].shape
    new_template_index = [traffic_light[PIXEL_INDEX][HEIGHT]
                          +up, traffic_light[PIXEL_INDEX][WIDTH]+left]


    startH = new_template_index[HEIGHT]
    endH = new_template_index[HEIGHT] + new_template_size[HEIGHT]
    startW = new_template_index[WIDTH]
    endW = new_template_index[WIDTH] + new_template_size[WIDTH]

    new_template = im[startH: endH, startW: endW]

    template = imresize(template, new_template_size)
    new_template = np.multiply(new_template,OLD_TO_NEW_RATIO)+\
                   np.multiply(np.reshape(template,new_template.shape),1-OLD_TO_NEW_RATIO)

    return new_template, new_template_index

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

"""""
camera = io.imread('/home/yovelrom/Downloads/dayTrain/dayClip3/frames/dayClip3--00000.png')
#camera = color.rgb2hsv(camera)

template = camera[361:376,625:632]
location = (361, 625)
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(template, cmap='gray')#, interpolation='nearest')
matplotlib.pyplot.show()

runtime = []
for i in range(1,80,1):
    tic()
    number_string = string(i)
    camera = cv2.imread('/home/yovelrom/Downloads/dayTrain/dayClip3/frames/dayClip3--' + number_string + '.png')
    #camera = color.rgb2hsv(camera)
    template, location = Track(camera,template, location)
    size = template.shape
    pts = (int(location[1]), int(location[0])), (int(location[1])+size[1], int(location[0])+size[0])
    img2 = camera
    cv2.rectangle(img2, pts[0], pts[1], (0,255,0))
    #f, arr = matplotlib.pyplot.subplots(1, 1)
    #arr.imshow(template, cmap='gray')#, interpolation='nearest')
    #matplotlib.pyplot.show()
    cv2.imshow('img2', img2)
    #cv2.imwrite("/home/yovelrom/Downloads/gif/" + number_string + ".jpg", camera)
    k = cv2.waitKey(60) & 0xff
    runtime.append(toc())
matplotlib.pyplot.plot(runtime)
matplotlib.pyplot.ylabel('running-time (sec)')
matplotlib.pyplot.xlabel('frame')
matplotlib.pyplot.show()
"""""