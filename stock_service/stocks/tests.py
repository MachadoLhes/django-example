from django.test import TestCase
from unittest import mock
from stocks.functions import parse_stock

class StockMockResponse:
    def __init__(self):
        self.status_code = 200
        self.text = "Symbol,Date,Time,Open,High,Low,Close,Volume,Name\nAAPL.US,2022-07-22,22:00:10,155.39,156.28,153.41,154.09,66675408,APPLE"

# Create your tests here.
class StockTestCase(TestCase):
    def test_parse_stock(self):
        stock_line = "Symbol,Date,Time,Open,High,Low,Close,Volume,Name\nAAPL.US,2022-07-22,22:00:10,155.39,156.28,153.41,154.09,66675408,APPLE"
        parsed = parse_stock(stock_line)
        self.assertEqual(parsed["symbol"], "aapl.us")
        self.assertEqual(parsed["date"], "2022-07-22")
        self.assertEqual(parsed["time"], "22:00:10")
        self.assertEqual(parsed["open"], "155.39")
        self.assertEqual(parsed["high"], "156.28")
        self.assertEqual(parsed["low"], "153.41")
        self.assertEqual(parsed["close"], "154.09")
        self.assertEqual(parsed["volume"], "66675408")
        self.assertEqual(parsed["name"], "apple")

    @mock.patch('stocks.functions.requests.get', return_value=StockMockResponse())
    def test_stock_view(self, mock_get_stock):
        response = self.client.get('/stock?stock_code=aapl.us')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
