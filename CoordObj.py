#   constants for screen size -> probably should add this to a CONSTANTS.py file
# MAX_X = 1280
# MAX_Y = 960
from DEFAULTS import SCREEN_DIMS


#   child object of coordList container - represents a boundary box for cropping
#   Louis Stubbolo, with help from Teddy K, April 2020
#   Note: This works with python 3.7 - not sure about others

class coordObj:
    #   default values
    name = "coord"
    topL = (50, 50)
    botR = (100, 100)

    MAX_X = SCREEN_DIMS['width']
    MAX_Y = SCREEN_DIMS['height']

    #   constructor with optional arguments
    #   Note! These arguments are positional! This means that you can
    #   override them, but only in increasing order
    def __init__(self, nameStr=name, topLeft=topL, botRight=botR):
        if isinstance(nameStr, str) and len(nameStr) > 0:
            self.name = nameStr

        #   make sure overloaded values are within bounds
        if isinstance(topLeft, tuple) and self.checkBounds(topLeft):
            self.topL = topLeft

        if isinstance(botRight, tuple) and self.checkBounds(botRight):
            self.botR = botRight

        #   make sure coords follow convention regardless of which corners the user clicked
        # self.organizeCoords()
        self.topL, self.botR = self.organizeCoords(self.topL, self.botR)

    #   organizes the values in the provided coords so that they match the topL, botR format
    def organizeCoords(self, topLeft, botRight):
        x_vals = [topLeft[0], botRight[0]]
        y_vals = [topLeft[1], botRight[1]]

        x_vals.sort()
        y_vals.sort()

        topLeft = (x_vals[0], y_vals[0])
        botRight = (x_vals[1], y_vals[1])

        return topLeft, botRight

    #   changes the object's name to the supplied string
    def rename(self, name):
        if isinstance(name, str):
            if len(name) > 0:
                self.name = str(name)
            else:
                print("that name is forbidden")
        else:
            print("invalid argument type")

    #   sets the topL and botR coords to the supplied values
    def setCoords(self, newTopL, newBotR):
        if isinstance(newTopL, tuple) and isinstance(newBotR, tuple):

            if self.checkBounds(newTopL) and self.checkBounds(newBotR):
                self.topL, self.botR = self.organizeCoords(newTopL, newBotR)

            else:
                print("supplied coords out of bounds!")

        else:
            print("invalid argument type!")

    #   resizes the the bounding box by adding / subtracting from coord values
    def resize(self, increment):
        if isinstance(increment, int):
            print("resizing")

            #   generate test coords
            test_x = self.topL[0] - increment  # x1
            test_y = self.topL[1] + increment  # y1
            testTopL = (test_x, test_y)

            test_x = self.botR[0] + increment  # x2
            test_y = self.botR[1] - increment  # y2
            testBotR = (test_x, test_y)

            #   reorganize test coords in case resizing swapped positions around
            testTopL, testBotR = self.organizeCoords(testTopL, testBotR)

            #   check that resize doesn't put one of the coords out of bounds
            inBounds = self.checkBounds(testTopL) and self.checkBounds(testBotR)

            #   only resize if new coords are valid
            if inBounds:
                self.setCoords(testTopL, testBotR)
            else:
                print("resize caused boundary error")
        else:
            print("invalid argument type!")

    #   translates the bounding box according to the supplied x/y tuple
    def move(self, translation):

        if isinstance(translation, tuple):
            #   generate test coords
            test_x = self.topL[0] + translation[0]  # x1
            test_y = self.topL[1] + translation[1]  # y1
            testTopL = (test_x, test_y)

            test_x = self.botR[0] + translation[0]  # x2
            test_y = self.botR[1] + translation[1]  # y2
            testBotR = (test_x, test_y)

            #   check bounds before reassignment
            if self.checkBounds(testTopL) and self.checkBounds(testBotR):
                self.setCoords(testTopL, testBotR)
            else:
                print("Invalid Move - bound Error!")
        else:
            print("invalid argument type!")

    #   returns false if provided coordinate is outside the boundaries of the screen area
    def checkBounds(self, testCoord):

        x_bound = self.MAX_X > testCoord[0] >= 0
        y_bound = self.MAX_Y > testCoord[1] >= 0

        return x_bound and y_bound

    #   returns true if the supplied x/y tuple lies inside the bounds of the topL and botR coords
    def checkInside(self, testPt):
        if isinstance(testPt, tuple):

            #   right X greater than center greater than left X
            check_X = self.botR[0] >= testPt[0] >= self.topL[0]

            #   top Y   greater than center greater than bottom Y
            check_Y = self.topL[1] >= testPt[1] >= self.botR[1]

            return check_X and check_Y

        else:
            print("invalid argument->must be tuple")
            return None

    #   prints the coord info to the console
    def printCoord(self):
        outStr = self.name + "\t: " + "TopL: " + str(self.topL) + "\t,\t" + "BotR: " + str(self.botR)
        print(outStr)

    #   get the coordObject as a dictionary -> used for serialization to json
    def getAsDict(self):
        tempDict = {}
        tempDict['name'] = self.name
        tempDict['botR'] = list(self.botR)
        tempDict['topL'] = list(self.topL)
        return tempDict
