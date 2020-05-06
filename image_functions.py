import os
import shutil

import cv2

from CoordList import coordList
from CoordObj import coordObj
from DEFAULTS import SCREEN_DIMS
from Utility_Functions import getFullPath

# import picamera


try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray

except ModuleNotFoundError:
    print("picamera can't be used ")


#   takes the source picture
def takeSource(srcPath=getFullPath('source.jpg')):
    print(f"Capturing Source Image, saving to \n\t'{srcPath}'")

    try:
        with PiCamera() as camera:
            camera.capture(srcPath)
            camera.stop_preview()
            camera.close()

    except NameError:
        print('**Cannot Use Camera On This System')
        print('->\tDuplicating Default \'kittens.jpg\' as \'source.jpg\'')
        shutil.copy(getFullPath('kittens.jpg'), srcPath)

    print('\tSource Image Captured!\n')


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
def showImage(cropObjs=coordList(), imgPath=getFullPath('source.jpg')):
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


#   displays current image with cropping regions,
#   if no image exists takes one
#   allows user to add an additional one by tapping the screen
def addCrop(cropObjs=coordList(), imgPath=getFullPath('source.jpg')):
    if not os.path.exists(imgPath):
        print("No Source Image, Running TakeSource")
        takeSource()

    else:
        #   load image from path, create a named window of the correct size

        image = cv2.imread(imgPath)

        windowName = "Source Image"
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, SCREEN_DIMS['width'], SCREEN_DIMS['height'])

        #   parameters to pass to the listener w/ important stuff added in
        param = [image, windowName, cropObjs]

        #   add mouse listener function,
        cv2.setMouseCallback(windowName, clickHandler, param)

        #   add rectangles to the window
        for obj in cropObjs.myList[1:]:
            cv2.rectangle(image, obj.topL, obj.botR, (0, 255, 0), 6)

        cv2.imshow(windowName, image)
        cv2.waitKey(0)


#   click handler for addCrop
#   first and second click append coords to param and draw to image
#   third click saves new coord obj and closes window
def clickHandler(event, x, y, flags, param):
    # if event == cv2.EVENT_LBUTTONDOWN:
    if event == cv2.EVENT_LBUTTONUP:
        image = param[0]
        windowName = param[1]

        #   adjust x/y for touchcreen inaccuracy
        #   *always returns slightly down and to the right
        coord = (x - 5, y - 5)

        #   using number of parameters to make decisions
        #   starts with two params, for the first two
        if (len(param) < 5):
            #   add coords to list
            param.append(coord)

            # draw a circle
            cv2.circle(image, coord, 15, (216, 230, 0), 5)
            cv2.imshow(windowName, image)
            cv2.waitKey(1)

            # Draw the rectangle after the second click
            if (len(param) == 5):
                cv2.rectangle(image, param[3], param[4], (0, 255, 0), 6)
                cv2.imshow(windowName, image)
                cv2.waitKey(1)
                param.append(0)

        #   on third click add the object and close the window
        else:
            cropObjs = param[2]
            #   create a new coord Obj and add to list
            name = "crop" + str(cropObjs.getSize())
            cropObjs.addObject(coordObj(name, param[3], param[4]))

            print("closing window ")
            cv2.destroyAllWindows()


#   generates cropped images based on source image and crop objects
#   returns a list of file paths for use with ocr
def cropSource(cropObjs=coordList, imgPath=getFullPath('source.jpg')):
    if not os.path.exists(imgPath):
        print("No Source Image, Fool! Run takeSource!")
        return

    else:
        #   load image from path
        image = cv2.imread(imgPath)

        #   iterate through cropped objects, skipping the first(default) object
        for obj in cropObjs.myList[1:]:
            name = obj.name + '.jpg'

            print(name)

            topL = obj.topL
            botR = obj.botR
            print(name, topL, botR)
            print('x:', topL[0], '->', botR[0])
            print('y:', topL[1], '->', botR[1])

            #   crop the image: y: bot-> top,   x: L->R
            crop_img = image[topL[1]:botR[1], topL[0]:botR[0]]
            cv2.imwrite(getFullPath(name), crop_img)
