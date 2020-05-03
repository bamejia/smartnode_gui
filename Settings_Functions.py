from DEFAULTS import *
from Utility_Functions import *
from  time import sleep
#   This set of function handles saving / loading settings




#   changes setting in object, saves it to file, returns the modified version
def changeSetting(obj, key, value):
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


    #   load
    else:
        #print(f"Settings File '{fileName}' Located and Non-Empty")
        with open(filePath, 'r') as myFile:
            settingsObj = json.load(myFile)

        #print("\tFile Loaded Successfully")
       # print()

    '''
    print("settings object in load settings function:")
    for i in settingsObj:
        print(f"\t{i}: {settingsObj[i]}")
    print()
    '''

    return settingsObj


#   generates settings file automatically from data in DEFAULTS
#   saves file and returns object
def genSettings(name, path):
    print(f"Generating Default Settings File: {name}")

    defSetting = {}

    #   gets default object saved in DEFAULTS
    try:
        defSetting = LIST_ALL[name]
    except(NameError, KeyError) as error:
        print(f"No settings default for {name}...")
        exit('Terminating in genSettings: cannot find default object')

        #   write object to file
    with open(path, 'w') as myFile:
        myFile.write(json.dumps(defSetting))

    return defSetting


#   sets the end time attribute of the provided settings object
#   based upon the provided offset(hours)
#   returns the modified settings object
def setEndtime(obj, offset):
    endObj = datetime.now().replace(microsecond=0) + timedelta(hours=offset)
    endStr = getTimeStr(endObj)

    return changeSetting(obj, 'loopEnd', endStr)