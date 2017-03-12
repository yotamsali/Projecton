import time

import cv2

mili_sec = 1000

class Streamer:
    def __init__(self, filepath, fps):
        self.timestamp = time.time()
        self.cap = cv2.VideoCapture(filepath)
        self.fps = fps
        self.frameNumber = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cv2.destroyAllWindows()

    def getImage(self):
        timeDiff = time.time() - self.timestamp
        if (self.cap.isOpened()):
            self.cap.set(cv2.CAP_PROP_POS_MSEC, mili_sec * timeDiff * self.fps)
            [ret, frame] = self.cap.read()
        else:
            return 0
        if not ret:
            return 0
        return frame

    def endStreamer(self):
        if not self.cap.isOpened:
            self.cap.release()





