# functions used by buttons in frams from ocr_gui.py

from Settings_Functions import loadSettings, changeSetting, resetDefault
from image_functions import *


#   Functions for CropSetup Frame

#   adds a cropping area
def cropSetup_add():
    print("adding crop bounding box")
    addCrop()

    print("modifying ocrSettings")

    #   load use size of coordList to get name of next entry
    tempList = coordList()
    newname = 'crop' + str(len(tempList.myList))

    #   modify all settings pertaining to doing ocr on the entry
    mySet = loadSettings('OCRSettings.json')

    #   if user has removed all items reset to default
    if len(mySet['cropImgs']) == 0:
        print("removed last entry -> resetting to default")
        modList = ('cropImgs', 'cropPSM', 'cropLang', 'cropTxt')
        for entry in modList:
            resetDefault(mySet, entry)

    else:
        changeSetting(mySet, 'cropImgs', newname, newname + '.jpg')
        changeSetting(mySet, 'cropPSM', newname, '7')
        changeSetting(mySet, 'cropLang', newname, 'ssd')
        changeSetting(mySet, 'cropTxt', newname, 'null')


#   removes a cropping area
def cropSetup_remove():
    mySet = loadSettings('OCRSettings.json')
    if len(mySet['cropImgs']) >= 1:

        print("removing last entry from coordList")

        myList = coordList()
        myList.popLast()
        myList.saveSet()

        print("removing last entry from Settings file")
        #   modify all settings pertaining to doing ocr on the entry
        mySet = loadSettings('OCRSettings.json')

        modList = ('cropImgs', 'cropPSM', 'cropLang', 'cropTxt')
        for entry in modList:
            print(f"removing from {entry}")
            temp = mySet[entry]
            temp.popitem()
            changeSetting(mySet, entry, temp)

        #   if we removed all the entries reset the flag in mainSettings
        changeSetting(loadSettings('mainSettings.json'), 'OCR_Setup', 'False')

    else:
        print("no entries remaining -> nothing removed")


#   displays source image with crop regions
def cropSetup_show():
    print("displaying image with crop areas")
    showImage()
