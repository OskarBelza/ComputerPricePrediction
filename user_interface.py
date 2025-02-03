import ttkbootstrap as tb
import pandas as pd
from tkinter import messagebox


class Root(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Computer Price Prediction')
        self.geometry('500x550')  # Powiększone okno, aby zmieścić przycisk trenowania


class UserInterface(Root):
    def __init__(self, model, train_callback):
        super().__init__()
        self.model = model  # Przechowujemy model predykcyjny
        self.train_callback = train_callback  # Funkcja do trenowania modelu

        self.label_powitalny = tb.Label(self, text="Welcome to Computer Price Prediction", font=('Helvetica', 16),
                                        justify="center", bootstyle="default")
        self.label_powitalny.place(relx=0.5, rely=0.08, anchor="center")

        # Procesor (kategorie zamiast modeli)
        self.label_procesor = tb.Label(self, text="Procesor:")
        self.label_procesor.place(relx=0.3, rely=0.15, anchor="center")
        self.combobox_procesor = tb.Combobox(self, values=["Intel i3", "Intel i5", "Intel i7", "Intel i9", "Intel Xeon",
                                                            "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9"])
        self.combobox_procesor.place(relx=0.6, rely=0.15, anchor="center")

        # Karta graficzna (kategorie)
        self.label_karta_graficzna = tb.Label(self, text="Karta Graficzna:")
        self.label_karta_graficzna.place(relx=0.3, rely=0.25, anchor="center")
        self.combobox_karta_graficzna = tb.Combobox(self, values=["NVIDIA GTX", "NVIDIA RTX", "AMD Radeon",
                                                                  "NVIDIA Quadro", "Intel Integrated"])
        self.combobox_karta_graficzna.place(relx=0.6, rely=0.25, anchor="center")

        # RAM
        self.label_ram = tb.Label(self, text="RAM:")
        self.label_ram.place(relx=0.3, rely=0.35, anchor="center")
        self.combobox_ram = tb.Combobox(self, values=["8GB", "16GB", "32GB", "64GB"])
        self.combobox_ram.place(relx=0.6, rely=0.35, anchor="center")

        # Pamięć (Dysk)
        self.label_pamiec = tb.Label(self, text="Pamięć:")
        self.label_pamiec.place(relx=0.3, rely=0.45, anchor="center")
        self.combobox_pamiec = tb.Combobox(self, values=["HDD", "SSD", "NVMe"])
        self.combobox_pamiec.place(relx=0.6, rely=0.45, anchor="center")

        # System Operacyjny
        self.label_system_operacyjny = tb.Label(self, text="System Operacyjny:")
        self.label_system_operacyjny.place(relx=0.3, rely=0.55, anchor="center")
        self.combobox_system_operacyjny = tb.Combobox(self, values=["Windows", "Linux", "Brak OS"])
        self.combobox_system_operacyjny.place(relx=0.6, rely=0.55, anchor="center")

        # Stan sprzętu
        self.label_stan = tb.Label(self, text="Stan:")
        self.label_stan.place(relx=0.3, rely=0.65, anchor="center")
        self.combobox_stan = tb.Combobox(self, values=["Nowy", "Bardzo dobry", "Używany", "Uszkodzony"])
        self.combobox_stan.place(relx=0.6, rely=0.65, anchor="center")

        # Przycisk do przewidywania ceny (dezaktywowany, jeśli brak modelu)
        self.button_confirm = tb.Button(self, text="Confirm", command=self.confirm, bootstyle="secondary")
        self.button_confirm.place(relx=0.5, rely=0.8, anchor="center")

        if self.model is None:
            self.button_confirm["state"] = "disabled"

        # Przycisk do trenowania modelu
        self.button_train = tb.Button(self, text="Trenuj Model", command=self.train_model, bootstyle="primary")
        self.button_train.place(relx=0.5, rely=0.9, anchor="center")

    def confirm(self):
        self.predict_price()

    def predict_price(self):
        """ Pobiera wartości z GUI i przewiduje cenę """
        input_data = {
            "processor": self.combobox_procesor.get(),
            "graphic_card": self.combobox_karta_graficzna.get(),
            "ram": self.combobox_ram.get(),
            "disk": self.combobox_pamiec.get(),
            "os": self.combobox_system_operacyjny.get(),
            "condition": self.combobox_stan.get()
        }

        if "" in input_data.values():
            messagebox.showwarning("Brak danych", "Proszę uzupełnić wszystkie pola przed kontynuacją.")
            return

        input_df = pd.DataFrame([input_data])

        # DEBUG: Sprawdzenie cech modelu
        print(f"🛠️ Debug: Cechy modelu: {self.model.features.columns.tolist()}")

        # Sprawdzamy, czy model został poprawnie załadowany i ma cechy
        if self.model is None or self.model.features is None or self.model.features.empty:
            messagebox.showerror("Błąd", "Model nie został poprawnie załadowany! Najpierw kliknij 'Trenuj Model'.")
            print("❌ Debug: Model nie ma poprawnych cech!")
            return

        print(f"✅ Debug: Model ma cechy: {self.model.features.columns.tolist()}")

        # Sprawdzamy, czy wszystkie kolumny są zgodne
        missing_cols = set(self.model.features.columns) - set(input_df.columns)
        if missing_cols:
            messagebox.showerror("Błąd", f"Brakujące kolumny: {missing_cols}")
            return

        input_df = input_df[self.model.features.columns]  # Zapewnienie zgodności kolumn

        try:
            predicted_price = self.model.predict(input_df)[0]
            messagebox.showinfo("Przewidywana cena", f"Szacowana cena: {predicted_price:.2f} zł")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się przewidzieć ceny: {str(e)}")

    def update_model(self, new_model):
        """ Aktualizuje model w GUI po ponownym trenowaniu """
        self.model = new_model
        self.button_confirm["state"] = "normal"
        print("✅ Model zaktualizowany w GUI!")

    def train_model(self):
        """ Trenuje model i aktywuje przycisk „Confirm” """
        self.train_callback()
        self.button_confirm["state"] = "normal"
        messagebox.showinfo("Sukces", "Model został ponownie wytrenowany i zapisany!")

