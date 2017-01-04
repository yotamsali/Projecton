import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure


FACTOR = 0.6

def templateMatcher (im):
    FACTORTEMPLATE = 0.05
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
    newWidth = (int) (width * FACTORTEMPLATE)
    newHeight = (int) (height * FACTORTEMPLATE)
    list = [newHeight, newWidth]
    arraySize = np.array(list)
    tlIm = imresize(tlIm, arraySize)

    f, arrPrint = matplotlib.pyplot.subplots(1, 2)
    arrPrint[0].imshow(tlIm, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()




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
"""""""""
imR = camera[:,:,0]
imG = camera[:,:,1]
imB = camera[:,:,2]

greenThresholG = 90
ThreshoDiff = 15
sum = imR +imB+ imG


#binaryColorGreen = np.floor((1/3)*(imG > 0.43*sum)
#                            + (1/3)*(imG > greenThresholG)
#                            + (1/3)* (sum > 120))



#binaryColorGreen = morphology.binary_opening(binaryColorGreen)
#removeSmall = morphology.remove_small_objects(binaryColorGreen)
#binaryColorGreen = binaryColorGreen - removeSmall
"""""""""""

tic()
camera = io.imread('tlHard.jpg')
#camera = color.rgb2gray(camera)
lstOrig = camera.shape
width = lstOrig[1]
height = lstOrig[0]
newWidth = (int)(width * FACTOR)
newHeight = (int)(height * FACTOR)
print(newHeight)
list = [newHeight, newWidth]
arraySize = np.array(list)
toc()
tic()
print(arraySize)
print([height, width])
tlIm = imresize(camera, arraySize)
tlIm = exposure.equalize_adapthist(tlIm)
toc()
tic()
map = templateMatcher(tlIm)
bin = map > 0.55
toc()

f, arr = matplotlib.pyplot.subplots(1, 2)
arr[0].imshow(tlIm, cmap='color', interpolation='nearest')
arr[1].imshow(bin, cmap='gray', interpolation='nearest')

matplotlib.pyplot.show()
