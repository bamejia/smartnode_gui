import tkinter as tk

import FireBase_Functions as fbFuncs
import Settings_Functions as settings
import general_button_label as gbl
import global_variables as gv
import image_functions as image
import ocr_functions as ocr
import ocr_gui_btns as ocrBtns
import collections

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
        self.running_display_label.grid(column=0, row=1, columnspan=2, pady=gv.BUTTON_SPACE, sticky='w')
        self.mode_display_label = gbl.DLabel(self, text='Run mode: ' + mySet['loopMode'])
        # self.mode_display_label.pack(side='left', pady=gv.BUTTON_SPACE)
        self.mode_display_label.grid(column=1, row=1, columnspan=2, pady=gv.BUTTON_SPACE, sticky='e')

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
            mySet = settings.changeSetting(settings.loadSettings('OCRSettings.json'), 'running', 'False')
            self.change_running_label('False')
            fb_message = {'running': "False"}
            fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, self.controller.firebase_database)
            self.will_update = False
            self.button_off = False
            return

    #   this is the function that handles the individual steps for a single ocr sampling run
    # def ocr_run_once(self):
    #     print("OCR_RUNTIME LOOP: " + str(self.count))
    #     mySet = settings.loadSettings('OCRSettings.json')
    #
    #     #   load ocrSettings / ocr output file, OCRData.json
    #     ocrData = settings.loadSettings('OCRData.json')
    #
    #     #   capture / crop source image
    #     image.takeSource()
    #     image.cropSource(debug=True)
    #
    #     #   perform ocr on all cropped images
    #     ocrData = ocr.do_OCR_all(ocrData, debug=True)
    #
    #     #   temporary printout of data captured during this run
    #     #   this information needs to be passed to display, firebase
    #     #   dataset is a dict saved in ocrData.json
    #     #       -> objects have same format as OCR_DATA_ENTRY in DEFAULTS
    #
    #     print("\nOCR data Captured:")
    #     dataSet = ocrData['dataset']
    #     data = {'ocr_data' : ""}
    #     mySet = settings.loadSettings("OCRSettings.json")
    #     print("DATA SET: " + str(dataSet))
    #     self.controller.frames['OCRStatus'].update_status(dataSet)
    #     fbFuncs.postFirebase(mySet['fb_data_url'], data, self.controller.firebase_database)
    #     return False
    #     # print(dataSet)
    #
    #     #   blank dict to send to firebase
    #     fbDict = {}
    #
    #     #   note -> dataSet[entry] and dataSet[entry]['name'] are the same string...
    #     for entry in dataSet:
    #         print(f"\t{dataSet[entry]['name']}: '{dataSet[entry]['text']}'")
    #         fbDict[dataSet[entry]['name']] = dataSet[entry]['text']
    #
    #     print(fbDict)
    #     #   post name:text values firebase
    #     fbFuncs.postFirebase(mySet['fb_data_url'], fbDict, self.controller.firebase_database)
    #
    #
    #     #   loop control variables
    #     endLoop = settings.check_LoopMode(mySet)
    #     loop_again = not endLoop
    #     return loop_again

    def ocr_run_once(self):
        ocrData = settings.loadSettings('OCRData.json')
        dataSet = ocrData['dataset']
        self.controller.frames['OCRStatus'].update_status(dataSet)


    # Starts the loop to call OCR called by button
    def ocr_on_off(self):
        self.will_update = not self.will_update
        if self.will_update:
            self.user_setup = settings.loadSettings("mainSettings.json")['OCR_Setup'] == 'True'
            if self.user_setup:
                mySet = self.preloop_flag_assignments()
                self.ocr_updater()
            else:
                self.will_update = False
                self.controller.show_frame("CropSetup")
        else:
            self.button_off = True

    def change_mode_label(self, new_mode):
        self.mode_display_label.configure(text='Run mode: ' + new_mode)

    def change_running_label(self, running):
        self.running_display_label.configure(text='Running: ' + running)

    def preloop_flag_assignments(self):
        self.change_running_label('True')
        mySet = settings.loadSettings('OCRSettings.json')
        mySet = settings.changeSetting(mySet, 'running', 'True')

        # fb_message = {'audio_detected': "not detected"}
        # fbFuncs.postFirebase(mySet['fb_data_url'], fb_message, self.controller.firebase_database)

        fb_message = {'running': "True"}
        fbFuncs.postFirebase(mySet['fb_status_url'], fb_message, self.controller.firebase_database)

        self.controller.frames['OCRStatus'].update_status({})
        return mySet


class OCRStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.no_data_label = gbl.DLabel(self, text="No Data")
        self.no_data_label.pack(pady=gv.BUTTON_SPACE)

        self.orc_data_labels = {}

        back_btn_func = lambda: (
            controller.show_frame("OCRMenu"))

        self.back_button = gbl.GButton(self, text="Go back",
                                  command=back_btn_func)

        self.back_button.pack(pady=gv.BUTTON_SPACE)

        self.update_status(settings.loadSettings('OCRData.json')['dataset'])

    # Dynamically creates or destroys labels according to the dataset dict passed from OCRData.json
    def update_status(self, status_update):
        if status_update == []:
            if self.orc_data_labels == {}:
                return
            else:
                for ocr_obj_name in list(self.orc_data_labels):
                    self.orc_data_labels[ocr_obj_name].destroy()
                    del self.orc_data_labels[ocr_obj_name]
                self.back_button.pack_forget()
                self.no_data_label.pack(pady=gv.BUTTON_SPACE)
                self.back_button.pack(pady=gv.BUTTON_SPACE)
        else:
            if self.orc_data_labels == {}:
                self.no_data_label.pack_forget()
                self.back_button.pack_forget()
                for ocr_obj_name in status_update:
                    ocr_obj = status_update[ocr_obj_name]
                    label_string = "%s: %s" % (ocr_obj_name, ocr_obj['text'])
                    obj_label = gbl.DLabel(self, text=label_string)
                    self.orc_data_labels[ocr_obj_name] = obj_label
                    obj_label.pack(pady=gv.BUTTON_SPACE)
                self.back_button.pack(pady=gv.BUTTON_SPACE)
            else:
                found = False
                for ocr_label_name in list(self.orc_data_labels):
                    for ocr_obj_name in status_update:
                        if ocr_obj_name == ocr_label_name:
                            found = True
                            ocr_obj_text = str(status_update[ocr_obj_name]['text'])
                            print(type(ocr_obj_text))
                            self.orc_data_labels[ocr_label_name].configure(text=ocr_obj_text)
                            break
                    if not found:
                        self.orc_data_labels[ocr_label_name].destroy()
                        del self.orc_data_labels[ocr_label_name]
                    found = False
                for ocr_obj_name in status_update:
                    for ocr_label_name in list(self.orc_data_labels):
                        if ocr_obj_name == ocr_label_name:
                            found = True
                            break
                    if not found:
                        self.back_button.pack_forget()
                        ocr_obj_text = status_update[ocr_obj_name]['text']
                        ocr_label = gbl.DLabel(self, text=ocr_obj_text)
                        self.orc_data_labels[ocr_obj_name] = ocr_label
                        ocr_label.pack(pady=gv.BUTTON_SPACE)
                        self.back_button.pack(pady=gv.BUTTON_SPACE)
                    found = False


class OCRSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR/Video Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn_funcs = {
            'crop_setup': lambda: (
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

            'ocr_setup': lambda: (
                controller.show_frame("OCRSetup")
            ),

            'back': lambda: (
                # ,
                controller.show_frame("Settings")
            ),
        }

        btn_objs = {
            'crop_setup': gbl.GButton(self, text="Cropping Setup"),
            'mode': gbl.GButton(self, text="Loop Mode: "),
            'ocr_setup': gbl.GButton(self, text="OCR Setup"),
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
                controller.show_frame("OCRSettings"),
                controller.frames['OCRSetup'].update_obj_names()
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


class OCRSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=gv.BACKGROUND_COLOR)
        self.controller = controller
        label = gbl.GLabel(self, text="OCR Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.ocr_obj_names = []
        self.choosen_obj_label = gbl.DLabel(self, text='No Cropped Images')
        self.choosen_obj_label.pack(pady=gv.BUTTON_SPACE)

        next_func = lambda: (
            self.choose_next_ocr_obj()
        )
        prev_func = lambda: (
            self.choose_prev_ocr_obj()
        )
        confirm_func = lambda: (
            controller.show_frame("OCRSettings")
        )
        back_btn_func = lambda: (
            controller.show_frame("OCRSettings")
        )

        next_btn = gbl.GButton(self, text="Next Crop", command=next_func)
        prev_btn = gbl.GButton(self, text="Prev Crop", command=prev_func)
        confirm_btn = gbl.GButton(self, text="Confirm", command=confirm_func)
        back_btn = gbl.GButton(self, text="Go back", command=back_btn_func)

        next_btn.pack(pady=gv.BUTTON_SPACE)
        prev_btn.pack(pady=gv.BUTTON_SPACE)
        confirm_btn.pack(pady=gv.BUTTON_SPACE)
        back_btn.pack(pady=gv.BUTTON_SPACE)

        self.update_obj_names()

    def choose_next_ocr_obj(self):
        if self.choosen_obj_label['text'] == 'No Cropped Images':
            return
        else:
            myDeque = collections.deque(self.ocr_obj_names)
            index = myDeque.index(self.choosen_obj_label['text'])
            myDeque.rotate(-1)
            self.choosen_obj_label.configure(text=myDeque[index])

    def choose_prev_ocr_obj(self):
        if self.choosen_obj_label['text'] == 'No Cropped Images':
            return
        else:
            myDeque = collections.deque(self.ocr_obj_names)
            index = myDeque.index(self.choosen_obj_label['text'])
            myDeque.rotate(1)
            self.choosen_obj_label.configure(text=myDeque[index])

    # Not the most optimal way to do it for a very large lists, but works well for small lists
    # Basically remakes the whole list every time with the new ocr data objects
    def update_obj_names(self):
        dataSet = settings.loadSettings("OCRData.json")['dataset']
        obj_ref_list = []
        for obj_ref in dataSet:
            obj_ref_list.append(obj_ref)
        if obj_ref_list == []:
            self.choosen_obj_label.configure(text='No Cropped Images')
        else:
            for obj_ref in obj_ref_list:
                self.choosen_obj_label.configure(text=obj_ref)
                break
        self.ocr_obj_names = obj_ref_list


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
                fbFuncs.postFirebase(settings.loadSettings("OCRSettings.json")['fb_status_url'],
                                     {'run_mode': self.current_mode}, controller.firebase_database),
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


