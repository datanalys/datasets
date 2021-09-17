#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import sys
import io
import time

url = 'https://api.nomics.com/v1/currencies/ticker?key=27f1ff74f18f01c5be6a2009fd0e424f9f1322a6&interval=1d,30d&convert=USD&per-page=100&page='


session = Session()


try:
    url_temp = url + '1'
    response = session.get(url)
    data = json.loads(response.text)
    df = pd.json_normalize(data)
    time.sleep(1) # Sleep for 1 seconds
    for i in range(2, 300):
        url_temp2 = url + str(i)
        response = session.get(url_temp2)
        print('page ', i)
        if(response.status_code == 200):
            data = json.loads(response.text)
            df2 = pd.json_normalize(data)
            df = df.append(df2, ignore_index = True)
            time.sleep(1.1) # Sleep for 1 seconds

    print(type(data))
    print(df)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)




dir = 'datasets/currencies/crypto/details.csv'
df.to_csv(dir, sep=',')