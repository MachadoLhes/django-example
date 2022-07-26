# encoding: utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from stocks.serializer import StockSerializer
from stocks.functions import get_stock


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

        serializer = StockSerializer(data=stock)

        if serializer.is_valid():
            print(f'{LOG_PREFIX}[stock][GET] found for stock code: {stock_code}')
            stock_json = serializer.data
            return Response(stock_json)

        print(f'{LOG_PREFIX}[stock][GET] invalid stock')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
