from user_interface import UserInterface
from data import Data
from model import PredictionModel
import tkinter as tk
from tkinter import messagebox
import os


class App:
    def __init__(self):
        """Inicjalizuje aplikację, ładuje model i uruchamia GUI."""
        self.data = None
        self.model = self.load_existing_model()
        self.user_interface = UserInterface(self.model, self.train_model)

    def load_existing_model(self):
        """Ładuje istniejący model lub wyświetla komunikat o jego braku."""
        if os.path.exists("model.pkl"):
            model = PredictionModel(load_existing=True)
            if model.features is not None and not model.features.empty:
                print("✅ Załadowano istniejący model!")
                return model
            else:
                print("⚠️ Model był pusty lub uszkodzony – wymagane ponowne trenowanie!")
                messagebox.showwarning("Błąd", "Wykryto problem z modelem – kliknij 'Trenuj Model', aby go odbudować.")
                return None
        print("⚠️ Brak modelu – najpierw kliknij 'Trenuj Model'.")
        return None

    def train_model(self):
        """Pobiera dane, trenuje nowy model i aktualizuje GUI."""
        print("🔄 Pobieranie danych...")
        data_instance = Data()
        self.data = data_instance.load_computer_data()

        if self.data is None or self.data.empty:
            messagebox.showerror("Błąd", "Nie udało się pobrać danych!")
            return

        print("✅ Dane pobrane! Rozpoczynam trenowanie modelu...")
        self.model = PredictionModel(self.data, load_existing=False)

        if self.model is None or self.model.features is None or self.model.features.empty:
            messagebox.showerror("Błąd", "Nie udało się wytrenować modelu!")
            return

        # Aktualizacja modelu w GUI
        self.user_interface.update_model(self.model)
        messagebox.showinfo("Sukces", "Model został poprawnie wytrenowany!")

    def run(self):
        """Uruchamia główną pętlę GUI."""
        self.user_interface.mainloop()
