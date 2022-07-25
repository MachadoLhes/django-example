from django.conf import settings
from datetime import datetime
import requests

def parse_stock(stock_line):
    stock_split = stock_line.lower().split('\n')

    keys = stock_split[0].replace('\r','').split(',')
    values = stock_split[1].replace('\r','').split(',')

    stock = dict(zip(keys, values))

    return stock

def combine_datetime(date, time):
    return datetime.strptime(f"{date} {time}","%Y-%m-%d %H:%M:%S")

def get_stock(stock_code):
    url = settings.STOOQ_URL + f'&s={stock_code}'
    resp = requests.get(url)
    stock = parse_stock(resp.text)

    stock['date'] = combine_datetime(stock['date'],stock['time'])

    return stock