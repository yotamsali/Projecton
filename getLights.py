import csv
import cv2

UPPER_LEFT = (2,3)
LOWER_RIGHT = (4,5)
X = 0
Y = 1

f = open('~/Downloads/dayClip1/annotations/1/frameAnnotationsBOX.csv') # change the path to your computer
r = csv.reader(f)

def GetInfo(row):
    return str.split(row,';')

def GetTrafficLight(image, upper_left, lower_right):
    return image[upper_left[Y]:lower_right[Y], upper_left[X]:lower_right[X]]

i = 0

for row in r:
    rowInfo = GetInfo(row[0])
    upper_left = (int(rowInfo[UPPER_LEFT[X]]),int(rowInfo[UPPER_LEFT[Y]]))
    lower_right = (int(rowInfo[LOWER_RIGHT[X]]),int(rowInfo[LOWER_RIGHT[Y]]))
    image = cv2.imread(rowInfo[0]) #change the path
    cv2.imwrite("/home/yovelrom/Downloads/gif/" + i + ".jpg", GetTrafficLight(image,upper_left,lower_right))
    i += 1


