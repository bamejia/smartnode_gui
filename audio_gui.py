import tkinter as tk

import Settings_Functions as settings
import audio_controller
import audio_functions as audio
import audio_gui_btns as audioBtns
import general_button_label as gbl
import global_variables as gv
from datetime import datetime
import FireBase_Functions as fbFuncs
import Utility_Functions as util
from tkinter import font as tkfont


UPDATE_RATE = 1000   # set flag for recording audio sample to see how small this can be made


class AudioMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Audio Menu", font=controller.title_font)
        label.grid(row=0, column=0, pady=gv.TITLE_PADY, columnspan=3, sticky='nsew')

        self.will_update = False  # changed by both button input and internal conditions
        self.button_off = False  # even if will_update loop is set to true, a botton off will always stop the loop
        self.user_setup = False

        holder_frame = gbl.DFrame(self)
        holder_frame.grid(row=1, column=0, columnspan=3, pady=gv.LABEL_PADY)

        mySet = settings.loadSettings('audioSettings.json')
        self.running_display_label = tk.Label(holder_frame, text='Running: ' + mySet['running'])
        self.running_display_label.configure(background=gv.LABEL_COLOR, font=tkfont.Font(size=26),
                                             fg=gv.LABEL_FONT_COLOR, justify='left')
        self.running_display_label.pack(side='left', pady=gv.LABEL_PADY, padx=gv.LABEL_PADX)

        x_padding_label = tk.Label(holder_frame)
        x_padding_label.configure(background=gv.LABEL_COLOR)
        x_padding_label.pack(side='left', padx=gv.LABEL_PADX * 3)

        self.mode_display_label = tk.Label(holder_frame, text='Run mode: ' + mySet['loopMode'])
        self.mode_display_label.configure(background=gv.LABEL_COLOR, font=tkfont.Font(size=26),
                                          fg=gv.LABEL_FONT_COLOR, justify='right')
        self.mode_display_label.pack(side='left', pady=gv.LABEL_PADY, padx=gv.LABEL_PADX)

        btn1_fnc = lambda: (
            self.audio_on_off())
        btn2_fnc = lambda: (
            controller.show_frame("AudioStatus"))
        back_btn_func = lambda: (
            controller.show_frame(controller.return_frame))

        btn1 = gbl.GButton(self, text="Start/Stop",
                           command=btn1_fnc)
        btn2 = gbl.GButton(self, text="Show Status",
                           command=btn2_fnc)
        back_btn = gbl.GButton(self, text="Go back",
                               command=back_btn_func)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # btn1.pack(pady=gv.BUTTON_SPACE)
        # btn2.pack(pady=gv.BUTTON_SPACE)
        # back_btn.pack(pady=gv.BUTTON_SPACE)
        btn1.grid(row=2, column=1, pady=gv.BUTTON_SPACE)
        btn2.grid(row=3, column=1, pady=gv.BUTTON_SPACE)
        back_btn.grid(row=4, column=1, pady=gv.BUTTON_SPACE)

    def audio_detector(self, mySet, data):
        audio.writeAudioFile(*data)

        self.will_update, audio_detection = audio_controller.loop(mySet, self.controller.firebase_database)

        #  updates audio status if sound is detected
        if audio_detection:
            audio_detection = util.reformatTime(audio_detection)
            self.controller.frames['AudioStatus'].update_status(audio_detection)

        # return values of external functions can change will_update flag or user_setup
        # self.will_update = False
        self.after(UPDATE_RATE, self.audio_updater, mySet)

    #   will_update
    def audio_updater(self, mySet):

        if self.will_update and not self.button_off:
            #   checks
            data = audio.recordAudio(mySet['smplPath'])
            self.after(int(data[3]*1000), self.audio_detector, mySet, data)
        else:
            print("\n\nSample Loop Completed!")
            self.change_running_label('False')
            fb_message = {'running': "False"}
            fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, self.controller.firebase_database)
            self.button_off = False
            self.will_update = False
            self.controller.frames["Settings"].switch_access_setting("audio")

    # Starts the loop to call OCR called by button
    def audio_on_off(self):

        self.will_update = not self.will_update

        if self.will_update:

            #   Checks flag in mainSettings.json to see if record sample has been run
            print("Audio Start function")
            self.user_setup = audio_controller.init_Audio()

            if self.user_setup:
                mySet = self.preloop_flag_assignments()
                print(f"Setup Complete -> Loop Mode: {mySet['loopMode']}")
                self.audio_updater(mySet)

            else:  # otherwise will switch to sample setup frame for recording
                print("\tAudio Not Set Up! -> Running recordRef\n")
                self.will_update = False
                self.controller.show_frame("SampleSetup")
        else:
            self.button_off = True

    def change_mode_label(self, new_mode):
        self.mode_display_label.configure(text='Run mode: ' + new_mode)

    def change_running_label(self, running):
        self.running_display_label.configure(text='Running: ' + running)

    def preloop_flag_assignments(self):
        self.controller.frames["Settings"].switch_access_setting("audio")
        self.change_running_label('True')
        mySet = settings.loadSettings('audioSettings.json')
        mySet = settings.changeSetting(mySet, 'detected', 'Not Detected')
        fb_message = {'audio_detected': "not detected"}
        fbFuncs.postFirebase(mySet['fb_data_url'], fb_message, self.controller.firebase_database)

        fb_message = {'running': "True"}
        fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, self.controller.firebase_database)

        self.controller.frames['AudioStatus'].update_status('Not Detected')
        return mySet


class AudioStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Audio Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        status_label_text = util.reformatTime(settings.loadSettings("audioSettings.json")['detected'])
        self.label_status = gbl.DLabel(self, text="Time detected: %s" % status_label_text)
        self.label_status.pack(pady=gv.BUTTON_SPACE)

        back_btn_func = lambda: (
            controller.show_frame("AudioMenu"))

        back_button = gbl.GButton(self, text="Go back",
                                  command=back_btn_func)

        back_button.pack(pady=gv.BUTTON_SPACE)

    def update_status(self, status_update):
        self.label_status.configure(text="Time detected: %s" % status_update)


#   done
class AudioSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Audio Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        btn1_fnc = lambda: (
            controller.show_frame("SampleSetup"))
        btn2_fnc = lambda: (
            controller.show_frame("AudioModeSetup"))
        # btn3_fnc = lambda: (
        #     controller.set_return_frame("AudioSettings"),
        #     controller.show_frame("AudioMenu"))
        back_btn_func = lambda: (
            controller.show_frame("Settings"))

        btn1 = gbl.GButton(self, text="Reference Setup",
                           command=btn1_fnc)
        btn2 = gbl.GButton(self, text="Run Mode",
                           command=btn2_fnc)
        # btn3 = gbl.GButton(self, text="Test Run",
        #                    command=btn3_fnc)
        back_btn = gbl.GButton(self, text="Go back",
                               command=back_btn_func)

        btn1.pack(pady=gv.BUTTON_SPACE)
        btn2.pack(pady=gv.BUTTON_SPACE)
        # btn3.pack(pady=gv.BUTTON_SPACE)
        back_btn.pack(pady=gv.BUTTON_SPACE)


#   totally Done
class SampleSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Sample Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        record_func = lambda: (
            audio.recordRef(),
        )

        playback_func = lambda: (
            audio.playReference(),
            # controller.show_frame("AudioSettings")
        )

        back_func = lambda: (
            controller.show_frame("AudioSettings"))

        record_btn = gbl.GButton(self, text="Record Reference",
                                 command=record_func)

        playback_btn = gbl.GButton(self, text="Play Sample",
                                   command=playback_func)

        back_btn = gbl.GButton(self, text="Go back",
                               command=back_func)

        record_btn.pack(pady=gv.BUTTON_SPACE)
        playback_btn.pack(pady=gv.BUTTON_SPACE)
        back_btn.pack(pady=gv.BUTTON_SPACE)


class AudioModeSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Audio Mode Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        self.current_mode = settings.loadSettings('audioSettings.json')['loopMode']

        self.mode_label = gbl.DLabel(self, text="mode: " + self.current_mode)
        self.mode_label.pack(pady=gv.BUTTON_SPACE)

        next_mode_func = lambda: (
            self.change_current_mode_display(audioBtns.next_mode(self.current_mode))
        )
        save_func = lambda: (
            settings.changeSetting(settings.loadSettings("audioSettings.json"), 'loopMode', self.current_mode),
            fbFuncs.postFirebase(settings.loadSettings("audioSettings.json")['fb_status_url'],
                                 {'run_mode': self.current_mode}, controller.firebase_database),
            self.controller.frames['AudioMenu'].change_mode_label(self.current_mode),
            controller.show_frame("AudioSettings")
        )
        cancel_func = lambda: (
            self.change_current_mode_display(settings.loadSettings("audioSettings.json")['loopMode']),
            controller.show_frame("AudioSettings")
        )

        next_mode_btn = gbl.GButton(self, text="Next Mode",
                                    command=next_mode_func)
        save_btn = gbl.GButton(self, text="Save",
                               command=save_func)
        cancel_btn = gbl.GButton(self, text="Cancel",
                                 command=cancel_func)

        next_mode_btn.pack(pady=gv.BUTTON_SPACE)
        save_btn.pack(pady=gv.BUTTON_SPACE)
        cancel_btn.pack(pady=gv.BUTTON_SPACE)

    def change_current_mode_display(self, display_text):
        self.current_mode = display_text
        self.mode_label.configure(text="mode: " + display_text)
