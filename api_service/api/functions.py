from api.models import UserRequestHistory
from django.db.models import Count

LOG_PREFIX = '[api][functions]'

def hide_field(dict, field):
    dict.pop(field, None)
    return dict

def get_top_stats(number=5):
    print(f'{LOG_PREFIX} querying top {number} stats from UserRequestHistory')
    queryset = UserRequestHistory.objects.all().values('symbol').annotate(total=Count('symbol')).order_by('-total')[:number]
    stats = []

    for item in queryset:
        stats.append({'stock': item['symbol'], 'times_requested': item['total']})

    return stats
