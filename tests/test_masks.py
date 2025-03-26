import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected_result",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("123456781234", "1234 56** **** 1234"),
        ("", " ** **** "),
    ],
)
def test_get_mask_card_number(card_number: str, expected_result: str) -> None:  # Добавлено
    assert get_mask_card_number(card_number) == expected_result


@pytest.mark.parametrize(
    "account_number, expected_result",
    [
        ("12345678901234567890", "**7890"),
        ("1234", "**1234"),
        ("", "**"),
    ],
)
def test_get_mask_account(account_number: str, expected_result: str) -> None:  # Добавлено
    assert get_mask_account(account_number) == expected_result
