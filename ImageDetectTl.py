from mask import*
def tlDetect (im):
    maskList = maskFilter(im)
    afterNeuralList = getAllLights(maskList)
    return afterNeuralList




