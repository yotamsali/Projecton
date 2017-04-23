from Tracking import Track
from streamer import*

path = 'examples/real.avi'
strm = Streamer(path,10)
im = strm.getImage()

