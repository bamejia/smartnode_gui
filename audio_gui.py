import tkinter as tk
import test


class AudioRuntime(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Runtime", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn1_fnc = lambda: (test.louis_replace_this_with_your_function_name())
        btn2_fnc = lambda: (test.louis_replace_this_with_your_function_name())
        btn3_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.show_frame("AudioStatus"))
        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame(controller.return_frame))

        btn1 = tk.Button(self, text="Start/Stop",
                            command=btn1_fnc)
        btn2 = tk.Button(self, text="Mode: ",
                         command=btn2_fnc)
        btn3 = tk.Button(self, text="Show Status",
                         command=btn3_fnc)
        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        btn1.pack()
        btn2.pack()
        btn3.pack()
        back_btn.pack()


class AudioStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Status", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("AudioRuntime"))

        back_button = tk.Button(self, text="Go back",
                                command=back_btn_func)

        back_button.pack()


class AudioSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        btn1_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.show_frame("SampleSetup"))
        btn2_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.show_frame("AudioModeSetup"))
        btn3_fnc = lambda: (test.louis_replace_this_with_your_function_name(),
                            controller.set_return_frame("AudioSettings"),
                            controller.show_frame("AudioRuntime"))
        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("Settings"))

        btn1 = tk.Button(self, text="Record Sample",
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


class SampleSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sample Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("AudioSettings"))

        back_btn = tk.Button(self, text="Go back",
                           command=back_btn_func)

        back_btn.pack()


class AudioModeSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Audio Mode Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        back_btn_func = lambda: (test.louis_replace_this_with_your_function_name(),
                                 controller.show_frame("AudioSettings"))

        back_btn = tk.Button(self, text="Go back",
                             command=back_btn_func)

        back_btn.pack()