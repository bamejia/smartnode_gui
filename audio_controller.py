# from PiResponses import respond, check_LoopMode
from FireBase_Functions import postFirebase
import audio_functions as audio
import finger_functions as finger
import Settings_Functions as settings
from datetime import datetime
import pytz

#   record new sample
def getData(samplePath):
    print("\tRecording Sample")
    audio.recordAudio(samplePath)


#   called during loop
#   get fundamental from sample, compare with reference, return result
def processData(samplePath, reference):
    print("\tgetting Fundamental from sample")
    newFund = float(audio.getFund(samplePath))
    reference = float(reference)

    # print("\tcomparing with reference fundamental")
    detected = audio.compareFreqs(newFund, reference)

    print(f"\tDone Comparison -> reference detected: {detected}")
    print()
    return detected


#   checks internal end conditions for the sampling loop
def getEndConditions(mySet):
    print("Checking OCR End Conditions")

    #   loop mode -> run once or run for time

    #   checks for loop end due to loopMode mySet (in Utility Functions)
    if settings.check_LoopMode(mySet):
        print("\tLoop Ended Due to Internal Trigger")
        print()
        return True

    print("\tLoop Continuing")
    return False


#   checks that main mySet[Audio_Setup] flag is true
def init_Audio():
    print("In init_Audio: Checking Audio Initialization")

    mainSet = settings.loadSettings('mainSettings.json')
    flag = mainSet['Audio_Setup']
    print(f"Main Settings Audio Setup Flag: {flag}")

    #   flag must be evaluated as string!
    return flag == "True"


#   single sampling run ->
#   mySet = Audio settings, loaded in start
def loop(mySet, db):
    print("In Loop Once...")
    print(mySet['smplPath'], mySet['reference'])
    detected = processData(mySet['smplPath'], mySet['reference'])

    if detected:

        This will break the code


        # if mySet['loopMode'] == 'press':
        #     finger.finger_looper(self.after, self.set_finger_press, delay, repeats, interval)
        #
        tz_NY = pytz.timezone('America/New_York')
        time_detected = datetime.now(tz_NY).strftime('%Y_%m_%d__%H_%M_%S__%f')[:-3]

        print("Running Updates")
        # updates JSON file with the date of when the sample match was found
        mySet = settings.changeSetting(mySet, 'detected', time_detected)

        # posts same data to Firebase
        fb_message = {'audio_detected': time_detected}
        postFirebase(mySet['fb_data_url'], fb_message, db)

        detected = time_detected

    endLoop = getEndConditions(mySet)
    print(f"Loop ended = {endLoop} -> Returning: {not endLoop}")

    print("\n>-------Loop COMPLETE-------<\n")

    return (not endLoop), detected
