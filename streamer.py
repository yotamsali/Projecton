import time

import imageio

# gil was here
class Streamer:
    def __init__(self, filepath, fps):
        self.timestamp = time.time()
        self.vid = imageio.get_reader(filepath,  'ffmpeg')
        self.fps = fps
        self.prev = 1

    def getImage(self):
        timeDiff = time.time() - self.timestamp
        try:
            self.prev = int(self.fps * timeDiff)
            return self.vid.get_data(self.prev)
        except:
            return 0

    def getNext(self):
        try:
            self.prev+=1
            return self.vid.get_data(self.prev)
        except:
            return 0











