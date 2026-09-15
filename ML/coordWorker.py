import category_encoders as ce
import geohash
import pandas as pd

from .models import load_model, save_model


def get_geohash(df: pd.DataFrame, lat_column, lon_column, target_colum):
    df["geohash"] = df.apply(
        lambda row: geohash.encode(row[lat_column], row[lon_column], precision=5), axis=1
    )
    encoder = ce.TargetEncoder(cols=["geohash"])
    df["geohash_te"] = encoder.fit_transform(df["geohash"], df[target_colum])

    # Сохраняем модель
    save_model(encoder, "encoder.pkl")

    df.pop("geohash")
    return df


def get_geohash_with_model(df: pd.DataFrame, lat_column, lon_column):
    df["geohash"] = df.apply(
        lambda row: geohash.encode(row[lat_column], row[lon_column], precision=5), axis=1
    )
    encoder = load_model("encoder.pkl")
    df["geohash_te"] = encoder.transform(df["geohash"])

    df.pop("geohash")
    return df
