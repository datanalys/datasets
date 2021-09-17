from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from datetime import datetime
import time
import numpy as np

# return the current date in the format year-month-day
def get_date():
    print("generating today...")
    today = datetime.today()
    return str(today.year) + '-' + str(today.month) + '-' + str(today.day)

# crete the file (if not already created)
def create_file(currency_name):
    print("Creting File...")
    file_name = 'datasets/currencies/crypto/historical/' + currency_name + '.csv'
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

def generate_endpoint(api_key, currency, from_date, to_date):
    return 'https://api.nomics.com/v1/exchange-rates/history?key=' + api_key + '&currency=' + currency + '&start=' + from_date +'T00%3A00%3A00Z&end='+ to_date + 'T00%3A00%3A00Z'


# initialize variables
session = Session()
api_key = '27f1ff74f18f01c5be6a2009fd0e424f9f1322a6'
currency = 'BTC'
from_date = '2009-01-01'
to_date = get_date()


url_getall = 'https://api.nomics.com/v1/currencies/ticker?key=27f1ff74f18f01c5be6a2009fd0e424f9f1322a6&interval=1d,30d&convert=USD&per-page=100&page=1'




currencies = get_crypto_list(session, url_getall)

for c in currencies:
    url = generate_endpoint(api_key, c, from_date, to_date)
    print("Retrieving ", c)
    response = session.get(url)
    if(response.status_code == 200):
        data = json.loads(response.text)
        df = pd.json_normalize(data)
        if(len(df.index) > 1):
            file_path = create_file(c)
            f = open(file_path, "a")
            df.to_csv(file_path, sep=',')
    time.sleep(1.3) # Sleep for 1 seconds


