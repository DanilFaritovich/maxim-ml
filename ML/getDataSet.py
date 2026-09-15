import pandas as pd
from sklearn.datasets import fetch_california_housing

data_set = fetch_california_housing(as_frame=True)


def get_data_set_data() -> pd.DataFrame:
    return data_set.data


def get_data_set_target() -> pd.DataFrame:
    return data_set.target


if __name__ == "__main__":
    get_data_set_data()
