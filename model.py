from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd


class PredictionModel:
    def __init__(self, data):
        self.features = data.iloc[:, :-1]
        print(self.features)
        self.target = data.iloc[:, -1]
        self.model = LinearRegression()

    def train_model(self, test_size=0.2, random_state=None):
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target, test_size=test_size,
                                                            random_state=random_state)
        self.model.fit(X_train, y_train)

        # Predictions
        y_pred = self.model.predict(X_test)

        # Evaluation
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')

    def adjust_data(self, data):
        data = data.apply(pd.to_numeric(), errors='coerce').astype('float64')
        data = data.fillna(0, inplace=True)
        print(data)
        return data

    def check(self):
        unique_values = self.features['processor'].unique()

        # Stwórz słownik mapujący unikalne wartości na liczby
        mapping_dict = {value: idx for idx, value in enumerate(unique_values)}
        print(mapping_dict)
        for items in mapping_dict.items():
            print(items)