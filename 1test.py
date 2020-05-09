import cv2
import pytesseract

import Utility_Functions as util

file = util.getFullPath('crop1.jpg')
psm = 8
lang = 'eng'

# Define configuration parameters
configStr = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata/"  -l {} --oem 1 --dpi 72 --psm {}'
# configStr = '--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata/" -l lang --oem 1 --dpi 72 --psm {} -l {}'
config = (configStr.format(lang, psm))

# Read image from Disk
img = cv2.imread(file)

# do the tesseracts
output = pytesseract.image_to_string(img, config=config, output_type='dict')

# print the text
print(output['text'])
