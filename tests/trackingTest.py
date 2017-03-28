"""
code for testing Tracking.py
"""
import Tracking
import cv2
from matplotlib import pyplot as plt
import streamer
import matplotlib
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
    image = cv2.imread('frame0.jpg')[245:321, 891:917]
    plt.imshow(image)
    plt.show()
    cv2.waitKey()
    cv2.imwrite("trackingTestPic1.jpg", image)  # save frame as JPEG file

path = 'ourCam25.3 16'
"""
getFirstImage(path)

im = cv2.imread('frame0.jpg')
plt.imshow(im)
plt.show()
"""

ster = streamer.Streamer(path, 10)
im = ster.getNext()
up, down, left, right = 245, 321, 891, 917

template = im[up:down, left:right]
matplotlib.pyplot.imshow(template)
matplotlib.pyplot.show()
for i in range(900):
    pt2 = (up + template.shape[0], left + template.shape[1])
    print(i)
    cv2.rectangle(im, (left, up), (pt2[1], pt2[0]), (225, 0, 0))
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    #cv2.imshow("grrr", im)
    cv2.imwrite("frame%d.jpg"%i, im)
    im = ster.getNext()

    template, (up,left) = Tracking.Track(im, template, (up,left))
#"""