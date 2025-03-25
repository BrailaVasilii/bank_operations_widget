from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"
    assert get_mask_card_number("123456781234") == "1234 56** **** 1234"
    assert get_mask_card_number("") == " ** **** "


def test_get_mask_account() -> None:
    assert get_mask_account("12345678901234567890") == "**7890"
    assert get_mask_account("1234") == "**1234"
    assert get_mask_account("") == "**"
