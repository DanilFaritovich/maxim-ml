from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TrainHistory(Base):
    __tablename__ = "train_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    R2: Mapped[float] = mapped_column(Float, nullable=False)
    MSE: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    MedInc: Mapped[float | None] = mapped_column(Float)
    HouseAge: Mapped[float | None] = mapped_column(Float)
    AveRooms: Mapped[float | None] = mapped_column(Float)
    AveBedrms: Mapped[float | None] = mapped_column(Float)
    Population: Mapped[float | None] = mapped_column(Float)
    AveOccup: Mapped[float | None] = mapped_column(Float)
    Latitude: Mapped[float | None] = mapped_column(Float)
    Longitude: Mapped[float | None] = mapped_column(Float)
    model_name: Mapped[str | None] = mapped_column(String)
    prediction: Mapped[float | None] = mapped_column(Float)
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
