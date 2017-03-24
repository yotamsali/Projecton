from scipy import io as sio
import tensorflow
from carcnn import carcnn
from keras.models import Sequential
from keras.layers import Dense
import numpy
import cv2
from scipy.misc import imresize
from skimage import io, feature
import matplotlib.pyplot
import numpy as np
from keras.models import save_model

SIZE = [120,70]

def ReturnXY():
    mldata_descr_ordering = np.zeros((2,), dtype=np.object)
    mldata_descr_ordering[0] = 'data'
    mldata_descr_ordering[1] = 'label'
    X = np.empty([10000,3*120*70], np.uint8)
    labels = np.empty([1,10000], np.uint8)
    j=0
    index = 0

    for dir in range(1, 13):
        T = '/home/yovelrom/Downloads/cutImages/clip' + str(dir) + '/0.jpg'
        F = '/home/yovelrom/Downloads/cutImages/neg' + str(dir) + '/neg0.jpg'
        rawImage = cv2.imread(T)
        rawnegIm = cv2.imread(F)
        i = 0  # change the path to your computer
        while not ((rawImage is None) or (rawnegIm is None)):
            image = imresize(rawImage,SIZE)
            negIm = imresize(rawnegIm,SIZE)
            reshapedImage = np.reshape(image, (1, 3 * 120 * 70))
            reshapedNegImage = np.reshape(negIm, (1, 3 * 120 * 70))
            X[index] = reshapedImage
            labels[0,index] = 1
            index += 1
            X[index] = reshapedNegImage
            labels[0,index] = 0
            index += 1
            T = '/home/yovelrom/Downloads/cutImages/clip' + str(dir) + '/' + str(i) + '.jpg'
            F = '/home/yovelrom/Downloads/cutImages/neg' + str(dir) + '/neg' + str(i) + '.jpg'
            rawImage = cv2.imread(T)
            rawnegIm = cv2.imread(F)
            i += 1
            if(i == 2161):
                print len(X)
            if (index == 10000):
                break
        print(dir)
        if (index == 10000):
            break

    print len(X)
    sio.savemat('images', {'data': X, 'label': labels, 'mldata_descr_ordering': mldata_descr_ordering})
    print ("yovel")


ReturnXY()