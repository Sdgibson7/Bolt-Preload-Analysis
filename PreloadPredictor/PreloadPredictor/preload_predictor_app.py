"""__preloadpredictor__.py: Presentation layer of the application. Utilizes customtkinter."""

__author__      = "Samuel Gibson"

import customtkinter
import preload_predictor_logic

# main application
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # the current model set by the user
        self.current_model = ""

        # configure window
        self.title("Preload Predictor")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x11)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(11, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Configure Model", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.input_model_button = customtkinter.CTkButton(self.sidebar_frame, text="Input Model", command=self.input_model_button_event, fg_color="green", hover_color="dark green")
        self.input_model_button.grid(row=1, column=0)
        self.model_textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=156, height=32, state="disabled")
        self.model_textbox.grid(row=1, column=1)

        # create widgets for coefficient settings
        self.c_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="Coefficient", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.c_label1.grid(row=2, column=0, padx=20, pady=10, stick="nsew")
        self.c_label2 = customtkinter.CTkLabel(self.sidebar_frame, text="Value", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.c_label2.grid(row=2, column=1, padx=20, pady=10, stick="nsew")

        #sealent
        self.s_label = customtkinter.CTkLabel(self.sidebar_frame, text= "sealant", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.s_label.grid(row=3, column=0)
        self.s_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["sealent1", "sealent2", "sealent3"])
        self.s_options.set("sealent1")
        self.s_options.grid(row=3, column=1, padx=20, pady=20)

        #plate material
        self.p_label = customtkinter.CTkLabel(self.sidebar_frame, text= "plate material", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.p_label.grid(row=4, column=0)
        self.p_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["aluminum", "carbon fiber", "material3"])
        self.p_options.set("aluminum")
        self.p_options.grid(row=4, column=1, padx=20, pady=20)

        #parameter3
        self.p3_label = customtkinter.CTkLabel(self.sidebar_frame, text= "parameter3", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.p3_label.grid(row=5, column=0)
        self.p3_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["value1", "value2", "value3"])
        self.p3_options.set("value1")
        self.p3_options.grid(row=5, column=1, padx=20, pady=20)

        #parameter4
        self.p4_label = customtkinter.CTkLabel(self.sidebar_frame, text= "parameter4", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.p4_label.grid(row=6, column=0)
        self.p4_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["value1", "value2", "value3"])
        self.p4_options.set("value2")
        self.p4_options.grid(row=6, column=1, padx=20, pady=20)

        # run button
        self.input_model_button = customtkinter.CTkButton(self.sidebar_frame, text="Run Prediction", command=self.input_model_button_event, fg_color="orange", hover_color="dark orange")
        self.input_model_button.grid(row=7, column=1, pady=20)

        # apperance options widgets
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, pady=20)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=1, pady=20)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=1)

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

    # handle events
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def input_model_button_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter preload loss model:", title="CTkInputDialog")
        input = dialog.get_input()

        # update the textbox to reflect the input
        self.current_model = input
        self.model_textbox.configure(state="normal")
        self.model_textbox.delete("0.0", "100.0")
        self.model_textbox.insert("0.0", text=input)
        self.model_textbox.configure(state="disabled")

        # clear any previous data
        preload_predictor_logic.clear()
        
        # parse the inputted equation
        preload_predictor_logic.parseEquation(input)

        # TODO update the list box with each coefficient found in the equation to allow the user to set the value
        coefficients = preload_predictor_logic.getCoefficients()
        self.c_options.configure(values=coefficients)
        self.c_options.set(coefficients[0])

    def value_set_button(self):
        new_value = self.c_entry.get() # the value in the entry box
        print("Setting " + self.c_options.get() + " to " + new_value)
        preload_predictor_logic.setCoefficientValue(self.c_options.get(), new_value)