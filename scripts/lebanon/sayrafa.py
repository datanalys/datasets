from datetime import datetime
from os import sep
import pandas as pd
import requests
import os

print("all necessary packages are imported!")
print()

base_url = "https://lirarate.org/wp-json/lirarate/v2/sayrafa?currency=LBP&_ver=t"    #version batch example: 202172612

# get today
today = datetime.today()
year = today.year
month = today.month
day = today.day
date_batch = str(year) + str(month) + str(day)

# add the the 1st part of the version batch to the base url
base_url = base_url + date_batch

# find the wordpress batch request number
for i in range(30, 0, -1):
    test_base_url = base_url + str(i)
    request = requests.get(test_base_url)
    print(test_base_url, request)
    if request.status_code == 200:
        base_url = test_base_url
        break

print("request call: ", base_url)

# create the request
request = requests.get(base_url)

# get request results
result = request.json()['sayrafa']


# create sayrafa dataframe
sayrafa = pd.DataFrame(result)
sayrafa = sayrafa.rename(columns={0: 'date', 1: 'rate'})
sayrafa['date'] = pd.to_datetime(sayrafa['date'] / 1000 ,unit='s')



# get cumulative change
sayrafa['cumulative_rate'] = sayrafa.rate - sayrafa.rate.shift(1)

dir = './datasets/lebanon/sayrafa.csv'

sayrafa.to_csv(dir, sep=',')