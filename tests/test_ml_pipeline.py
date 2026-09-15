import pandas as pd
from sklearn.linear_model import LinearRegression

from ML.pipeline import FEATURE_COLUMNS, build_model_pipeline


def _housing_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [2.0, 10, 4.0, 1.0, 100, 2.0, 34.0, -118.0],
            [3.0, 15, 5.0, 1.1, 200, 2.2, 35.0, -119.0],
            [4.0, 20, 6.0, 1.2, 300, 2.4, 36.0, -120.0],
            [5.0, 25, 7.0, 1.3, 400, 2.6, 37.0, -121.0],
            [6.0, 30, 8.0, 1.4, 500, 2.8, 38.0, -122.0],
            [7.0, 35, 9.0, 1.5, 600, 3.0, 39.0, -123.0],
        ],
        columns=FEATURE_COLUMNS,
    )


def test_pipeline_uses_fitted_preprocessing_for_consistent_predictions() -> None:
    features = _housing_rows()
    target = pd.Series([1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    pipeline = build_model_pipeline(LinearRegression()).fit(features, target)

    first_prediction = pipeline.predict(features.iloc[[0]])[0]
    repeated_prediction = pipeline.predict(features.iloc[[0]])[0]
    another_prediction = pipeline.predict(features.iloc[[5]])[0]

    assert first_prediction == repeated_prediction
    assert first_prediction != another_prediction


def test_scaler_is_fitted_on_training_rows_not_prediction_row() -> None:
    features = _housing_rows()
    pipeline = build_model_pipeline(LinearRegression()).fit(
        features, pd.Series(range(len(features)))
    )

    transformed = pipeline.named_steps["preprocessor"].transform(features.iloc[[0]])

    # A scaler fitted on this single prediction row would produce zeroes for every numeric feature.
    assert transformed[0, : len(FEATURE_COLUMNS)].any()
