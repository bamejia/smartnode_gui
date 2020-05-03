from FireBase_Functions import checkCommands
from Utility_Functions import checkTime
import time

#   Functions that allow looping functions to check if
#   These responses can originate from Firebse or the GUI

#   check firebase for recent commands
def checkFirebase():
    print("\tin PiResponses.checkFirebase")
    print("\t\tChecking Firebase for commands")

    #   get response from Firebase
    fbResponse = checkCommands()

    return fbResponse


#   this is the function that interacts with the outside functions
def respond(action_arg = "nope", obj_arg = "nope", external_Flag = False):
    print("\nin PiResponses.interface")

    #   Action is the thing that has to happen, object is the thing it has to happen to

    #   check if this function was called externally
    #   ->  most calls will be done internally, checking for kill signals from Firebase or
    #   ->  external flag comes from user input on the Pi

    #   if this function was called internally to check for firebase commands
    if external_Flag == False:
        (action, obj) = checkFirebase()

    #  Flag should only be true if set by user input
    else:
        (action, obj) = (action_arg, obj_arg)


    #   list comprehension for handling firebase input
    actions = {"nope": noResp, "Stop": stopRun, "Start_Run": startRun, "Run_Once": runOnce}

    #   call the action function with the object to perform the action
    status = actions[action](obj)

    print(f"\tResponse was")
    return status


def noResp(obj):
    print(f"\tNo action needed for '{obj}'")

    if obj == "OCR":
        print("OBJ = OCR")

    return "nope"


def stopRun(obj):
    print(f"\nstopping run for {obj}...")
    time.sleep(.5)
    print(f"\tStand-in for handling termination for {obj}")
    return "Stopped"


def startRun(obj):
    print(f"\nstarting run for {obj}")
    time.sleep(.5)
    print(f"\tStand-in for handling Starting for {obj}")
    return "Stopped"


def runOnce(obj):
    print(f"\nrunning once for {obj}")
    time.sleep(.5)
    print(f"\tStand-in for handling Starting for {obj}")
    return "Ran_Once"


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