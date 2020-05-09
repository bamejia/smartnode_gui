import pyrebase
from time import sleep
import sys

my_stream = None
command_list = ""
firebase_commands_func = None

config = {
    "apiKey": "AIzaSyApYhula2ltA-5CeHm4l333G9z1Pjz7sOM",
    "authDomain": "smartnode-ed0a9.firebaseapp.com",
    "databaseURL": "https://smartnode-ed0a9.firebaseio.com/",
    "storageBucket": "smartnode-ed0a9.appspot.com",
    "serviceAccount": "C:/Users/bamxm/PycharmProjects/piGUI/py/smartnode_key.json"
    # /home/pi/smartkey.json
}

try:
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
except Exception as e:
    print(e)

def stream_handler(message):
    global command_list
    global firebase_commands_func

    # print("MESSAGE IS: " + str(message))
    if message['path'] != "/":
        command_list[message['path'][1:]] = message['data']
    else:
        command_list = message['data']
        if command_list == "":
            return

    for command in command_list:
        firebase_commands_func(command_list[command]['command'])
        # print("Command: " + command_list[command]['command'])

    recent_commands = {"recent_commands" : ""}
    db.update(recent_commands)


def run(firebase_func):
    global command_list
    global firebase_commands_func
    global my_stream

    try:
        firebase_commands_func = firebase_func
        command_list = db.child("recent_commands").get().val()
        my_stream = db.child("recent_commands").stream(stream_handler)
    except Exception as e:
        print(e)
        print("DID NOT CONNECT TO FIREBASE")
        sys.exit()


def close():
    global my_stream
    try:
        my_stream.close()
    except Exception as e:
        print(e)