import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import global_variables as gv
import test
import image_capture
import ocr_gui, audio_gui, finger_gui

# from firebase import firebase
# from firecreds import connect_to_firebase
# import os
# import json
# from firebase_admin import db
#
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db



UPDATE_RATE = 1000


class SmartnodeGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window_width = round(gv.WINDOW_W / 1)
        window_length = round(gv.WINDOW_L / 1)
        window_x = round(gv.WINDOW_W * 3 / 5)
        window_y = round(gv.WINDOW_L * 2 / 5)
        geometry_dimensions = "%dx%d+%d+%d" % (window_width, window_length, window_x, window_y)

        self.geometry(geometry_dimensions)

        self.attributes('-fullscreen', True)  #800x480
        # self.attributes('-zoomed', True)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame_classes = (
            MainMenu,
            Settings,
            ocr_gui.OCRRuntime,
            ocr_gui.OCRSettings,
            ocr_gui.CropSetup,
            ocr_gui.CropSetup2,
            ocr_gui.OCRModeSetup,
            ocr_gui.OCRStatus,
            audio_gui.AudioRuntime,
            audio_gui.AudioSettings,
            audio_gui.AudioStatus,
            audio_gui.AudioModeSetup,
            audio_gui.SampleSetup,
            finger_gui.FingerSettings
        )

        for F in frame_classes:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.return_frame = "MainMenu"  #  for returning to previous frame from frames that are accessed from multiple other frames
        self.current_frame = "fidja"
        self.whitelisted_frames = {   #  frames in which firebase can start a loop
            "MainMenu",
            "Settings",
            "OCRRUntime",
            "OCRStatus"
            "AudioRuntime",
            "AudioStatus"
        }
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def set_return_frame(self, page_name):
        self.return_frame = page_name

    # def connect_to_firebase():
    #
    #     print("Initializing Firebase Connection...")
    #     # Fetch the service account key JSON file contents
    #
    #     FILES_DIR = 'smartnode_key.json'
    #
    #     cred = credentials.Certificate(FILES_DIR)
    #
    #     print("Credentials Found. ")
    #
    #     # Initialize the app with a service account, granting admin privileges
    #     response = firebase_admin.initialize_app(cred, {'databaseURL': 'https://smartnode-ed0a9.firebaseio.com/%27%7D)'})
    #
    # def firebase_setup(self):
    #
    #     connect_to_firebase()
    #
    #     recent_commands = {"recent_commands": ""}
    #
    #     recent_command = {
    #         '12:24': {
    #             'command': 'Light_ON',
    #             'time': '12:24'
    #         },
    #
    #         '12:25': {
    #             'command': 'Light_OFF',
    #             'time': '12:25'
    #         }
    #     }
    #
    #     def show(command):
    #         print(command)
    #
    #     # points to the parent node in firebase directory
    #     command = db.reference('/recent_commands')
    #
    #     # The Dictionary get() method returns the value of the item with the specified key.
    #     commands = command.get()
    #
    #     print(commands)
    #
    #     for c in commands:
    #         show(commands[c]['command'])
    #
    #     # erase commands
    #     # result = db.reference('/').update(recent_commands)
    #
    # # from pi_configs import FILES_DIR  # root directory of project
    #
    # def firebase_updater(self):
    #     pass
    #
    # def firebase_commands(self, command):
    #     if command == "OCR_ON_OFF":
    #
    #             self.frames["OCRRuntime"].ocr_on_off()
    #     elif command == "AUDIO_ON_OFF":
    #         pass
    #     elif command == "FINGER_PRESS":
    #         pass


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Menu", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        ocr_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                controller.set_return_frame("MainMenu"),
                                controller.show_frame("OCRRuntime"))
        audio_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                  controller.set_return_frame("MainMenu"),
                                  controller.show_frame("AudioRuntime"))
        settings_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                controller.show_frame("Settings"))
        quit_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                controller.destroy())

        self.start_stop_ocr_btn = tk.Button(self, text="OCR",
                                 command=ocr_btn_func, height=1, width=10)
        start_stop_audio_btn = tk.Button(self, height=2, width=10, text="Audio",
                                       command=audio_btn_func)
        settings_btn = tk.Button(self, text="Settings",
                            command=settings_btn_func)
        quit_btn = tk.Button(self, text="Quit",
                            command=quit_btn_func)

        self.start_stop_ocr_btn.pack()
        start_stop_audio_btn.pack()
        settings_btn.pack()
        quit_btn.pack()

        self.count = 0
        self.will_update = True
        self.updater()

    def update_button1(self):
        if self.will_update:
            self.start_stop_ocr_btn["text"] = str(self.count)
            self.count += 1

    def updater(self):
        self.update_button1()
        self.after(UPDATE_RATE, self.updater)


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        ocr_settings_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                controller.show_frame("OCRSettings"))
        audio_settings_func = lambda: (test.louis_replace_this_with_your_function_name(),
                             controller.show_frame("AudioSettings"))
        finger_settings_func = lambda: (test.louis_replace_this_with_your_function_name(),
                             controller.show_frame("FingerSettings"))
        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                             controller.show_frame("MainMenu"))

        ocr_settings_btn = tk.Button(self, text="OCR Settings",
                            command=ocr_settings_func)
        audio_settings_btn = tk.Button(self, text="Audio Settings",
                            command=audio_settings_func)
        finger_settings_btn = tk.Button(self, text="Finger Settings",
                            command=finger_settings_func)
        back_button_btn = tk.Button(self, text="Go back",
                                command=back_btn_func)

        ocr_settings_btn.pack()
        audio_settings_btn.pack()
        finger_settings_btn.pack()
        back_button_btn.pack()


if __name__ == "__main__":
    app = SmartnodeGUI()
    app.mainloop()