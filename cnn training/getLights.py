import csv
import cv2

UPPER_LEFT = (2,3)
LOWER_RIGHT = (4,5)
X = 0
Y = 1

def GetInfo(row):
    return str.split(row,';')

def GetTrafficLight(image, upper_left, lower_right):
    return image[upper_left[Y]:lower_right[Y], upper_left[X]:lower_right[X]]


for dir in range(13, 14):
    f = open('/home/yovelrom/Downloads/dayTrain/dayClip'+ str(dir) + '/frameAnnotationsBOX.csv')  # change the path to your computer
    r = csv.reader(f)
    i = 0
    j = 0
    for row in r:
        if j==0:
            j+=1
            continue
        rowInfo = GetInfo(row[0])
        upper_left = (int(rowInfo[UPPER_LEFT[X]]),int(rowInfo[UPPER_LEFT[Y]]))
        lower_right = (int(rowInfo[LOWER_RIGHT[X]]),int(rowInfo[LOWER_RIGHT[Y]]))
        name = rowInfo[0][11:]
        image = cv2.imread("/home/yovelrom/Downloads/dayTrain/dayClip"+ str(dir) +"/frames" + name) #change the path
        cv2.imwrite("/home/yovelrom/Downloads/cutImages/clip" + str(dir) + "/" + str(i) + ".jpg", GetTrafficLight(image,upper_left,lower_right))
        #cv2.imshow("im",GetTrafficLight(image,upper_left,lower_right))
        #cv2.waitKey(0)
        i += 1


