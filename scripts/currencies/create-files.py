from requests import Request, Session
import json
import pandas as pd
import time
from pathlib import Path
import os


# crete the file (if not already created)
def create_file(currency_name):
    file_name = 'datasets/currencies/crypto/historical/' + currency_name + '.csv'
    Path(file_name).touch()
    print("File Created: datasets/currencies/crypto/historical/", currency_name)
    return file_name

# return the cryptocurrencies list as an array
def get_crypto_list(session, url):
    print("requesting list of cryptocurrencies")
    response = session.get(url)

    if(response.status_code == 200):
        print("Request Status: 200")
        data = json.loads(response.text)
        df = pd.json_normalize(data)
        print("Data Retrieved")
    time.sleep(2)
    return df['id'].to_numpy()

# initialize variables
session = Session()
api_key = '27f1ff74f18f01c5be6a2009fd0e424f9f1322a6'
url = 'https://api.nomics.com/v1/currencies/ticker?key=27f1ff74f18f01c5be6a2009fd0e424f9f1322a6&interval=1d,30d&convert=USD&per-page=100&page=1'


currencies = get_crypto_list(session, url)

for c in currencies:
        file_path = create_file(c)

