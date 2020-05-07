#   This is the main controller file. This is a temporary stand-in for what will be in the GUI

import Audio_Controller
import OCR_Controller
from Audio_Functions import playReference, recordAudio
from OCR_Functions import takeSource, showImage
from guiTest import *

from Settings_Functions import *


def Settings():
    print(f"\nSETTINGS ->\tThis function has access to settings json files")

    # launch settings screen

    print("In Controller from Settings, going back to Main Menu")

def OCR():
    print("\nYou entered OCR!")
    OCR_Controller.start()
    print("In Controller from OCR, going back to Main Menu")

def Audio():
    print("\nYou entered Audio!")
    Audio_Controller.start()
    print("In Controller from Audio, going back to Main Menu")


#   exits the program -> erase main settings file
def EXIT():

    '''print(f"removing mainSettings File")
    path = getFullPath('mainSettings.json')
    os.remove(path)
    print(f"\tmainSettings.json deleted")
    '''

    print("Done Exit Process\nHave A Nice Day!")
    exit('\nExiting Program...')


#   lets the user wipe all files of a specific type
def WIPE():
    print('You entered Wipe!)')
    print('-> Enter file extension, 1 for a specific file, or nothing to cancel')
    print('-> Please note, in pyCharm the list @ left is only updated after termination')
    wipeInput = input('\nEnter(1, json, wav, jpg, png): ')


    if wipeInput == '1':
        oneInput = input('Please Enter [name].[ext]: ')
        wipeOne(oneInput)

    else:
        wipeAll(wipeInput)

#   launches test GUI
def launchTestGUI():
    print("Launching Smartnode GUI")
    app = SmartnodeGUI()
    app.mainloop()
    print("GUI has closed")



#   init function for the entire project
#   This function will automatically terminate with error
#   if the settings file read/write system isn't working
def init_Main():
    #   load main settings file
    mainSet = loadSettings('mainSettings.json')

    #   overwrite error flag in mainSettings
    print("Writing Main Settings Error Flag to False")
    changeSetting(mainSet, 'error', 'False')
    mainSet = loadSettings('mainSettings.json')

    print(f"\tSettings Load Error: {mainSet['error']}")
    print()

    #   check that flag was overwritten successfully
    if not mainSet['error'] == 'False':
        print("Failed to Load / Generate Main Settings")
        exit("Main Settings Failure")


# main
if __name__ == "__main__":

    #   make sure settings system is working, exit if there are issues
    init_Main()

    menus = ['Settings', 'OCR', 'Audio', 'EXIT', 'WIPE', 'Rec Ref', 'Play Ref', 'Take Pic', 'Display Pic', 'Test GUI']

    options = {1: Settings, 2: OCR, 3: Audio, 4: EXIT, 5: WIPE, 6: recordAudio, 7: playReference, 8: takeSource,
               9: showImage, 10: launchTestGUI}

    userInput = -1


    while userInput != 4:

        print("MAIN MENU")
        for str in menus:
            print(f"{menus.index(str)+1}) {str}")

        userInput = input(f"\nEnter 1-{len(options)}: ")
        print("")
        try:
            options[int(userInput)]()
        except ValueError:
            pass

        print("\nBack in Main Menu")