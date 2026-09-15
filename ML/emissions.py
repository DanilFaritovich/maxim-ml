import operator

import numpy as np
import pandas as pd


def del_emissions_log1p(df):
    return np.log1p(df)


def del_emissions_by_columns_log1p(df, columns):
    df[columns] = del_emissions_log1p(df[columns])
    return df


operators = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "!=": operator.ne,
}


def del_values(df: pd.DataFrame, conditions):
    for condition in conditions:
        df = df.loc[operators[condition["operator"]](df[condition["column"]], condition["number"])]
    return df
