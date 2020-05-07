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

    #   files that can't be deleted
    ignore = defaults.FORBIDDEN
    for file in ignore:
        ignore[file] = getFullPath(file)

    #   check if you are allowed to remove this type of file
    #   break if input is empty
    if not (fileType):
        return

    #   see if inserting a '.' fixes the issue
    if fileType.find('.') < 0:
        fileType = '.' + fileType

    #   check if it is an allowed file type
    if not allowable.__contains__(fileType):
        print(f"You can't remove '{fileType}' files")

    #   proceed if file type is allowed
    else:

        #   makes a list of all files in the root directory
        directory = os.path.dirname(__file__)
        allFiles = os.listdir(directory)

        #   extract all files ending with the provided filetype
        allType = [f for f in allFiles if f.endswith(fileType)]

        for file in allType:
            path_to_file = os.path.join(directory, file)

            #   remove file if not in list of forbidden files
            if ignore.find(path_to_file) < 0:
                os.remove(path_to_file)

        print(f"\tAll {fileType} files Removed")
        print()


#   attempts to remove a specific file if it exists and is of an allowable filetype
def wipeOne(fileName):
    allowable = ('.wav', '.json', '.png', '.jpg')

    #   files that can't be deleted
    ignore = []
    for file in defaults.FORBIDDEN:
        ignore.append(getFullPath(file))

    print(ignore)

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
        if ignore.__contains__(fullPath):
            print(f"You aren't allowed to delete '{fileName}'")
            return

        #   exit if file not found
        if not os.path.exists(fullPath):

            print(f"{fileName} not found!\nPath: {fullPath}")
            return

        #   remove the file if it is found
        else:
            os.remove(fullPath)
            print(f"'{fileName}' was removed")


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