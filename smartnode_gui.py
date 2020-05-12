import tkinter as tk  # python 3
from tkinter import font  as tkfont  # python 3

import firebase_listener
import FireBase_Functions as fbFuncs
import Settings_Functions as settings
import audio_gui
import finger_gui
import general_button_label as gbl
import global_variables as gv
import ocr_gui
import finger_functions as finger


UPDATE_RATE = 1000


class SmartnodeGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.firebase_database = None
        self.finger_press = True

        window_width = round(gv.WINDOW_W / 1)
        window_length = round(gv.WINDOW_L / 1)
        window_x = round(gv.WINDOW_W * 3 / 5)
        window_y = round(gv.WINDOW_L * 2 / 5)
        geometry_dimensions = "%dx%d+%d+%d" % (window_width, window_length, window_x, window_y)

        self.attributes('-fullscreen', True)  # 800x480
        # self.attributes('-zoomed', True)
        # self.overrideredirect(True)  # gets rid of top minimizing, maximizing, and closing buttons bar

        self.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")
        self.button_font = tkfont.Font(size=26)

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
            ocr_gui.OCRMenu,
            ocr_gui.OCRSettings,
            ocr_gui.CropSetup,
            ocr_gui.OCRSetup,
            ocr_gui.OCRCropConfig,
            ocr_gui.CropSettingConfig,
            ocr_gui.CropNameChange,
            ocr_gui.OCRModeSetup,
            ocr_gui.OCRStatus,
            audio_gui.AudioMenu,
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
        self.current_frame = "MainMenu"
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
        self.current_frame = page_name
        frame = self.frames[page_name]
        frame.tkraise()

    def set_return_frame(self, page_name):
        self.return_frame = page_name

    def firebase_command_handler(self, command):
        if command == "ocr_on_off":
            print("App command: " + command)
            self.frames["OCRMenu"].ocr_on_off()
        elif command == "audio_on_off":
            print("App command: " + command)
            self.frames['AudioMenu'].audio_on_off()
        elif command == "press":
            print("App command: " + command)
            if self.finger_press:
                self.finger_press = False
                delay, repeats, interval = 500, 0, 500
                finger.finger_looper(self.after, self.set_finger_press, delay, repeats, interval)
            else:
                print("Cannot press finger that fast")


    def addFirebaseDatabase(self, db):
        self.firebase_database = db


    def set_finger_press(self, val):
        self.finger_press = val


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, "Main Menu", controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        ocr_btn_func = lambda: (
            controller.set_return_frame("MainMenu"),
            controller.show_frame("OCRMenu"))

        audio_btn_func = lambda: (
            controller.set_return_frame("MainMenu"),
            controller.show_frame("AudioMenu"))

        settings_btn_func = lambda: (
                                controller.show_frame("Settings"))

        reset_btn_func = lambda: (
            reset_all_running_flags(self.controller),
            reset_all_reset_mode(self.controller),
            settings.fullReset(),
            fbFuncs.postFirebase(settings.loadSettings("OCRSettings.json")['fb_data_url'],
                                 {'ocr_data': settings.loadSettings("OCRData.json")['dataset']},
                                 self.controller.firebase_database),
            fbFuncs.postFirebase(settings.loadSettings("audioSettings.json")['fb_data_url'],
                                 {'audio_detected': settings.loadSettings("audioSettings.json")['detected']},
                                 self.controller.firebase_database)
        )
        quit_btn_func = lambda: (
                                controller.destroy())

        self.start_stop_ocr_btn = gbl.GButton(self, "OCR", ocr_btn_func)
        start_stop_audio_btn = gbl.GButton(self, "Audio", audio_btn_func)
        settings_btn = gbl.GButton(self, "Settings", settings_btn_func)

        reset_btn = gbl.GButton(self, "Reset Files", reset_btn_func)

        quit_btn = gbl.GButton(self, "Quit", quit_btn_func)

        self.start_stop_ocr_btn.pack(pady=gv.BUTTON_SPACE)
        start_stop_audio_btn.pack(pady=gv.BUTTON_SPACE)
        settings_btn.pack(pady=gv.BUTTON_SPACE)
        reset_btn.pack(pady=gv.BUTTON_SPACE)
        quit_btn.pack(pady=gv.BUTTON_SPACE)

        self.count = 0
        self.will_update = True
        # self.updater()

    def update_button1(self):
        if self.will_update:
            self.start_stop_ocr_btn["text"] = str(self.count)
            self.count += 1

    def updater(self):
        self.update_button1()
        self.after(UPDATE_RATE, self.updater)


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, "Settings", controller.title_font)
        label.pack(side="top", fill="x", pady=8)

        ocr_settings_func = lambda: (
                                controller.show_frame("OCRSettings"))
        audio_settings_func = lambda: (
                             controller.show_frame("AudioSettings"))
        finger_settings_func = lambda: (
                             controller.show_frame("FingerSettings"))
        back_btn_func = lambda: (
                             controller.show_frame("MainMenu"))

        ocr_settings_btn = gbl.GButton(self, "OCR Settings", ocr_settings_func)
        audio_settings_btn = gbl.GButton(self, "Audio Settings", audio_settings_func)
        finger_settings_btn = gbl.GButton(self, "Finger Settings", finger_settings_func)
        back_button_btn = gbl.GButton(self, "Go back", back_btn_func)

        ocr_settings_btn.pack(pady=gv.BUTTON_SPACE)
        audio_settings_btn.pack(pady=gv.BUTTON_SPACE)
        finger_settings_btn.pack(pady=gv.BUTTON_SPACE)
        back_button_btn.pack(pady=gv.BUTTON_SPACE)


