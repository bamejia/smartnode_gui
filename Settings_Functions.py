import datetime
import json
import os
import finger_functions as finger
import DEFAULTS as defaults
import Utility_Functions as util
from CoordList import coordList


#   This set of function handles saving / loading settings

#   checks loop ending conditions common to both kinds of loop
def check_LoopMode(mySet):
    if mySet['loopMode'] == 'infinite':
        return False

    if mySet['loopMode'] == 'single':
        return True

    #   returns true if enough time has passed
    if mySet['loopMode'] == 'timed':
        return util.checkTime(mySet['loopEnd'])

    if mySet['loopMode'] == 'press once':
        if loadSettings("audioSettings.json")["detected"] != "Not Detected":
            delay, num_presses, interval = 300, 1, 300
            finger.finger_looper(delay, num_presses, interval)
            return True

    if mySet['loopMode'] == 'press inf':
        if loadSettings("audioSettings.json")["detected"] != "Not Detected":
            delay, num_presses, interval = 300, 1, 300
            finger.finger_looper(delay, num_presses, interval)


    else:
        return False


#   changes setting in object, saves it to file, returns the modified version
def changeSetting(obj, key, value):

    #   every settings object has an attribute called self
    #   which is the local path to where it is saved
    path = util.getFullPath(obj['self'])
    obj[key] = value

    #   save to file
    with open(path, 'w') as myFile:
        myFile.write(json.dumps(obj))

    return obj


#   returns a settings object from a filename
def loadSettings(fileName):
    filePath = util.getFullPath(fileName)

    #   check if file is missing and / or empty
    missing = not os.path.exists(filePath)
    if missing:
        empty = False
    else:
        empty = os.path.getsize(filePath) == 0

    #   if missing or empty generate and save default file
    if (missing or empty):
        print(f"Error Loading {fileName}\n\tMissing: {missing}\t\tEmpty: {empty}")
        print()

        settingsObj = genSettings(fileName, filePath)

        print("\tFile Created Successfully")
        print()

    else:
        with open(filePath, 'r') as myFile:
            settingsObj = json.load(myFile)

    return settingsObj


#   generates settings file automatically from data in DEFAULTS
#   saves file and returns object
def genSettings(name, path, save=True):
    print(f"Generating Default Settings File: {name}")

    defSetting = {}

    #   gets default object saved in DEFAULTS
    try:
        defSetting = defaults.LIST_ALL[name]
    except(NameError, KeyError) as error:
        print(f"No settings default for {name}...")
        exit('Terminating in genSettings: cannot find default object')

    #   write object to file
    if (save):
        with open(path, 'w') as myFile:
            myFile.write(json.dumps(defSetting))

    return defSetting

#   resets the key in object to its default value
def resetDefault(obj, key):
    name = obj['self']
    path = util.getFullPath(name)

    print(f"resetting default for {name} at path {path}")
    tempObj = genSettings(name, path, False)
    obj[key] = tempObj[key]

    with open(path, 'w') as myFile:
        myFile.write(json.dumps(obj))

    return obj


#   loads every settings file -> we should run this in the main gui controller to kill off some bugs
def loadAllSettings():
    #   load the standard settings.json
    allSettings = defaults.LIST_ALL
    for setting in allSettings:
        loadSettings(setting)

    coordList()


#   wipes deletes all settings files, saved pictures and audio clips; reloads all settings
def fullReset():
    print("\n\n----------------Wiping Files & Settings----------------\n")

    #   delete all json, jpg, and wav files(except forbidden)
    util.wipeAll('.json', True)
    util.wipeAll('.jpg', True)
    util.wipeAll('.wav', True)

    #   load all settings
    loadAllSettings()

    print("\n----------------Done Loading Settings----------------\n\n")

#   sets the end time attribute of the provided settings object
#   based upon the provided offset(hours)
#   returns the modified settings object
def setEndtime(obj, offset):
    endObj = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=offset)
    endStr = util.getTimeStr(endObj)

    return changeSetting(obj, 'loopEnd', endStr)
