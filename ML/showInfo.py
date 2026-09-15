import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .emissions import del_emissions_log1p
from .getDataSet import get_data_set_data, get_data_set_target


def show_data_set_info(df):
    print(df.head())
    print(df.info())
    print(df.shape)


def show_data_set_data_info():
    df = get_data_set_data()
    show_data_set_info(df)


def show_data_set_target_info():
    df = get_data_set_target()
    show_data_set_info(df)


def check_target(df=None):
    if df is None:
        df = get_data_set_target()
    print(df.describe())
    sns.histplot(df, kde=True)
    plt.title(f"Распределение столбца: {df.name}")


def check_box_plot(df=None):
    if df is None:
        df = get_data_set_target()

    sns.boxplot(df)


def check_target_with_del_emissions():
    df = get_data_set_target()
    df = del_emissions_log1p(df)
    check_target(df)


def check_number_signs(df=None):
    if df is None:
        df = get_data_set_data()
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    print(df[numeric_cols].describe().to_string())


def check_corr(df: pd.DataFrame):
    corr_matrix = df.corr()
    print(corr_matrix.to_string())


if __name__ == "__main__":
    check_target()
    check_target_with_del_emissions()
