import cv2
import mask
import matplotlib.pyplot
import numpy as np

RED = 2
GREEN = 1

IMAGE = 0
Y = 1
X = 2

Factor = 0.4


DEBUG_MODE = True

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc

# gets the color of the traffic light, returns the relevant static int
def light_color(light):

    sumR = np.sum(light[:,:,RED])
    sumG = np.sum(light[:,:,GREEN])

    if sumG > sumR:
        return GREEN
    else:
        return RED

# gets 2 lists of tuples: (traffic lights images cropped, Y location, X location),
# (lights (of tl) images cropped, Y location, X location).
# returns a list of cropped tl (y,x,h,w, color).
def frame_traffic_lights(tl_lst, lights):
    # the list that will be returned
    cropped_tls = []

    for index in range(len(lights)):

        # that the location that we know from the light, and need to the rest of the process

        # light information (the width is the same as the tl's)
        light_im = lights[index][IMAGE]
        width = light_im.shape[1] # assume that X - 1
        light_height = light_im.shape[0]
        lightY = lights[index][Y]
        lightX = lights[index][X]
        color = light_color(light_im)

        # image information
        im = tl_lst[index][IMAGE]
        minY = tl_lst[index][Y]
        minX = tl_lst[index][X]

        # location of the light in the cropped frame we got
        tl_left = lightX - minX
        tl_right = tl_left + width

        # cut the sides that are not relevant
        cut_im = im[ : ,tl_left:tl_right]

        #matplotlib.pyplot.imshow(im)
        #matplotlib.pyplot.show()
        if color == RED:
            print("RED")
            # we only need the location of the bottom of the tl.
            # steps:
            # 1. cut the light from the image. 2. change it to grayscale and do open 3. mask it by lower than average
            # 4. run upwards until most of the line is black (this is our line!)
            tl_up = lightY - minY
            cut_im = cut_im[tl_up + light_height:, : ]
            # matplotlib.pyplot.imshow(cut_im)
            # matplotlib.pyplot.show()
            gray = cv2.cvtColor(cut_im, cv2.COLOR_BGR2GRAY)
            #matplotlib.pyplot.imshow(gray)
            #matplotlib.pyplot.show()
            gray = np.array(gray)
            thresh = np.average(gray)
            mask = cv2.inRange(gray, 0, thresh)
            #matplotlib.pyplot.imshow(mask)
            #matplotlib.pyplot.show()

            kernelOPEN = np.ones((light_height + 1, width//10 + 1), np.uint8)

            mask = cv2.erode(mask, kernelOPEN, iterations=1)
            mask = cv2.dilate(mask, kernelOPEN, iterations=1)

            #matplotlib.pyplot.imshow(mask)
            #matplotlib.pyplot.show()

            tl_down = tl_up + 3*(light_height//4)
            #rows = np.sqrt(np.sum(mask*mask, axis=1))
            rows = np.sum(mask, axis=1)
            for i in range(cut_im.shape[0]):
                if rows[-i-1] >= int(width*Factor)*255:
                    tl_down = tl_up + light_height + cut_im.shape[0]-(i + 1)
                    break
            tl = im[tl_up:tl_down, tl_left:tl_right]
            #print (toc())
            matplotlib.pyplot.imshow(tl)
            matplotlib.pyplot.show()

        if color == GREEN:
            print ("GREEN")
            # we only need the location of the upper bound of the tl.
            # steps:
            # 1. cut the light from the image. 2. change it to grayscale and do open 3. mask it by lower than average
            # 4. run downwards until most of the line is black (this is our line!)
            tl_down = lightY - minY + light_height
            cut_im = cut_im[:tl_down-light_height, :]
            # matplotlib.pyplot.imshow(cut_im)
            # matplotlib.pyplot.show()
            gray = cv2.cvtColor(cut_im, cv2.COLOR_BGR2GRAY)
            #matplotlib.pyplot.imshow(gray)
            #matplotlib.pyplot.show()
            gray = np.array(gray)
            # thresh1 = np.sqrt(np.sum(np.square(gray)))
            thresh = np.average(gray)

            # mask1 = cv2.inRange(gray, 0, thresh1)
            mask = cv2.inRange(gray, 0, thresh)
            #matplotlib.pyplot.imshow(mask)
            #matplotlib.pyplot.show()

            kernelOPEN = np.ones((light_height +1, width // 10 + 1), np.uint8)

            mask = cv2.erode(mask, kernelOPEN, iterations=1)
            mask = cv2.dilate(mask, kernelOPEN, iterations=1)

            #matplotlib.pyplot.imshow(mask)
            #matplotlib.pyplot.show()

            tl_up =  light_height // 3
            rows = np.sum(mask, axis=1)
            for i in range(cut_im.shape[0]):
                if rows[i] >= int(width*Factor)* 255:
                    tl_up = i
                    break
            tl = im[tl_up:tl_down, tl_left:tl_right]
            #print (toc())

            matplotlib.pyplot.imshow(tl)
            matplotlib.pyplot.show()

        # add (y,x,h,w,color)
        cropped_tls.append((tl_up + minY, minX + tl_left, tl_down - tl_up, width, color))

    return cropped_tls
"""
im = cv2.imread('/home/aviv/PycharmProjects/Projecton/framing/labeled_0.jpg')
matplotlib.pyplot.imshow(im)
matplotlib.pyplot.show()

tls, lights = mask.maskFilter(im)
frame_traffic_lights(tls, lights)
"""

for i in range(15,24):

    im = cv2.imread('/home/aviv/PycharmProjects/Projecton/framing/'+str(i)+'.jpg')
    #im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    matplotlib.pyplot.imshow(im)
    matplotlib.pyplot.show()

    tic()
    tls, lights = mask.maskFilter(im)
    frame_traffic_lights(tls, lights)
    print (toc())
