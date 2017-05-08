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
RED_LOW = [100,100,160]
RED_UP = [210,255,255]
GREEN_LOW = [150,150,80]
GREEN_UP = [255,255,170]
DILATION_RADIUS_BLACK = 25
DILATION_RADIUS_COLOR_RED = 9
DILATION_RADIUS_COLOR_GREEN = 15
OPEN_RADIUS = 2
DEBUG_MODE = True
BLACK_AVG_FACTOR_FULL = 0.5
BLACK_AVG_FACTOR_CUT = 1
GREEN_TO_RED_FACTOR = 40
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
    MIN_CNT_SIZE = 8 #minimum connectivity component size
    MAX_CNT_SIZE = 40 #maximum     "           "        "
    MAX_DIM_RATIO = 1.5 #max ratio between width and height
    X_PAD_RATIO = 6
    Y_PAD_RATIO = 10

    #find connectivity components
    contours, useless = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #_, contours, heirs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dim = mask.shape[:2]
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


        xPadded, yPadded, wPadded, hPadded = getPadding(x, y, w, h, X_PAD_RATIO, Y_PAD_RATIO, im.shape[:2])
        light = im[y: y + h, x: x + w]
        tl_imPadded = im[yPadded: yPadded + hPadded, xPadded: xPadded + wPadded]
        tls.append((tl_imPadded, yPadded, xPadded))
        lights.append((light, y, x))
        print((y,x,h,w))

    return tls, lights



def maskFilter(image, full_or_cropped = BLACK_AVG_FACTOR_FULL):

    org_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # define range of black color in HSV
    lower_black = np.array(0)
    upper_black_thresh = int(full_or_cropped*np.average(gray))
    upper_black = np.array(upper_black_thresh)
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(gray, lower_black, upper_black)
    kernelDILATION = np.ones((DILATION_RADIUS_BLACK,DILATION_RADIUS_BLACK),np.uint8)

    mask = cv2.dilate(mask,kernelDILATION,iterations = 1)

    # Bitwise-OR mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(res, cv2.COLOR_RGB2HSV)
    #blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

    #matplotlib.pyplot.imshow(org_hsv)
    #matplotlib.pyplot.show()

    #print hsv[966][304]
    lower_red1 = np.array(RED_LOW)
    upper_red1 = np.array(RED_UP)
    lower_green = np.array(GREEN_LOW)
    upper_green = np.array(GREEN_UP)

    maskR = cv2.inRange(hsv, lower_red1, upper_red1)

    mask2 = cv2.inRange(image, lower_green, upper_green)
    mask3 = (image[:,:,1] > image[:,:,2]+GREEN_TO_RED_FACTOR).astype(np.uint8)
    maskG = cv2.bitwise_and(mask2, mask3)

    matplotlib.pyplot.imshow(maskR)
    matplotlib.pyplot.show()

    kernelOPEN = np.ones((OPEN_RADIUS, OPEN_RADIUS), np.uint8)
    maskR = cv2.erode(maskR, kernelOPEN, iterations = 1)

    kernelDILATION_RED = np.ones((DILATION_RADIUS_COLOR_RED, DILATION_RADIUS_COLOR_RED), np.uint8)
    maskR = cv2.dilate(maskR, kernelDILATION_RED, iterations=1)

    kernelOPEN = np.ones((OPEN_RADIUS, OPEN_RADIUS), np.uint8)
    maskR = cv2.erode(maskR, kernelOPEN, iterations=1)

    kernelDILATION_GREEN = np.ones((DILATION_RADIUS_COLOR_GREEN, DILATION_RADIUS_COLOR_GREEN), np.uint8)
    maskG = cv2.dilate(maskG,kernelDILATION_GREEN,iterations = 1)
    mask = cv2.bitwise_xor(maskR, maskG)
    #kernel = np.ones((8,8),np.uint8)
    res2 = cv2.bitwise_and(res, res, mask=mask)
    #labels = morphology.label(res2, background=0)


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
        matplotlib.pyplot.imshow(maskR)
        matplotlib.pyplot.show()
    except:
        pass
    try:
        matplotlib.pyplot.imshow(res2)
        matplotlib.pyplot.show()
    except:
        pass

    # x = measure.regionprops(res)
    bw_connectivity = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
    return getTrafficLights(bw_connectivity, image)


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

