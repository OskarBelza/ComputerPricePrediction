import bs4
import requests
import numpy as np
import pandas as pd


class Data:
    def __init__(self):
        """
        Initializes the Data object and loads the main webpage.
        """
        self.url = "https://zikom.pl/poleasingowe-komputery-stacjonarne/"
        self.main_page = self.load_main_page()

    def load_main_page(self):
        """
        Loads the main webpage using requests and BeautifulSoup.
        Returns the parsed HTML content or None if an error occurs.
        """
        try:
            page = requests.get(self.url, timeout=5)
            page.raise_for_status()
            return bs4.BeautifulSoup(page.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error loading the page: {e}")
            return None

    def get_number_of_pages(self):
        """
        Extracts the number of available pages from the website.
        Assumes pagination is present in the HTML structure.
        """
        return int(self.main_page.find_all('a', class_="js-search-link")[-2].text.strip())

    def load_computer_data(self):
        """
        Scrapes computer specifications and prices from the website.
        Returns a Pandas DataFrame containing the extracted data.
        """
        computer_data = {
            'processor': [], 'disk': [], 'ram': [], 'os': [],
            'condition': [], 'graphic_card': [], 'price': []
        }

        # Loop through all pages of product listings
        for i in range(1, self.get_number_of_pages() + 1):
            page = requests.get(self.url + "?page=" + str(i))
            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            # Extract product information
            for block in soup.find_all('div', class_='decriptions-short'):
                # Extract processor details
                processor = block.find('td', class_='kp-tabela-tdleft', string=lambda s: 'Model procesora:' in s or 'Procesor:' in s)
                if processor and processor.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['processor'].append(processor.find_next('td', class_='kp-tabela-tdright').text.strip().replace("\xa0", ""))
                else:
                    computer_data['processor'].append(np.nan)

                # Extract disk details
                disk = block.find('td', class_='kp-tabela-tdleft', string=lambda s: 'Dysk:' in s or 'Pojemność dysku:' in s)
                if disk and disk.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['disk'].append(disk.find_next('td', class_='kp-tabela-tdright').text.strip().replace("\xa0", ""))
                else:
                    computer_data['disk'].append(np.nan)

                # Extract RAM details
                ram = block.find('td', class_='kp-tabela-tdleft', string=lambda s: 'Pamięć: RAM:' in s or 'Ilość pamięci RAM:' in s)
                if ram and ram.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['ram'].append(ram.find_next('td', class_='kp-tabela-tdright').text.strip())
                else:
                    computer_data['ram'].append(np.nan)

                # Extract OS details
                os = block.find('td', class_='kp-tabela-tdleft', string='System operacyjny:')
                if os and os.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['os'].append(os.find_next('td', class_='kp-tabela-tdright').text.strip().replace("\xa0", "").replace("Windows 11 Pro", "Windows 11Pro"))
                else:
                    computer_data['os'].append(np.nan)

                # Extract condition details
                condition = block.find('td', class_='kp-tabela-tdleft', string='Stan:')
                if condition and condition.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['condition'].append(condition.find_next('td', class_='kp-tabela-tdright').text.strip())
                else:
                    computer_data['condition'].append(np.nan)

                # Extract graphic card details
                graphic_card = block.find('td', class_='kp-tabela-tdleft', string='Karta graficzna:')
                if graphic_card and graphic_card.find_next('td', class_='kp-tabela-tdright'):
                    computer_data['graphic_card'].append(graphic_card.find_next('td', class_='kp-tabela-tdright').text.strip().replace("\xa0", ""))
                else:
                    computer_data['graphic_card'].append(np.nan)

                # Extract price details
                price_div = block.find_previous('div', class_='product-price-and-shipping hidden-md-up')
                if price_div:
                    price_span = price_div.find('span', class_='price')
                    if price_span:
                        computer_data['price'].append(float(price_span.text.replace(" ", "").replace(",", ".").replace("zł", "").replace("\xa0", "")))
                    else:
                        computer_data['price'].append(np.nan)
                else:
                    computer_data['price'].append(np.nan)

        return pd.DataFrame(computer_data)
