# import the necessary packages
import argparse
import cv2
from scipy import misc as m
import os
import random

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
NUMBER_OF_IMAGES = 20 ;


def getIndexes():
    if(not os.path.exists(os.getcwd()+"/counter.txt")):
        counter_file = open("counter.txt", "w")
        counter_file.close()

    counter_file = open("counter.txt", "r+")


    line1 = counter_file.readline()
    if(not line1):
        print("Initializng file name. starting from positive0")
        counter_file.write("Positive Counter is 0\n")
        posIndex = 0
    else:
        posIndex = [int(s) for s in line1.split() if s.isdigit()][0]
    line2 = counter_file.readline()
    if(not line2):
        print("Initializng file name. starting from negative0")
        counter_file.write("Negative Counter is 0\n")
        negIndex = 0
    else:
        negIndex = [int(s) for s in line2.split() if s.isdigit()][0]
    counter_file.close()
    return posIndex,negIndex

def setIndexes(posIndex,negIndex):
    counter_file = open("counter.txt", "r+")
    counter_file.write("Positive Counter is "+str(posIndex)+"\n")
    counter_file.write("Negative Counter is "+str(negIndex)+"\n")
    counter_file.close()

def initFolders():
    if (not os.path.isdir(os.getcwd() + "/pos")):
        os.makedirs(os.getcwd() + "/pos")
    if (not os.path.isdir(os.getcwd() + "/neg")):
        os.makedirs(os.getcwd() + "/neg")
    if (not os.path.isdir(os.getcwd() + "/labeled")):
        os.makedirs(os.getcwd() + "/labeled")


def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False

		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

def getNewImageCoo(cord):
    if(cord[0][0]<cord[1][0]):
        if(cord[0][1] < cord[1][1]):
            return cord
        else: #coordinates[0][1] > coordinates[1][1]
            return [(cord[0][0],cord[1][1]),(cord[1][0],cord[0][1])]
    else: #cord[0][0]>cord[1][0]
        if(cord[0][1] < cord[1][1]):
            return [(cord[1][0], cord[0][1]), (cord[0][0], cord[1][1])]
        else:
            return [(cord[1][0], cord[1][1]), (cord[0][0], cord[0][1])]









print ("How to use the program?\nwrite the path of the folder where the images are.\nnow, images will start to appear."
       " mark the required area in the image. if you arent happy with how you marked, press r in order to reset."
       "\nif the sample is a positive sample, press g in order to save it. if the sample is negative, "
       "press b in order to save it.\nwhen you finished with a picture, press f to move on.\n")
path = raw_input("Enter the path of the pictures folder\n")
print("Searching images in folder: "+path)
pictures = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
pictures.sort()
to_break = False # a boolean to break the loop with 'q'
for pictureName in pictures:
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread(path+"/"+pictureName)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    initFolders()
    posCounter, negCounter = getIndexes()

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("g"):
            cooAr = getNewImageCoo(refPt)
            tl_height = abs(cooAr[0][0] - cooAr[1][0])
            tl_width = abs(cooAr[0][1] - cooAr[1][1])
            tl_up = cooAr[0][1]
            tl_down = cooAr[1][1]
            tl_right = cooAr[1][0]
            tl_left = cooAr[0][0]
            image_height , image_width , useless  = image.shape
            for i in range(NUMBER_OF_IMAGES):
                random_right = random.randint(0, tl_width / 2)
                random_left = random.randint(0, tl_width / 2)
                random_up = random.randint(0, tl_height / 2)
                random_down = random.randint(0, tl_height / 2)
                if (tl_right + random_right >= image_width):
                    random_right = image_width - tl_right
                if (tl_left - random_left <= 0):
                    random_left = tl_left
                if (tl_up - random_up <=0 ):
                    random_up = tl_up
                if (tl_down + random_down >= image_height):
                    random_down = image_height - tl_down
                roi = clone[tl_up-random_up:tl_down+random_down, tl_left-random_left:tl_right+random_right]
                goodpath = "posIndex:"+str(i)+"-u_"+str(random_up)+"_d_"+str(random_down)+"_l_"+str(random_left)+"_r_"+str(random_right)+"_number:"+str(posCounter) + ".jpg"
                m.imsave(os.path.join("pos", goodpath), roi[..., ::-1])
                image = clone.copy()
                posCounter = posCounter + 1

        elif key == ord("b"):
            cooAr = getNewImageCoo(refPt)
            roi = clone[cooAr[0][1]:cooAr[1][1], cooAr[0][0]:cooAr[1][0]]
            badpath = str(negCounter) + ".jpg"
            m.imsave(os.path.join("neg", badpath), roi[..., ::-1])
            image = clone.copy()
            negCounter = negCounter + 1


        elif key == ord("f"):
            break

        elif key == ord("q"):
            to_break = True
            break
    if to_break:
        break



    # close all open windows
    setIndexes(posCounter, negCounter)
    cv2.destroyAllWindows()
    os.rename(path+"/"+pictureName, "labeled/"+"labeled_"+pictureName)