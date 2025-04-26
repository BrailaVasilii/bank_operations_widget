import os
from src.data_loader import load_operations_from_json, load_operations_from_csv, load_operations_from_xlsx
from src.operations import (
    filter_operations_by_status,
    filter_operations_by_description,
    sort_operations_by_date,
    count_operation_categories,
    filter_operations_by_currency,
)


def main() -> None:
    # Определяем базовую директорию проекта (где расположена папка data)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    print("Привет! Добро пожаловать в программу для работы с транзакциями.")

    # Шаг 1: выбор формата данных
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

    # Шаг 2: фильтр по статусу
    while True:
        status = input("\nВведите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Некорректный статус: {status}. Попробуйте снова.")
            continue

        operations = filter_operations_by_status(operations, status)
        print(f"Найдено {len(operations)} операций со статусом '{status}'.")
        break

    # Шаг 3: фильтр по валюте
    currency_choice = input("Выводить только рублёвые транзакции? (да/нет): ").strip().lower()
    if currency_choice == "да":
        print(operations)
        operations = filter_operations_by_currency(operations, "RUB")
        print(f"Оставлено {len(operations)} операций в рублях.")

    # Шаг 4: сортировка по дате
    sort_choice = input("Сортировать операции по дате? (да/нет): ").strip().lower()
    if sort_choice == "да":
        order = input("Сортировать по возрастанию или убыванию? ").strip().lower()
        ascending = order == "возрастание"
        operations = sort_operations_by_date(operations, ascending)

    # Шаг 5: фильтр по описанию
    description_choice = input("Фильтровать по описанию? (да/нет): ").strip().lower()
    if description_choice == "да":
        search_term = input("Введите ключевое слово для фильтрации: ").strip()
        operations = filter_operations_by_description(operations, search_term)

    # Шаг 6: вывод результатов
    if not operations:
        print("Подходящие операции не найдены.")
    else:
        print("\nРезультаты:")
        for op in operations:
            date = op["date"]
            description = op["description"]
            amount = op["operationAmount"]["amount"]
            currency = op["operationAmount"]["currency"]["name"]
            print(f"{date} {description}: {amount} {currency}")

    # Шаг 7: статистика
    categories = count_operation_categories(operations)
    print("\nКатегории операций и их количество:")
    for category, count in categories.items():
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()
