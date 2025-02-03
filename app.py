from user_interface import UserInterface
from data import Data
from model import PredictionModel
import tkinter as tk
from tkinter import messagebox
import os


class App:
    """
    Main application class responsible for managing the GUI, model loading, and training.
    """

    def __init__(self):
        """
        Initializes the application by loading an existing model (if available)
        and setting up the user interface.
        """
        self.model = self.load_existing_model()  # Load existing model or prompt retraining
        self.user_interface = UserInterface(self.model, self.train_model)  # Initialize the GUI

    def load_existing_model(self):
        """
        Loads an existing trained model from file if available.
        If the model is missing or corrupted, the user will be prompted to retrain it.
        """
        if os.path.exists("model.pkl"):
            model = PredictionModel(load_existing=True)

            # Ensure the model has valid features before returning it
            if model.features is not None and not model.features.empty:
                return model
            else:
                print("⚠️ The model is empty or corrupted – retraining is required!")
                messagebox.showwarning("Error", "Detected issues with the model. Please retrain it.")
                return None

        print("⚠️ No existing model found – please train the model first.")
        return None

    def train_model(self):
        """
        Retrieves data, trains a new model, and updates the GUI with the new model.
        """
        print("🔄 Fetching data from the website...")
        data_instance = Data()  # Create a Data object
        self.data = data_instance.load_computer_data()  # Load the dataset

        # Validate if the dataset is correctly loaded
        if self.data is None or self.data.empty:
            messagebox.showerror("Error", "Failed to retrieve data from the website!")
            return

        print("✅ Data successfully retrieved! Starting model training...")
        self.model = PredictionModel(self.data, load_existing=False)  # Train a new model

        # Ensure the model was successfully trained
        if self.model is None or self.model.features is None or self.model.features.empty:
            messagebox.showerror("Error", "Model training failed! Please check the data.")
            return

        # Update the model in the GUI after retraining
        self.user_interface.update_model(self.model)

    def run(self):
        """
        Starts the main event loop for the GUI.
        """
        self.user_interface.mainloop()  # Start the GUI event loop
