"""
creates initial mask on camera image.
returns possible traffic light candidates
"""
import cv2
import matplotlib.pyplot
import numpy as np
from skimage import measure
from skimage import morphology


# IMPORTANT PARAMETERS*****************************************************
RED_LOW1 = [169,0,160]
RED_UP1 = [176,255,255]
RED_LOW2 = [0,0,240]
RED_UP2 = [25,70,255]

GREEN_LOW1 = [90,0,150]
GREEN_LOW2 = [85,0,210]
GREEN_UP = [105,170,255]
DILATION_RADIUS_BLACK = 15
DILATION_RADIUS_LAP = 2
DILATION_RADIUS_COLOR_RED = 7
DILATION_RADIUS_COLOR_GREEN = 11
OPEN_RADIUS = 4
DEBUG_MODE = True
BLACK_AVG_FACTOR_FULL = 0.3
BLACK_AVG_FACTOR_CUT = 1
RED_TO_BLUE_FACTOR = 55
GREEN_TO_RED_FACTOR = 38
RED_TO_GREEN_FACTOR = 170
UPPER_BLACK_THRESH = 170
UPPER_LAP = 255
LOWER_LAP = 70
RED = 2
GREEN = 1
BLUE = 0
#**************************************************************************



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

def light_color(light):

    sumR = np.sum(light[:, :, RED])
    sumG = np.sum(light[:, :, GREEN])

    if sumG > sumR:
        return GREEN
    else:
        return RED
# ********************* TO IMPLEMENT ****************************
def getCroppedImages(mask, orig):
    return [orig]
#******************************************************************

