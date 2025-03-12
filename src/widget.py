from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(account_card: str) -> str:
    """
    Masks a card or account number.
    """
    parts = account_card.split()
    if parts[0].lower() in ["visa", "maestro", "mastercard"]:
        return f"{parts[0]} {get_mask_card_number(''.join(parts[1:]))}"
    elif parts[0].lower() == "счет":
        return f"{parts[0]} {get_mask_account(''.join(parts[1:]))}"
    else:
        return "Неизвестный тип карты/счета"


def get_date(date_str: str) -> str:
    """
    Converts a date string to DD.MM.YYYY format.
    """
    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d.%m.%Y")
