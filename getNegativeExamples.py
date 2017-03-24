import random
import cv2

UPPER_LEFT = (2,3)
LOWER_RIGHT = (4,5)
X = 0
Y = 1

def GetInfo(row):
    return str.split(row,';')

def GetTrafficLight(image, upper_left, lower_right):
    return image[upper_left[Y]:lower_right[Y], upper_left[X]:lower_right[X]]

def string(i):
    new = ''
    if i==0:
        return "00000"
    inte = 10000
    while i/inte == 0:
        new += '0'
        inte /= 10
    new += str(i)
    return new


for dir in range(2, 14):
    f = '/home/yovelrom/Downloads/dayTrain/dayClip' + str(dir) + '/frames/dayClip'+str(dir)+'--00000.png'
    image = cv2.imread(f)
    i = 0# change the path to your computer
    while not image == None:
        #cv2.imshow("im", image)
        #cv2.waitKey(0)
        for j in range(5):
            up = random.randrange(0, 950)
            down = min(960, up + random.randrange(15, 120))
            left = random.randrange(0, 1275)
            right = min(1280, left + random.randrange(5, 40))


            cv2.imwrite("/home/yovelrom/Downloads/cutImages/neg"+ str(dir) + "/neg" + str(i) + ".jpg", image[up:down,left:right])
        i += 1
        f = '/home/yovelrom/Downloads/dayTrain/dayClip' + str(dir) + '/frames/dayClip'+str(dir)+'--'+string(i)+'.png'
        image = cv2.imread(f)
