#   This file contains all the functional code for interacting with firebase
from Settings_Functions import *

#   establishes firebase connection
def setupFirebase():
    print(f"Setup for Firebase....")

    #load settings
    fireBaseSettings = loadSettings('firebaseSettings.json')
    print(f"\tFirebase Settings Loaded")

    #connect to server
    print(f"\tConnection Code Not Yet Implemented")

    #   set flag depending on whether connection was successful
    print(f"\tManually Setting Flag to True")

    changeSetting(fireBaseSettings, 'connected', 'True')
    print("Done FB Setup\n")


#   checks if there has been a recent command posted to firebaseSettings json
def checkCommands():
    print("Checking for Firebase Commands")
    print(f"\t**THIS FUNCTION NOT YET IMPLEMENTED")
    fireBaseSettings = loadSettings('firebaseSettings.json')
    message = fireBaseSettings['msg_from_fb']
    return message

#   post provided message to the provided url on firebase
def postFirebase(dest_url, message):
    #   check if firebase is connected
    fireBaseSettings = loadSettings('firebaseSettings.json')
    connected = fireBaseSettings['connected'] == 'True'

    if(connected):
        print(f"\tPosting message: {message} to {dest_url}")
        print(f"\t**THIS FUNCTION NOT YET IMPLEMENTED")

    else:
        print("Firebase is not connected!")