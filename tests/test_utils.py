from unittest.mock import patch, mock_open
from src.utils import read_json_file
from typing import List, Dict, Any


class TestReadJsonFile:
    """Тесты для функции read_json_file."""

    def test_read_json_file_not_found(self) -> None:
        """Тестирует обработку FileNotFoundError."""
        result: List[Dict[str, Any]] = read_json_file("nonexistent.json")
        assert result == []

    def test_read_json_file_list_of_dictionaries_with_id(self) -> None:
        """Тестирует чтение списка словарей с ключом 'id'."""
        mocked_open = mock_open(read_data='[{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]')
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("test.json")
            assert result == [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
            mocked_open.assert_called_once_with("test.json", "r")

    def test_read_json_file_list_of_dictionaries_without_id(self) -> None:
        """Тестирует чтение списка словарей без ключа 'id'."""
        mocked_open = mock_open(read_data='[{"value": "a"}, {"value": "b"}]')
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("test.json")
            assert result == [{"value": "a"}, {"value": "b"}]
            mocked_open.assert_called_once_with("test.json", "r")

    def test_read_json_file_list_of_numbers(self) -> None:
        """Тестирует чтение списка чисел."""
        mocked_open = mock_open(read_data="[1, 2, 3]")
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("numbers.json")
            assert result == [{}, {}, {}]
            mocked_open.assert_called_once_with("numbers.json", "r")

    def test_read_json_file_list_with_mixed_types(self) -> None:
        """Тестирует чтение списка с миксом из словарей и не-словарей."""
        mocked_open = mock_open(read_data='[{"key": "value"}, 123, {"other_key": "value"}]')
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("mixed.json")
            assert result == [{"key": "value"}, {}, {"other_key": "value"}]
            mocked_open.assert_called_once_with("mixed.json", "r")

    def test_read_json_file_not_a_list(self) -> None:
        """Тестирует чтение файла, где корневой элемент не является списком."""
        mocked_open = mock_open(read_data='{"not": "a list"}')
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("not_list.json")
            assert result == []
            mocked_open.assert_called_once_with("not_list.json", "r")

    def test_read_json_file_empty_file(self) -> None:
        """Тестирует чтение пустого файла."""
        mocked_open = mock_open(read_data="")
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("empty.json")
            assert result == []
            mocked_open.assert_called_once_with("empty.json", "r")

    def test_read_json_file_invalid_json(self) -> None:
        """Тестирует чтение файла с некорректным JSON."""
        mocked_open = mock_open(read_data="not a json")
        with patch("builtins.open", mocked_open):
            result: List[Dict[str, Any]] = read_json_file("invalid.json")
            assert result == []
            mocked_open.assert_called_once_with("invalid.json", "r")

    def test_read_json_file_permission_error(self) -> None:
        """Тестирует обработку исключения PermissionError."""
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            result: List[Dict[str, Any]] = read_json_file("test.json")
            assert result == []

    def test_read_json_file_io_error(self) -> None:
        """Тестирует обработку исключения IOError."""
        with patch("builtins.open", side_effect=IOError("Input/output error")):
            result: List[Dict[str, Any]] = read_json_file("test.json")
            assert result == []

    def test_read_json_file_other_exception(self) -> None:
        """Тестирует обработку других исключений при чтении файла."""
        with patch("builtins.open", side_effect=Exception("Some other error")):
            result: List[Dict[str, Any]] = read_json_file("test.json")
            assert result == []
