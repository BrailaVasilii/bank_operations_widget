# src/masks.py
import logging
import os

logger_masks = logging.getLogger(__name__)
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
file_handler_masks = logging.FileHandler(os.path.join(logs_dir, "masks.log"), mode="w", encoding="utf-8")
file_formatter_masks = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_masks.setFormatter(file_formatter_masks)
logger_masks.addHandler(file_handler_masks)
logger_masks.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """
    Masks a card number in the format XXXX XX** **** XXXX.
    """
    logger_masks.debug(f"Вызвана функция get_mask_card_number с номером: {card_number}")
    card_number = str(card_number)
    if not card_number:
        logger_masks.warning("Получен пустой номер карты, возвращается шаблон.")
        return " ** **** "
    if not card_number.isdigit():
        logger_masks.error(f"Некорректный формат номера карты (не только цифры): {card_number}")
        return "Некорректный номер карты"
    if len(card_number) < 16:
        logger_masks.warning(f"Короткий номер карты, маскировка неполная: {card_number}")
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[len(card_number)-4:]}"
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger_masks.info(f"Номер карты успешно замаскирован: {masked_number}")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Masks an account number in the format **XXXX.
    """
    logger_masks.debug(f"Вызвана функция get_mask_account с номером: {account_number}")
    account_number = str(account_number)
    if not account_number:
        logger_masks.warning("Получен пустой номер счета, возвращается шаблон.")
        return "**"
    if not account_number.isdigit():
        logger_masks.error(f"Некорректный формат номера счета (не только цифры): {account_number}")
        return "Некорректный номер счета"
    if len(account_number) < 4:
        logger_masks.warning(f"Короткий номер счета, маскировка неполная: {account_number}")
        return f"**{account_number[-4:]}"
    masked_number = f"**{account_number[-4:]}"
    logger_masks.info(f"Номер счета успешно замаскирован: {masked_number}")
    return masked_number
