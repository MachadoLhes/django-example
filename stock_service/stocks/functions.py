from django.conf import settings
import requests

def parse_stock(stock_line):
    stock_split = stock_line.lower().split('\n')

    keys = stock_split[0].replace('\r','').split(',')
    values = stock_split[1].replace('\r','').split(',')

    stock = dict(zip(keys, values))

    return stock

def get_stock(stock_code):
    url = settings.STOOQ_URL + f'&s={stock_code}'
    resp = requests.get(url)
    stock = parse_stock(resp.text)

    return stock