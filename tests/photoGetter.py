"""
useful code for getting images from a video
"""

import cv2
vidcap = cv2.VideoCapture('./stop_line_frames/ourCam25.9')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  #print ('Read a new frame: ', success)
  cv2.imwrite("stop_line_frames/frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1