# def louis_function(command):
#     print(command)
#     if command == 'OCR_ON_OFF':
#         turn_light_on()
#
# all_commands = {
#     '12:24': {
#         'command' : 'LIGHT_ON',
#         'time' : '12:24'
#     },
#     '12:25': {
#         'command' : 'LIGHT_OFF',
#         'time' : '12:25'
#     }
# }
#
# for c in all_commands:
#     louis_function(all_commands[c]['command'])
#
#
# recent_commands = {"recent_commands" : ""}

#  firebase.post("\", recent_commands)


def new_function():
    print("hello")

a = new_function

b = lambda: (print("hi"), print("YES"))


a()
b()