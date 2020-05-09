import tkinter as tk

import Settings_Functions as settings
import general_button_label as gbl
import global_variables as gv
import image_functions as image
import ocr_functions as ocr
import ocr_gui_btns as ocrBtns
import general_button_label as gbl


UPDATE_RATE = 500


#   This Screen Displays when the app is currently running the OCR sampling loop
class OCRRuntime(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Runtime", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # flag for looping OCR
        self.will_update = False  # changed by both button input and internal conditions
        self.button_off = False  # even if will_update loop is set to true, a botton off will always stop the loop
        self.user_setup = False

        # List functions called in order on button press

        btn_funcs = {
            'toggle': lambda: (
                # ,
                self.ocr_on_off()
            ),

            'mode': lambda: (
                #
            ),

            'show': lambda: (
                # ,
                controller.show_frame("OCRStatus")
            ),

            'back': lambda: (
                # ,
                controller.show_frame(controller.return_frame)
            )
        }

        btn_objs = {
            'toggle': gbl.GButton(self, text="Start/Stop"),
            'mode': gbl.GButton(self, text="Mode: "),
            'show': gbl.GButton(self, text="Show Status"),
            'back': gbl.GButton(self, text="Go back")
        }

        for btn in btn_objs:
            btn_objs[btn].configure(command=btn_funcs[btn])
            btn_objs[btn].pack(pady=gv.BUTTON_SPACE)

        self.count = 0

    def ocr_updater(self):
        # This is the ocr loop by recursion
        if self.will_update and not self.button_off:

            self.will_update = self.ocr_run_once()
            # return values of external functions can change will_update flag or user_setup
            # self.will_update = False
            self.after(UPDATE_RATE, self.ocr_updater)
        else:
            self.button_off = False
            return

    def ocr_run_once(self):
        print("TEST LOOP: " + str(self.count))
        # mySet = settings.loadSettings('OCRSettings.json')
        ocrData = settings.loadSettings('OCRData.json')
        image.takeSource()
        image.cropSource()
        ocrData = ocr.doOCR_All(ocrData)
        self.count += 1

        loop_again = False
        return loop_again

    # Starts the loop to call OCR called by button
    def ocr_on_off(self):
        self.will_update = not self.will_update
        if (self.will_update):
            self.ocr_updater()
        else:
            self.button_off = True


class OCRStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
            # ,
            controller.show_frame("OCRRuntime"))

        back_button = gbl.GButton(self, text="Go back",
                                  command=back_btn_func)

        back_button.pack(pady=gv.BUTTON_SPACE)


class OCRSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR/Video Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn_funcs = {
            'setup': lambda: (
                #   make sure all the settings for OCR are loaded
                settings.loadSettings('OCRSettings.json'),
                settings.loadSettings('OCRData.json'),
                settings.loadSettings('coordFile.json'),

                controller.frames["CropSetup"].update(),
                controller.show_frame("CropSetup")
            ),

            'mode': lambda: (
                # ,
                controller.show_frame("OCRModeSetup")
            ),

            'test': lambda: (
                # ,
                controller.set_return_frame("OCRSettings"),
                controller.show_frame("OCRRuntime")
            ),

            'back': lambda: (
                # ,
                controller.show_frame("Settings")
            ),
        }

        btn_objs = {
            'setup': gbl.GButton(self, text="Cropping Setup"),
            'mode': gbl.GButton(self, text="Loop Mode: "),
            'test': gbl.GButton(self, text="Test Run"),
            'back': gbl.GButton(self, text="Go back"),
        }

        for btn in btn_objs:
            btn_objs[btn].configure(command=btn_funcs[btn])
            btn_objs[btn].pack(pady=gv.BUTTON_SPACE)


class CropSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Crop Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn_funcs = {
            'add': lambda: (
                ocrBtns.cropSetup_add(),
            ),

            'remove': lambda: (
                ocrBtns.cropSetup_remove(),
            ),

            'show': lambda: (
                ocrBtns.cropSetup_show()
            ),

            'back': lambda: (
                # ,
                controller.show_frame("OCRSettings")
            )
        }

        btn_objs = {
            'add': gbl.GButton(self, text="Add Crop Area"),
            'remove': gbl.GButton(self, text="Remove Last"),
            'show': gbl.GButton(self, text="Show Current"),
            'back': gbl.GButton(self, text="Go back"),
        }

        for btn in btn_objs:
            btn_objs[btn].configure(command=btn_funcs[btn])
            btn_objs[btn].pack(pady=gv.BUTTON_SPACE)

class CropSetup2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="Crop Setup 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
            # ,
            controller.show_frame("CropSetup")
        )

        back_btn = gbl.GButton(self, text="Go back", command=back_btn_func)

        back_btn.pack(pady=gv.BUTTON_SPACE)


class OCRModeSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Mode Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        self.current_mode = settings.loadSettings("OCRSettings.json")['loopMode']
        print(self.current_mode)
        
        dlabel = gbl.DLabel(self, text=self.current_mode)

        btn_funcs = {
            'next mode': lambda: (
                ocrBtns.cropSetup_add(),
            ),

            'save': lambda: (
                ocrBtns.cropSetup_remove(),
            ),

            'cancel': lambda: (
                controller.show_frame("OCRSettings")
            )
        }

        btn_objs = {
            'next mode': gbl.GButton(self, text="Next Mode"),
            'save': gbl.GButton(self, text="Save"),
            'cancel': gbl.GButton(self, text="Cancel"),
        }

        for btn in btn_objs:
            btn_objs[btn].configure(command=btn_funcs[btn])
            btn_objs[btn].pack(pady=gv.BUTTON_SPACE)


