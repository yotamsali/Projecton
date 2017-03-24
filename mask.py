import cv2
import matplotlib.pyplot
import numpy as np
from skimage import measure
from skimage import morphology


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



# ********************* TO IMPLEMENT ****************************
def getCroppedImages(mask, orig):
    return [orig]
#******************************************************************

#get padding for TL image
#returns (x, y, w, h) times the ratios given
#im_dim image dimensions
def getPadding(x, y, w, h, x_ratio, y_ratio, im_dim):
    #add padding
    mid_x = x + w / 2
    mid_y = y + h / 2
    temp_w = w * x_ratio
    temp_h = h * y_ratio
    temp_x = mid_x - temp_w / 2
    temp_y = mid_y - temp_h / 2

    #fit to image
    new_x = int(max(0, temp_x))
    new_y = int(max(0, temp_y))
    new_w = int(min(im_dim[1], temp_w + temp_x) - new_x)
    new_h = int(min(im_dim[0], temp_h + temp_y) - new_y)

    return new_x, new_y, new_w, new_h



#returns the traffic lights in image
def getTrafficLights(mask, im):
    MIN_CNT_SIZE = 4 #minimum connectivity component size
    X_PAD_RATIO = 3
    Y_PAD_RATIO = 15

    #find connectivity components (רכיבי קשירות)
    _, contours, heirs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dim = mask.shape[:2]
    tls = [] #traffic lights
    for cnt in contours:
        #cnt = contours[-1]
        x, y, w, h = cv2.boundingRect(cnt)

        if (w < MIN_CNT_SIZE | h > MIN_CNT_SIZE):
            continue

        x, y, w, h = getPadding(x, y, w, h, X_PAD_RATIO, Y_PAD_RATIO, im.shape[:2])
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 0, 0), 2)
        tl_im = im[y: y + h, x: x + w]
        tls.append((tl_im, y, x))

    return tls



def maskFilter(image):
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

    #matplotlib.pyplot.imshow(org_hsv)
    #matplotlib.pyplot.show()

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
    labels = morphology.label(res2, background=0)

    """matplotlib.pyplot.imshow(mask1)
    matplotlib.pyplot.show()
    matplotlib.pyplot.imshow(res)
    matplotlib.pyplot.show()
    matplotlib.pyplot.imshow(res2)
    matplotlib.pyplot.show()

    x = measure.regionprops(res)
    x =x"""
    bw_connectivity = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
    return getTrafficLights(bw_connectivity, image)
