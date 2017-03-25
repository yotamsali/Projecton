from mask import*
import numpy as np
from tlDetectionCNN import*
def tlDetect (im):
    f, arr = matplotlib.pyplot.subplots(1, 1)
    arr.imshow(im, cmap='gray')  # , interpolation='nearest')
    matplotlib.pyplot.show()
    im = np.array(im)
    maskList = maskFilter(im)
    afterNeuralList = ReturnLights(maskList)
    return afterNeuralList




