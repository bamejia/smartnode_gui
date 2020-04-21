#!/bin/python3

'''

This script allows the user to set cropping coords by clicking an image with their mouse
Coordinates are stored in a json file 
'''

import tkinter
import cv2
import crop_original.jsonCoords as jsonCoords
import os

# handler for mouse events - called with every mouse movement and click
def click_handler(event, x, y, flags, param):
    
    # weird workaround to to allow program to modify global variables
    global clone, oldCoords, newCoords 
    
    # check to see if the left mouse button was released
    if event == cv2.EVENT_LBUTTONUP:
        
        # record mouse coordinates to coord array
        newCoords.append((x, y))
        clicked = True
        
        # on 3rd click update crop rectange instead of displaying circle
        if len(newCoords) > 2:
            print('\n>Saving New Coords')
            clone = srcImage.copy()
            updateCrop()
        
        # put a circle on the screen where the click happened
        else:
            cv2.circle(clone, (x, y), 10, (255, 0, 0), 2)
            cv2.imshow("source", clone)
            #print("released: ", x, ", ",
            
    # refreshes rectangle with every mouse movement... possibly take this out
    elif (len(newCoords) == 1):
        clone = srcImage.copy()
        cv2.circle(clone, newCoords[0], 10, (255, 0, 0), 2)
        cv2.rectangle(clone, newCoords[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("source", clone)
        
# displays the cloned image with a rectangle at oldCoords
def show_crop():
    #cv2.imshow("source", clone)
    cv2.rectangle(clone, oldCoords[0], oldCoords[1], (0, 255, 0), 2)
    cv2.imshow("source", clone)

# updates cropping coords and refreshes display of image
def updateCrop():
    global oldCoords, newCoords
    oldCoords = newCoords
    saveCoords()
    newCoords = []
    show_crop()

# crop the image (if applicable)

def cropImage(thisImg, cropArea):
    #create a new cropped image
    cropImg = thisImg[cropArea[0][1]:cropArea[1][1], cropArea[0][0]:cropArea[1][0]]
    canCrop = True
    
    # check that image has non-zero height and width before saving
    if cropImg.shape[0] <1:
        print("\n<ERROR: Cropped image has 0 height!")
        canCrop = False
    
    if cropImg.shape[1] <1:
        print("\n<ERROR: Cropped image has 0 width!")
        canCrop = False
    
    if canCrop:    
        cv2.imwrite(cropPath, cropImg)
        cv2.namedWindow("cropped")
        cv2.imshow("cropped", cropImg)

    else:
        print("Crop Aborted.")


# exit the program
def exitProgram():
    # close all open windows and terminate script
    cv2.destroyAllWindows()
    # exit(0)

# uses jsonCoords to load in saved cropping coords
def loadCoords():
    path = jsonCoords.getFilePath()
    obj = jsonCoords.loadObject(path)
    coords = (jsonCoords.getCoord(obj,0), jsonCoords.getCoord(obj,1))
    return coords

def saveCoords():
    path = jsonCoords.getFilePath()
    obj = jsonCoords.loadObject(path)
    obj = jsonCoords.setCoord(obj, 0, newCoords[0])
    obj = jsonCoords.setCoord(obj, 1, newCoords[1])
    jsonCoords.saveObject(path, obj)

def run():
    #print opening message
    print("\nPress:\t'c' to crop\t'r' to reset\t'x' to  exit")
    print("Click:\t1) top-left\t2) bot-right\t3) save area")


    # global variables
    global newCoords
    global oldCoords
    newCoords = []
    oldCoords = loadCoords()



    # get local directory
    dir = os.path.dirname(__file__)

    #paths to source&cropped images
    global srcPath
    global cropPath
    srcPath = os.path.join(dir, 'kittens.jpg')
    cropPath = os.path.join(dir, 'kittens_cropped.jpg')

    #load image from srcPath
    global srcImage
    srcImage = cv2.imread(srcPath)

    return srcImage

    # open a window named 'source'
    # cv2.namedWindow("source")
    # cv2.imwrite("source", srcImage)
    #
    # # assign click handler to window
    # cv2.setMouseCallback("source", click_handler)
    #
    # #make a copy of the image
    # global clone
    # clone = srcImage.copy()
    #
    # #display the image until a key is pressed
    # cv2.imshow("source", clone)
    # show_crop()
    #
    #
    # #loop forever until 'x' is pressed
    # while True:
    #     key = cv2.waitKey(0)
    #
    #     '''
    #     if len(newCoords) > 1:
    #         print('two clicks!')
    #         updateCrop()
    #    '''
    #     # 'r' key -> reset the cropping region
    #     if key == ord("r"):
    #         print('\n>Resetting Crop Area')
    #         clone = srcImage.copy()
    #         newCoords = []
    #         show_crop()
    #
    #     # 'c' key -> crop image
    #     if key == ord("c"):
    #         print('\n>Cropping Image')
    #         cropImage(clone, oldCoords)
    #         clone = srcImage.copy()
    #         newCoords = []
    #         show_crop()
    #
    #     # 'x' key -> exit
    #     if key == ord('x'):
    #         print('\n>Exiting Program')
    #         exitProgram()
    #         break


#Source: https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

