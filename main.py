from ImageDetectTl import*
from calcDistanceLib import*
from carControl import*
from colorGetter import*
from streamer import*
from Tracking import*
from chooseLight import*
import imageio
from pynput.keyboard import Key, Listener
import threading
import matplotlib.pyplot
import cv2


RUN_TIME = 5
FPS = 10


path = 'examples/real2.avi'
strm = Streamer(path, FPS)
im = strm.getImage()
leftIm = imageio.imread('examples/left.jpg')
forwardIm = imageio.imread('examples/forward.jpg')
arrow = forwardIm
carCntrl = carControl()
arrowChar = 'F'
import time


def threadShowWhile():
    listener = Listener(
        on_press=on_press
    )
    listener.start()
    while True:
        #tic()
        im = strm.getImage()
        #print('time of read' + str(toc()))
        #tic()
        #cv2.imshow(np.array(im))
        #print('time of show' + str(toc()))
    '''''
    pygame.display.set_caption(path)
    clip = VideoFileClip(path)
    clip.preview()
    pygame.quit()
    '''''


def on_press(key):
    global arrow
    global carCntrl
    global arrowChar
    if key == Key.up :
        print("UP")
        arrow = forwardIm
        carCntrl.direction = 'F'
        arrowChar = 'F'
    if key == Key.down :
        print("DOWN")
    if key == Key.left :
        print("LEFT")
        arrow = leftIm
        carCntrl.direction = 'L'
        arrowChar = 'L'
    if key == Key.right :
        print("RIGHT")
        arrow = leftIm[:,::-1]
        carCntrl.direction = 'R'
        arrowChar = 'R'


#checks if the tracker lost the traffic light
#parameters:
#oldXY - previous position of TL
#newXY - current position of TL
#tlDim - dimensions of TL template
#imDim - dimensions of the image
def lostTL(oldXY, newXY, tlDim, imDim):
    MAX_DISTANCE  = 7 #maximum pixels tracker can move
    EF_DISTANCE = 3
    sqr_dist = np.linalg.norm(np.array(oldXY[0] - newXY[0]))
    if (sqr_dist > MAX_DISTANCE ^ 2):
        return True
    if (oldXY[1] < EF_DISTANCE): #TL exited from top
        return True
    if ((oldXY[0] < EF_DISTANCE) | (oldXY[0] + tlDim[0] > imDim[0] - EF_DISTANCE)): #TL exited from sides
        return True

    return False

#tlim - traffic light image
#indX, indY - coordinates of upper left corner of TL
#fullim - complete camera image
#exits when done tracking light
def trackMain (fullIm, tl_im, indX, indY):
    global carCntrl
    frame_counter = 0
    CNN_RATE = 10 # num of frames that are tracked before cnn is reactivated
    oldXY = (indX, indY)
    newXY = oldXY
    fullim_dim = fullIm.shape[:2]

    while ((not lostTL(oldXY, newXY, tl_im.shape[:2],fullim_dim)) & (frame_counter < CNN_RATE)):
        #carCntrl.moveCar(0)
        #TODO call CNN on ROI
        #TODO Here to implement green blinking
        color = getColor(tl_im)

        dist = tlDistCalc(tl_im.shape[0], tl_im.shape[1])
        DecisionMaker(color, dist)

        oldXY = newXY
        fullIm = strm.getImage()
        tl_im, newXY = Track(fullIm, tl_im, newXY)
        tup2 = (newXY[1] + 3*tl_im.shape[1], newXY[0] + 3*tl_im.shape[0])
        tup1 = (newXY[1] - 3*tl_im.shape[1], newXY[0] - 3*tl_im.shape[0])

        cv2.rectangle(fullIm, tup1, tup2, (255, 0, 0))
        matplotlib.pyplot.imshow(fullIm)
        matplotlib.pyplot.show()

        print('tracking')
        print(color)
        print(newXY)
    #carCntrl.moveCar(2)




def DecisionMaker(color, distance):
    global carCntrl
    if color == 'Green':
        carCntrl.drive(50)
    # Here to implement green blinking (ירוק מהבהב)
    else:
        carCntrl.stop(distance)


def main():
    tic()
    global carCntrl
    toc()
    while True:
        tic()
        im = strm.getImage()
        print(toc())
        #TODO
        #im[:100, :100] = arrow
        listTl = tlDetect(im)
        listOfOurTl = []
        direc = carCntrl.direction
        print(np.array(listTl).shape)
        selectedshowTh = threading.Thread(target=threadShowWhile)
        TlTuple = ReturnDirections(listTl, carCntrl.direction)
        """""
        for cam in listTl:
            print(np.array(cam).shape)
            if (ReturnDirections(cam[0]) == direc):
                listOfOurTl += [cam]
                print(np.array(listOfOurTl).shape)
        """
        if TlTuple != None:
            print('found! started tracking')
            trackMain(im, TlTuple[0], TlTuple[1], TlTuple[2])
        else:
            carCntrl.drive(65)

#carCntrl.moveCar(2)
showTh = threading.Thread(target=threadShowWhile)
showTh.start()
main()