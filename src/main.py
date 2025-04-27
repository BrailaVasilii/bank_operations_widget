import os
from datetime import datetime

from src.data_loader import load_operations_from_json, load_operations_from_csv, load_operations_from_xlsx
from src.operations import (
    filter_operations_by_status,
    filter_operations_by_description,
    sort_operations_by_date,
    filter_operations_by_currency,
)


def main() -> None:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    print("Привет! Добро пожаловать в программу для работы с транзакциями.")

    print("\nВыберите формат файла для загрузки данных:")
    print("1. JSON (operations.json)")
    print("2. CSV (transactions.csv)")
    print("3. XLSX (transactions_excel.xlsx)")
    choice = input("Ваш выбор (1/2/3): ").strip()

    try:
        if choice == "1":
            file_path = os.path.join(DATA_DIR, "operations.json")
            operations = load_operations_from_json(file_path)
        elif choice == "2":
            file_path = os.path.join(DATA_DIR, "transactions.csv")
            operations = load_operations_from_csv(file_path)
        elif choice == "3":
            file_path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
            operations = load_operations_from_xlsx(file_path)
        else:
            print("Некорректный выбор файла!")
            return
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    print("Операции успешно загружены из выбранного файла!")

    while True:
        status = input("\nВведите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Некорректный статус: {status}. Попробуйте снова.")
            continue

        operations = filter_operations_by_status(operations, status)
        print(f"Найдено {len(operations)} операций со статусом '{status}'.")
        break

    currency_choice = input("Выводить только рублёвые транзакции? (да/нет): ").strip().lower()
    if currency_choice == "да":
        print(operations)
        operations = filter_operations_by_currency(operations, "RUB")
        print(f"Оставлено {len(operations)} операций в рублях.")

    sort_choice = input("Сортировать операции по дате? (да/нет): ").strip().lower()
    if sort_choice == "да":
        order = input("Сортировать по возрастанию или убыванию? ").strip().lower()
        ascending = order == "возрастание"
        operations = sort_operations_by_date(operations, ascending)

    description_choice = input("Фильтровать по описанию? (да/нет): ").strip().lower()
    if description_choice == "да":
        search_term = input("Введите ключевое слово для фильтрации: ").strip()
        operations = filter_operations_by_description(operations, search_term)

    if not operations:
        print("Подходящие операции не найдены.")
    else:
        print("\nПрограмма:")
        print(f"Всего банковских операций в выборке: {len(operations)}\n")
        for op in operations:
            try:
                # Используем безопасную обработку ISO формата
                date = datetime.fromisoformat(op["date"].replace("Z", "+00:00")).strftime("%d.%m.%Y")
            except ValueError:
                print(f"Ошибка преобразования даты: {op['date']}")
                date = "Неизвестно"

            description = op["description"]
            amount = op["operationAmount"]["amount"]
            currency = op["operationAmount"]["currency"]["name"]

            if "from" in op and "to" in op:
                from_info = op.get("from", "")
                to_info = op.get("to", "")
                print(f"{date} {description}")
                print(f"{from_info} -> {to_info}")
                print(f"Сумма: {amount} {currency}\n")
            elif "to" in op:
                to_info = op.get("to", "")
                print(f"{date} {description}")
                print(f"Счет {to_info}")
                print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
