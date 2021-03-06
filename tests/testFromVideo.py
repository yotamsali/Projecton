import cv2
import matplotlib.pyplot

import Tracking
from streamer import*

TRACK_LIGHT = 1
TRACK_GARBAGE = 2
NOTHING = 0
MAX_SIZE = 40
GARBAGE_PATH = 'Garbage/'
TL_PATH = 'tl.avi'
TL_DIR_PATH = 'Tl/'
ERROR_VAL = 0






def ShowVideo(path, fps):

    s = Streamer(path, fps)
    im = s.getNext()
    while type(im) == imageio.core.util.Image:
        f, arr = matplotlib.pyplot.subplots(1, 1)
        arr.imshow(im, cmap='gray')#, interpolation='nearest')
        matplotlib.pyplot.show()
        print("0 - next frame, 1 - Track Light, 2 - Track something else")
        sit = int(input())
        if sit == NOTHING:
            pass
        if sit == TRACK_LIGHT:
            matplotlib.pyplot.show()
            print("up, down, left, right in that order")
            up = int(input())
            down = int(input())
            left = int(input())
            right = int(input())
            print("the last index of picture")
            maxindex = int(input())
            TrackLight(im,up,down,left,right,maxindex,s)
        if sit == TRACK_GARBAGE:
            print("up, down, left, right in that order")
            up = int(input())
            down = int(input())
            left = int(input())
            right = int(input())
            print("the last index of picture")
            maxindex = int(input())
            TrackLight(im, up, down, left, right, maxindex,s)
        else:
           for i in range(sit):
                im = s.getNext()
        try:
            check = (im == 0)
        except:
            check = True


def TrackLight(im,up,down,left,right,max_index,s):
    counter = 2
    start = 2
    New_Template, Template_XY = im[up:down,left:right], (up,left)
    # save given traffic light
    cv2.imwrite(TL_DIR_PATH + str(1 + max_index)+".jpg",New_Template)  # todo update path!!!!!!!!!!
    # Track loop
    while New_Template.shape[0] <= MAX_SIZE:
        im = s.getNext()
        if counter > start + 50:
            f, arr = matplotlib.pyplot.subplots(1, 1)
            arr.imshow(im, cmap='gray')  # , interpolation='nearest')
            matplotlib.pyplot.show()
            print("up, down, left, right in that order")
            up = int(input())
            down = int(input())
            left = int(input())
            right = int(input())
            New_Template, Template_XY = im[up:down, left:right], (up, left)
            cv2.imwrite(TL_DIR_PATH + str(counter + max_index) + ".jpg", New_Template)
            start = counter
        else:
            New_Template, Template_XY = Tracking.Track(im,New_Template,Template_XY)
            cv2.imwrite(TL_DIR_PATH + str(counter+max_index) + ".jpg",New_Template) #todo update path!!!!!!!!!!
        counter+=1


def TrackGarbage(im,up,down,left,right,max_index,s):
    counter = 2
    start = 2
    New_Template, Template_XY = im[up:down,left:right], (up,left)
    # save given Garbage
    cv2.imwrite(GARBAGE_PATH + str(1 + max_index)+".jpg",New_Template)
    # Track loop
    while New_Template.shape[0] <= MAX_SIZE:
        im = s.getNext()
        if counter > start + 50:
            f, arr = matplotlib.pyplot.subplots(1, 1)
            arr.imshow(im, cmap='gray')#, interpolation='nearest')
            matplotlib.pyplot.show()
            print("up, down, left, right in that order")
            up = int(input())
            down = int(input())
            left = int(input())
            right = int(input())
            New_Template, Template_XY = im[up:down, left:right], (up, left)
            cv2.imwrite(GARBAGE_PATH + str(counter + max_index) + ".jpg", New_Template)
            start = counter
        else:
            New_Template, Template_XY = Tracking.Track(im,New_Template,Template_XY)
            cv2.imwrite(GARBAGE_PATH + str(counter+max_index) + ".jpg",New_Template)
        counter+=1

fps = 40
ShowVideo(TL_PATH, fps)
