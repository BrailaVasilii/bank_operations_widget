from typing import List, Dict


def filter_by_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Filters a list of dictionaries by the 'state' key.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sorts a list of dictionaries by the 'date' key.
    """
    return sorted(data, key=lambda x: x.get("date"), reverse=reverse)