#get padding for TL image
#returns (x, y, w, h) times the ratios given
#im_dim image dimensions
def getPadding(x, y, w, h, x_ratio, y_ratio, im_dim, color = RED):
    #add padding
    mid_x = x + w / 2
    mid_y = y + h / 2
    temp_w = w * x_ratio
    temp_h = h * y_ratio
    temp_x = mid_x - temp_w / 2
    temp_y = mid_y - temp_h / 2

    # fit to image
    if color == RED:
        new_x = int(max(0, temp_x))
        new_y = int(max(0, temp_y))
        new_w = int(min(im_dim[1], temp_w + temp_x) - new_x)
        new_h = int(min(im_dim[0], temp_h + temp_y) - new_y)

    if color == GREEN:
        new_x = int(max(0, temp_x))
        new_y = int(max(0, temp_y - temp_h//4))
        new_w = int(min(im_dim[1], temp_w + temp_x) - new_x)
        new_h = int(min(im_dim[0], temp_h + temp_y) - new_y )

    return new_x, new_y, new_w, new_h



# returns the traffic lights in image
def getTrafficLights(mask, im, color):
    MIN_CNT_SIZE = 8 #minimum connectivity component size
    MAX_CNT_SIZE = 40 #maximum     "           "        "
    MAX_DIM_RATIO = 2 #max ratio between width and height
    X_PAD_RATIO = 3
    Y_PAD_RATIO = 8

    #find connectivity components
    contours, useless = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #_, contours, heirs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tls = [] #traffic lights
    lights = [] # lights locations

    for cnt in contours:
        #cnt = contours[-1]
        x, y, w, h = cv2.boundingRect(cnt)

        if (w < MIN_CNT_SIZE or h < MIN_CNT_SIZE):
            continue
        if (w > MAX_CNT_SIZE or h > MAX_CNT_SIZE):
            continue
        if ((w / h > MAX_DIM_RATIO) or (h / w > MAX_DIM_RATIO)):
            continue

        xPadded, yPadded, wPadded, hPadded = getPadding(x, y, w, h, X_PAD_RATIO, Y_PAD_RATIO, im.shape[:2], color)
        light = im[y: y + h, x: x + w]
        tl_imPadded = im[yPadded: yPadded + hPadded, xPadded: xPadded + wPadded]
        tls.append((tl_imPadded, yPadded, xPadded))
        lights.append((light, y, x,color))

    print(len(tls))
    return tls, lights



def maskFilter(image, cropped = False):

    if not cropped:
        image = image[:-image.shape[0]//5,image.shape[1]//8:-image.shape[1]//8,:]
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    lap = np.abs(cv2.Laplacian(gray, cv2.CV_64F))
    """
    matplotlib.pyplot.imshow(lap)
    matplotlib.pyplot.show()
    matplotlib.pyplot.imshow(gray)
    matplotlib.pyplot.show()
    """
    # define range of black color in HSV
    lower_black = np.array(0)
    if cropped:
        # Bitwise-OR mask and original image
        res = image
        # Convert BGR to HSV
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
        # blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    else:
        upper_black_thresh = UPPER_BLACK_THRESH
        upper_black = np.array(upper_black_thresh)
        # Threshold the HSV image to get only blue colors
        maskB1 = cv2.inRange(gray, lower_black, upper_black)

        maskB2 = cv2.inRange(lap, LOWER_LAP, UPPER_LAP)
        kernelDILATION_LAP = np.ones((DILATION_RADIUS_BLACK, DILATION_RADIUS_BLACK), np.uint8)
        maskB2 = cv2.dilate(maskB2,kernelDILATION_LAP,iterations = 1)

        mask = cv2.bitwise_and(maskB1, maskB2)

        kernelDILATION = np.ones((DILATION_RADIUS_BLACK,DILATION_RADIUS_BLACK),np.uint8)

        mask = cv2.dilate(mask,kernelDILATION,iterations = 1)
        #matplotlib.pyplot.imshow(mask)
        #matplotlib.pyplot.show()
        # Bitwise-OR mask and original image
        res = cv2.bitwise_and(image, image, mask=mask)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
        #blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    #print hsv[966][304]
    lower_red1 = np.array(RED_LOW1)
    upper_red1 = np.array(RED_UP1)
    lower_red2 = np.array(RED_LOW2)
    upper_red2 = np.array(RED_UP2)
    lower_green1 = np.array(GREEN_LOW1)
    lower_green2 = np.array(GREEN_LOW2)
    upper_green = np.array(GREEN_UP)

    maskR1 = cv2.inRange(hsv, lower_red1, upper_red1)
    kernelDILATION_RED = np.ones((DILATION_RADIUS_COLOR_RED, DILATION_RADIUS_COLOR_RED), np.uint8)

    maskRtemp = cv2.dilate(maskR1, kernelDILATION_RED, iterations=1)
    maskR2temp = cv2.inRange(hsv, lower_red2, upper_red2)
    maskR2 = cv2.bitwise_and(maskRtemp, maskR2temp)

    maskR3 =  np.array(image[:,:,BLUE] < image[:,:,RED] - RED_TO_BLUE_FACTOR).astype(np.uint8)

    maskR = cv2.bitwise_or(maskR1, maskR2)
    maskR = cv2.bitwise_and(maskR, maskR3)


    maskG1 = cv2.inRange(hsv, lower_green1, upper_green)
    maskG2 = cv2.inRange(hsv, lower_green2, upper_green)

    maskG3 = np.array(image[:,:,GREEN] > image[:,:,RED] + GREEN_TO_RED_FACTOR).astype(np.uint8)

    maskG = cv2.bitwise_or(maskG1, maskG2)
    maskG = cv2.bitwise_and(maskG, maskG3)

    kernelOPEN = np.ones((1, 1), np.uint8)
    maskR = cv2.erode(maskR, kernelOPEN, iterations = 1)

    kernelDILATION_RED = np.ones((DILATION_RADIUS_COLOR_RED, DILATION_RADIUS_COLOR_RED), np.uint8)
    maskR = cv2.dilate(maskR, kernelDILATION_RED, iterations=1)

    kernelOPEN = np.ones((OPEN_RADIUS, OPEN_RADIUS), np.uint8)
    #maskR = cv2.erode(maskR, kernelOPEN, iterations=1)

    kernelDILATION_GREEN = np.ones((DILATION_RADIUS_COLOR_GREEN, DILATION_RADIUS_COLOR_GREEN), np.uint8)
    kernelDILATION_SMALL = np.ones((2, 2), np.uint8)

    maskG = cv2.dilate(maskG, kernelDILATION_SMALL, iterations=1)

    maskG = cv2.erode(maskG, kernelOPEN, iterations=1)

    maskG = cv2.dilate(maskG,kernelDILATION_GREEN,iterations = 1)
    mask = cv2.bitwise_or(maskR, maskG)
    #kernel = np.ones((8,8),np.uint8)
    resG = cv2.bitwise_and(res, res, mask=maskG)
    resR = cv2.bitwise_and(res, res, mask=maskR)
    #labels = morphology.label(res2, background=0)

    """
    try:
        matplotlib.pyplot.imshow(image)
        matplotlib.pyplot.show()
    except:
        pass
    try:
        matplotlib.pyplot.imshow(res)
        matplotlib.pyplot.show()
    except:
        pass

    try:
        matplotlib.pyplot.imshow(hsv)
        matplotlib.pyplot.show()
    except:
        pass

    try:
        matplotlib.pyplot.imshow(maskG)
        matplotlib.pyplot.show()
    except:
        pass

    try:
        matplotlib.pyplot.imshow(maskR)
        matplotlib.pyplot.show()
    except:
        pass
    try:
        matplotlib.pyplot.imshow(resR)
        matplotlib.pyplot.show()
    except:
        pass

    try:
        matplotlib.pyplot.imshow(cv2.cvtColor(res2, cv2.COLOR_BGR2HSV))
        matplotlib.pyplot.show()
    except:
        pass
    """
    # x = measure.regionprops(res)
    bw_connectivityG = cv2.cvtColor(resG, cv2.COLOR_BGR2GRAY)
    bw_connectivityR = cv2.cvtColor(resR, cv2.COLOR_BGR2GRAY)
    tlsG, lightsG = getTrafficLights(bw_connectivityG, image, GREEN)
    tlsR, lightsR = getTrafficLights(bw_connectivityR, image, RED)
    tls = tlsG + tlsR
    lights = lightsG +lightsR

    return tls, lights


#test code - if add this breaks main
if __name__ == '__main__':
    im = cv2.imread('/home/aviv/PycharmProjects/Projecton/framing/_number:65_posIndex:1-u_11_d_9_l_6_r_8.jpg')
    tls, lights = maskFilter(im)
    print(len(tls))
    for i in range(len(tls)):
        (temp_im, y, x) = tls[i]

        dy, dx, _ = temp_im.shape

        print((y, x, dy, dx))
        cv2.rectangle(im, (x, y), (x + dx, y + dy), (0, 255, 0), 2)
        cv2.imshow("grrrr", temp_im)
        cv2.waitKey(0)
    matplotlib.pyplot.imshow(im)
    matplotlib.pyplot.show()

    cv2.waitKey(0)

