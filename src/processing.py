from typing import Any, Dict, List


def filter_by_state(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Filters a list of dictionaries by the 'state' key.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sorts a list of dictionaries by the 'date' key.
    """

    def get_date_str(item: Dict[Any, Any]) -> str:
        date_str = item.get("date")
        return date_str if date_str else ""

    return sorted(data, key=get_date_str, reverse=reverse)
