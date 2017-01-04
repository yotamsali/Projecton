import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure

TEMPS_SIZES = [1,1.1,1.2,1.3] #The image is half from its original size
MATCH_RATE = 0
PIXEL_INDEX = 1
TEMPLATE_INDEX = 2
HEIGHT = 0
WIDTH = 1
FACTOR = 0.66


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
        template_size = np.array([(int)(height * factor) ,(int)(width * factor)])
        templates_list.append(my_imresize(template,template_size))

    return templates_list

# gets List of template matched images
# returns the best matched pixel, the match rate and the right template
def max_spot(arr):

    best_match = 0;
    best_match_index = 0;
    best_template= 0;

    for a in arr:
        new_candidate = np.max(a)
        if new_candidate > best_match:
            best_match = new_candidate
            best_match_index = np.unravel_index(a.argmax(), a.shape)
            best_template = arr.index(a)

    return best_match, best_match_index, best_template

# gets image and a traffic light template (from a moment ago)
# returns new relevant template and the location of the traffic light right now
def Track(im, template):

    possible_templates_list = templates(template)
    filters = []
    i = 0;
    for t in possible_templates_list:
        filters.append(feature.match_template(im, t, pad_input=False))
        i+=1
        """
        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(feature.match_template(im, t, pad_input=False), cmap='gray', interpolation='nearest')
        matplotlib.pyplot.show()
        """
    traffic_light = max_spot(filters)

    new_template_size = possible_templates_list[traffic_light[TEMPLATE_INDEX]].shape
    new_template_index = traffic_light[PIXEL_INDEX]
    new_template = im[new_template_index[HEIGHT]:new_template_index[HEIGHT]+new_template_size[HEIGHT],
                   new_template_index[WIDTH]:new_template_index[WIDTH]+new_template_size[WIDTH]]

    return new_template, new_template_index

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")

camera = io.imread('1a.PNG')
camera = color.rgb2gray(camera)
"""
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(camera, cmap='gray', interpolation='nearest')
matplotlib.pyplot.show()
"""
template = camera[256:285,924:934]
camera = io.imread('a2.PNG')
camera = camera[220:290,860:915]
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(camera, cmap='gray', interpolation='nearest')
matplotlib.pyplot.show()

camera = color.rgb2gray(camera)
tic()
result = Track(camera,template)
toc()
f, arr = matplotlib.pyplot.subplots(1, 1)
arr.imshow(result[0], cmap='gray', interpolation='nearest')
matplotlib.pyplot.show()
x=3



