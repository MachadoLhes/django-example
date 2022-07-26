from api.models import UserRequestHistory
from django.db.models import Count
from django.conf import settings
import requests

LOG_PREFIX = '[api][functions]'

def hide_field(dict:dict, field:str) -> dict:
    dict.pop(field, None)
    return dict

def get_stock(stock_code:str) -> dict:
    url = settings.STOCK_SERVICE_URL + f'stock_code={stock_code}'
    resp = requests.get(url)
    return resp.json()

def get_top_stats(number:int = 5) -> dict :
    print(f'{LOG_PREFIX} querying top {number} stats from UserRequestHistory')
    queryset = UserRequestHistory.objects.all().values('symbol').annotate(total=Count('symbol')).order_by('-total')[:number]
    stats = []

    for item in queryset:
        stats.append({'stock': item['symbol'], 'times_requested': item['total']})

    return stats
