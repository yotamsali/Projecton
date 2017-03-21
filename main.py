from ImageDetectTl import*
from calcDistanceLib import*
from carControl import*
from colorGetter import*
from direction import*
from streamer import*

path = 'try.avi'
strm = Streamer(path)
global carCntrl


#tlim - traffic light image
#indX, indY - coordinates of upper left corner of TL
#fullim - complete camera image
#exits when done tracking light
#TODO insert CNN check every time period

def trackMain (tl_im, indX, indY, fullim):
    while(notLost): #TODO how to check if lost TL
        #TODO Here to implement green blinking (ירוק מהבהב)
        color = getColor(tl_im)
        dist = getDistance(tl_im, indX, indY, fullim)
        DecisionMaker(color, dist)


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