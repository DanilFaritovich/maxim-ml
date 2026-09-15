import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DataBase.database import SessionLocal, get_db
from DataBase.models import TrainHistory
from ML import (
    get_data_set_data,
    get_data_set_target,
    learn_gradient_boosting_regressor_model,
    learn_linear_regression_model,
    save_model,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/train", tags=["Train"])


class TrainResponse(BaseModel):
    status: str
    message: str
    model_name: str | None = None


@router.post("/{model_name}", response_model=TrainResponse)
def create_item(model_name: str):
    db = SessionLocal()
    try:
        logger.info("Training requested for model=%s", model_name)
        if model_name == "linear_regression":
            model, R2, MSE = learn_linear_regression_model(
                get_data_set_data(), get_data_set_target()
            )
            save_model(model, "liner_regression.pkl")
            status = "success"
            message = "Модель Linear Regression успешно обучена"
        elif model_name == "gradient_boosting_regressor":
            model, R2, MSE = learn_gradient_boosting_regressor_model(
                get_data_set_data(), get_data_set_target()
            )
            save_model(model, "gradient_boosting_regressor.pkl")
            status = "success"
            message = "Модель Gradient Boosting Regressor успешно обучена"
        else:
            raise HTTPException(status_code=400, detail=f"Модель '{model_name}' не поддерживается")
        history = TrainHistory(
            model_name=model_name,
            status=status,
            message=message,
            R2=R2,
            MSE=MSE,
            timestamp=datetime.now(timezone.utc),
        )
        db.add(history)
        db.commit()
        logger.info("Training completed for model=%s R2=%.4f MSE=%.4f", model_name, R2, MSE)
        return TrainResponse(status=status, message=message, model_name=model_name)
    except Exception as e:
        db.add(
            TrainHistory(
                model_name=model_name,
                status="error",
                message=str(e),
                R2=0,
                MSE=0,
                timestamp=datetime.now(timezone.utc),
            )
        )
        db.commit()
        logger.exception("Training failed for model=%s", model_name)
        raise
    finally:
        db.close()


class TrainHistoryResponse(BaseModel):
    id: int
    model_name: str
    status: str
    message: str
    R2: float
    MSE: float
    timestamp: str


@router.get("/history", response_model=List[TrainHistoryResponse])
def get_train_history(db: Session = Depends(get_db)):
    history = db.query(TrainHistory).order_by(TrainHistory.timestamp.desc()).all()
    return [
        TrainHistoryResponse(
            id=row.id,
            model_name=row.model_name,
            status=row.status,
            message=row.message,
            R2=row.R2,
            MSE=row.MSE,
            timestamp=row.timestamp.isoformat(),
        )
        for row in history
    ]
