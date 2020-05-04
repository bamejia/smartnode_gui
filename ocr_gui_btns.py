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
    newFile = newname + '.jpg'

    mySet = loadSettings('OCRSettings.json')

    changeSetting(mySet, 'srcImg', 'source.jpg')
    #
    # 'cropImgs': {'crop1': 'crop1.jpg'},
    # 'cropPSM': {'crop1': '7'},
    # 'cropLang': {'crop1': 'ssd'},
    # 'cropTxt': {'crop1': ''}
