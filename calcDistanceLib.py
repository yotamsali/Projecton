import math 

#returns distance by size of traffic light dimentions
#returns also variance (of calc by col and row) 
def getDistance():
	return 5
def tlDistCalc(rowSize, colSize):

	# we have prior knowledge on example
	#Parametrs
	rowKnown = 30 # these three should be measured once to calibrate
	colKnown = 14
	distKnown = 16.79458
	# calc the distnace using proportionality
	colDist = distKnown * colKnown / colSize # proportionality by triangle similarity
	rowDist = distKnown * rowKnown / rowSize
	avgDist = 0.5* (colDist + rowDist)
	variance = (colDist - rowDist)/min(colDist,rowDist) # this should be about zero. If not, somthing's wrong
	return [avgDist, variance]


def lineDistCalc(yPixels):
	# yPixels is the number of pixels from bottom of 
	# picture to stopping line, which we assume is at the center
	# Practicaly, we maybe shall not use this function but rather
	# manually check distances and interpolate
	
	#Parameters:
	height = 1.5 # of camera from ground, in meters
	radinansToPixels = 0.0034 # ratio between them
	distBottom = 2.3 # distance of camera from bottom of picture in reality, in meters

	#calc the distance from stopping line
	tanArg = (radinansToPixels * yPixels) + math.atan(distBottom / height)
	dist = height*math.tan(tanArg)
	return dist



print(lineDistCalc(50))
print(tlDistCalc(60,28))
print(tlDistCalc(60,50))
	
	
