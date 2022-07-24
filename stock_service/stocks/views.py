# encoding: utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.serializer import StockSerializer
from stocks.functions import get_stock
from datetime import datetime

LOG_PREFIX = '[stock][views]'

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        print(f'{LOG_PREFIX}[stock][GET] request received')
        stock_code = request.query_params.get('stock_code')
        print(f'{LOG_PREFIX}[stock][GET] searching for stock code: {stock_code}')
        stock = get_stock(stock_code)

        stock['date'] = datetime.now()

        serializer = StockSerializer(stock)

        return Response(serializer.data)
