import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure

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

def tocReturn():
    import time
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc
    else:
        print ("Toc: start time not set")

#********** SCRIPT *********************************************************

def cameraTry(Total,filepath):

    FACTOR = 0.5 * Total
    TEMP1 = 0.04 * Total
    TEMP2 = 0.09 * Total
    TEMP3 = 0.14 * Total

    rowMin = (int)(0 * Total)
    rowMax = (int)(250 * Total)
    culMin = (int)(50 * Total)
    culMax = (int)(750 * Total)

    camera = io.imread(filepath)
    tic()
    camera = color.rgb2gray(camera)
    lstOrig = camera.shape
    width = lstOrig[1]
    height = lstOrig[0]
    newWidth = (int)(width * FACTOR)
    newHeight = (int)(height * FACTOR)
    list = [newHeight, newWidth]
    arraySize = np.array(list)
    tlIm = imresize(camera, arraySize)
    tlIm = exposure.equalize_adapthist(tlIm)
    tim1 = tocReturn();
    tic()
    tlIm = tlIm[rowMin:rowMax, culMin:culMax]

    map1 = templateMatcher(tlIm, TEMP1)
    map2 = templateMatcher(tlIm, TEMP2)
    map3 = templateMatcher(tlIm, TEMP3)

    factorThreshold = 0.8
    THRESHOLD1 = np.min([factorThreshold* np.max(map1),0.64])
    THRESHOLD2 = np.min([factorThreshold* np.max(map2),0.64])
    THRESHOLD3 = np.min([factorThreshold* np.max(map3),0.64])

    print([THRESHOLD1,THRESHOLD2, THRESHOLD3])

    bin1 = map1 > THRESHOLD1
    bin2 = map2 > THRESHOLD2
    bin3 = map3 > THRESHOLD3

    tim2 = tocReturn()
    print(str(tim2)+ " sec")

    f, arr = matplotlib.pyplot.subplots(1, 4)
    arr[0].imshow(tlIm, cmap='gray', interpolation='nearest')
    arr[1].imshow(bin1, cmap='gray', interpolation='nearest')
    arr[2].imshow(bin2, cmap='gray', interpolation='nearest')
    arr[3].imshow(bin3, cmap='gray', interpolation='nearest')
    matplotlib.pyplot.show()
    return [tim1, tim2]


"""""
const = 17
str = 'tlData.png'
res = []
for k in range(const):
    res+=[0.2+k*0.05]
print(res)
timeTemplate = [0 for i in range(len(res))]
timeNabaz = [0 for i in range(len(res))]
ind = 0
for elem in res:
    vec = cameraTry(elem)
    timeTemplate[ind] = (vec[1]/3)
    timeNabaz[ind] = vec[0]
    ind += 1
print(timeTemplate)
print(timeNabaz)
matplotlib.pyplot.plot(res, timeTemplate)
matplotlib.pyplot.show()
matplotlib.pyplot.plot(res, timeNabaz)
matplotlib.pyplot.show()
"""""

cameraTry(1, 'tlData3.png')
cameraTry(1, 'tlData2.png')
cameraTry(1, 'tlData2.png')