from src.widget import get_date, mask_account_card


def test_mask_account_card() -> None:
    assert mask_account_card("Visa 1234567812345678") == "Visa 1234 56** **** 5678"
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"
    assert mask_account_card("Unknown 1234") == "Неизвестный тип карты/счета"


def test_get_date() -> None:
    assert get_date("2023-10-26T12:00:00.000000") == "26.10.2023"
    assert get_date("invalid date") == ""
    assert get_date("") == ""
