import unittest
from unittest.mock import patch, Mock
import os
import json
import requests
from src.external_api import convert_currency_to_rub
from src.utils import read_json_file


class TestExternalApiCoverage(unittest.TestCase):

    def setUp(self) -> None:
        self.original_api_key = os.environ.get("EXCHANGE_RATES_API_KEY")
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_key"  # Для тестов

    def tearDown(self) -> None:
        if self.original_api_key is not None:
            os.environ["EXCHANGE_RATES_API_KEY"] = self.original_api_key
        elif "EXCHANGE_RATES_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATES_API_KEY"]

    @patch("requests.get")
    def test_convert_currency_to_rub_no_rub_rate_present(self, mock_get: Mock) -> None:
        """Тестирует случай, когда в ответе API отсутствует курс RUB."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"rates": {"JPY": 130.0, "USD": 1.1}}
        mock_get.return_value = mock_response
        transaction = {"currency": "EUR", "amount": 20}
        result = convert_currency_to_rub(transaction)
        self.assertEqual(result, 20.0)  # Ожидается возврат исходной суммы

    @patch("requests.get")
    def test_convert_currency_to_rub_api_request_exception(self, mock_get: Mock) -> None:
        """Тестирует обработку исключения requests.exceptions.RequestException."""
        mock_get.side_effect = requests.exceptions.RequestException("API request failed")
        transaction = {"currency": "GBP", "amount": 50}
        result = convert_currency_to_rub(transaction)
        self.assertEqual(result, 50.0)  # Ожидается возврат исходной суммы

    @patch("requests.get")
    def test_convert_currency_to_rub_api_json_decode_error(self, mock_get: Mock) -> None:
        """Тестирует обработку исключения json.JSONDecodeError."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "document", 0)
        mock_get.return_value = mock_response
        transaction = {"currency": "CAD", "amount": 100}
        result = convert_currency_to_rub(transaction)
        self.assertEqual(result, 0.0)  # Ожидается возврат 0.0


class TestUtilsCoverage(unittest.TestCase):

    @patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "document", 0))
    def test_read_json_file_json_decode_error(self, mock_file: Mock) -> None:
        """Тестирует обработку исключения json.JSONDecodeError при чтении файла."""
        result = read_json_file("test.json")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_read_json_file_permission_error(self, mock_file: Mock) -> None:
        """Тестирует обработку исключения PermissionError при чтении файла."""
        result = read_json_file("test.json")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=IOError("Input/output error"))
    def test_read_json_file_io_error(self, mock_file: Mock) -> None:
        """Тестирует обработку исключения IOError при чтении файла."""
        result = read_json_file("test.json")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=Exception("Some other error"))
    def test_read_json_file_other_exception(self, mock_file: Mock) -> None:
        """Тестирует обработку других исключений при чтении файла."""
        result = read_json_file("test.json")
        self.assertEqual(result, [])
