#   this file is for directly testing simple bits of code -> override run settings prior to launch

import DEFAULTS as defaults
import Settings_Functions as settings


#   prints the contents of ocrData['dataset']
def printDataSet(ocrData):
    dataset = ocrData['dataset']
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
def removeLast(ocrData):
    #   copy dataset from ocrData file
    dataset = ocrData['dataset']
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
def addEntry(ocrData, newName):
    #   copy dataset from ocrData file
    dataset = ocrData['dataset']

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
    settings.changeSetting(ocrData, 'dataset', ocrData['dataSet'])


#   load ocrData from file
ocrData = settings.loadSettings('OCRData.json')

# printDataSet(ocrData)
objs = getOCRObjects(ocrData)
for obj in objs:
    options = getOCROptions(ocrData, obj)
    setOCRText(ocrData, obj, obj + '_text')
    text = setOCRText(ocrData, obj)
    print(f"{obj}: {options[0]}, {options[1]}, {options[2]}, {text}")

# setOCRText(ocrData, 'crop1', )
# removeLast(ocrData)

printDataSet(ocrData)
