import tkinter as tk
import test
import audio_controller
import global_variables as gv


UPDATE_RATE = 500


class AudioRuntime(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Audio Runtime", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.will_update = False
        self.user_setup = False

        btn1_fnc = lambda: (
                            self.audio_on_off())
        btn2_fnc = lambda: ()
        btn3_fnc = lambda: (
                            controller.show_frame("AudioStatus"))
        back_btn_func = lambda: (
                                 controller.show_frame(controller.return_frame))

        btn1 = tk.Button(self, text="Start/Stop",
                            command=btn1_fnc)
        btn2 = tk.Button(self, text="Mode: ",
                         command=btn2_fnc)
        btn3 = tk.Button(self, text="Show Status",
                         command=btn3_fnc)
        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        btn1.pack()
        btn2.pack()
        btn3.pack()
        back_btn.pack()

    def audio_updater(self, mySet):
        # This is the ocr loop by recursion
        if self.will_update:

            audio_controller.loop(mySet)
            # return values of external functions can change will_update flag or user_setup
            # self.will_update = False
            self.after(UPDATE_RATE, self.audio_updater, mySet)
        else:
            print("\n\nSample Loop Completed!")
            return

    # Starts the loop to call OCR called by button
    def audio_on_off(self):
        self.will_update = not self.will_update
        if (self.will_update):
            # checks to see if user recorded a sample
            print("Audio Start function")
            self.user_setup = audio_controller.init_Audio()
            if self.user_setup:
                mySet = audio_controller.pre_loop()
                self.audio_updater(mySet)
            else:  # otherwise will switch to sample setup frame for recording
                print("\tAudio Not Set Up! -> Running recordRef\n")
                self.controller.show_frame("SampleSetup")


class AudioStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Audio Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
                                 controller.show_frame("AudioRuntime"))

        back_button = tk.Button(self, text="Go back",
                                command=back_btn_func)

        back_button.pack()


class AudioSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Audio Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn1_fnc = lambda: (
                            controller.show_frame("SampleSetup"))
        btn2_fnc = lambda: (
                            controller.show_frame("AudioModeSetup"))
        btn3_fnc = lambda: (
                            controller.set_return_frame("AudioSettings"),
                            controller.show_frame("AudioRuntime"))
        back_btn_func = lambda: (
                                 controller.show_frame("Settings"))

        btn1 = tk.Button(self, text="Record Sample",
                         command=btn1_fnc)
        btn2 = tk.Button(self, text="Run Mode: ",
                         command=btn2_fnc)
        btn3 = tk.Button(self, text="Test Run",
                         command=btn3_fnc)
        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        btn1.pack()
        btn2.pack()
        btn3.pack()
        back_btn.pack()


class SampleSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Sample Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        record_func = lambda: (
                               audio_controller.record(),
                            controller.show_frame("AudioSettings"))

        back_func = lambda: (
                                 controller.show_frame("AudioSettings"))

        record_btn = tk.Button(self, text="Record",
                           command=record_func)

        back_btn = tk.Button(self, text="Go back",
                           command=back_func)

        record_btn.pack()
        back_btn.pack()


class AudioModeSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Audio Mode Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
                                 controller.show_frame("AudioSettings"))

        back_btn = tk.Button(self, text="Go back",
                             command=back_btn_func)

        back_btn.pack()