"""
distance calculating module
"""
import math
import cv2
import numpy as np
import matplotlib.pyplot
import sys
from main import*

#Parameters: TODO change these parameters
HEIGHT = 1.5 # of camera from ground, in meters
RAD2PIX = 0.0034 # ratio between radians and pixels
DIST_BOTTOM = 2.3 # distance of camera from bottom of picture in reality, in meters
THRESHOLD_DIST = 10 #(meters) distance in which the calculation switches to finding stopline
NO_SKY = 536 #the height from the top of picture to ground
NO_CAR = 250 #the height from bottom of picture, that will delete the car
#receives dimensions of traffiimport Tkinterc light
#returns distance and error
def tlDistCalc(rowSize, colSize):

	# we have prior knowledge on example
	#Parameters
	rowKnown = 30 #TODO these three should be measured once to calibrate
	colKnown = 14
	distKnown = 16.79458
	# calc the distnace using proportionality
	colDist = distKnown * colKnown / colSize # proportionality by triangle similarity
	rowDist = distKnown * rowKnown / rowSize
	avgDist = 0.5* (colDist + rowDist)
    #TODO update variance
	variance = (colDist - rowDist)/min(colDist,rowDist) # this should be about zero. If not, somthing's wrong
	return [avgDist, variance]



#img - the image to be cropped with triangle
#dim - tuple of (width, height) of image
#returns the cropped image

def crop(img):
    # cropping
    (height, width) = img.shape[0:2]
    print(width, height)
    mask = np.zeros(img.shape, dtype=np.uint8)
    #roi_corners = np.array([[(width, height), (0, height), (width/2, height/4)]], dtype=np.int32)
    roi_corners = np.array([[(0,NO_SKY) , (0, height), (width, height), (width , NO_SKY)]], dtype=np.int32)
    channel_count = img.shape[2]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)

    # apply the mask
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


#img - the image to be processed
#show_img - the image to be printed upon
#currently draws the relevant lines on the picture and returns them
#TODO !!!!needs to be changed!!!!

def hough(img, show_img):
    #running time can be improved if we replace this with a probabilistic hough algorithm
    #(cf Radon transform)

    lines = cv2.HoughLines(img, 1, np.pi / 180, 200)
    good_lines = []
    for t in lines:
        for rho, theta in t:

            if ((theta <= 0.3 * 2 * 3.14) & (theta >= 0.2 * 2 * 3.14)):
                #block comment prints picture and draws lines
                if DEBUG_MODE:
                    f, arr = matplotlib.pyplot.subplots(1, 1)
                    arr.imshow(show_img, cmap='gray')  # , interpolation='nearest')
                    matplotlib.pyplot.show()
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                #cv2.line(show_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                good_lines.append((rho,theta))
    return good_lines

#receives dimension of image, rho and theta of line
#returns height of middle of line from bottom of image
def getLineHeight(dim, rho, theta):
    height, width = dim
    y = (rho - width * np.cos(theta) / 2) / np.sin(theta)
    h = height - y
    return h


#receives complete camera image
#returns height of stopline in pixels
def findStopLineHeight(image):
    dim = image.shape[0:2]
    gray = cv2.cvtColor(crop(image), cv2.COLOR_BGR2GRAY)
    bound = [(190, 255)]
    for (lower, upper) in bound:
        mask = cv2.inRange(gray, lower, upper)
        masked = cv2.bitwise_and(gray, gray, mask=mask)

    kernel = np.ones((5, 20), np.float32) / 100
    blurred = cv2.filter2D(masked, -1, kernel)
    kernel = np.ones((5, 20), np.uint8)
    erosion = cv2.erode(blurred, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    if DEBUG_MODE:
        matplotlib.pyplot.imshow(dilation)
        matplotlib.pyplot.show()
    lines = hough(dilation,image)
    print (lines)
    rho, theta = lines[0]
    return getLineHeight(dim, rho, theta)


#receives full camera image
#returns distance from stop line
def lineDistCalc(image):
	# yPixels is the number of pixels from bottom of 
	# picture to stopping line, which we assume is at the center
	# Practically, we may not use this function but rather
	# manually check distances and interpolate

	yPixels = findStopLineHeight(image)

	#calc the distance from stopping line
	tanArg = (RAD2PIX * yPixels) + math.atan(DIST_BOTTOM / HEIGHT)
	dist = HEIGHT * math.tan(tanArg)
	return dist


#returns the distance from the stop line
#tl_im image of TL
#x,y coordinates of upper left corner of TL
#full_im full camera image
def getDistance(tl_im, x, y, full_im):
    distance, variance = tlDistCalc(tl_im.shape[0], tl_im.shape[1])
    if (distance <= THRESHOLD_DIST):
        distance = lineDistCalc(full_im)
    return distance

"""""
im = cv2.imread('stop_line_frames/frame1253.jpg')
im = im[0:len(im)-NO_CAR, 0:len(im[0])]
print(im)
matplotlib.pyplot.imshow(im)
matplotlib.pyplot.show()
lineDistCalc(im)
"""""