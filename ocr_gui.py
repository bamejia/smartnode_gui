import tkinter as tk
import cv2
import image_capture
from PIL import Image
from PIL import ImageTk
import test
import time


UPDATE_RATE = 500

#   This Screen Displays when the app is currently running the OCR sampling loop
class OCRRuntime(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OCR Runtime", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # flag for looping OCR
        self.will_update = False
        self.user_setup = False

        # List functions called in order on button press
        start_stop_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            self.ocr_on_off())
        mode_fnc = lambda: (test.louis_replace_this_with_your_function_name())
        show_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.show_frame("OCRStatus"))
        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame(controller.return_frame))


        start_stop_btn = tk.Button(self, text="Start/Stop",
                            command=start_stop_fnc)
        mode_btn = tk.Button(self, text="Mode: ",
                         command=mode_fnc)
        show_btn = tk.Button(self, text="Show Status",
                         command=show_fnc)
        back_button_btn = tk.Button(self, text="Go back",
                                command=back_btn_func)

        start_stop_btn.pack()
        mode_btn.pack()
        show_btn.pack()
        back_button_btn.pack()

        self.count = 0

    # def update_ocr(self):
    #     if self.will_update:
    #         self.test_loop()

    def ocr_updater(self):
        # This is the ocr loop by recursion
        if self.will_update:

            self.ocr_run_once()
            # return values of external functions can change will_update flag or user_setup
            # self.will_update = False
            self.after(UPDATE_RATE, self.ocr_updater)
        else:
            return

    def ocr_run_once(self):
        print("TEST LOOP: " + str(self.count))
        self.count += 1

    # Starts the loop to call OCR called by button
    def ocr_on_off(self):
        self.will_update = not self.will_update
        if (self.will_update):
            self.ocr_updater()


class OCRStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OCR Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("OCRRuntime"))

        back_button = tk.Button(self, text="Go back",
                                command=back_btn_func)

        back_button.pack()


class OCRSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OCR/Video Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn1_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.frames["CropSetup"].update(),
                            controller.show_frame("CropSetup"))
        btn2_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.show_frame("OCRModeSetup"))
        btn3_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.set_return_frame("OCRSettings"),
                            controller.show_frame("OCRRuntime"))
        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("Settings"))

        btn1 = tk.Button(self, text="Setup OCR",
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


class CropSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Crop Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("OCRSettings"))

        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        back_btn.pack()

        self.image = cv2.cvtColor(image_capture.capture_image(), cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)

        panelA = tk.Label(self, image=self.image)
        panelA.image = self.image
        panelA.pack(side="top", fill="x", pady=10)

    def update(self):
        print("CATS")
        self.image = cv2.cvtColor(image_capture.capture_image(), cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)


class CropSetup2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Crop Setup 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("CropSetup"))

        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        back_btn.pack()


class OCRModeSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OCR Mode Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("OCRSettings"))

        back_btn = tk.Button(self, text="Go back",
                             command=back_btn_func)

        back_btn.pack()