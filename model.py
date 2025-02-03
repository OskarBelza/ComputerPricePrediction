import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd

MODEL_FILENAME = "model.pkl"

class PredictionModel:
    def __init__(self, data=None, load_existing=True):
        """Ładuje model z pliku lub trenuje nowy, jeśli dane są dostępne"""
        if load_existing and os.path.exists(MODEL_FILENAME):
            loaded_model = self.load_model()
            if loaded_model:
                self.__dict__.update(loaded_model.__dict__)
                print("✅ Załadowano istniejący model!")
                return
            else:
                print("⚠️ Model był pusty lub uszkodzony – wymagane ponowne trenowanie!")

        if data is not None:
            self.train_new_model(data)
        else:
            print("⚠️ Brak modelu – najpierw kliknij 'Trenuj Model'.")

    def categorize_processor(self, processor_name):
        """ Grupuje procesory w ogólne kategorie """
        if isinstance(processor_name, str):
            if "i3" in processor_name:
                return "Intel i3"
            elif "i5" in processor_name:
                return "Intel i5"
            elif "i7" in processor_name:
                return "Intel i7"
            elif "i9" in processor_name:
                return "Intel i9"
            elif "Ryzen 3" in processor_name:
                return "AMD Ryzen 3"
            elif "Ryzen 5" in processor_name:
                return "AMD Ryzen 5"
            elif "Ryzen 7" in processor_name:
                return "AMD Ryzen 7"
            elif "Ryzen 9" in processor_name:
                return "AMD Ryzen 9"
            elif "Xeon" in processor_name:
                return "Intel Xeon"
        return "Inny"

    def categorize_graphic_card(self, graphic_card_name):
        """ Grupuje karty graficzne w ogólne kategorie """
        if isinstance(graphic_card_name, str):
            if "GTX" in graphic_card_name:
                return "NVIDIA GTX"
            elif "RTX" in graphic_card_name:
                return "NVIDIA RTX"
            elif "Radeon" in graphic_card_name:
                return "AMD Radeon"
            elif "Quadro" in graphic_card_name:
                return "NVIDIA Quadro"
            elif "Integrated" in graphic_card_name or "Intel" in graphic_card_name:
                return "Intel Integrated"
        return "Inna"

    def categorize_ram(self, ram_value):
        """ Grupuje wartości RAM w standardowe opcje """
        if isinstance(ram_value, str):
            if "8GB" in ram_value:
                return "8GB"
            elif "16GB" in ram_value:
                return "16GB"
            elif "32GB" in ram_value:
                return "32GB"
            elif "64GB" in ram_value:
                return "64GB"
        return "Inna"

    def categorize_disk(self, disk_type):
        """ Grupuje dyski na SSD, HDD, NVMe """
        if isinstance(disk_type, str):
            if "HDD" in disk_type:
                return "HDD"
            elif "NVMe" in disk_type:
                return "NVMe"
            elif "SSD" in disk_type:
                return "SSD"
        return "Inny"

    def categorize_os(self, os_name):
        """ Grupuje systemy operacyjne """
        if isinstance(os_name, str):
            if "Windows" in os_name:
                return "Windows"
            elif "Linux" in os_name:
                return "Linux"
            elif "Brak" in os_name:
                return "Brak OS"
        return "Inny"

    def categorize_condition(self, condition_name):
        """ Grupuje stan sprzętu """
        if isinstance(condition_name, str):
            if "Nowy" in condition_name:
                return "Nowy"
            elif "Bardzo dobry" in condition_name:
                return "Bardzo dobry"
            elif "Używany" in condition_name:
                return "Używany"
            elif "Uszkodzony" in condition_name:
                return "Uszkodzony"
        return "Nieznany"

    def train_new_model(self, data):
        """Trenuje nowy model i zapisuje go do pliku"""
        print("🔄 Trenuję nowy model...")

        if data is None or data.empty:
            print("❌ Błąd: Brak danych do trenowania!")
            return

        data["processor"] = data["processor"].apply(self.categorize_processor)
        data["graphic_card"] = data["graphic_card"].apply(self.categorize_graphic_card)
        data["ram"] = data["ram"].apply(self.categorize_ram)
        data["disk"] = data["disk"].apply(self.categorize_disk)
        data["os"] = data["os"].apply(self.categorize_os)
        data["condition"] = data["condition"].apply(self.categorize_condition)

        self.features = data.iloc[:, :-1]
        self.target = data.iloc[:, -1]
        self.model = LinearRegression()

        if self.features is None or self.features.empty:
            print("❌ Błąd: Model nie posiada cech po przetworzeniu danych!")
            return

        self.encoders = {}
        for column in self.features.columns:
            if self.features[column].dtype == 'object':
                self.encoders[column] = LabelEncoder()
                self.features[column] = self.encoders[column].fit_transform(self.features[column])

        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target, test_size=0.2, random_state=42)

        if X_train.empty:
            print("❌ Błąd: Dane treningowe są puste!")
            return

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"📊 Model wytrenowany! MSE: {mse:.2f}, R^2: {r2:.2f}")

        if self.features is None or self.features.empty:
            print("❌ Błąd: Model nie posiada cech i nie może zostać zapisany!")
            return

        self.save_model()

    def save_model(self):
        """Zapisuje cały model do pliku, zapewniając poprawność cech"""
        if not hasattr(self, "features") or self.features is None or self.features.empty:
            print("❌ Błąd: Model nie posiada poprawnych cech i nie może zostać zapisany!")
            return

        try:
            with open(MODEL_FILENAME, "wb") as file:
                pickle.dump(self, file)

            print(f"✅ Model został poprawnie zapisany do {MODEL_FILENAME}")

        except Exception as e:
            print(f"❌ Wystąpił błąd podczas zapisu modelu: {e}")

    @staticmethod
    def load_model():
        """Wczytuje cały model z pliku i sprawdza poprawność"""
        try:
            with open(MODEL_FILENAME, "rb") as file:
                loaded_model = pickle.load(file)

            if not hasattr(loaded_model, "features") or loaded_model.features is None or loaded_model.features.empty:
                print("❌ Błąd: Model został załadowany, ale cechy są niepoprawne! Plik zostanie usunięty.")
                os.remove(MODEL_FILENAME)
                return None

            print(f"✅ Model poprawnie załadowany! Cechy: {loaded_model.features.columns.tolist()}")
            return loaded_model

        except Exception as e:
            print(f"❌ Błąd podczas ładowania modelu: {e}")
            return None

    def predict(self, input_df):
        """Konwertuje dane wejściowe i przewiduje cenę"""
        input_df["processor"] = input_df["processor"].apply(self.categorize_processor)
        input_df["graphic_card"] = input_df["graphic_card"].apply(self.categorize_graphic_card)
        input_df["ram"] = input_df["ram"].apply(self.categorize_ram)
        input_df["disk"] = input_df["disk"].apply(self.categorize_disk)
        input_df["os"] = input_df["os"].apply(self.categorize_os)
        input_df["condition"] = input_df["condition"].apply(self.categorize_condition)

        for column, encoder in self.encoders.items():
            if column in input_df.columns:
                input_df[column] = input_df[column].map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)

        return self.model.predict(input_df)



