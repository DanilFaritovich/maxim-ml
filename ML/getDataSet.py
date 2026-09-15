from functools import lru_cache

import pandas as pd
from sklearn.datasets import fetch_california_housing


@lru_cache
def _get_data_set():
    """Load the dataset only when training needs it, not when the API starts."""
    return fetch_california_housing(as_frame=True)


def get_data_set_data() -> pd.DataFrame:
    return _get_data_set().data


def get_data_set_target() -> pd.Series:
    return _get_data_set().target


if __name__ == "__main__":
    get_data_set_data()
