from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TrainHistory(Base):
    __tablename__ = "train_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=False)
    R2 = Column(Float, nullable=False)
    MSE = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    MedInc = Column(Float)
    HouseAge = Column(Float)
    AveRooms = Column(Float)
    AveBedrms = Column(Float)
    Population = Column(Float)
    AveOccup = Column(Float)
    Latitude = Column(Float)
    Longitude = Column(Float)
    model_name = Column(String)
    prediction = Column(Float)
    is_correct = Column(Boolean)
