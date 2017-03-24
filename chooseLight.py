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
    model.load_weights('~/PycharmProjects/Projecton/arrows')
    return model

choosing_net = getMiniCnn()
heat_maps = []

def ReturnDirections(arrowsList):
    global choosing_net
    answers = []
    for image in arrowsList:
        image_answer = []
        myImage = imresize(image, ARROW_SIZE)
        type = choosing_net.predict([color for row in myImage for pix in row for color in pix])
        if max(type) == UNDEFINED:
            image_answer.append('U')
        else:
            if max(type) == FORWARD or max(type) == RIGHT_UP or max(type) == LEFT_UP:
                image_answer.append('F')
            if max(type) == RIGHT or max(type) == RIGHT_UP or max(type) == RIGHT_LEFT:
                image_answer.append('R')
            if max(type) == LEFT or max(type) == LEFT_UP or max(type) == RIGHT_LEFT:
                image_answer.append('L')
        answers.append(image_answer)
    return answers
