import sys

import cv2
import matplotlib.pyplot
import numpy as np


def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")


image = cv2.imread(sys.argv[1])
org_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# define range of black color in HSV
lower_black = np.array(0)
upper_black = np.array(100)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(gray, lower_black, upper_black)
kernel = np.ones((8,8),np.uint8)
mask = cv2.dilate(mask,kernel,iterations = 1)

# Bitwise-OR mask and original image
res = cv2.bitwise_and(image, image, mask=mask)
# Convert BGR to HSV
hsv = cv2.cvtColor(res, cv2.COLOR_RGB2HSV)
#blurred = cv2.GaussianBlur(hsv, (5, 5), 0)


matplotlib.pyplot.imshow(org_hsv)
matplotlib.pyplot.show()


#print hsv[966][304]
lower_red1 = np.array([90,150,180])
upper_red1 = np.array([130,255,255])
lower_green = np.array([15,150,100])
upper_green = np.array([35,255,255])


mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_green, upper_green)
mask = cv2.bitwise_or(mask1, mask2)

kernel = np.ones((8,8),np.uint8)
res2 = cv2.bitwise_and(res, res, mask=mask)
cv2.imshow("org", image)
#cv2.imshow("mask", mask1)
cv2.imshow("med", res)
#cv2.imshow("hsv", hsv)
cv2.imshow("final", res2)
cv2.waitKey(0)
cv2.imwrite('black.png', res)

