#   All OCR-related functions go in here -> image captuer / cropping files are in image_functions
import json

import cv2
import pytesseract

import DEFAULTS as defaults
import Settings_Functions as settings


#   cycles through list of entries in ocrData, capturing text from each
#   saves OCRData to file and returns modified version
def doOCR_All(ocrData):
    #   get list of ocrObjects
    objects = getOCRObjects(ocrData)

    #   iterate through list
    for obj in objects:
        options = getOCROptions(ocrData, obj)
        newText = doOCR_Single(options)
        setOCRText(ocrData, obj, newText)

    #   write these values to file once completed
    saveOCRData(ocrData)
    return ocrData


#   actual OCR function -> accepts options, returns a string

#   default lang is 'eng' -> normal english characters
#   call this function with 'ssd' for lang to use 7-segment library
#   PSM 7 is the single line page segmentation mode -> this one works best for clock displays
#   PSM 8 is the single word page segmentation mode
def doOCR_Single(options):
    #   This function is almost a direct duplicate of the one by David Matimu located at:
    #   https: // github.com / Davidmatimu / Firebase / blob / master / ocr.py
    file = options[0]
    psm = options[1]
    lang = options[2]

    print(f"Performing OCR on file: {file}")

    # Define configuration parameters
    configStr = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata/" -l lang --oem 1 --dpi 72 --psm {} -l {}'
    config = (configStr.format(psm, lang))

    # Read image from Disk
    image = cv2.imread(file)

    print(f"Processing image with PSM {psm} using language {lang}")
    text = pytesseract.image_to_string(image, config=config, output_type='dict')

    return text['text']


#   prints the contents of ocrData['dataset']
def printDataSet(ocrData):
    dataset = json.loads(ocrData['dataset'])
    print("\nContents of OCRData")
    #   each obj in dataset has entries like name, file, and ocr settings/output
    for obj in dataset:
        print(f"\n{obj}:")
        objData = dataset[obj]

        #   print out the individual key/value fields in the current entry
        for entry in objData:
            print(f"\t'{entry}': '{objData[entry]}'")


#   remove last entry from OCRData['dataset']
#   argument is the parent container, OcrData
#   returns modified version
def removeLast_OCRData(ocrData):
    #   copy dataset from ocrData file
    dataset = json.loads(ocrData['dataset'])
    print(f"entries in dataset: {len(dataset)}")

    #   remove last entry
    if len(dataset) > 0:
        removed = dataset.popitem()
        print(f"removed {removed} from dataset")

        #   if size is now zero set ocrSetup flag in mainSettings to True
        if len(dataset) == 0:
            mainSet = settings.loadSettings('mainSettings.json')
            settings.changeSetting(mainSet, 'OCR_Setup', 'True')

        #   save changes
        return settings.changeSetting(ocrData, 'dataset', dict(dataset))

    else:
        print("Unable to remove from empty dataset")
    return ocrData


#   adds an entry to OCRData -> needs ocrData object in order to save changes
#   returns modified version
def addEntry_OCRData(ocrData, newName):
    #   copy dataset from ocrData file

    if isinstance(ocrData['dataset'], dict):
        dataset = ocrData['dataset']
    else:
        dataset = json.loads(ocrData['dataset'])

    #   default data object from DEFAULTS
    defObj = defaults.OCR_DATA_ENTRY

    #   change default name and file
    defObj['name'] = newName
    defObj['file'] = newName + '.jpg'

    #   use builtin setdefault method to automatically append
    dataset.setdefault(newName, defObj)

    #   if size of dataset is now exactly 1 it was empty when it started
    #       -> set ocr setup flag to true
    if len(dataset) == 1:
        mainSet = settings.loadSettings('mainSettings.json')
        settings.changeSetting(mainSet, 'OCR_Setup', 'True')

    #   save changes to file and return modified version
    return settings.changeSetting(ocrData, 'dataset', dict(dataset))


#   returns a list of the entries in ocrData['dataset']
def getOCRObjects(ocrData):
    return list(ocrData['dataset'].keys())


#   returns array containing ocr options for the spcified entry
#   return is [file, psm, lang]
def getOCROptions(ocrData, name):
    entry = ocrData['dataset'][name]
    return [entry['file'], entry['psm'], entry['lang']]


#   changes text field of the provided entry in OCRData
#   DOES NOT SAVE (can also be used to access text)
def setOCRText(ocrData, name, newText=""):
    #   modify ocrData object with newText if it is provided and return modified version
    if newText:
        ocrData['dataset'][name]['text'] = newText
        return ocrData
    else:
        return ocrData['dataset'][name]['text']


#   saves ocrData to file after sample run has been completed
def saveOCRData(ocrData):
    settings.changeSetting(ocrData, 'dataset', ocrData['dataset'])
