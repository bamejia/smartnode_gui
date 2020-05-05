# functions used by buttons in frams from ocr_gui.py
import Settings_Functions as settings
import image_functions as image
import ocr_functions as ocr
from CoordList import coordList


#   Functions for CropSetup Frame

#   calls addCrop function in image functions
#   modifies ocrData file (setup flag modified here)
def cropSetup_add():
    print("adding crop bounding box")
    image.addCrop()

    print("adding ocrData entry")
    #   load use size of coordList to get name of next entry
    tempList = coordList()
    newName = 'crop' + str(len(tempList.myList))

    ocrData = settings.loadSettings('ocrData.json')
    ocr.addEntry_OCRData(ocrData, newName)


#   removes coord object and ocrData entry (setup flag modified here)
#   returns true on success
def cropSetup_remove():
    mySet = settings.loadSettings('OCRSettings.json')
    if len(mySet['cropImgs']) >= 1:
        print("removing last entry from coordList")
        myList = coordList()
        myList.popLast()
        myList.saveSet()

        print("removing last entry from Settings file")
        ocrData = settings.loadSettings('ocrData.json')
        ocr.removeLast_OCRData(ocrData)

        return True
    else:
        print("Noting removed - data is empty")
        return False


#   displays source image with crop regions
def cropSetup_show():
    print("displaying image with crop areas")
    image.showImage()
