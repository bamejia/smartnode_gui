import tkinter as tk

import global_variables as gv
import general_button_label as gbl


class FingerSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Finger Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
                                 controller.show_frame("Settings"))

        back_btn = gbl.GButton(self, text="Go back",
                           command=back_btn_func)

        back_btn.pack()