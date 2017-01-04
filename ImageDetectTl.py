import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure

FACTOR = 0.2
THRESHOLD = 0.43
TEMP1 = 0.09
TEMP2 = 0.06


def templateMatcher (im, factorTemplate):
    """
    tlIm = io.imread('tl.png')
    tlIm = tlIm[220:255,488:500,:]
    tlIm = color.rgb2gray(tlIm)
    sizeOrig = tlIm.shape
    height = sizeOrig[0]
    width = sizeOrig[1]
    newWidth = (int) (width * FACTOR)
    newHeight = (int) (height * FACTOR)
    list = [newHeight, newWidth]
    """""
    tlIm = io.imread('template.jpg')
    tlIm = color.rgb2gray(tlIm)
    tlIm = tlIm[210:508, 351:491]
    sizeOrig = tlIm.shape
    height = sizeOrig[0]
    width = sizeOrig[1]
    newWidth = (int) (width * factorTemplate)
    newHeight = (int) (height * factorTemplate)
    list = [newHeight, newWidth]
    arraySize = np.array(list)
    tlIm = imresize(tlIm, arraySize)
    """""
    f, arrPrint = matplotlib.pyplot.subplots(1, 2)
    arrPrint[0].imshow(tlIm, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    """""
    map = feature.match_template(im, tlIm, pad_input=True)
    return map

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

#********** SCRIPT *********************************************************




camera = io.imread('tlData2.png')
tic()
camera = color.rgb2gray(camera)
lstOrig = camera.shape
width = lstOrig[1]
height = lstOrig[0]
newWidth = (int)(width * FACTOR)
newHeight = (int)(height * FACTOR)
print(newHeight)
list = [newHeight, newWidth]
arraySize = np.array(list)
print(arraySize)
print([height, width])
tlIm = imresize(camera, arraySize)
tlIm = exposure.equalize_adapthist(tlIm)
toc()
tic()
map1 = templateMatcher(tlIm, TEMP1);
map2 =  templateMatcher(tlIm,TEMP2);
bin1 = map1 > THRESHOLD
bin2 = map2 > THRESHOLD
toc()

f, arr = matplotlib.pyplot.subplots(1, 3)
arr[0].imshow(tlIm, cmap='gray', interpolation='nearest')
arr[1].imshow(bin1, cmap='gray', interpolation='nearest')
arr[2].imshow(bin2, cmap='gray', interpolation='nearest')

matplotlib.pyplot.show()
