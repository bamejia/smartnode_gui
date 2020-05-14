import json
import os
import subprocess
from datetime import datetime

import DEFAULTS as defaults


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
def runBashScript(scriptName, args=""):
    directory = os.path.dirname(__file__)
    filePath = os.path.join(directory, scriptName)
    try:        subprocess.call([filePath, args])

    except PermissionError:
        print(f"'{scriptName}' has not been set to executable!")
        print(f"while in this directory run sudo chmod +x {scriptName}")


#   removes all files in root directory of the specified type(if allowable)
def wipeAll(fileType, debug=False):
    print(f"Attempting to wipe all files of type '{fileType}'")
    allowable = ('.wav', '.json', '.png', '.jpg')

    #   files that can't be deleted
    ignore = []
    for file in defaults.FORBIDDEN:
        ignore.append(getFullPath(file))

    #   make sure filetype was provided, entered correctly and allowable
    if not (fileType):
        return
    if fileType.find('.') < 0:
        fileType = '.' + fileType
    if not allowable.__contains__(fileType):
        if debug: print(f"You can't remove '{fileType}' files")


    #   proceed if file type is allowed
    else:
        #   makes a list of all files in the root directory
        directory = os.path.dirname(__file__)
        allFiles = os.listdir(directory)

        #   extract all files ending with the provided filetype
        allType = [f for f in allFiles if f.endswith(fileType)]

        for file in allType:
            #   get full path to current file
            fullPath = os.path.join(directory, file)

            #   double check that file is ok to delete
            if ignore.__contains__(fullPath):
                if debug: print(f"\tskipped: {file}")

            else:
                if debug: print(f"\tremoving: '{file}'")
                os.remove(fullPath)

        if debug: print(f"All '{fileType}' Files Removed\n")


#   attempts to remove a specific file if it exists and is of an allowable filetype
def wipeOne(fileName, debug=False):
    allowable = ('.wav', '.json', '.png', '.jpg')

    #   files that can't be deleted
    ignore = []
    for file in defaults.FORBIDDEN:
        ignore.append(getFullPath(file))

    #   check if file is of an allowable type, exit if invalid
    valid = False
    for allowed in allowable:
        if fileName.find(allowed) > -1:
            valid = True
            break

    if not valid:
        if debug: print(f"{fileName} has invalid file type")
        return

    #   check if file exists
    else:
        #   get absolute path to file
        directory = os.path.dirname(__file__)
        fullPath = os.path.join(directory, fileName)

        #   check if removal of this file is explicitly forbidden
        if ignore.__contains__(fullPath):
            if debug: print(f"You aren't allowed to delete '{fileName}'")
            return

        #   exit if file not found
        if not os.path.exists(fullPath):

            if debug: print(f"{fileName} not found!\nPath: {fullPath}")
            return

        #   remove the file if it is found
        else:
            os.remove(fullPath)
            if debug: print(f"'{fileName}' was removed")


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

def reformatTime(input_time):
    if input_time == 'Not Detected':
        return input_time
    else:
        date = datetime.strptime(input_time, "%Y_%m_%d__%H_%M_%S__%f").strftime('%m-%d-%Y %H:%M:%S')
        return date
