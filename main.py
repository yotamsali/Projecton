from ImageDetectTl import tlDetect
from calcDistanceLib import getDistance
from carControl import carControl
from colorGetter import getColor
from direction import getDirection
from streamer import Streamer
from Tracking import Track

path = 'try.avi'
strm = Streamer(path)
global carCntrl




#checks if the tracker lost the traffic light
#parameters:
#oldXY - previous position of TL
#newXY - current position of TL
#tlDim - dimensions of TL template
#imDim - dimensions of the image
def lostTL(oldXY, newXY, tlDim, imDim):
    MAX_DISTANCE  = 7 #maximum pixels tracker can move
    EF_DISTANCE = 3 #exited frame distance, possibly useless TODO check what happens when TL exits frame
    sqr_dist = (oldXY[0] - newXY[0]) ^ 2 + (oldXY[1] - newXY[1]) ^ 2
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
        #TODO Here to implement green blinking (ירוק מהבהב)
        color = getColor(tl_im)
        dist = getDistance(tl_im, indX, indY, fullim)
        DecisionMaker(color, dist)

        oldXY = newXY
        fullim = strm.getImage()
        tl_im, newXY = Track(fullim, tl_im, newXY)



def DecisionMaker(color, distance):
    if color == 'Green':
        carCntrl.Drive(50)
    #TODO Here to implement green blinking (ירוק מהבהב)
    else:
        carCntrl.Break(distance)

def main():
    carCntrl = carControl()
    while True:
        im = strm.getImage()
        listTl = tlDetect(im)
        listOfOurTl = []
        direc = carCntrl.direction()
        for cam in listTl:
            if (getDirection(cam[0]) == direc):
                listOfOurTl += [cam]
        if len(listOfOurTl) > 1:
            # check TODO document what this function does
            tlChosen = [max(listOfOurTl, key=lambda p: p[0].shape[0] * p.shape[1])]
        elif len(listOfOurTl) == 1:
            tlChosen = listOfOurTl[0]
        else:
            tlChosen = 0
        if tlChosen != 0:
            trackMain(tlChosen[0], tlChosen[1], tlChosen[2], im)
        else:
            carCntrl.Drive(65)