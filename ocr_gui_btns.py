# functions used by buttons in frams from ocr_gui.py

from Settings_Functions import loadSettings, changeSetting
from image_functions import *


#   Functions for CropSetup Frame

#   adds a
def cropSetup_add():
    print("adding crop bounding box")
    addCrop()

    print("modifying ocrSettings")

    #   load use size of coordList to get name of next entry
    tempList = coordList()
    newname = 'crop' + str(len(tempList.myList))

    #   modify all settings pertaining to doing ocr on the entry
    mySet = loadSettings('OCRSettings.json')
    changeSetting(mySet, 'cropImgs', newname, newname + '.jpg')
    changeSetting(mySet, 'cropPSM', newname, '7')
    changeSetting(mySet, 'cropLang', newname, 'ssd')
    changeSetting(mySet, 'cropLang', newname, '')
