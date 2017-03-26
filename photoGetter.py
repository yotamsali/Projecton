import cv2
vidcap = cv2.VideoCapture('./my/ourCam25.3 11')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  #print ('Read a new frame: ', success)
  cv2.imwrite("my/frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1