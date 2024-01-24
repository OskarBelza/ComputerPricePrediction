from user_interface import UserInterface
from data import Data
from model import PredictionModel

class App:
    def __init__(self):
        self.user_interface = UserInterface()

    def run(self):
        data = Data().load_computer_data()
        model = PredictionModel(data)
        model.check()
        # model.train_model()
        self.user_interface.mainloop()
