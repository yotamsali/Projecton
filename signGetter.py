"""
returns the picture of the traffic light with the sign above
"""
ADD2TOP_RATIO = 0.4
CROP_FROM_BOTTOM_RATIO = 0.5

#x, y - coordinates of upper left corner of TL image
#w, h - width and height of TL image
#returns x,y,w,h of image that contains the sign above the TL
def getSign(x, y, w, h):

    #calculate ratios
    temp_y = y - h * ADD2TOP_RATIO
    temp_h = h * (1 + ADD2TOP_RATIO - CROP_FROM_BOTTOM_RATIO)

    #fit to image
    new_y = max(0, temp_y)
    new_h = temp_h - (new_y - temp_y)

    return x, new_y, w, new_h