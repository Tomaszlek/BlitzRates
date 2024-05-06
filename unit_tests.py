import unittest
from unittest.mock import patch, Mock
import plotly.graph_objects as go
import charts
import requests
from api_requests import get_currencies_rates, get_gold_rate


class TestDataVisualization(unittest.TestCase):

    def test_currency_chart(self):
        fig = charts.plot_currency_chart('USD', 20, 'RSI')
        self.assertIsInstance(fig, go.Figure)

    def test_gold_chart(self):
        fig = charts.plot_gold_chart(0, '')
        self.assertIsInstance(fig, go.Figure)


class TestAPIFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_get_currencies_rates(self, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "effectiveDate": "2024-05-01",
                "rates": [
                    {"currency": "Dolar amerykański", "code": "USD", "mid": 4.2},
                    {"currency": "Euro", "code": "EUR", "mid": 4.8},
                ]
            },
        ]
        mock_get.return_value = mock_response

        result = get_currencies_rates()

        self.assertEqual(len(result), 2)

    @patch('requests.get')
    def test_get_gold_rate(self, mock_get):
        # Mocking response from API
        mock_response = Mock()
        mock_response.json.return_value = [
            {"data": "2024-05-01", "cena": 200},
        ]
        mock_get.return_value = mock_response

        result = get_gold_rate()

        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
