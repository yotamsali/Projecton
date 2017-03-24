from keras.models import Sequential
from keras.layers import Dense
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure
import operator

FACTOR = 1.1
SMALLEST_TL = [6,3]
X = 1
Y = 0
up = 0
down = 1
left = 0
right = 1

HEIGHT = 20
WIDTH = 12

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc
'''
builds the cnn from weights
'''
def getMiniCnn():
    model = Sequential()
    model.add(Dense(12, input_dim=720, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))
    model.load_weights('/home/yovelrom/PycharmProjects/Projecton/avivtut')
    return model

minicnn = getMiniCnn()
heat_maps = []

'''
returns the 
'''
def get_heat_map(images):
    for image in images:
        print(image.shape)
        tic()
        regionList = []
        #cv2.imshow("a", image)
        #cv2.waitKey(0)
        for y in range(image.shape[Y]-HEIGHT):
            for x in range(image.shape[X]-WIDTH):
                rawRegion = image[y:y+HEIGHT, x:x+WIDTH]
                region = [color for row in rawRegion for pix in row for color in pix]
                regionList.append(region)
        predictions = minicnn.predict(regionList)
        '''
        weird_map = np.zeros((image.shape[Y]- HEIGHT,image.shape[X]-WIDTH))
        height, width = weird_map.shape
        for i in range(height):
            for j in range(width):
                weird_map[i,j] = predictions[i*height +j]
        '''
        heat_map = np.reshape(predictions,(image.shape[Y]- HEIGHT,image.shape[X]-WIDTH))
        print heat_map.shape
        print(toc())
        heat_maps.append(heat_map)

#Gets the index of the biggest contour
def GetMax(contours):
    lst = []
    for c in contours:
        lst.append(sum(c.shape))
    return lst.index(max(lst))

lst = [cv2.imread("/home/yovelrom/Downloads/dayTrain/dayClip1/frames/dayClip1--00000.png")[322:433,602: 790]]


def ReturnLights(cutImlst):
    get_heat_map(cutImlst)
    np.multiply(heat_maps, 255)
    returnlst = []
    for i in range(len(heat_maps)):
        heat = np.array(heat_maps[i], dtype=np.float32)
        heat = np.multiply(heat,255)
        hm = np.array(heat, dtype=np.uint8)
        ret, thresh = cv2.threshold(hm, 230,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        max_contour = GetMax(contours)
        x, y, w, h = cv2.boundingRect(contours[max_contour])
        cX,cY = x+w/2+3,y+h/2+10
        heightAddition = SMALLEST_TL[Y]
        widthAddition = SMALLEST_TL[X]
        lstSizesOptions = []
        size = []
        while widthAddition <= 40:
            candidate = imresize(cutImlst[i][cY-int(heightAddition):cY+int(heightAddition),cX-int(widthAddition):cX+int(widthAddition)],[20,12])
            f, arr = matplotlib.pyplot.subplots(1, 1)
            arr.imshow(candidate, cmap='gray')#, interpolation='nearest')
            matplotlib.pyplot.show()

            lstSizesOptions.append([color for row in candidate for pix in row for color in pix])
            heightAddition*=FACTOR
            widthAddition*=FACTOR
        predictions = minicnn.predict(lstSizesOptions)
        print(size)
        print(predictions)
        return y,x,h,w

ReturnLights(lst)



