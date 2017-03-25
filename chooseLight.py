from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from scipy.misc import imresize
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot
import numpy as np
from scipy.misc import imresize
from skimage import io, feature , color, exposure

FACTOR = 1.1
SMALLEST_TL = [6,3]
X = 1
Y = 0
up = 0
down = 1
left = 0
right = 1
ARROW_SIZE = (30,30)
UNDEFINED = 0
FORWARD = 1
RIGHT = 2
LEFT = 3
RIGHT_UP = 4
RIGHT_LEFT = 5
LEFT_UP = 6
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


def getMiniCnn():
    model = Sequential()
    model.add(Dense(20, input_dim=900, init='uniform', activation='relu'))
    model.add(Dense(7, init='uniform', activation='sigmoid'))
    model.load_weights('arrows')
    return model

def ReturnDirections(arrowsList, direction):
    global choosing_net
    answers = []
    #TODO
    try:
        return arrowsList[0]
    except:
        return None
    for tuple in arrowsList:
        #the string of chars of direction
        strAns = ''
        #resizing the tuple image size to standart size
        img = tuple[0]
        imgToNeural = imresize(img, ARROW_SIZE)
        vectorToNeural = np.array([coulor for row in imgToNeural for pix in row for coulor in pix])
        print(vectorToNeural.shape)
        type = choosing_net.predict(vectorToNeural)
        if max(type) == UNDEFINED:
            strAns += 'U'
        else:
            if max(type) == FORWARD or max(type) == RIGHT_UP or max(type) == LEFT_UP:
                strAns += 'F'
            if max(type) == RIGHT or max(type) == RIGHT_UP or max(type) == RIGHT_LEFT:
                strAns += 'R'
            if max(type) == LEFT or max(type) == LEFT_UP or max(type) == RIGHT_LEFT:
                strAns += 'L'
        answers.append(strAns)

    candidateList = arrowsList[not answers.__contains__('U') and answers.__contains__(direction)]
    if len(candidateList) == 0:
        return None
    # return the maximal size image
    finalTuple = max(candidateList, lambda elem: elem[0].shape[0] * elem[0].shape[1])
    return finalTuple


choosing_net = getMiniCnn()
heat_maps = []