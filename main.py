from ImageDetectTl import*
from calcDistanceLib import*
from carControl import*
from colorGetter import*
from direction import*
from streamer import*
from Tracking import*
from pynput.keyboard import Key, Listener
import threading
import visvis as vv

fps = 24
path = 'examples/real.avi'
strm = Streamer(path, fps)
leftIm = imageio.imread('examples/left.jpg')
forwardIm = imageio.imread('examples/forward.jpg')
arrow = forwardIm
carCntrl = carControl()

def threadShowWhile():
    while True:
        vv.imshow(strm.getImage())
        vv.processEvents()

def on_press(key):
    global arrow
    global carCntrl
    if key == Key.up :
        print("UP")
        arrow = forwardIm
        carCntrl.direction = 'F'
    if key == Key.down :
        print("DOWN")
    if key == Key.left :
        print("LEFT")
        arrow = leftIm
        carCntrl.direction = 'L'
    if key == Key.right :
        print("RIGHT")
        arrow = leftIm[:,::-1]
        carCntrl.direction = 'R'


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
def trackMain (tl_im, indX, indY, fullim):
    frame_counter = 0
    CNN_RATE = 10 # num of frames that are tracked before cnn is reactivated
    oldXY = (indX, indY)
    newXY = oldXY
    fullim_dim = fullim.shape[:2]

    while ((not lostTL(oldXY, newXY, tl_im.shape[:2],fullim_dim)) & (frame_counter < CNN_RATE)):
        #TODO call CNN on ROI
        #TODO Here to implement green blinking
        color = getColor(tl_im)
        print('tracking')
        dist = tlDistCalc(tl_im.shape[0], tl_im.shape[1])
        DecisionMaker(color, dist)

        oldXY = newXY
        fullim = strm.getImage()
        vv.imshow(fullim)
        vv.processEvents()
        tl_im, newXY = Track(fullim, tl_im, newXY)



def DecisionMaker(color, distance):
    global carCntrl
    if color == 'Green':
        carCntrl.drive(50)
    # Here to implement green blinking (ירוק מהבהב)
    else:
        carCntrl.stop(distance)


def main():
    listener = Listener(
        on_press=on_press
    )
    listener.start()
    global carCntrl
    while True:
        im = strm.getImage()
        im[:100, :100] = arrow
        vv.imshow(im)
        vv.processEvents()
        listTl = tlDetect(im)
        listOfOurTl = []
        direc = carCntrl.direction
        print(np.array(listTl).shape)
        for cam in listTl:
            print(np.array(cam).shape)
            if (getDirection(cam[0]) == direc):
                listOfOurTl += [cam]
                print(np.array(listOfOurTl).shape)
        if len(listOfOurTl) > 1:
            tlChosen = [max(listOfOurTl, key=lambda p: p[0].shape[0] * p[0].shape[1])]
        elif len(listOfOurTl) == 1:
            tlChosen = listOfOurTl[0]
        else:
            tlChosen = 0
        if tlChosen != 0:
            print('found! started tracking')
            print(np.array(tlChosen).shape)
            trackMain(tlChosen[0][0], tlChosen[0][1], tlChosen[0][2], im)
        else:
            carCntrl.drive(65)

showTh = threading.Thread(target=threadShowWhile)
showTh.start()
main()