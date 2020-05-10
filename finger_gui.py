import tkinter as tk

import global_variables as gv
import general_button_label as gbl
import finger_functions as finger


class FingerSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Finger Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.finger_press = True

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
        if self.finger_press:
            self.finger_press = False
            delay, repeats, interval = 500, 0, 500
            finger.finger_looper(self.after, self.set_finger_press, delay, repeats, interval)

    def set_finger_press(self, val):
        self.finger_press = val