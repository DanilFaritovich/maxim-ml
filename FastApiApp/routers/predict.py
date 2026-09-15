import traceback

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ML import load_model, preprocessing_data_df

router = APIRouter(prefix="/predict", tags=["Predict"])


class PredictionResponse(BaseModel):
    status: str
    message: str
    prediction: float | None = None


class PredictionRequest(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@router.post("/{model_name}", response_model=PredictionResponse)
async def predict_item(model_name: str, data: PredictionRequest):
    try:
        # Загрузка модели
        if model_name == "linear_regression":
            model = load_model("liner_regression.pkl")
        elif model_name == "gradient_boosting_regressor":
            model = load_model("gradient_boosting_regressor.pkl")
        else:
            raise FileNotFoundError()

        # Преобразуем входные данные в массив numpy нужной формы
        input_data = np.array(
            [
                [
                    data.MedInc,
                    data.HouseAge,
                    data.AveRooms,
                    data.AveBedrms,
                    data.Population,
                    data.AveOccup,
                    data.Latitude,
                    data.Longitude,
                ]
            ]
        )

        input_data = preprocessing_data_df(
            pd.DataFrame(input_data, columns=list(data.__dict__.keys()))
        )

        # Предсказание
        prediction = model.predict(input_data)[0]
        prediction = round(prediction * 100_000, 3)

        return PredictionResponse(
            status="success",
            message=f"Предсказание выполнено моделью {model_name}",
            prediction=prediction,
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении предсказания: {str(e)}")
