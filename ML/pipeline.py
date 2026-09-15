"""Reusable, fitted preprocessing pipeline for housing-price models."""

import geohash
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

FEATURE_COLUMNS = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]
LOG_COLUMNS = ["AveRooms", "Population", "AveOccup"]


def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """Apply stateless feature engineering to raw API or training input."""
    frame = data.loc[:, FEATURE_COLUMNS].copy()
    frame = frame.astype({column: float for column in LOG_COLUMNS})
    frame.loc[:, LOG_COLUMNS] = frame.loc[:, LOG_COLUMNS].apply("log1p")
    frame["geohash"] = frame.apply(
        lambda row: geohash.encode(row["Latitude"], row["Longitude"], precision=5), axis=1
    )
    return frame


def build_preprocessor() -> Pipeline:
    """Create an unfitted transformer. It must be fitted only on training data."""
    return Pipeline(
        steps=[
            ("feature_engineering", FunctionTransformer(engineer_features, validate=False)),
            (
                "preprocessing",
                ColumnTransformer(
                    transformers=[
                        ("numeric", StandardScaler(), FEATURE_COLUMNS),
                        ("geohash", TargetEncoder(cols=["geohash"]), ["geohash"]),
                    ]
                ),
            ),
        ]
    )


def build_model_pipeline(regressor) -> Pipeline:
    """Bundle raw-feature preprocessing and a regressor in one persisted artifact."""
    return Pipeline(steps=[("preprocessor", build_preprocessor()), ("regressor", regressor)])
