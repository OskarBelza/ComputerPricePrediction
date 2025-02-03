import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

# Define the filename for saving/loading the trained model
MODEL_FILENAME = "model.pkl"

class PredictionModel:
    """
    A class that handles machine learning predictions, model training,
    and saving/loading the model.
    """

    # Mappings to standardize categorical values
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
        "os": {"Windows": "Windows", "Linux": "Linux", "Brak": "No OS"},
        "condition": {"Nowy": "New", "Bardzo dobry": "Very Good", "Używany": "Used", "Uszkodzony": "Damaged"}
    }

    def __init__(self, data=None, load_existing=True):
        """
        Initializes the prediction model. Loads an existing model if available,
        otherwise trains a new one if data is provided.
        """
        self.features = None  # Model features
        self.target = None  # Model target variable (price)
        self.encoder = None  # OneHotEncoder instance
        self.model = None  # The trained Linear Regression model

        if load_existing and os.path.exists(MODEL_FILENAME):
            loaded_model = self.load_model()
            if loaded_model:
                self.__dict__.update(loaded_model.__dict__)
                return

        # If no existing model is found, check if data is provided to train a new model
        if data is not None:
            self.train_new_model(data)
        else:
            print("⚠️ No model found – train it first.")

    def categorize_feature(self, feature_type, value):
        """
        Standardizes categorical feature values based on predefined mappings.
        """
        if isinstance(value, str):
            for key, category in self.CATEGORICAL_MAPPINGS.get(feature_type, {}).items():
                if key in value:
                    return category
        return "Other"

    def train_new_model(self, data):
        """
        Trains a new Linear Regression model on the provided dataset.
        """
        print("🔄 Training a new model...")

        if data is None or data.empty:
            print("❌ Error: No data available for training!")
            return

        # Standardize categorical data
        for column in self.CATEGORICAL_MAPPINGS.keys():
            data[column] = data[column].apply(lambda x: self.categorize_feature(column, x))

        self.features = data.iloc[:, :-1]  # All columns except the last one
        self.target = data.iloc[:, -1]  # The last column (price)

        if self.features.empty:
            print("❌ Error: No valid features after preprocessing!")
            return

        # Encode categorical features using OneHotEncoder
        categorical_features = [col for col in self.features.columns if self.features[col].dtype == 'object']
        self.encoder = ColumnTransformer([("encoder", OneHotEncoder(handle_unknown='ignore'), categorical_features)],
                                         remainder='passthrough')

        X_transformed = self.encoder.fit_transform(self.features)

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_transformed, self.target, test_size=0.2, random_state=42)

        if X_train.shape[0] == 0:
            print("❌ Error: Training data is empty!")
            return

        # Train the Linear Regression model
        self.model = LinearRegression().fit(X_train, y_train)

        # Evaluate model performance
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"📊 Model trained successfully! MSE: {mse:.2f}, R²: {r2:.2f}")

        self.save_model()

    def save_model(self):
        """
        Saves the trained model to a file using pickle.
        """
        if not hasattr(self, "features") or self.features.empty:
            print("❌ Error: The model has no valid features and cannot be saved!")
            return

        try:
            with open(MODEL_FILENAME, "wb") as file:
                pickle.dump(self, file)
            print(f"✅ Model saved to {MODEL_FILENAME}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")

    @staticmethod
    def load_model():
        """
        Loads a previously saved model from a file.
        """
        try:
            with open(MODEL_FILENAME, "rb") as file:
                loaded_model = pickle.load(file)

            if not hasattr(loaded_model, "features") or loaded_model.features.empty:
                print("❌ Error: Model lacks valid features! Deleting file.")
                os.remove(MODEL_FILENAME)
                return None

            print(f"✅ Model loaded successfully!")
            return loaded_model
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None

    def predict(self, input_df):
        """
        Predicts the price based on input data.
        """
        if self.model is None:
            raise ValueError("❌ Error: No trained model loaded!")

        # Ensure input data matches expected categories
        for column in self.CATEGORICAL_MAPPINGS.keys():
            input_df[column] = input_df[column].apply(lambda x: self.categorize_feature(column, x))

        if self.encoder is None:
            raise ValueError("❌ Error: Encoder is missing! Train the model first.")

        input_transformed = self.encoder.transform(input_df)

        # Perform prediction and ensure the price is not negative
        prediction = self.model.predict(input_transformed)
        return np.maximum(prediction, 0)  # Ensure non-negative prices
