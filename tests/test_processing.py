from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> List[Dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-26"},
        {"id": 2, "state": "CANCELED", "date": "2023-10-25"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-27"},
    ]


def test_filter_by_state(sample_data: List[Dict]) -> None:
    assert filter_by_state(sample_data, "EXECUTED") == [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-26"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-27"},
    ]
    assert filter_by_state(sample_data, "CANCELED") == [
        {"id": 2, "state": "CANCELED", "date": "2023-10-25"},
    ]
    assert filter_by_state(sample_data, "PENDING") == []


def test_sort_by_date(sample_data: List[Dict]) -> None:
    assert sort_by_date(sample_data) == [
        {"id": 3, "state": "EXECUTED", "date": "2023-10-27"},
        {"id": 1, "state": "EXECUTED", "date": "2023-10-26"},
        {"id": 2, "state": "CANCELED", "date": "2023-10-25"},
    ]
    assert sort_by_date(sample_data, reverse=False) == [
        {"id": 2, "state": "CANCELED", "date": "2023-10-25"},
        {"id": 1, "state": "EXECUTED", "date": "2023-10-26"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-27"},
    ]
