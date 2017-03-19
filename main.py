from ImageDetectTl import*
from calcDistanceLib import*
from carControl import*
from colorGetter import*
from direction import*
from streamer import*

path = 'try.avi'
strm = Streamer(path)
global carCntrl

def trackMain (tlim, indX, indY, fullim):
    # Here to implement green blinking (ירוק מהבהב)
    color = getColor(tlim)
    dist = getDistance(tlim, indX, indY, fullim)
    DecisionMaker(color, dist)

def DecisionMaker(color, distance):
    if color == 'Green':
        carCntrl.Drive(50)
    # Here to implement green blinking (ירוק מהבהב)
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
            # check
            tlChosen = [max(listOfOurTl, key=lambda p: p[0].shape[0] * p.shape[1])]
        elif len(listOfOurTl) == 1:
            tlChosen = listOfOurTl[0]
        else:
            tlChosen = 0
        if tlChosen != 0:
            trackMain(tlChosen[0], tlChosen[1], tlChosen[2], im)
        else:
            carCntrl.Drive(65)




