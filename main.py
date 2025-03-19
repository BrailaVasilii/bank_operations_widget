# main.py
from src.masks import get_mask_card_number, get_mask_account  # Импортируем функции из модуля masks


def main():
    """Основная функция программы."""
    card_number = input("Введите номер карты: ")  # Запрашиваем у пользователя номер карты
    masked_card = get_mask_card_number(card_number)  # Маскируем номер карты с помощью функции
    print(f"Маскированный номер карты: {masked_card}")  # Выводим маскированный номер карты

    account_number = input("Введите номер счета: ")  # Запрашиваем у пользователя номер счета
    masked_account = get_mask_account(account_number)  # Маскируем номер счета с помощью функции
    print(f"Маскированный номер счета: {masked_account}")  # Выводим маскированный номер счета


if __name__ == "__main__":
    main()  # Вызываем функцию main, если скрипт запущен напрямую
