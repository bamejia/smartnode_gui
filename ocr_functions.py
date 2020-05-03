#   All OCR-related functions go in here
from Settings_Functions import *
import shutil
import cv2
from DEFAULTS import SCREEN_DIMS

try:
    import picamera
except ModuleNotFoundError:
    print('picamera not found - camera functions will not work')


#   takes the source picture
def takeSource(srcPath=getFullPath('source.jpg')):
    print(f"Capturing Source Image, saving to \n\t'{srcPath}'")

    try:
        with picamera.PiCamera() as camera:
            camera.capture(srcPath)
            camera.stop_preview()
            camera.close()

    except NameError:
        print('**Cannot Use Camera On This System')
        print('->\tDuplicating Default \'kittens.jpg\' as \'source.jpg\'')
        shutil.copy(getFullPath('kittens.jpg'), srcPath)

    print('\tSource Image Captured!\n')


#   Generates Cropped Images from a Source Image
def cropSource(cropImgs):
    print("Cropping Source Image...")
    print("\t**NOT IMPLEMENTED-> CROP SOURCE IMAGE")
    print("\tcontents of arguments")
    for entry in cropImgs:
        print(f"\t\t{entry}")
    print()


#   Performs OCR on each of the Cropped Images
def doOCR(image, PSM, lang):
    print("Performing OCR")
    print("\t**IMPLEMENTED BUT NOT INTEGRATED -> David's Code")
    print(f"\tpath: {image}, PSM: {PSM}, lang: {lang}")


#   Cropping Setup Function
def cropSetup():
    print("Cropping Setup Function")
    print("\t**IN DEVELOPMENT BY BRYAN")

    print("\tManually Setting OCR Setup Flag to True in Main Settings")
    changeSetting(loadSettings('mainSettings.json'), 'OCR_Setup', True)


#   attempts to display the image at the provided path
def showImage(imgPath=getFullPath('source.jpg')):
    print("print displaying image... Warning, this may crash all your shit...")

    def closeWin(event, x, y, flags, param):
        print("\tClosing Image")
        cv2.destroyAllWindows()

    if (not os.path.exists(imgPath)):
        print("No Source Image, Fool! Run takeSource!")
        return

    else:
        image = cv2.imread(imgPath)
        windowName = "Source Image"

        cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow(windowName, SCREEN_DIMS['width'], SCREEN_DIMS['height'])
        cv2.setMouseCallback(windowName, closeWin)

        cv2.imshow(windowName, image)
        cv2.waitKey(0)