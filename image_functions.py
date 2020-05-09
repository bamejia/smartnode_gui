import os
import shutil

import cv2

import Utility_Functions as util
from CoordList import coordList
from CoordObj import coordObj
from DEFAULTS import SCREEN_DIMS

# import picamera

#   try-catch for picamera import
#       -> this is needed if this file is loaded on a non-raspberry pi system
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray

except ModuleNotFoundError:
    print("PiCamera Not Detected When Loadig image_functions.py")
    print("\t-> image / video capture may not work correctly!")


#   Functions used in OCR sampling Runs

#   takes the source picture
def takeSource(srcPath='source.jpg', debug=False):
    srcPath = util.getFullPath(srcPath)
    if debug:
        print(f"Capturing Source Image, saving to \n\t'{srcPath}'")

    try:
        with PiCamera() as camera:
            camera.capture(srcPath)
            camera.stop_preview()
            camera.close()

    except NameError:
        print('**Cannot Use Camera On This System')
        print("->\tDuplicating Default 'kittens.jpg' as 'source.jpg'")
        shutil.copy(util.getFullPath('kittens.jpg'), srcPath)

    if debug:
        print('\tSource Image Captured!\n')


#   generates cropped images based on source image and crop objects
#   returns a list of file paths for use with ocr
def cropSource(src_path='source.jpg', debug=False):
    if not os.path.exists(src_path):
        print("No Source Image, Fool! Run takeSource!")
        return

    else:
        #   load image from path
        src_img = cv2.imread(util.getFullPath(src_path))

        #   load the coordList
        cropObjs = coordList()

        #   iterate through cropped objects, skipping the first(default) object
        for obj in cropObjs.myList[1:]:
            name = obj.name + '.jpg'
            topL = obj.topL
            botR = obj.botR

            if debug:
                print("Cropping Source Image")
                print(f"\tname: {name}, topL: {topL}, botR: {botR}")
                print(f"\tx: {topL[0]} -> {botR[0]}")
                print(f"\ty: {topL[1]} -> {botR[1]}")

            #   crop the image: y: bot-> top,   x: L->R
            crop_img = src_img[topL[1]:botR[1], topL[0]:botR[0]]
            cv2.imwrite(util.getFullPath(name), crop_img)


#   Functions used by Cropping Setup


#   adds an entry to cropFile.json
#   displays current image with cropping regions,
#   if no image exists takes one
#   allows user to add an additional one by tapping the screen
def addCrop(cropObjs, imgPath='source.jpg'):
    util.getFullPath(imgPath)

    if not os.path.exists(imgPath):
        print("No source image, Running takeSource")

        #   WARNING-> takeSource will duplicate 'kittens' image if the camera isn't connected
        takeSource()

        # return

    #   load image from path, create a named window of the correct size
    image = cv2.imread(imgPath)

    windowName = "Source Image"
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, SCREEN_DIMS['width'], SCREEN_DIMS['height'])

    #   parameters to pass to the listener w/ important stuff added in
    param = [image, windowName, cropObjs]

    #   add mouse listener function,
    cv2.setMouseCallback(windowName, addCropHandler, param)

    #   add rectangles to the window
    for obj in cropObjs.myList[1:]:
        cv2.rectangle(image, obj.topL, obj.botR, (0, 255, 0), 6)

    cv2.imshow(windowName, image)
    cv2.waitKey(0)

    return cropObjs


#   click handler for addCrop
#   first and second click append coords to param and draw to image
#   third click saves new coord obj and closes window
def addCropHandler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print(f"\nCLICK DETECTED! Len of Params: {len(param)}")

        image = param[0]
        windowName = param[1]
        cropObjs = param[2]

        #   adjust x/y for touchscreen inaccuracy
        #   *always returns slightly down and to the right->adjusted
        coord = (x - 5, y - 5)

        #   using number of parameters to make decisions
        #   number of params starts at 3
        #       -> the next two events append x/y coords to list of params
        if len(param) < 5:
            print(f"appending coord {coord}")
            #   add coords to list
            param.append(coord)

            # draw a circle
            cv2.circle(image, coord, 15, (216, 230, 0), 5)
            cv2.imshow(windowName, image)
            cv2.waitKey(1)

        # Draw the rectangle after the second click
        if len(param) == 5:
            print("drawing rectangle")
            topL = param[3]
            botR = param[4]
            cv2.rectangle(image, topL, botR, (0, 255, 0), 6)
            cv2.imshow(windowName, image)
            cv2.waitKey(1)

            #   append a zero to params just to require one more click before saving
            param.append(0)

        #   on third click add the object and close the window
        elif len(param) == 6:
            # param = [image, windowName], cropObjs]
            print("saving coordObj")

            name = "crop" + str(cropObjs.getSize())
            topL = param[3]
            botR = param[4]

            cropObjs.addObject(coordObj(name, topL, botR))

            print("closing window ")
            cv2.destroyAllWindows()


#   shows a video ###currently broken af
def showVid():
    with PiCamera() as camera:
        # camera.resolution = (640, 480)
        camera.resolution = (800, 480)

        camera.framerate = 32
        # rawCapture = PiRGBArray(camera, size=(640, 480))
        rawCapture = PiRGBArray(camera, size=(800, 480))

        windowName = "Live Feed"
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

        # terminate = False
        param = []

        #   set window size, move window
        cv2.resizeWindow(windowName, SCREEN_DIMS['width'], SCREEN_DIMS['height'])

        #   load in the crop objs
        cropObjs = coordList()

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            #   draw the rectangles on the image
            for obj in cropObjs.myList[1:]:
                cv2.rectangle(image, obj.topL, obj.botR, (0, 255, 0), 3)

            # show the frame
            cv2.imshow(windowName, image)

            cv2.setMouseCallback(windowName, closeEvent, param)
            cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop

            if param:
                break

    cv2.destroyWindow(windowName)
    print("Outside of loop\n\n")


#   shows the source image with the bounding areas for cropping
def showImage(imgPath=util.getFullPath('source.jpg')):
    if not os.path.exists(imgPath):
        print("No Source Image, Fool! Run takeSource!")
        return

    else:
        #   load image from path, create a named window
        image = cv2.imread(imgPath)
        windowName = "Source Image"
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

        #   set window size, move window
        cv2.resizeWindow(windowName, SCREEN_DIMS['width'], SCREEN_DIMS['height'])
        # cv2.moveWindow(windowName, 0, -50)

        #   add mouse listener function
        cv2.setMouseCallback(windowName, closeEvent)

        cropObjs = coordList()

        #   add rectangles to the window
        for obj in cropObjs.myList[1:]:
            cv2.rectangle(image, obj.topL, obj.botR, (0, 255, 0), 3)

        cv2.imshow(windowName, image)
        cv2.waitKey(0)


#   Use this event listener if you want to close after one click only
def closeEvent(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print("Closing...")
        param.append(True)
