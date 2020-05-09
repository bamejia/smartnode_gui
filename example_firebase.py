
import pyrebase
from time import sleep

my_stream = None
command_list = ""
firebase_commands_func = None

config = {
  "apiKey": "AIzaSyApYhula2ltA-5CeHm4l333G9z1Pjz7sOM",
  "authDomain": "smartnode-ed0a9.firebaseapp.com",
  "databaseURL": "https://smartnode-ed0a9.firebaseio.com/",
  "storageBucket": "smartnode-ed0a9.appspot.com",
  "serviceAccount": "C:/Users/bamxm/PycharmProjects/piGUI/py/smartnode_key.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def printcontents(message):
  print("\n\n--------NEw MESSAGE--------")
  data = message['data']
  target = list(data.keys()).pop()
  command = data[target]

  print(f"target: {target}, command: {command}")
  print("--------END MESSAGE--------\n\n\n")

def handleCommands(target, command):
  print(f"I am handling the command {command} for target {target}\n")
  global superFlag
  if target == 'FINGER' and command == 'DEMO_FINGER':
    superFlag = True
  else:
    pass

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
    # print("DB: " + str(command_list))

    for command in command_list:
        firebase_commands_func(command_list[command]['command'])
        print("Command: " + command_list[command]['command'])


    recent_commands = {"recent_commands" : ""}
    db.update(recent_commands)


#   # extracting key / value pair from firebase message
#   data = message['data']
#   target = list(data.keys()).pop()
#   command = data[target]

#   # if message is NOT blank
#   if command:
#     db.child("command").update({target: ""})

#     # call the smart fucntion that knows how to do... stuff?
#     handleCommands(target, command)

#   # if handler is called due to updating itself (w/ blank command)-> ignore
#   else:
#     pass

def run(firebase_func):
    global command_list
    global firebase_commands_func
    global my_stream

    firebase_commands_func = firebase_func
    print(type(firebase_commands_func))

    command_list = db.child("recent_commands").get().val()
    # # print(command_list)
    #
    my_stream = db.child("recent_commands").stream(stream_handler)

def close():
    global my_stream
    my_stream.close()