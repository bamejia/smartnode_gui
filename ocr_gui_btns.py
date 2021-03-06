# functions used by buttons in frams from ocr_gui.py
import collections
import json

import DEFAULTS as defaults
import Settings_Functions as settings
import image_functions as image
import ocr_functions as ocr
from CoordList import coordList


#   Functions for CropSetup Frame

#   calls addCrop function in image functions
#   modifies ocrData file (setup flag modified here)
def cropSetup_add(debug=False):
    tempList = coordList()

    if debug: print("adding crop bounding box")
    image.addCrop(tempList)

    if debug: print("adding ocrData entry")

    #   use size of coordList to get name of next entry
    newName = 'crop' + str(len(tempList.myList) - 1)

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


# used for choosing between run modes
def next_mode(current_mode):
    myDeque = collections.deque(defaults.OCR_LOOP_TYPES)
    index = myDeque.index(current_mode)
    myDeque.rotate(-1)
    return myDeque[index]


# used when configuring the ocr settings for each crop object
def next_option(current_option, options):
    myDeque = collections.deque(options)
    index = myDeque.index(current_option)
    myDeque.rotate(-1)
    return myDeque[index]
