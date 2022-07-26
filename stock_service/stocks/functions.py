from django.conf import settings
from datetime import datetime
import requests

def combine_datetime(date:str, time:str) -> datetime:
    return datetime.strptime(f"{date} {time}","%Y-%m-%d %H:%M:%S")

def parse_stock(stock_line:str) -> dict:
    stock_split = stock_line.lower().split('\n')

    keys = stock_split[0].replace('\r','').split(',')
    values = stock_split[1].replace('\r','').split(',')

    stock = dict(zip(keys, values))

    try:
        stock['date'] = combine_datetime(stock['date'],stock['time'])
    except:
        pass

    return stock

def get_stock(stock_code:str) -> dict:
    url = settings.STOOQ_URL + f'&s={stock_code}'
    resp = requests.get(url)
    stock = parse_stock(resp.text)

    return stock