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

SIZE = [20,12]

def ReturnXY():
    X = []
    Y = []
    j=0
    for dir in range(1, 1):
        T = '/home/yovelrom/Downloads/cutImages/clip' + str(dir) + '/0.jpg'
        F = '/home/yovelrom/Downloads/cutImages/neg' + str(dir) + '/neg0.jpg'
        rawImage = cv2.imread(T)
        rawnegIm = cv2.imread(F)
        i = 0  # change the path to your computer
        while not ((rawImage is None) or (rawnegIm is None)):
            #matplotlib.pyplot.imshow(rawImage)
            #f, arr = matplotlib.pyplot.subplots(1, 1)
            #arr.imshow(rawImage, cmap='gray')#, interpolation='nearest')
            #arr.imshow(rawnegIm, cmap='gray')#, interpolation='nearest')
            #matplotlib.pyplot.show()
            image = imresize(rawImage,SIZE)
            negIm = imresize(rawnegIm,SIZE)

            X.append([color for row in image for pix in row for color in pix])
            X.append([color for row in negIm for pix in row for color in pix])
            Y.append(1)
            Y.append(0)
            T = '/home/yovelrom/Downloads/cutImages/clip' + str(dir) + '/' + str(i) + '.jpg'
            F = '/home/yovelrom/Downloads/cutImages/neg' + str(dir) + '/neg' + str(i) + '.jpg'
            rawImage = cv2.imread(T)
            rawnegIm = cv2.imread(F)
            i += 1
            if(i == 2161):
                print len(X)
        print(dir)
    print len(X)
    return X, Y



#initialize input(X) output(Y)
X,Y = ReturnXY()
'''
f = open('X', mode = 'w')
for x in X:
    f.write(str(x))
    f.write(",")
f = open('Y', mode = 'w')
for y in Y:
    f.write(str(y))
    f.write(",")
    '''
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# create model
model = Sequential()
model.add(Dense(12, input_dim = 720, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
'''
#Fit the model
model.fit(X, Y, nb_epoch=1000, batch_size=30)
'''
f = '/home/yovelrom/Downloads/cutImages/clip13/0.jpg'
image = cv2.imread(f)
i = 0  # change the path to your computer
posTest = []
while not image == None:
    # cv2.imshow("im", image)
    # cv2.waitKey(0)
    resIm = imresize(image, SIZE)
    toAppend = [color for row in resIm for pix in row for color in pix]
    posTest.append(toAppend)
    i += 1
    f = '/home/yovelrom/Downloads/cutImages/clip13/' + str(i) + '.jpg'
    image = cv2.imread(f)

posPredictions = model.predict(posTest)
rounded = [round(x[0]) for x in posPredictions]
print ("The false negative err value is: " + str(1-sum(rounded)/i))

f = '/home/yovelrom/Downloads/cutImages/neg13/neg0.jpg'
image = cv2.imread(f)
i = 0  # change the path to your computer
posTest = []
while not image == None:
    # cv2.imshow("im", image)
    # cv2.waitKey(0)
    resIm = imresize(image, SIZE)
    toAppend = [color for row in resIm for pix in row for color in pix]
    posTest.append(toAppend)
    i += 1
    f = '/home/yovelrom/Downloads/cutImages/neg13/neg' + str(i) + '.jpg'
    image = cv2.imread(f)

posPredictions = model.predict(posTest)
rounded = [round(x[0]) for x in posPredictions]
print ("The false positive err value is: " + str(sum(rounded)/i))


save_model(model,'/home/yovelrom/PycharmProjects/Projecton/avivtut')

