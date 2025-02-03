import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

MODEL_FILENAME = "model.pkl"


class PredictionModel:
    CATEGORICAL_MAPPINGS = {
        "processor": {
            "i3": "Intel i3", "i5": "Intel i5", "i7": "Intel i7", "i9": "Intel i9",
            "Ryzen 3": "AMD Ryzen 3", "Ryzen 5": "AMD Ryzen 5", "Ryzen 7": "AMD Ryzen 7", "Ryzen 9": "AMD Ryzen 9",
            "Xeon": "Intel Xeon"
        },
        "graphic_card": {
            "GTX": "NVIDIA GTX", "RTX": "NVIDIA RTX", "Radeon": "AMD Radeon", "Quadro": "NVIDIA Quadro"
        },
        "ram": {"8GB": "8GB", "16GB": "16GB", "32GB": "32GB", "64GB": "64GB"},
        "disk": {"HDD": "HDD", "NVMe": "NVMe", "SSD": "SSD"},
        "os": {"Windows": "Windows", "Linux": "Linux", "Brak": "Brak OS"},
        "condition": {"Nowy": "Nowy", "Bardzo dobry": "Bardzo dobry", "Używany": "Używany", "Uszkodzony": "Uszkodzony"}
    }

    def __init__(self, data=None, load_existing=True):
        """Inicjalizacja modelu – ładowanie z pliku lub trenowanie nowego."""
        self.features = None  # Inicjalizacja cech
        self.target = None  # Inicjalizacja celu
        self.encoder = None  # Inicjalizacja kodera cech
        self.model = None  # Model ML

        if load_existing and os.path.exists(MODEL_FILENAME):
            loaded_model = self.load_model()
            if loaded_model:
                self.__dict__.update(loaded_model.__dict__)
                print("✅ Załadowano istniejący model!")
                return

        if data is not None:
            self.train_new_model(data)
        else:
            print("⚠️ Brak modelu – najpierw kliknij 'Trenuj Model'.")

    def categorize_feature(self, feature_type, value):
        """Kategoryzuje wartości na podstawie mapowań."""
        if isinstance(value, str):
            for key, category in self.CATEGORICAL_MAPPINGS.get(feature_type, {}).items():
                if key in value:
                    return category
        return "Inny"

    def train_new_model(self, data):
        """Trenuje nowy model, zapisuje i oblicza metryki."""
        print("🔄 Trenuję nowy model...")

        if data is None or data.empty:
            print("❌ Błąd: Brak danych do trenowania!")
            return

        # Kategoryzacja cech
        for column in self.CATEGORICAL_MAPPINGS.keys():
            data[column] = data[column].apply(lambda x: self.categorize_feature(column, x))

        self.features = data.iloc[:, :-1]
        self.target = data.iloc[:, -1]

        if self.features.empty:
            print("❌ Błąd: Model nie posiada cech po przetworzeniu danych!")
            return

        # OneHotEncoder zamiast LabelEncoder
        categorical_features = [col for col in self.features.columns if self.features[col].dtype == 'object']
        self.encoder = ColumnTransformer([("encoder", OneHotEncoder(handle_unknown='ignore'), categorical_features)],
                                         remainder='passthrough')

        X_transformed = self.encoder.fit_transform(self.features)

        # Podział danych
        X_train, X_test, y_train, y_test = train_test_split(X_transformed, self.target, test_size=0.2, random_state=42)

        if X_train.shape[0] == 0:
            print("❌ Błąd: Dane treningowe są puste!")
            return

        # Trenowanie modelu
        self.model = LinearRegression().fit(X_train, y_train)

        # Obliczenie metryk
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"📊 Model wytrenowany! MSE: {mse:.2f}, R²: {r2:.2f}")

        self.save_model()

    def save_model(self):
        """Zapisuje model do pliku."""
        if not hasattr(self, "features") or self.features.empty:
            print("❌ Błąd: Model nie posiada poprawnych cech i nie może zostać zapisany!")
            return

        try:
            with open(MODEL_FILENAME, "wb") as file:
                pickle.dump(self, file)
            print(f"✅ Model zapisany do {MODEL_FILENAME}")
        except Exception as e:
            print(f"❌ Błąd zapisu modelu: {e}")

    @staticmethod
    def load_model():
        """Ładuje model z pliku."""
        try:
            with open(MODEL_FILENAME, "rb") as file:
                loaded_model = pickle.load(file)

            if not hasattr(loaded_model, "features") or loaded_model.features.empty:
                print("❌ Błąd: Model nie posiada poprawnych cech! Usuwam plik.")
                os.remove(MODEL_FILENAME)
                return None

            print(f"✅ Model poprawnie załadowany! Cechy: {loaded_model.features.columns.tolist()}")
            return loaded_model
        except Exception as e:
            print(f"❌ Błąd ładowania modelu: {e}")
            return None

    def predict(self, input_df):
        """Dokonuje predykcji na podstawie danych wejściowych."""
        if self.model is None:
            raise ValueError("❌ Model nie został załadowany!")

        for column in self.CATEGORICAL_MAPPINGS.keys():
            input_df[column] = input_df[column].apply(lambda x: self.categorize_feature(column, x))

        if self.encoder is None:
            raise ValueError("❌ Brak encodera! Model musi być wytrenowany przed użyciem.")

        input_transformed = self.encoder.transform(input_df)

        prediction = self.model.predict(input_transformed)
        return np.maximum(prediction, 0)  # Zapewniamy, że wartości są nieujemne



