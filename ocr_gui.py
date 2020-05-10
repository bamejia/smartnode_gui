import tkinter as tk

import Settings_Functions as settings
import general_button_label as gbl
import global_variables as gv
import image_functions as image
import ocr_functions as ocr
import ocr_gui_btns as ocrBtns

UPDATE_RATE = 500


#   This Screen Displays when the app is currently running the OCR sampling loop
class OCRMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Menu", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=0, pady=10, columnspan=3, sticky='nsew')

        # flag for looping OCR
        self.will_update = False  # changed by both button input and internal conditions
        self.button_off = False  # even if will_update loop is set to true, a botton off will always stop the loop
        self.user_setup = False

        mySet = settings.loadSettings('OCRSettings.json')
        self.running_display_label = gbl.DLabel(self, text='Running: ' + mySet['running'])
        # self.running_display_label.pack(side='left', pady=gv.BUTTON_SPACE)
        self.running_display_label.grid(column=0, row=1, columnspan=2, pady=gv.BUTTON_SPACE)
        self.mode_display_label = gbl.DLabel(self, text='Run mode: ' + mySet['loopMode'])
        # self.mode_display_label.pack(side='left', pady=gv.BUTTON_SPACE)
        self.mode_display_label.grid(column=1, row=1, columnspan=2, pady=gv.BUTTON_SPACE)

        # List functions called in order on button press

        btn_funcs = {
            'toggle': lambda: (
                # ,
                self.ocr_on_off()
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
            'show': gbl.GButton(self, text="Show Status"),
            'back': gbl.GButton(self, text="Go back")
        }

        count = 2
        for btn in btn_objs:
            btn_objs[btn].configure(command=btn_funcs[btn])
            # btn_objs[btn].pack(pady=gv.BUTTON_SPACE)
            btn_objs[btn].grid(row=count, column=1, pady=gv.BUTTON_SPACE)
            count += 1

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

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

    #   this is the function that handles the individual steps for a single ocr sampling run
    def ocr_run_once(self):
        print("OCR_RUNTIME LOOP: " + str(self.count))
        # mySet = settings.loadSettings('OCRSettings.json')

        #   load ocrSettings / ocr output file, OCRData.json
        ocrData = settings.loadSettings('OCRData.json')

        #   capture / crop source image
        image.takeSource()
        image.cropSource(debug=True)

        #   perform ocr on all cropped images
        ocrData = ocr.do_OCR_all(ocrData, debug=True)

        #   temporary printout of data captured during this run
        #   this information needs to be passed to display, firebase
        #   dataset is a dict saved in ocrData.json
        #       -> objects have same format as OCR_DATA_ENTRY in DEFAULTS

        print("\nOCR data Captured:")
        dataSet = ocrData['dataset']

        #   note -> dataSet[entry] and dataSet[entry]['name'] are the same string...
        for entry in dataSet:
            print(f"\t{dataSet[entry]['name']}: '{dataSet[entry]['text']}'")

        #   loop control variables
        self.count += 1
        loop_again = False
        return loop_again

    # Starts the loop to call OCR called by button
    def ocr_on_off(self):
        self.will_update = not self.will_update
        if self.will_update:
            self.ocr_updater()
        else:
            self.button_off = True

    def change_mode_label(self, new_mode):
        self.mode_display_label.configure(text='Run mode: ' + new_mode)


class OCRStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (
            # ,
            controller.show_frame("OCRMenu"))

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
                controller.show_frame("OCRMenu")
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

        self.mode_label = gbl.DLabel(self, text=self.current_mode)
        self.mode_label.pack(pady=gv.BUTTON_SPACE)

        btn_funcs = {
            'next mode': lambda: (
                self.change_current_mode_display(ocrBtns.next_mode(self.current_mode))
            ),

            'save': lambda: (
                settings.changeSetting(settings.loadSettings("OCRSettings.json"), 'loopMode', self.current_mode),
                controller.show_frame("OCRSettings")
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

    def change_current_mode_display(self, display_text):
        self.current_mode = display_text
        self.mode_label.configure(text=display_text)
        self.controller.frames['OCRMenu'].change_mode_label(display_text)


