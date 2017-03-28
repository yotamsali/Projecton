"""
returns all detected traffic lights
"""

from mask import*
import numpy as np
from tlDetectionCNN import*
import cv2
def tlDetect (im):
    f, arr = matplotlib.pyplot.subplots(1, 1)
    try:
        arr.imshow(im, cmap='gray')  # , interpolation='nearest')
    except:
        exit(0)
    matplotlib.pyplot.show()
    im = np.array(im)
    maskList = maskFilter(im)

    afterNeuralList = ReturnLights(maskList)
    return afterNeuralList




