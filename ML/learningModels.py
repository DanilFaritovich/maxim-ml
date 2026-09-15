import logging

import pandas as pd
from scipy.stats import randint, uniform
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split

from DataBase.database import get_db
from DataBase.models import Feedback

from .preprocessing import model_preprocessing

logger = logging.getLogger(__name__)


def get_fresh_feedback():
    session = next(get_db())
    try:
        query = session.query(
            Feedback.MedInc,
            Feedback.HouseAge,
            Feedback.AveRooms,
            Feedback.AveBedrms,
            Feedback.Population,
            Feedback.AveOccup,
            Feedback.Latitude,
            Feedback.Longitude,
            Feedback.prediction,
        ).where(Feedback.is_correct)
        feedback = pd.DataFrame(
            list(query.all()),
            columns=[
                "MedInc",
                "HouseAge",
                "AveRooms",
                "AveBedrms",
                "Population",
                "AveOccup",
                "Latitude",
                "Longitude",
                "MedHouseVal",
            ],
        )
        logger.info("Loaded %s approved feedback records", len(feedback))
        return feedback
    finally:
        session.close()


def learn_linear_regression_model(df_data: pd.DataFrame, df_target: pd.DataFrame):
    # print(df_target)
    # Предобработка
    data_columns = list(df_data.columns)
    df: pd.DataFrame = pd.concat([df_data, df_target], axis="columns")
    db_df = get_fresh_feedback()
    if not db_df.empty:
        df = pd.concat([df, db_df], axis="rows")
    df = model_preprocessing(df, data_columns)

    # print(df)
    X_train, X_test, y_train, y_test = train_test_split(
        df[data_columns], df["MedHouseVal"], test_size=0.33, random_state=42
    )

    # Моделирование
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    R2 = r2_score(y_test, y_pred)
    MSE = mean_squared_error(y_test, y_pred)

    logger.info("Linear Regression trained: R2=%.4f MSE=%.4f", R2, MSE)

    # res = model.predict(X_test.head(1))
    # print(X_test.head(1))
    # print(y_test.head(1))
    # print(res)

    return model, R2, MSE


def learn_gradient_boosting_regressor_model(df_data: pd.DataFrame, df_target: pd.DataFrame):
    # print(df_target)
    # Предобработка
    data_columns = list(df_data.columns)
    df: pd.DataFrame = pd.concat([df_data, df_target], axis="columns")
    db_df = get_fresh_feedback()
    if not db_df.empty:
        df = pd.concat([df, db_df], axis="index")
    df = model_preprocessing(df, data_columns)

    # print(df)
    X_train, X_test, y_train, y_test = train_test_split(
        df[data_columns], df["MedHouseVal"], test_size=0.33, random_state=42
    )

    # Параметры для подбора
    param_dist = {
        "n_estimators": randint(50, 300),
        "learning_rate": uniform(0.01, 0.3),
        "max_depth": randint(1, 10),
        "min_samples_split": randint(2, 11),
        "min_samples_leaf": randint(1, 6),
        "subsample": uniform(0.6, 0.4),  # 0.6 до 1.0
    }

    # Настройка метрик
    scoring = {"r2": "r2", "mse": "neg_mean_squared_error"}

    # Модель
    model = GradientBoostingRegressor(random_state=42)

    # Поиск лучших параметров
    search = RandomizedSearchCV(
        model,
        param_dist,
        n_iter=50,  # количество случайных комбинаций
        scoring=scoring,
        refit="r2",
        cv=5,
        n_jobs=-1,
        verbose=1,
        random_state=42,
    )

    search.fit(X_train, y_train)

    # Вывод результатов
    logger.info("Gradient Boosting best parameters: %s", search.best_params_)

    y_pred = search.predict(X_test)

    R2 = r2_score(y_test, y_pred)
    MSE = mean_squared_error(y_test, y_pred)

    logger.info("Gradient Boosting trained: R2=%.4f MSE=%.4f", R2, MSE)

    return search, R2, MSE
