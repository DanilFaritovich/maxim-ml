import pandas as pd
from matplotlib import pyplot as plt

from .coordWorker import get_geohash, get_geohash_with_model
from .emissions import del_emissions_by_columns_log1p, del_values
from .scaling import standart_scaler
from .showInfo import check_box_plot, check_target


def model_preprocessing(df: pd.DataFrame, data_columns):
    del_val_list = [
        {"column": "MedInc", "operator": "<=", "number": 12},
        {"column": "HouseAge", "operator": "<", "number": 52},
        {"column": "AveRooms", "operator": "<", "number": 12},
        {"column": "AveBedrms", "operator": "<", "number": 3},
        {"column": "AveBedrms", "operator": ">", "number": 0.45},
        {"column": "Population", "operator": "<", "number": 8000},
        {"column": "AveOccup", "operator": "<", "number": 10.5},
        {"column": "AveOccup", "operator": ">", "number": 0.8},
        {"column": "MedHouseVal", "operator": "<", "number": 5},
    ]
    df = del_values(df, del_val_list)

    if False:
        for col in df:
            check_target(df[col])
            plt.show()
            check_box_plot(df[col])
            plt.show()

    # check_number_signs(df)
    df = del_emissions_by_columns_log1p(df, ["AveRooms", "Population", "AveOccup"])
    # check_number_signs(df)
    # check_corr(df.iloc[:, :-1])
    df = get_geohash(df, "Latitude", "Longitude", "MedHouseVal")
    # df.pop('Latitude')
    # df.pop('Longitude')
    data_columns.append("geohash_te")
    df.loc[:, data_columns] = standart_scaler(df[data_columns], data_columns)

    # print(df.head().to_string())
    # check_number_signs(df)

    return df


def preprocessing_data_df(df: pd.DataFrame):
    data_columns = list(df.columns)

    # check_number_signs(df)
    df = del_emissions_by_columns_log1p(df, ["AveRooms", "Population", "AveOccup"])
    # check_number_signs(df)
    # check_corr(df.iloc[:, :-1])
    df = get_geohash_with_model(df, "Latitude", "Longitude")
    # df.pop('Latitude')
    # df.pop('Longitude')
    data_columns.append("geohash_te")
    df.loc[:, data_columns] = standart_scaler(df[data_columns], data_columns)

    return df
