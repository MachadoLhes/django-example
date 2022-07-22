# encoding: utf-8
import requests, json

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        # TODO: Call the stock service, save the response, and return the response to the user
        url = settings.STOCK_SERVICE_URL + f'stock_code={stock_code}'

        resp = requests.get(url)
        stock = resp.json()
        serializer = UserRequestHistorySerializer(data=stock)

        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    # TODO: Filter the queryset so that we get the records for the user making the request.


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        return Response()
