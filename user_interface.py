import ttkbootstrap as tb


class Root(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Computer Price Prediction')
        self.geometry('400x400')

class UserInterface(Root):
    def __init__(self):
        super().__init__()
        self.label_powitalny = tb.Label(self, text="Welcome to computer price prediction", font=('Helvetica', 16),
                                        justify="center", bootstyle="default")
        self.label_powitalny.place(relx=0.5, rely=0.08, anchor="center")

        self.label_procesor = tb.Label(self, text="Procesor:")
        self.label_procesor.place(relx=0.3, rely=0.2, anchor="center")
        self.combobox_procesor = tb.Combobox(self, values=["Intel i5", "Intel i7", "AMD Ryzen 5", "AMD Ryzen 7"])
        self.combobox_procesor.place(relx=0.6, rely=0.2, anchor="center")

        # Karta graficzna
        self.label_karta_graficzna = tb.Label(self, text="Karta Graficzna:")
        self.label_karta_graficzna.place(relx=0.3, rely=0.3, anchor="center")
        self.combobox_karta_graficzna = tb.Combobox(self,
                                                     values=["NVIDIA GTX 1660", "AMD Radeon RX 580", "NVIDIA RTX 3060"])
        self.combobox_karta_graficzna.place(relx=0.6, rely=0.3, anchor="center")

        # RAM
        self.label_ram = tb.Label(self, text="RAM:")
        self.label_ram.place(relx=0.3, rely=0.4, anchor="center")
        self.combobox_ram = tb.Combobox(self, values=["8 GB", "16 GB", "32 GB", "64 GB"])
        self.combobox_ram.place(relx=0.6, rely=0.4, anchor="center")

        # Zasilacz
        self.label_zasilacz = tb.Label(self, text="Zasilacz:")
        self.label_zasilacz.place(relx=0.3, rely=0.5, anchor="center")
        self.combobox_zasilacz = tb.Combobox(self, values=["500W", "650W", "750W", "1000W"])
        self.combobox_zasilacz.place(relx=0.6, rely=0.5, anchor="center")

        # Pamięć
        self.label_pamiec = tb.Label(self, text="Pamięć:")
        self.label_pamiec.place(relx=0.3, rely=0.6, anchor="center")
        self.combobox_pamiec = tb.Combobox(self, values=["SSD 256GB", "SSD 512GB", "HDD 1TB", "HDD 2TB"])
        self.combobox_pamiec.place(relx=0.6, rely=0.6, anchor="center")

        # Obudowa
        self.label_obudowa = tb.Label(self, text="Obudowa:")
        self.label_obudowa.place(relx=0.3, rely=0.7, anchor="center")
        self.combobox_obudowa = tb.Combobox(self, values=["Mini Tower", "Mid Tower", "Full Tower"])
        self.combobox_obudowa.place(relx=0.6, rely=0.7, anchor="center")

        self.button_confirm = tb.Button(self, text="Confirm", command=self.confirm, bootstyle="secondary")
        self.button_confirm.place(relx=0.5, rely=0.85, anchor="center")


    def confirm(self):
        pass