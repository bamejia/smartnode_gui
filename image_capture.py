'''''

TODO: DELETE THIS

'''


import os

import cv2


def capture_image():
    # #print opening message
    # print("\nPress:\t'c' to crop\t'r' to reset\t'x' to  exit")

    # print("Click:\t1) top-left\t2) bot-right\t3) save area")
    #
    #
    # # global variables
    # global newCoords
    # global oldCoords
    # newCoords = []
    # oldCoords = loadCoords()


    # get local directory
    dir = os.path.dirname(__file__)

    #paths to source&cropped images
    # global srcPath
    # global cropPath
    srcPath = os.path.join(dir, 'kittens.jpg')
    # cropPath = os.path.join(dir, 'kittens_cropped.jpg')

    #load image from srcPath
    # global srcImage
    srcImage = cv2.imread(srcPath)

    return srcImage