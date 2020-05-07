import tkinter as tk

import global_variables as gv


# from tkinter import font  as tkfont


class GButton(tk.Button):

    def __init__(self, frame, input_text, input_command=lambda: print("button command not set")):
        tk.Button.__init__(self, frame, text=input_text, command=input_command, bd=gv.BUTTON_DEPTH, bg=gv.BUTTON_COLOR,
                           height=gv.BUTTON_HEIGHT, width=gv.BUTTON_WIDTH,
                           activebackground=gv.BUTTON_PRESS_COLOR, fg=gv.FONT_COLOR)
        self.configure(font=tk.font.Font(size=26))


class GLabel(tk.Label):
    def __init__(self, frame, input_text, input_font):
        tk.Label.__init__(self, frame, text=input_text, font=input_font, bg=gv.TITLE_COLOR, fg=gv.FONT_COLOR,
                         bd=gv.TITLE_DEPTH, relief=tk.RAISED, pady=gv.TITLE_PADY)
