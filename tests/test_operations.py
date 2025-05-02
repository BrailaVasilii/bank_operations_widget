from src.operations import (
    filter_operations_by_status,
    filter_operations_by_description,
    sort_operations_by_date,
    count_operation_categories,
)


def test_filter_operations_by_status() -> None:
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]

    filtered = filter_operations_by_status(operations, "EXECUTED")
    assert len(filtered) == 2
    assert all(op["state"] == "EXECUTED" for op in filtered)


def test_filter_operations_by_description() -> None:
    operations = [
        {"id": 1, "description": "Payment for services"},
        {"id": 2, "description": "Salary payment"},
        {"id": 3, "description": "Utility payment"},
    ]

    filtered = filter_operations_by_description(operations, "payment")
    assert len(filtered) == 3

    filtered = filter_operations_by_description(operations, "salary")
    assert len(filtered) == 1


def test_sort_operations_by_date() -> None:
    operations = [
        {"id": 1, "date": "2023-01-01T00:00:00Z"},
        {"id": 2, "date": "2023-01-03T00:00:00Z"},
        {"id": 3, "date": "2023-01-02T00:00:00Z"},
    ]

    sorted_ops = sort_operations_by_date(operations, ascending=True)
    assert sorted_ops[0]["date"] == "2023-01-01T00:00:00Z"
    assert sorted_ops[-1]["date"] == "2023-01-03T00:00:00Z"

    sorted_ops = sort_operations_by_date(operations, ascending=False)
    assert sorted_ops[0]["date"] == "2023-01-03T00:00:00Z"
    assert sorted_ops[-1]["date"] == "2023-01-01T00:00:00Z"


def test_count_operation_categories() -> None:
    operations = [
        {"id": 1, "description": "Payment for services"},
        {"id": 2, "description": "Salary payment"},
        {"id": 3, "description": "Payment for services"},
    ]

    categories = count_operation_categories(operations)
    assert categories["Payment for services"] == 2
    assert categories["Salary payment"] == 1
