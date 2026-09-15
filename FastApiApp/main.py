from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.predict import router as predict_router
from .routers.reLearnModels import router as train_router
from .routers.train_feedback import router as train_feedback_router

app = FastAPI(title="FastAPI с async и роутерами")

# Разрешённые источники (добавьте сюда адрес вашего фронтенда)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Можно добавить другие адреса, если фронтенд размещён в другом месте
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешённые источники
    allow_credentials=True,  # Разрешить куки и авторизацию
    allow_methods=["*"],  # Разрешить все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключение роутеров
app.include_router(train_router)
app.include_router(predict_router)
app.include_router(train_feedback_router)
