import math 
import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt


#receives dimensions of traffic light
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
	variance = (colDist - rowDist)/min(colDist,rowDist) # this should be about zero. If not, somthing's wrong
	return [avgDist, variance]



#img - the image to be cropped with triangle
#dim - tuple of (width, height) of image
#returns the cropped image

def crop(img,dim):
    # cropping
    (width, height) = dim
    mask = np.zeros(img.shape, dtype=np.uint8)
    roi_corners = np.array([[(width, height), (0, height), (width/2, height/4)]], dtype=np.int32)
    channel_count = img.shape[2]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)

    # apply the mask
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


#img - the image to be processed
#show_img - the image to be printed upon
#currently draws the relevant lines on the picture and returns them
#TODO !!!!needs to changed!!!!

def hough(img, show_img):
    #running time can be improved if we replace this with a probabilistic hough algorithm
    #(cf Radon transform)

    lines = cv2.HoughLines(img, 1, np.pi / 180, 200)
    good_lines = []
    for t in lines:
        for rho, theta in t:

            if ((theta <= 0.3 * 2 * 3.14) & (theta >= 0.2 * 2 * 3.14)):
                #block comment prints picture and draws lines
                """cv2.imshow('r', show_img)
                cv2.waitKey(0)
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(show_img, (x1, y1), (x2, y2), (0, 0, 255), 2)"""
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
    dim = image.shape[0:1] #TODO check if this returns correct dimention
    gray = cv2.cvtColor(crop(image,dim), cv2.COLOR_BGR2GRAY)
    bound = [(156, 255)]
    for (lower, upper) in bound:
        mask = cv2.inRange(gray, lower, upper)
        masked = cv2.bitwise_and(gray, gray, mask=mask)

    kernel = np.ones((5, 20), np.float32) / 100
    blurred = cv2.filter2D(masked, -1, kernel)
    kernel = np.ones((5, 20), np.uint8)
    erosion = cv2.erode(blurred, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    lines = hough(dilation,image)
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

	#Parameters: TODO change these parameters
	height = 1.5 # of camera from ground, in meters
	radinansToPixels = 0.0034 # ratio between them
	distBottom = 2.3 # distance of camera from bottom of picture in reality, in meters

	#calc the distance from stopping line
	tanArg = (radinansToPixels * yPixels) + math.atan(distBottom / height)
	dist = height*math.tan(tanArg)
	return dist