class PopUp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller

        label = gbl.GLabel(self, "Settings", controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        ocr_settings_func = lambda: (
            controller.show_frame("OCRSettings"))
        audio_settings_func = lambda: (
            controller.show_frame("AudioSettings"))
        finger_settings_func = lambda: (
            controller.show_frame("FingerSettings"))
        back_btn_func = lambda: (
            controller.show_frame("MainMenu"))

        ocr_settings_btn = gbl.GButton(self, "OCR Settings", ocr_settings_func)
        audio_settings_btn = gbl.GButton(self, "Audio Settings", audio_settings_func)
        finger_settings_btn = gbl.GButton(self, "Finger Settings", finger_settings_func)
        back_button_btn = gbl.GButton(self, "Go back", back_btn_func)

        ocr_settings_btn.pack(pady=gv.BUTTON_SPACE)
        audio_settings_btn.pack(pady=gv.BUTTON_SPACE)
        finger_settings_btn.pack(pady=gv.BUTTON_SPACE)
        back_button_btn.pack(pady=gv.BUTTON_SPACE)


def reset_all_running_flags(app):
    mySet = settings.changeSetting(settings.loadSettings('OCRSettings.json'), 'running', 'False')
    fb_message = {'running': "False"}
    fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, app.firebase_database)

    mySet = settings.changeSetting(settings.loadSettings('audioSettings.json'), 'running', 'False')
    fb_message = {'running': "False"}
    fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, app.firebase_database)


def reset_all_reset_mode(app):
    mySet = settings.changeSetting(settings.loadSettings('OCRSettings.json'), 'loopMode', 'infinite')
    fb_message = {'run_mode': "infinite"}
    fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, app.firebase_database)

    mySet = settings.changeSetting(settings.loadSettings('audioSettings.json'), 'loopMode', 'infinite')
    fb_message = {'run_mode': "infinite"}
    fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, app.firebase_database)


if __name__ == "__main__":
    app = SmartnodeGUI()

    firebase_listener.run(app.firebase_command_handler)
    app.addFirebaseDatabase(firebase_listener.db)

    app.mainloop()

    reset_all_running_flags(app)

    finger.cleanup()
    firebase_listener.close()
