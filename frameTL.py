import cv2
import mask
import matplotlib.pyplot
import numpy as np

RED = 0
GREEN = 1

IMAGE = 0
Y = 1
X = 2

Factor = 0.86

DEBUG_MODE = True

def light_color(light):
    return  RED

def frame_traffic_lights(tl_lst, lights):

    for index in range(len(lights)):

        light_im = lights[index][IMAGE]
        width = light_im.shape[1] # assume that X - 1
        height = light_im.shape[0]
        lightY = lights[index][Y]
        lightX = lights[index][X]

        im = tl_lst[index][IMAGE]
        minY = tl_lst[index][Y]
        minX = tl_lst[index][X]

        color = light_color(light_im)
        tl_left = lightX - minX
        tl_right = tl_left + width
        cut_im = im[ : ,tl_left:tl_right]

        if color == RED:
            tl_up = lightY - minY
            cut_im = cut_im[tl_up + height:, : ]
            matplotlib.pyplot.imshow(cut_im)
            matplotlib.pyplot.show()
            gray = cv2.cvtColor(cut_im, cv2.COLOR_BGR2GRAY)
            matplotlib.pyplot.imshow(gray)
            matplotlib.pyplot.show()
            gray = np.array(gray)
            #thresh1 = np.sqrt(np.sum(np.square(gray)))
            thresh = np.average(gray)

            #mask1 = cv2.inRange(gray, 0, thresh1)
            mask = cv2.inRange(gray, 0, thresh)
            matplotlib.pyplot.imshow(mask)
            matplotlib.pyplot.show()

            kernelOPEN = np.ones((cut_im.shape[0]//10, width//10), np.uint8)

            mask = cv2.erode(mask, kernelOPEN, iterations=1)
            mask = cv2.dilate(mask, kernelOPEN, iterations=1)
            matplotlib.pyplot.imshow(mask)
            matplotlib.pyplot.show()

            #tl_down = FIND MIN Y
            tl_down = tl_up + 3*(height//4)
            rows = np.sum(mask, axis=1)
            for i in range(cut_im.shape[0]):
                if rows[-i-1] >= width//4*255:
                    tl_down = tl_up + height + cut_im.shape[0]-(i + 1)
                    break
            tl = im[tl_up:tl_down, tl_left:tl_right]
            matplotlib.pyplot.imshow(tl)
            matplotlib.pyplot.show()

        if color == GREEN:
            tl_down = lightY
            cut_im = cut_im[:tl_down, :]
            matplotlib.pyplot.imshow(cut_im)
            matplotlib.pyplot.show()
            gray = cv2.cvtColor(cut_im, cv2.COLOR_BGR2GRAY)
            matplotlib.pyplot.imshow(gray)
            matplotlib.pyplot.show()
            gray = np.array(gray)
            # thresh1 = np.sqrt(np.sum(np.square(gray)))
            thresh = np.average(gray)

            # mask1 = cv2.inRange(gray, 0, thresh1)
            mask = cv2.inRange(gray, 0, thresh)
            matplotlib.pyplot.imshow(mask)
            matplotlib.pyplot.show()

            kernelOPEN = np.ones((cut_im.shape[0] // 10, width // 10), np.uint8)

            mask = cv2.erode(mask, kernelOPEN, iterations=1)
            mask = cv2.dilate(mask, kernelOPEN, iterations=1)
            matplotlib.pyplot.imshow(mask)
            matplotlib.pyplot.show()

            # tl_down = FIND MIN Y
            tl_up = tl_up + (height // 4)
            rows = np.sum(mask, axis=0)
            for i in range(cut_im.shape[0]):
                if rows[i] >= 3* width // 4 * 255:
                    tl_down = tl_down + i
                    break
            tl = im[tl_up:tl_down, tl_left:tl_right]
            matplotlib.pyplot.imshow(tl)
            matplotlib.pyplot.show()
for i in range(2,7):
    im = cv2.imread('/home/aviv/PycharmProjects/Projecton/framing/'+str(i)+'.jpg')
    matplotlib.pyplot.imshow(im)
    matplotlib.pyplot.show()

    tls, lights = mask.maskFilter(im)
    frame_traffic_lights(tls, lights)