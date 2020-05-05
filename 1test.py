import Settings_Functions as settings
import ocr_functions as ocr

ocrData = settings.loadSettings('OCRData.json')

# settings.resetDefault(ocrData, 'dataset')
# ocr.addEntry_OCRData(ocrData, 'crop2')

ocr.printDataSet(ocrData)

ocrData = ocr.doOCR_All(ocrData)
ocr.printDataSet(ocrData)
