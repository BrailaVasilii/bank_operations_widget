import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_string, expected_result",
    [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Unknown 1234", "Неизвестный тип карты/счета"),
    ],
)
def test_mask_account_card(input_string: str, expected_result: str) -> None:  # Добавлено
    assert mask_account_card(input_string) == expected_result


@pytest.mark.parametrize(
    "date_string, expected_result",
    [
        ("2023-10-26T12:00:00.000000", "26.10.2023"),
        ("invalid date", ""),
        ("", ""),
    ],
)
def test_get_date(date_string: str, expected_result: str) -> None:  # Добавлено
    assert get_date(date_string) == expected_result
