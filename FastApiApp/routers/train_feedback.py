import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DataBase.database import get_db
from DataBase.models import Feedback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/train_feedback", tags=["TrainFeedback"])


class FeedbackRequest(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float
    modelName: str
    prediction: float
    isCorrect: bool


@router.post("/feedback")
def add_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    try:
        existing = (
            db.query(Feedback)
            .filter_by(
                MedInc=feedback.MedInc,
                HouseAge=feedback.HouseAge,
                AveRooms=feedback.AveRooms,
                AveBedrms=feedback.AveBedrms,
                Population=feedback.Population,
                AveOccup=feedback.AveOccup,
                Latitude=feedback.Latitude,
                Longitude=feedback.Longitude,
                model_name=feedback.modelName,
                prediction=feedback.prediction,
                is_correct=feedback.isCorrect,
            )
            .first()
        )

        if existing:
            logger.info("Duplicate feedback received for model=%s", feedback.modelName)
            return {"status": "duplicate", "message": "Такой отзыв уже существует"}

        feedback_record = Feedback(
            MedInc=feedback.MedInc,
            HouseAge=feedback.HouseAge,
            AveRooms=feedback.AveRooms,
            AveBedrms=feedback.AveBedrms,
            Population=feedback.Population,
            AveOccup=feedback.AveOccup,
            Latitude=feedback.Latitude,
            Longitude=feedback.Longitude,
            model_name=feedback.modelName,
            prediction=feedback.prediction,
            is_correct=feedback.isCorrect,
        )
        db.add(feedback_record)
        db.commit()
        logger.info("Feedback stored for model=%s", feedback.modelName)
        return {"status": "success", "message": "Отзыв успешно добавлен"}
    except Exception as e:
        db.rollback()
        logger.exception("Failed to store feedback")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении отзыва: {str(e)}",
        )
