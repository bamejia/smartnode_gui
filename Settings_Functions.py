from DEFAULTS import *
from Utility_Functions import *

#   This set of function handles saving / loading settings

#   checks loop ending conditions common to both kinds of loop
def check_LoopMode(mySet):
    if mySet['loopMode'] == 'infinite':
        return False

    if mySet['loopMode'] == 'single':
        return True

    #   returns true if enough time has passed
    if mySet['loopMode'] == 'timed':
        return checkTime(mySet['loopEnd'])

    else:
        return False


#   changes setting in object, saves it to file, returns the modified version
def changeSetting(obj, key, value, subvalue=''):
    #   if modifying a dict behave differently if a 4th value is provided
    if len(subvalue) > 0 and isinstance(obj[key], dict):
        obj[key][value] = subvalue
    else:
        obj[key] = str(value)

    #   every settings object has an attribute called self
    #   which is the local path to where it is saved
    path = getFullPath(obj['self'])

    #   save to file
    with open(path, 'w') as myFile:
        myFile.write(json.dumps(obj))

    return obj


#   returns a settings object from a filename
def loadSettings(fileName):
    filePath = getFullPath(fileName)

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
        defSetting = LIST_ALL[name]
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
    path = getFullPath(obj['self'])
    tempObj = genSettings(obj['self'], path, False)
    obj[key] = tempObj[key]

    with open(path, 'w') as myFile:
        myFile.write(json.dumps(obj))

    return obj

#   sets the end time attribute of the provided settings object
#   based upon the provided offset(hours)
#   returns the modified settings object
def setEndtime(obj, offset):
    endObj = datetime.now().replace(microsecond=0) + timedelta(hours=offset)
    endStr = getTimeStr(endObj)

    return changeSetting(obj, 'loopEnd', endStr)
