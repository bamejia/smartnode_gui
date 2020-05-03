import subprocess
import os
from datetime import datetime, timedelta
import json
import sys


#   returns the absolute path to the local path provided
def getFullPath(fileName):
    #   gets the directory of the file
    directory = os.path.dirname(__file__)

    #   set path to json file-> append file name to directory
    filePath = os.path.join(directory, fileName)

    return filePath

#   This is the least secure code I think i have ever written
#   attempts to run the bash script based on the name provided
#   args are optional, but
def runBashScript(scriptName, args=()):
    directory = os.path.dirname(__file__)
    filePath = os.path.join(directory, scriptName)
    try:
        subprocess.call([filePath, args])
    except PermissionError:
        print(f"'{scriptName}' has not been set to executable!")
        print(f"while in this directory run sudo chmod +x {scriptName}")


#   removes all files in root directory of the specified type(if allowable)
def wipeAll(fileType):
    allowable = ('.wav', '.json', '.png', '.jpg')

    #   you must never delete the kittens
    forbidden = (os.path.join(os.path.dirname(__file__), 'kittens.jpg'))

    #   check if you are allowed to remove this type of file
    #   break if input is empty
    if not (fileType):
        return

    if fileType.find('.') < 0:
        fileType = '.' + fileType
        print(f"inserting '.', type is now {fileType}")

    if not allowable.__contains__(fileType):
        print(f"You can't remove '{fileType}' files")

    else:

        #   makes a list of all files in the root directory
        directory = os.path.dirname(__file__)
        allFiles = os.listdir(directory)

        #   extract all files ending with the provided filetype
        allType = [f for f in allFiles if f.endswith(fileType)]

        for file in allType:
            path_to_file = os.path.join(directory, file)

            #   remove file if not in list of forbidden files
            if forbidden.find(path_to_file) < 0:
                os.remove(path_to_file)

        print(f"\tAll {fileType} files Removed")
        print()


#   attempts to remove a specific file if it exists and is of an allowable filetype
def wipeOne(fileName):
    allowable = ('.wav', '.json', '.png', '.jpg')
    forbidden = (os.path.join(os.path.dirname(__file__), 'kittens.jpg'))

    print(forbidden)

    #   check if file is of an allowable type, exit if invalid
    valid = False
    for allowed in allowable:
        if fileName.find(allowed) > -1:
            valid = True
            break

    if not valid:
        print(f"{fileName} has invalid file type")
        return

    #   check if file exists
    else:
        #   get ablsolute path to file
        directory = os.path.dirname(__file__)
        fullPath = os.path.join(directory, fileName)

        #   check if removal of this file is explicitly forbidden
        if forbidden.find(fullPath) > -1:
            print("you aren't allowed to delete the kittens picture... jerk")
            return

        #   exit if file not found
        if not os.path.exists(fullPath):
            print("File not found!")
            return

        #   remove the file if it is found
        else:
            os.remove(fullPath)
            print("File Removed")


#   datetime stuff

#   gets a json string from a datetime object
def getTimeStr(timeObj):
    timeStr = json.dumps(timeObj, default=datetime.__str__)
    return timeStr


#   gets a json formatted time string, returns if current time is greater
def checkTime(input):
    endTime = datetime.strptime(json.loads(input), '%Y-%m-%d %H:%M:%S')
    current = datetime.now().replace(microsecond=0)
    return current > endTime