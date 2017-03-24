from mask import*
import numpy as np
from tlDetectionCNN import*
def tlDetect (im):
    im = np.array(im)
    maskList = maskFilter(im)
    afterNeuralList = ReturnLights(maskList)
    return afterNeuralList




