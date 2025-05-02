import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from functools import wraps

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def save_report_to_file(filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename or f"{func.__name__}_report.json"
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            logging.info(f"Отчёт сохранён: {file_name}")
            return result

        return wrapper

    return decorator


@save_report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> float:
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    date = datetime.now().strftime("%Y-%m-%d") if date is None else date
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Категория"] == category)
    ]
    return float(filtered["Сумма операции"].sum())


@save_report_to_file()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    date = datetime.now().strftime("%Y-%m-%d") if date is None else date
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    filtered = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]
    if filtered.empty:
        return {}

    weekday_mapping = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }
    filtered["День недели"] = filtered["Дата операции"].dt.day_name().map(weekday_mapping)
    result = filtered.groupby("День недели")["Сумма операции"].mean().round(2)
    return result.to_dict()


@save_report_to_file()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    date = datetime.now().strftime("%Y-%m-%d") if date is None else date
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=90)
    filtered = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]
    if filtered.empty:
        return {}

    filtered["Тип дня"] = filtered["Дата операции"].dt.dayofweek.apply(lambda x: "Рабочий" if x < 5 else "Выходной")
    result = filtered.groupby("Тип дня")["Сумма операции"].mean().round(2)
    return result.to_dict()
