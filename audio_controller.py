# from PiResponses import respond, check_LoopMode
from FireBase_Functions import postFirebase
from audio_functions import *


#   record new sample
def getData(samplePath):
    print("\tRecording Sample")
    recordAudio(samplePath)


#   called during loop
#   get fundamental from sample, compare with reference, return result
def processData(samplePath, reference):
    print("\tgetting Fundamental from sample")
    newFund = float(getFund(samplePath))
    reference = float(reference)

    #print("\tcomparing with reference fundamental")
    detected = compareFreqs(newFund, reference)

    print(f"\tDone Comparison -> reference detected: {detected}")
    print()
    return detected


#   called during loop - > updates local values
#   any function calls that need to happen depending loop data should happen here
def updateLocal(mySet, detected):
    #   update local values if audio signal was detected
    if (detected):
        print("Updating Local Stuff")
        print(f"\tSetting Audio Setting 'detected' to {detected}")
        mySet = changeSetting(mySet, 'detected', detected)

        print("\t**NOT IMPLEMENTED-> UPDATE SCREEN")
        print()
    else:
        print(f"\tLocal Update Skipped Because detected: {detected}")

    return mySet


#   called during loop -> Push results to Firebase
def updateServer(fb_url, detected):
    print(f"Updating Server-> Not Yet Implemented")
    if (detected):
        fb_message = {'audioDetected': detected}

        postFirebase(fb_url, fb_message)

        print("\tFirebase Update Complete")
        print()

    else:
        print(f"\tFirebase Update Skipped Because detected: {detected}")

#   checks internal end conditions for the sampling loop
def getEndConditions(mySet):
    print("Checking OCR End Conditions")

    #   loop mode -> run once or run for time



    #   checks for loop end due to loopMode mySet (in Utility Functions)
    if check_LoopMode(mySet):
        print("\tLoop Ended Due to Internal Trigger")
        print()
        return True

    print("\tLoop Continuing")
    return False

#   checks that main mySet[Audio_Setup] flag is true
def init_Audio():
    print("In init_Audio: Checking Audio Initialization")

    mainSet = loadSettings('mainSettings.json')
    flag = mainSet['Audio_Setup']
    print(f"Main Settings Audio Setup Flag: {flag}")

    #   flag must be evaluated as string!
    return flag == "True"


#   sub controller function -> runs everything needed for Audio runs
def start():
    print("Audio Start function")

    #   THis just checks main menu flags for whether the record REF funcion has been called
    setupSuccess = init_Audio()

    #   take this auto call out -> switch to sample setup

    if not setupSuccess:
        print("\tAudio Not Set Up! -> Running recordRef\n")

        #   map this function to the record button
        recordRef()
        print("\tdone\n")


    #   copy this
    print("Loading Audio Settings")
    mySet = loadSettings('audioSettings.json')

    print(f"Setup Complete -> Loop Mode: {mySet['loopMode']}")

    endFlag = False
    while not endFlag:
        print("\n--------Loop Starting--------\n")


        #   run function that checks if loop should
        endFlag = getEndConditions(mySet)

        #   runs exatly one loop
        loopOnce(mySet)

    #   loop has terminated
    print("\n\nSample Loop Completed!")


#   single sampling run ->
#   mySet = Audio settings, loaded in start
def loopOnce(mySet):
    print("In Loop Once...")
    getData(mySet['smplPath'])
    detected = processData(mySet['smplPath'], mySet['reference'])

    print("Running Updates")
    updateLocal(mySet, detected)
    updateServer(mySet['fb_url'], detected)
    print("\n>-------Loop COMPLETE-------<\n")


#   loads settings and prints a statement
def pre_loop():
    print("Loading Audio Settings")
    mySet = loadSettings('audioSettings.json')
    print(f"Setup Complete -> Loop Mode: {mySet['loopMode']}")
    return mySet


#   loops once, returns inverted flag from getEndConditions
def loop(mySet):
    loopOnce(mySet)
    endLoop = getEndConditions(mySet)
    print(f"Loop ended = {endLoop} -> Returning: {not endLoop}")
    return not endLoop


#   calls record ref function
def record():
    print("RECORDING REFERENCE")
    recordRef()
    print("\tdone\n")