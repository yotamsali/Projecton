from keras.models import Sequential
from keras.layers import Dense
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure


FACTOR = 1.2
SMALLEST_TL = [6,3]
MIDDLE_TL = [23,12]
LARGE_TL = [45,23]
SMALL = 0
MEDIUM = 1
LARGE = 2
WRONG = -1
SIZES = [SMALLEST_TL,MIDDLE_TL,LARGE_TL]

X = 1
Y = 0
up = 0
down = 1
left = 0
right = 1

HEIGHT = 20
WIDTH = 12

OPEN_RADIUS = 2
MATCH_THRESHOLD = 0.7

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
    model.load_weights('avivtut')
    return model

minicnn = getMiniCnn()


'''
returns the 
'''
def get_heat_map(images):
    heat_maps = []
    sizes = []
    for image_tuple in images:
        #print(image.shape)
        #tic()

        image = image_tuple[0]
        #f, arr = matplotlib.pyplot.subplots(1, 1)
        #arr.imshow(image, cmap='gray')  # , interpolation='nearest')
        #matplotlib.pyplot.show()

        regionList, newSize = addImages(image)
        if len(regionList[-1]) <= 0 :
            heat_maps.append([])
            continue
        #TODO - just fix the error in neural network
        try:
            predictions = minicnn.predict(regionList)
        except:
            raise Exception('Error in heatmap - fix it using keras !')

        '''
        weird_map = np.zeros((image.shape[Y]- HEIGHT,image.shape[X]-WIDTH))
        height, width = weird_map.shape
        for i in range(height):
            for j in range(width):
                weird_map[i,j] = predictions[i*height +j]
        '''
        sizes.append(newSize)
        heat_map = np.reshape(predictions,(image.shape[Y]- SIZES[newSize][Y],
                                           image.shape[X]-SIZES[newSize][X]))
        print (heat_map.shape)
        print(toc())
        heat_maps.append(heat_map)
        #if heat_map != []:
        #    f, arr = matplotlib.pyplot.subplots(1, 1)
        #    arr.imshow(heat_map, cmap='gray')#, interpolation='nearest')
        #    matplotlib.pyplot.show()



    return heat_maps, sizes

def addImages(image):
    candidates = []
    newSize = -1
    # check im size and fit the candidates to it
    size = (image.shape[Y],image.shape[X])
    if size[Y] - SMALLEST_TL[Y] < 1 or size[X] - SMALLEST_TL[X] < 1:
        return [], newSize
    elif size[Y] - MIDDLE_TL[Y] < 1 or size[X] - MIDDLE_TL[X] < 1:
        step = (SMALLEST_TL[Y], SMALLEST_TL[X])
        newSize = SMALL

    elif size[Y] - LARGE_TL[Y] < 1 or size[X] - LARGE_TL[X] < 1:
        step = (MIDDLE_TL[Y], MIDDLE_TL[X])
        newSize = MEDIUM
    else:
        step = (LARGE_TL[Y], LARGE_TL[X])
        newSize = LARGE

    for y in range(size[Y] - step[Y]):
        for x in range(size[X] - step[X]):
            rawRegion = imresize(image[y:y + step[Y], x:x + step[X]], (HEIGHT,WIDTH))
            region = [color for row in rawRegion for pix in row for color in pix]
            candidates.append(region)
    return candidates, newSize

# Gets the index of the biggest contour
def GetMax(contours):
    lst = []
    for c in contours:
        lst.append(sum(c.shape))
    return lst.index(max(lst))


def ReturnLights(cutImlst):
    tic()
    heat_maps, sizes = get_heat_map(cutImlst)
    print("CNN - "+str(toc()))
    #np.multiply(heat_maps, 255)
    returnlst = []
    for i in range(len(cutImlst)):
        if len(heat_maps[i]) <= 0:
            continue

        heat = np.array(heat_maps[i], dtype=np.float32)
        heat = np.multiply(heat,255)
        hm = np.array(heat, dtype=np.uint8)
        ret, thresh = cv2.threshold(hm, 230,255,cv2.THRESH_BINARY)

        #kernelOPEN = np.ones((OPEN_RADIUS, heat.shape[X], OPEN_RADIUS), np.uint8)
        #thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOPEN)
        img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(thresh, cmap='gray')#, interpolation='nearest')
        try:
           matplotlib.pyplot.show()
        except:
           pass
        contours = [contours[GetMax(contours)]]
        fit_options = []
        fit_value = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            cX,cY = x + w//2 + SIZES[sizes[i]][X]//4, y + h//2 + SIZES[sizes[i]][Y]//4
            heightAddition = SMALLEST_TL[Y]
            widthAddition = SMALLEST_TL[X]
            lstSizesOptions = []
            size = []
            print ('c')
            while widthAddition <= 40 and cY >= int(heightAddition) and cX >= int(widthAddition) \
                        and cutImlst[i][0].shape[Y]-cY  >= int(heightAddition) and cutImlst[i][0].shape[X]-cX >= int(widthAddition) :
                candidate = imresize(cutImlst[i][0][cY-int(heightAddition):cY+int(heightAddition), cX-int(widthAddition):cX+int(widthAddition)],[20,12])
                """"
                f, arr = matplotlib.pyplot.subplots(1, 1)
                arr.imshow(candidate, cmap='gray')#, interpolation='nearest')
                try:
                    matplotlib.pyplot.show()
                except:
                    pass
                """
                size.append((int(heightAddition), int(widthAddition)))
                lstSizesOptions.append([color for row in candidate for pix in row for color in pix])
                heightAddition += 2
                widthAddition += 1
            if len(lstSizesOptions) == 0:
                continue
            predictions = minicnn.predict(lstSizesOptions)
            # get max match
            if max(predictions) < MATCH_THRESHOLD:
                continue
            max_match = np.amax(predictions)
            index = np.where(predictions == max_match)
            max_fit_size = size[index[0][0]]
            fit_options.append((cutImlst[i][0][cY - max_fit_size[Y]: cY + max_fit_size[Y], cX - max_fit_size[X]: cX + max_fit_size[X]]))
            f, arr = matplotlib.pyplot.subplots(1,1)
            arr.imshow(fit_options[-1], cmap='gray')  # , interpolation='nearest')
            try:
                matplotlib.pyplot.show()
            except:
                pass
            fit_value.append(max_match)
            print(size)
            print(predictions)
        if len(fit_options) == 0:
            continue
        index = fit_value.index(max(fit_value))
        returnlst.append(fit_options[index])
    return returnlst




