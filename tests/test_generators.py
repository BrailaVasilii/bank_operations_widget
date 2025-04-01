from typing import Any, Dict, List

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

transactions: List[Dict[str, Any]] = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def test_filter_by_currency() -> None:
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 3
    assert usd_transactions[0]["operationAmount"]["currency"]["code"] == "USD"
    assert usd_transactions[1]["operationAmount"]["currency"]["code"] == "USD"
    assert usd_transactions[2]["operationAmount"]["currency"]["code"] == "USD"

    rub_transactions = list(filter_by_currency(transactions, "RUB"))
    assert len(rub_transactions) == 2
    assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"
    assert rub_transactions[1]["operationAmount"]["currency"]["code"] == "RUB"

    eur_transactions = list(filter_by_currency(transactions, "EUR"))
    assert len(eur_transactions) == 0


def test_transaction_descriptions() -> None:
    descriptions = list(transaction_descriptions(transactions))
    assert len(descriptions) == 5
    assert descriptions[0] == "Перевод организации"
    assert descriptions[1] == "Перевод со счета на счет"
    assert descriptions[2] == "Перевод со счета на счет"
    assert descriptions[3] == "Перевод с карты на карту"
    assert descriptions[4] == "Перевод организации"


def test_card_number_generator() -> None:
    card_numbers = list(card_number_generator(1, 5))
    assert len(card_numbers) == 5
    assert card_numbers[0] == "0000 0000 0000 0001"
    assert card_numbers[1] == "0000 0000 0000 0002"
    assert card_numbers[2] == "0000 0000 0000 0003"
    assert card_numbers[3] == "0000 0000 0000 0004"
    assert card_numbers[4] == "0000 0000 0000 0005"
