from django.test import TestCase
from django.contrib.auth.models import User
from api.models import UserRequestHistory
from datetime import datetime
from unittest import mock
from api.functions import get_stock, get_top_stats

class StockMockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {"date": datetime(2022, 7, 23, 13, 51, 24, 143099),
                "name":'apple',
                "symbol":'aapl.us',
                "open":155.39,
                "high":156.28,
                "low":153.41,
                "close":154.09}


class ApiTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test_user', email='test_user@example.com', password='test')
        test_user_admin = User.objects.create_superuser(username='test_user_admin', email='test_user@example.com', password='test')
        UserRequestHistory.objects.create(date=datetime(2022, 7, 23, 13, 51, 24, 143099),
                                          name='apple',
                                          symbol='aapl.us',
                                          open=155.39,
                                          high=156.28,
                                          low=153.41,
                                          close=154.09,
                                          user=test_user)
        UserRequestHistory.objects.create(date=datetime(2022, 7, 23, 14, 8, 21, 778696),
                                          name='webster financial',
                                          symbol='wbs.us',
                                          open=46.11,
                                          high=46.29,
                                          low=44.74,
                                          close=45.06,
                                          user=test_user)
        UserRequestHistory.objects.create(date=datetime(2022, 7, 23, 14, 8, 21, 778696),
                                          name='webster financial',
                                          symbol='wbs.us',
                                          open=46.11,
                                          high=46.29,
                                          low=44.74,
                                          close=45.06,
                                          user=test_user_admin)

    def test_top_stats(self):
        "Should get the n most called stats"
        stats = get_top_stats(2)
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0], {'stock': 'wbs.us', 'times_requested': 2})

    @mock.patch('api.functions.requests.get', return_value=StockMockResponse())
    def test_stock_view(self, mock_get_stock):
        "Test stock view happy path"

        self.client.login(username="test_user", password="test")
        response = self.client.get('/stock?q=aapl.us')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_stock_view_unauthorized(self):
        "Should fail if not authorized"

        response = self.client.get('/stock?q=aapl.us')
        self.assertEqual(response.status_code, 403)

    def test_history_view(self):
        "Should return stock history"
        self.client.login(username="test_user", password="test")
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),2)

    def test_stats_view(self):
        "Only superusers can view stats"
        self.client.login(username="test_user_admin", password="test")
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'stock': 'wbs.us', 'times_requested': 2}, {'stock': 'aapl.us', 'times_requested': 1}])

    def test_stats_view_forbidden(self):
        "Only superusers can view stats"
        self.client.login(username="test_user", password="test")
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 403)
