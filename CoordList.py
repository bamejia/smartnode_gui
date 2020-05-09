import json
import os

import DEFAULTS as defaults
from CoordObj import *


#   custom collection of coordObjects
#   handles loading from file and dealing with collection-y stuff
#   Louis Stubbolo, with help from Teddy K, April 2020

class coordList():
    myList = []
    directory = ""
    filePath = ""

    #   constructor w/ optional fileName
    def __init__(self, fileName="coordFile.json"):
        #   gets the directory of the file
        directory = os.path.dirname(__file__)

        #   set path to json file-> append file name to directory
        self.filePath = os.path.join(directory, fileName)

        #   check if file doesn't exist
        missing = not (os.path.exists(self.filePath))
        #   if it exists check if empty -> if empty treat like doesn't exist
        if not missing:
            # print("coordFile not missing")
            missing = os.stat(self.filePath).st_size == 0
        #   create default file if missing (or empty)
        if missing:
            print("Generating 'coordFile.json' in CoordList constructor")
            tempObj = defaults.COORD_OBJ

            # use open() to create a file, add default obj to file, add autosaves
            with open(self.filePath, "w+") as myFile:
                # myFile.write(json.dumps(tempObj))
                self.addObject(coordObj(tempObj['name'], tuple(tempObj['topL']), tuple(tempObj['botR'])))

        #print("loading set from constructor")
        self.loadSet()

    #   override the default iterator
    def __iter__(self):
        return iter(self.myList)

    #   adds a coordObject to the collection
    #   if no object is passed, creates a new one and adds it
    def addObject(self, newObj=coordObj()):
        if isinstance(newObj, coordObj):
            self.myList.append(newObj)
            self.saveSet()
        else:
            print("object not added:")
            print("invalid argument -> must be coordObject")

    #   removes the specified coordObj from the list
    def removeObj(self, obj):
        #   flag to indicate successful removal
        objRemoved = False

        try:
            self.myList.remove(obj)
            objRemoved = True
            self.saveSet()

        #   catch the error
        except ValueError:
            objRemoved = False
            print("object not removed - argument must be member object")

        return objRemoved

    #   wipes all stored coordObjs from the list and adds a blank one
    def wipeList(self):
        self.addObject(coordObj())
        while len(self.myList) > 1:
            self.popFirst()

    #   returns object at index 0 and removes from list if there are at least 2 entries in the list
    def popFirst(self):
        entry = None

        if len(self.myList) >= 2:
            entry = self.myList[0]
            self.removeObj(entry)

        else:
            print("too few elements to pop")

        return entry

    #   returns object with highest index greater than 1 and removes it from the list
    def popLast(self):
        index = len(self.myList) - 1
        if index >= 1:
            entry = self.myList[index]
            self.removeObj(entry)
            return entry

        else:
            print("too few elements to pop")
            return False

    #

    #   attempts to return first entry in the list via specified value (index)
    def getObjIndex(self, index):
        if len(self.myList) > index > 0:
            return self.myList[index]
        else:
            print("no object found or index out of range")
            return None

    #   attempts to return first entry in the list via specified value (name)
    def getObjName(self, name):
        for entry in self.myList:
            if entry.name == name:
                return entry

        print("no object found")
        return None

    #   attempts to return first entry in the list via specified value (point)
    def getObjPoint(self, point):
        for entry in self.myList[1:]:
            if entry.checkInside(point):
                return entry
        else:
            print("no object found")
            return None

    #   return the last entry in the list
    def peekLast(self):
        index = len(self.myList) - 1
        if index >= 1:
            entry = self.myList[index]
            return entry

        else:
            print("CoordList is empty")
            return False

    #   loads a data set from file
    def loadSet(self):

        #   copy file contents to tempporary object
        with open(self.filePath, 'r') as myFile:
            temp_list = json.loads(myFile.read())

        #   wipe current set
        self.myList = []

        #   flag to indicate one dummy entry was added
        for entry in temp_list:
            tempObj = coordObj(entry['name'], tuple(entry['topL']), tuple(entry['botR']))
            self.myList.append(tempObj)

    #   saves myList object to file
    def saveSet(self):
        # print("saving set")

        #   temporary list of python dicts to be
        tempList = []

        #   iterate through all coordObject entries in myList
        for entry in self.myList:
            #   get each entry as a dict object
            tempList.append(entry.getAsDict())

        #   write the list of dicts to file as a json string w/ dumps
        with open(self.filePath, 'w+') as myFile:
            myFile.write(json.dumps(tempList))

    #   prints the contents of the set
    def printSet(self):
        for entry in self.myList:
            entry.printCoord()

    #   returns the number of objects in the set
    def getSize(self):
        return len(self.myList)

    #   These functions shadow the ones in the child class
    #   functions that modify entries trigger saveSet afterwords

    def rename(self, obj, name):
        if isinstance(obj, coordObj):
            obj.rename(name)
            self.saveSet()
        else:
            print("invalid type!")

    def setCoords(self, obj, newTopL, newBotR):
        if isinstance(obj, coordObj):
            obj.setCoords(newTopL, newBotR)
            self.saveSet()
        else:
            print("invalid type!")

    def move(self, obj, translation):
        if isinstance(obj, coordObj):
            obj.move(translation)
            self.saveSet()
        else:
            print("invalid type!")

    def resize(self, obj, increment):
        if isinstance(obj, coordObj):
            obj.resize(increment)
            self.saveSet()
        else:
            print("invalid type!")

    def checkBounds(self, obj, testCoord):
        if isinstance(obj, coordObj):
            return obj.checkBounds(testCoord)
        else:
            print("invalid type!")
