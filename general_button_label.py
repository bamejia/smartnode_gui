import tkinter as tk

import global_variables as gv


# from tkinter import font  as tkfont


class GButton(tk.Button):

    def __init__(self, frame, text, command=lambda: print("button command not set")):
        tk.Button.__init__(self, frame, text=text, command=command, bd=gv.BUTTON_DEPTH, bg=gv.BUTTON_COLOR,
                           height=gv.BUTTON_HEIGHT, width=gv.BUTTON_WIDTH,
                           activebackground=gv.BUTTON_PRESS_COLOR, fg=gv.BUTTON_FONT_COLOR)
        self.configure(font=tk.font.Font(size=26))


class GLabel(tk.Label):
    def __init__(self, frame, text, font):
        tk.Label.__init__(self, frame, text=text, font=font, bg=gv.TITLE_COLOR, fg=gv.BUTTON_FONT_COLOR,
                         bd=gv.TITLE_DEPTH, relief=tk.RAISED, pady=gv.TITLE_PADY)
        self.configure(font=tk.font.Font(size=26), justify='center')


class DLabel(tk.Label):
    def __init__(self, frame, text):
        tk.Label.__init__(self, frame, text=text, bg=gv.LABEL_COLOR, fg=gv.LABEL_FONT_COLOR, bd=gv.LABEL_DEPTH,
                          relief=tk.SUNKEN, height=gv.BUTTON_HEIGHT, pady=gv.LABEL_PADY, padx=gv.LABEL_PADX)
        self.configure(font=tk.font.Font(size=26), justify='center')


class DFrame(tk.Frame):
    def __init__(self, frame):
        tk.Frame.__init__(self, frame, bg=gv.LABEL_COLOR, bd=gv.LABEL_DEPTH,
                          relief=tk.SUNKEN, height=gv.BUTTON_HEIGHT, pady=gv.LABEL_PADY, padx=gv.LABEL_PADX)