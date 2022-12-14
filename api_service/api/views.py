# encoding: utf-8
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer, UserSerializer
from api.functions import hide_field, get_stock, get_top_stats

import json

LOG_PREFIX = '[api][views]'

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    def get(self, request, *args, **kwargs):
        print(f'{LOG_PREFIX}[stock][GET] request received')
        stock_code = request.query_params.get('q')
        print(f'{LOG_PREFIX}[stock][GET] searching for stock code: {stock_code}')
        stock = get_stock(stock_code)

        serializer = UserRequestHistorySerializer(data=stock)

        if serializer.is_valid():
            print(f'{LOG_PREFIX}[stock][GET] found for stock code: {stock_code}')
            serializer.save(user = self.request.user)
            print(f'{LOG_PREFIX}[stock][GET] request added to user history')
            stock_json = serializer.data
            return Response(hide_field(stock_json, 'date'))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer

    def list(self, request):
        print(f'{LOG_PREFIX}[history][GET] request received')
        queryset = self.get_queryset().filter(user=request.user)
        serializer = UserRequestHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        print(f'{LOG_PREFIX}[stats][GET] request received')
        top_stocks = get_top_stats()

        return Response(top_stocks)

class UsersView(APIView):
    """
    Allows super users to create another users.
    """
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        print(f'{LOG_PREFIX}[user][POST] request received')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        serializer = UserSerializer(data=body)
        if serializer.is_valid():
            if User.objects.filter(username=body['username']).exists():
                return Response(f"User {body['username']} already exists", status=status.HTTP_409_CONFLICT)

            print(f'{LOG_PREFIX}[user][POST] creating new user {body["username"]}')
            serializer.save()
            print(f'{LOG_PREFIX}[user][POST] new user {body["username"]} created successfully')

            return Response(f'User {body["username"]} created successfully')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)