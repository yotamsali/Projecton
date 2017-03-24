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


'''
returns the 
'''
def get_heat_map(images):
    heat_maps = []
    for image_tuple in images:
        #print(image.shape)
        #tic()
        image = image_tuple[0]
        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(image, cmap='gray')#, interpolation='nearest')
        matplotlib.pyplot.show()
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
        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(heat_map, cmap='gray')#, interpolation='nearest')
        matplotlib.pyplot.show()
    return heat_maps

#Gets the index of the biggest contour
def GetMax(contours):
    lst = []
    for c in contours:
        lst.append(sum(c.shape))
    return lst.index(max(lst))

lst = [(cv2.imread("/home/yovelrom/Downloads/dayTrain/dayClip1/frames/dayClip1--00000.png")[322:433,602: 790], 0, 0)]


def ReturnLights(cutImlst):
    heat_maps = get_heat_map(cutImlst)
    np.multiply(heat_maps, 255)
    returnlst = []
    for i in range(len(cutImlst)):
        heat = np.array(heat_maps[i], dtype=np.float32)
        heat = np.multiply(heat,255)
        hm = np.array(heat, dtype=np.uint8)
        ret, thresh = cv2.threshold(hm, 230,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours.sort(key=lambda c: sum(c.shape))
        #contour = GetMax(contours)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cX,cY = x+w/2+3,y+h/2+10
            heightAddition = SMALLEST_TL[Y]
            widthAddition = SMALLEST_TL[X]
            lstSizesOptions = []
            size = []
            print ('c')
            while widthAddition <= 40:
                candidate = imresize(cutImlst[i][0][cY-int(heightAddition):cY+int(heightAddition),cX-int(widthAddition):cX+int(widthAddition)],[20,12])
                #f, arr = matplotlib.pyplot.subplots(1, 1)
                #arr.imshow(candidate, cmap='gray')#, interpolation='nearest')
                #matplotlib.pyplot.show()

                lstSizesOptions.append([color for row in candidate for pix in row for color in pix])
                heightAddition*=FACTOR
                widthAddition*=FACTOR
            predictions = minicnn.predict(lstSizesOptions)
            index = -1
            for j in range(predictions.shape[0]):
                if predictions[predictions.shape[0] - j-1] > 0.99:
                    returnlst.append((lstSizesOptions[predictions.shape[0] - j], y+cutImlst[i][1], x+cutImlst[i][2]))
                    break
            print(size)
            print(predictions)
    return returnlst

ReturnLights(lst)



