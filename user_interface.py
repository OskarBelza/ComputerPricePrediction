import ttkbootstrap as tb
import pandas as pd
from tkinter import messagebox


class Root(tb.Window):
    def __init__(self):
        """
        Initializes the root window of the application with a predefined theme.
        """
        super().__init__(themename='darkly')  # Dark mode theme for better visibility
        self.title('Computer Price Prediction')
        self.geometry('500x550')  # Window size adjusted to fit all UI components


class UserInterface(Root):
    def __init__(self, model, train_callback):
        """
        Creates the graphical interface for user interaction.

        :param model: The machine learning model used for price prediction.
        :param train_callback: Function to retrain the model.
        """
        super().__init__()
        self.button_confirm = None
        self.combobox_condition = None
        self.combobox_os = None
        self.combobox_storage = None
        self.combobox_ram = None
        self.combobox_graphic_card = None
        self.combobox_processor = None
        self.button_train = None
        self.model = model  # Store the predictive model
        self.train_callback = train_callback  # Function for training the model

        # Welcome Label
        self.label_welcome = tb.Label(self, text="Welcome to Computer Price Prediction",
                                      font=('Helvetica', 16), justify="center", bootstyle="default")
        self.label_welcome.place(relx=0.5, rely=0.08, anchor="center")

        # Dropdown menus for selecting computer specifications
        self.create_comboboxes()

        # Buttons for confirming price prediction and training the model
        self.create_buttons()

    def create_comboboxes(self):
        """
        Creates dropdown selection boxes for various computer specifications.
        """
        # Processor
        self.create_label("Processor:", 0.15)
        self.combobox_processor = self.create_combobox(["Intel i3", "Intel i5", "Intel i7", "Intel i9", "Intel Xeon",
                                                        "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9"],
                                                       0.15)

        # Graphics Card
        self.create_label("Graphics Card:", 0.25)
        self.combobox_graphic_card = self.create_combobox(["NVIDIA GTX", "NVIDIA RTX", "AMD Radeon",
                                                           "NVIDIA Quadro", "Intel Integrated"], 0.25)

        # RAM
        self.create_label("RAM:", 0.35)
        self.combobox_ram = self.create_combobox(["8GB", "16GB", "32GB", "64GB"], 0.35)

        # Storage
        self.create_label("Storage:", 0.45)
        self.combobox_storage = self.create_combobox(["HDD", "SSD", "NVMe"], 0.45)

        # Operating System
        self.create_label("Operating System:", 0.55)
        self.combobox_os = self.create_combobox(["Windows", "Linux", "No OS"], 0.55)

        # Condition
        self.create_label("Condition:", 0.65)
        self.combobox_condition = self.create_combobox(["New", "Very Good", "Used", "Damaged"], 0.65)

    def create_label(self, text, rel_y):
        """
        Helper function to create labels for input fields.
        """
        label = tb.Label(self, text=text)
        label.place(relx=0.3, rely=rel_y, anchor="center")

    def create_combobox(self, values, rel_y):
        """
        Helper function to create dropdown comboboxes.
        """
        combobox = tb.Combobox(self, values=values)
        combobox.place(relx=0.6, rely=rel_y, anchor="center")
        return combobox

    def create_buttons(self):
        """
        Creates buttons for confirming predictions and training the model.
        """
        # Confirm button for price prediction
        self.button_confirm = tb.Button(self, text="Confirm", command=self.confirm, bootstyle="secondary")
        self.button_confirm.place(relx=0.5, rely=0.8, anchor="center")

        # Disable confirm button if no model is loaded
        if self.model is None:
            self.button_confirm["state"] = "disabled"

        # Train Model button
        self.button_train = tb.Button(self, text="Train Model", command=self.train_model, bootstyle="primary")
        self.button_train.place(relx=0.5, rely=0.9, anchor="center")

    def confirm(self):
        """
        Handles confirmation button click and triggers price prediction.
        """
        self.predict_price()

    def predict_price(self):
        """
        Predicts the price of a computer based on user input.
        """
        input_data = {
            "processor": self.combobox_processor.get(),
            "graphic_card": self.combobox_graphic_card.get(),
            "ram": self.combobox_ram.get(),
            "disk": self.combobox_storage.get(),
            "os": self.combobox_os.get(),
            "condition": self.combobox_condition.get()
        }

        # Check if all fields are filled
        if "" in input_data.values():
            messagebox.showwarning("Missing Data", "Please fill in all fields before proceeding.")
            return

        input_df = pd.DataFrame([input_data])

        # Ensure the model is loaded and ready
        if self.model is None or self.model.features is None or self.model.features.empty:
            messagebox.showerror("Error", "The model is not properly loaded! Please train it first.")
            return

        # Ensure the input columns match the model’s expected features
        missing_cols = set(self.model.features.columns) - set(input_df.columns)
        if missing_cols:
            messagebox.showerror("Error", f"Missing columns: {missing_cols}")
            return

        # Align input data with model features
        input_df = input_df[self.model.features.columns]

        try:
            predicted_price = self.model.predict(input_df)[0]
            messagebox.showinfo("Predicted Price", f"Estimated price: {predicted_price:.2f} zł")
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

    def update_model(self, new_model):
        """
        Updates the model in the UI after retraining.
        """
        self.model = new_model
        self.button_confirm["state"] = "normal"  # Enable the confirm button
        print("✅ Model updated in GUI!")

    def train_model(self):
        """
        Trains the model and updates the UI.
        """
        self.train_callback()
        self.button_confirm["state"] = "normal"
        messagebox.showinfo("Success", "The model has been retrained and saved!")
