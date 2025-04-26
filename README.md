Markdown

# Bank Operations Widget

This project contains functions for processing bank operations data.

## Installation

1. Clone the repository.
2. Install dependencies using Poetry:
   ```bash
   poetry install
Usage
filter_by_state
Filters a list of dictionaries by the 'state' key.

Python

from src.processing import filter_by_state

data = [...]  # Your data
filtered_data = filter_by_state(data, 'CANCELED')
print(filtered_data)
sort_by_date
Sorts a list of dictionaries by the 'date' key.

Python

from src.processing import sort_by_date

data = [...]  # Your data
sorted_data = sort_by_date(data)
print(sorted_data)
convert_currency_to_rub
Converts the 'amount' in a transaction dictionary to Russian Rubles (RUB) using an external exchange rate API.

Python

import os
from src.external_api import convert_currency_to_rub

# Make sure to set the EXCHANGE_RATES_API_KEY environment variable
os.environ["EXCHANGE_RATES_API_KEY"] = "YOUR_API_KEY_HERE"

transaction = {"currency": "USD", "amount": 100}
amount_in_rub = convert_currency_to_rub(transaction)
print(f"Amount in RUB: {amount_in_rub}")
read_json_file
Reads data from a JSON file and returns a list of dictionaries.

Python

from src.utils import read_json_file

file_path = "data.json"
transactions = read_json_file(file_path)
print(transactions)
mask_account_number
Masks an account number, showing only the first and last few digits.

Python

from src.masks import mask_account_number

account_number = "1234567890123456"
masked_number = mask_account_number(account_number)
print(f"Masked account number: {masked_number}")
Тестирование
Для тестирования проекта используются следующие инструменты:

pytest: Фреймворк для запуска тестов.
coverage.py: Инструмент для измерения покрытия кода тестами.
Запуск тестов
Чтобы запустить тесты, выполните следующую команду:

Bash

poetry run pytest tests/
Отчет о покрытии кода
Чтобы сгенерировать отчет о покрытии кода, выполните следующие команды:

Bash

poetry run coverage run -m pytest tests/
poetry run coverage report -m
Модуль decorators
Этот модуль содержит декоратор log, который автоматически логирует детали выполнения функций.

Декоратор log
Декоратор @log используется для автоматической регистрации информации о вызове функции, ее аргументах, результате и любых возникших ошибках.

Использование:

Декоратор можно применять к любой функции, добавив @log перед ее определением. Вы можете настроить имя файла для логирования, передав аргумент filename декоратору. По умолчанию логи записываются в стандартный вывод.

Python

from src.decorators import log

@log()
def my_function(x, y):
    return x + y

@log(filename="mylog.txt")
def another_function(data):
    print(f"Processing: {data}")
Переменные окружения
Для корректной работы некоторых функций могут потребоваться следующие переменные окружения:

EXCHANGE_RATES_API_KEY: Ключ API для сервиса обмена валют. Необходим для функции convert_currency_to_rub. Вы можете получить ключ, зарегистрировавшись на одном из сервисов, предоставляющих API курсов валют.
Пожалуйста, создайте файл .env в корне проекта и укажите в нем значение этой переменной:

EXCHANGE_RATES_API_KEY=YOUR_ACTUAL_API_KEY

Модуль readers
Этот модуль предоставляет функции для чтения данных из различных форматов файлов.

read_csv_file
Функция read_csv_file считывает данные из CSV-файла и возвращает их в виде списка словарей. 
Каждый словарь представляет строку из CSV-файла, где ключи соответствуют заголовкам столбцов.

read_excel_file
Функция read_excel_file считывает данные из Excel-файла (XLSX) и возвращает их в виде списка словарей.  
Подобно read_csv_file, каждый словарь представляет строку, а ключи - это заголовки столбцов.

read_json_file
Функция read_json_file считывает данные из JSON-файла и возвращает список словарей.

Модуль test_readers
Этот модуль содержит набор тестов pytest для проверки правильности работы функций чтения данных, определенных в модуле readers.  
Он включает тесты для чтения из CSV, Excel и JSON файлов, гарантируя, что каждая функция правильно разбирает данные и возвращает ожидаемую структуру данных.

 Анализ банковских операций

## Описание
Данный проект позволяет анализировать банковские операции из файлов форматов JSON, CSV и XLSX. Реализованы фильтрация, сортировка и подсчет категорий операций.

## Основные функции
1. Фильтрация операций по статусу.
2. Поиск операций по ключевым словам.
3. Сортировка операций по дате.
4. Подсчет количества операций по категориям.

## Команды для тестирования
Тесты можно запустить с помощью команды:

```bash
pytest
```
