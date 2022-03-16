from datetime import datetime
from os import sep
import pandas as pd
import requests
import os
import check_api

print("all necessary packages are imported!")
print()

base_url = "https://lirarate.org/wp-json/lirarate/v2/rates?currency=LBP&_ver=t"    #version batch example: 202172612

# get today
today = datetime.today()
year = today.year
month = today.month
day = today.day
date_batch = str(year) + str(month) + str(day)

# add the the 1st part of the version batch to the base url
base_url = base_url + date_batch

# create the request
request = check_api.get_request(base_url)

# get request results
result_buy = request.json()['buy']
result_sell = request.json()['sell']

# create lirarate (buy) dataframe
lirarate_buy = pd.DataFrame(result_buy)
lirarate_buy = lirarate_buy.rename(columns={0: 'date', 1: 'buy'})
lirarate_buy['date'] = pd.to_datetime(lirarate_buy['date'] / 1000 ,unit='s')

# create lirarate (sell) dataframe
lirarate_sell = pd.DataFrame(result_sell)
lirarate_sell = lirarate_sell.rename(columns={0: 'date', 1: 'sell'})
lirarate_sell['date'] = pd.to_datetime(lirarate_sell['date'] / 1000 ,unit='s')

# merge buy and sell of lirarate dataframe
lirarate = lirarate_buy.merge(lirarate_sell, left_on='date', right_on='date')

# get cumulative change
lirarate['cumulative_buy'] = lirarate.buy - lirarate.buy.shift(1)

dir = './datasets/lebanon/lirarate.csv'

lirarate.to_csv(dir, sep=',')