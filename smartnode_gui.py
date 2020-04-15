import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import global_variables as gv
import test

#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2


class SmartnodeGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window_width = round(gv.WINDOW_W / 1)
        window_length = round(gv.WINDOW_L / 1)
        window_x = round(gv.WINDOW_W * 3 / 5)
        window_y = round(gv.WINDOW_L * 2 / 5)
        geometry_dimensions = "%dx%d+%d+%d" % (window_width, window_length, window_x, window_y)

        self.geometry(geometry_dimensions)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, Settings, OCRVideoSettings, AudioSettings, AutomationSettings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Menu", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        start_stop_ocr_btn = tk.Button(self, text="Start/Stop OCR",
                                 command=lambda: test.ocr_test())
        start_stop_audio_btn = tk.Button(self, text="Start/Stop Audio",
                                       command=lambda: test.audio_test())
        settings_btn = tk.Button(self, text="Settings",
                            command=lambda: controller.show_frame("Settings"))
        quit_btn = tk.Button(self, text="Quit",
                            command=lambda: controller.destroy())
        start_stop_ocr_btn.pack()
        start_stop_audio_btn.pack()
        settings_btn.pack()
        quit_btn.pack()


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="OCR/Video Settings",
                            command=lambda: controller.show_frame("OCRVideoSettings"))
        button2 = tk.Button(self, text="Audio Settings",
                            command=lambda: controller.show_frame("AudioSettings"))
        button3 = tk.Button(self, text="Automation Settings",
                            command=lambda: controller.show_frame("AutomationSettings"))
        back_button = tk.Button(self, text="Go back",
                                command=lambda: controller.show_frame("MainMenu"))
        button1.pack()
        button2.pack()
        button3.pack()
        back_button.pack()


class OCRVideoSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OCR/Video Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("Settings"))
        button.pack()


class AudioSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("Settings"))
        button.pack()


class AutomationSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Automation Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("Settings"))
        button.pack()


if __name__ == "__main__":
    app = SmartnodeGUI()
    app.mainloop()