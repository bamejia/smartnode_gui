import tkinter as tk

import global_variables as gv


class FingerSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Finger Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
                                 controller.show_frame("Settings"))

        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        back_btn.pack()