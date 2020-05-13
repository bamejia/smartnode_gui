import tkinter as tk

import global_variables as gv
import general_button_label as gbl
import finger_functions as finger


class FingerSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Finger Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=gv.TITLE_PADY)

        press_finger_func = lambda :(
            self.press_finger()
        )

        back_btn_func = lambda: (
            controller.show_frame("Settings")
        )

        pressfinger_btn = gbl.GButton(self, text="Press Finger",
                           command=press_finger_func)

        back_btn = gbl.GButton(self, text="Go back",
                           command=back_btn_func)

        pressfinger_btn.pack(pady=gv.BUTTON_SPACE)
        back_btn.pack(pady=gv.BUTTON_SPACE)

    def press_finger(self):
        delay, num_presses, interval = 300, 1, 300
        finger.finger_handler(delay, num_presses, interval)
