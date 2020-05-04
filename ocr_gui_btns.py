# functions used by buttons in frams from ocr_gui.py

from image_functions import *


#   Functions for CropSetup Frame

#   adds a
def cropSetup_add():
    print("adding crop bounding box")
    addCrop()

    print("modifying ocrSettings")

    #   load use size of coordList to get name of next entry
    tempList = coordList()
    newObj = 'crop' + str(len(tempList.myList))
