# functions used by buttons in frams from ocr_gui.py
import json

import Settings_Functions as settings
import image_functions as image
import ocr_functions as ocr
from CoordList import coordList
import DEFAULTS as defaults


#   Functions for CropSetup Frame

#   calls addCrop function in image functions
#   modifies ocrData file (setup flag modified here)
def cropSetup_add():
    tempList = coordList()

    print("adding crop bounding box")
    image.addCrop(tempList)

    print("adding ocrData entry")
    #   load use size of coordList to get name of next entry
    newName = 'crop' + str(len(tempList.myList))

    ocrData = settings.loadSettings('OCRData.json')
    ocr.addEntry_OCRData(ocrData, newName)


#   removes coord object and ocrData entry (setup flag modified here)
#   returns true on success
def cropSetup_remove():
    ocrData = settings.loadSettings('OCRData.json')

    if isinstance(ocrData['dataset'], str):
        dataset = json.loads(ocrData['dataset'])
    else:
        dataset = ocrData['dataset']

    if len(dataset) >= 1:
        print("removing last entry from coordList")
        myList = coordList()
        myList.popLast()
        myList.saveSet()

        print("removing last entry from Settings file")
        ocr.removeLast_OCRData(ocrData)

        return True
    else:
        print("Noting removed - data is empty")
        return False


#   displays source image with crop regions
def cropSetup_show():
    print("displaying image with crop areas")

    # image.showImage()

    #   currently broken but would be cool if we could kill it
    image.showVid()


def next_mode(current_mode):
    defaults.LOOP_TYPES[current_mode].ord