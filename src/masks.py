def get_mask_card_number(card_number: str) -> str:
    """
    Masks a card number in the format XXXX XX** **** XXXX.
    """
    card_number = str(card_number)
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Masks an account number in the format **XXXX.
    """
    account_number = str(account_number)
    return f"**{account_number[-4:]}"
