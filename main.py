from carControl import*
from streamer import*
path = 'try.avi'
strm = Streamer(path)
while True:
    im = strm.getImage()
    Light = recognize()
    if Light[0] == True:
        Direction = getDirection()
        if Direction == True:
            main_Track(Light)
        else:
            Drive(Light[0])

def main_Track (Light):
    color = list(5)
    color2 = list(5)
    while Light[0] == True:   ## reset color list.
        for i in range(0,4):
            color2[i] = color[i]
        for i in range(0,4):
            color[i] = color2[i+1]
        color[4] = color(Light[1]) ##get the new color
        Deci_Maker(color,Light[1])
        Light = Tracker(Light[1], Light[2])

def Deci_Maker(color, distance):
    if color[4] == 'green':
        empty_color = False
        for i in range(0,3): ## checks if it is glancing green
            if color[i] == 'empty':
                empty_color = True
        if empty_color == False:
            Drive(True)
        else:
            color[4] = 'empty'
    else:
        Break(distance)

def Break(distance):
    return

