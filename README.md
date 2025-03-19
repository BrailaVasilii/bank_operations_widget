# Bank Operations Widget

This project contains functions for processing bank operations data.

## Installation

1. Clone the repository.
2. Install dependencies.

## Usage

### filter_by_state

Filters a list of dictionaries by the 'state' key.

```python
from src.processing import filter_by_state

data = [...]  # Your data
filtered_data = filter_by_state(data, 'CANCELED')
print(filtered_data)
```

### sort_by_date

Sorts a list of dictionaries by the 'date' key.

```python
from src.processing import sort_by_date

data = [...]  # Your data
sorted_data = sort_by_date(data)
print(sorted_data)
```