# encoding: utf-8
import requests, json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from stocks.serializer import StockSerializer
from stocks.utils import parse_stock
from datetime import datetime

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('stock_code')
        url = settings.STOOQ_URL + f'&s={stock_code}'

        resp = requests.get(url)
        stock = parse_stock(resp.text)

        stock['date'] = datetime.now()

        serializer = StockSerializer(stock)

        return Response(serializer.data)
