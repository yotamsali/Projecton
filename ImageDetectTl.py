from mask import*

def tlDetect (im):
    maskList = maskFilter(im)
    afterNeuralList = getAllTl(maskList)




