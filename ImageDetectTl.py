from mask import*
import numpy as np
from tlDetectionCNN import*
def tlDetect (im):
    im = np.array(im)
    maskList = maskFilter(im)
    afterNeuralList = getAllLights(maskList)
    return afterNeuralList




