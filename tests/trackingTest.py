"""
code for testing Tracking.py
"""
import Tracking
import cv2
from matplotlib import pyplot as plt
import streamer
import matplotlib
""""
def getFirstImage(path):
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()
    count = 0
    success = True
    while success & count <  1:
      success,image = vidcap.read()
      print ('Read a new frame: ', success)
      plt.imshow(image)
      cv2.waitKey()
      cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
      count += 1
    image = cv2.imread('frame0.jpg')[353:399, 1049:1064]
    plt.imshow(image)
    plt.show()
    cv2.waitKey()
    cv2.imwrite("trackingTestPic1.jpg", image)  # save frame as JPEG file
"""
def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        return time.time() - startTime_for_tictoc

"""
getFirstImage(path)

im = cv2.imread('frame0.jpg')
plt.imshow(im)
plt.show()
"""


path = '/media/aviv/DC5C192D5C190444/ourCam25_3_24'
ster = streamer.Streamer(path, 10)
for i in range(1280):
    im = ster.getNext()
matplotlib.pyplot.imshow(im)
matplotlib.pyplot.show()
#location of the traffic light in the first frame
up, down, left, right = 280, 340, 581, 603

template = im[up:down, left:right]
matplotlib.pyplot.imshow(template)
matplotlib.pyplot.show()
diff = [0,0]
imClone = im.copy()
for i in range(900):

    pt2 = (up + template.shape[0], left + template.shape[1])
    print(i)
    cv2.rectangle(imClone, (left, up), (pt2[1], pt2[0]), (225, 0, 0))
    imClone = cv2.cvtColor(imClone, cv2.COLOR_RGB2BGR)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    cv2.imshow("grrr", imClone)
    cv2.waitKey(100)
    cv2.imwrite("/home/aviv/PycharmProjects/Projecton/frames/%d.jpg"%i, im)
    #im = ster.getNext()
    #im = ster.getNext()
    im = ster.getNext()
    im = ster.getNext()
    im = ster.getNext()
    imClone = im[:].copy()
    tic()
    #Tl, (up,left),template, diff  = Tracking.Track(im, template, (up,left), diff)
    print(toc())
    #print(diff)
    #matplotlib.pyplot.imshow(Tl)
    #matplotlib.pyplot.show()
    #matplotlib.pyplot.imshow(im)
    #matplotlib.pyplot.show()

