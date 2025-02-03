from user_interface import UserInterface
from data import Data
from model import PredictionModel
import tkinter as tk
from tkinter import messagebox
import os

class App:
    def __init__(self):
        # Próba załadowania modelu
        self.model = None
        if os.path.exists("model.pkl"):
            self.model = PredictionModel(load_existing=True)
            if self.model.features is None or self.model.features.empty:
                print("⚠️ Model był pusty lub uszkodzony – wymagane ponowne trenowanie!")
                messagebox.showwarning("Błąd", "Wykryto problem z modelem – kliknij 'Trenuj Model', aby ponownie go stworzyć.")
                self.model = None
            else:
                print("✅ Załadowano istniejący model!")
        else:
            print("⚠️ Brak modelu – najpierw kliknij 'Trenuj Model'.")

        # Inicjalizacja GUI
        self.user_interface = UserInterface(self.model, self.train_model)

    def train_model(self):
        """ Scrapuje dane, trenuje nowy model i aktualizuje GUI """
        print("🔄 Pobieranie danych...")
        data_instance = Data()
        self.data = data_instance.load_computer_data()

        if self.data is None or self.data.empty:
            messagebox.showerror("Błąd", "Nie udało się pobrać danych!")
            return

        print("✅ Dane pobrane! Rozpoczynam trenowanie modelu...")
        self.model = PredictionModel(self.data, load_existing=False)

        # Aktualizujemy model w GUI
        self.user_interface.update_model(self.model)

    def run(self):
        self.user_interface.mainloop()
