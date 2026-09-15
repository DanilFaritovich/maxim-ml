# MaximML

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)](https://www.sqlalchemy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-f7931e?logo=scikitlearn)](https://scikit-learn.org/)
[![React](https://img.shields.io/badge/React-Frontend-61dafb?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178c6?logo=typescript)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**MaximML** is a full-stack machine-learning application for training regression models, predicting California Housing prices, and collecting feedback on prediction results. It combines a FastAPI backend, SQLite persistence, and a typed React interface.

The project was built as a portfolio application to demonstrate practical Python ML workflows together with an HTTP API, a TypeScript frontend, model persistence, and local training history.

## What this project demonstrates

### Backend and ML

- FastAPI REST API with typed Pydantic request and response models.
- Regression workflow based on the California Housing dataset.
- Linear Regression and Gradient Boosting Regressor training pipelines.
- Feature preprocessing, outlier handling, geohash-based location features, and scaling.
- Saved model artifacts loaded by the prediction API.
- SQLAlchemy models for training history and user feedback.
- CORS configuration for the local React client.

### Frontend

- React + TypeScript single-page interface.
- Forms for submitting housing characteristics and receiving predictions.
- Controls for launching model training.
- Training history view backed by the FastAPI API.
- Typed Axios client for backend requests.

## Tech stack

| Area | Technologies |
| --- | --- |
| Backend | Python 3.12, FastAPI, Pydantic, SQLAlchemy |
| Machine learning | scikit-learn, pandas, NumPy, category-encoders |
| Frontend | React, TypeScript, Axios, Create React App |
| Infrastructure | Docker, Docker Compose, Nginx |
| CI | GitHub Actions |
| Persistence | SQLite |
| Model artifacts | joblib / pickle |

## Architecture

```text
React / TypeScript UI
        │
        │ HTTP
        ▼
FastAPI routers
        │
        ├── Prediction router
        ├── Training router
        └── Feedback router
                │
                ├── ML preprocessing and model services
                ├── Saved model artifacts
                └── SQLAlchemy
                        │
                        ▼
                      SQLite
```

The frontend is responsible for user interaction and API requests. Dataset preparation, training, prediction, and persistence remain on the backend.

## Run the application with Docker

Requirements:

- Docker Engine or Docker Desktop
- Docker Compose

```bash
docker compose up --build
```

Open the application at:

```text
http://127.0.0.1:8080
```

Nginx serves the React build and proxies API requests to the FastAPI container. The SQLite database and trained model artifacts are stored in named Docker volumes, so they survive container recreation.

## Run for development

### Backend

Requirements: Python 3.12. The pinned dependency set has not been verified with newer Python releases.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Requirements: Node.js and npm.

```bash
cd react-app
npm ci
npm start
```

The client normally starts at:

```text
http://localhost:3000
```

For local development, configure a development proxy or run the frontend through Docker Compose.

## API overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/predict/{model_name}` | Predict a housing price |
| `POST` | `/train/{model_name}` | Train and save a model |
| `GET` | `/train/history` | Return training history |
| `POST` | `/train_feedback/feedback` | Store prediction feedback |

Supported `{model_name}` values:

- `linear_regression`
- `gradient_boosting_regressor`

Example prediction request:

```bash
curl -X POST http://127.0.0.1:8000/predict/gradient_boosting_regressor \\
  -H "Content-Type: application/json" \\
  -d '{
    "MedInc": 8.3252,
    "HouseAge": 41,
    "AveRooms": 6.984127,
    "AveBedrms": 1.023810,
    "Population": 322,
    "AveOccup": 2.264706,
    "Latitude": 37.88,
    "Longitude": -122.23
  }'
```

## Quality checks

### Backend

Install development dependencies and run:

```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
ruff format --check .
mypy
pytest -q
```

### Frontend production build

```bash
cd react-app
npm run format:check
npm run lint
npm run typecheck
npm run test:ci
npm run build
```

GitHub Actions runs these quality checks for pull requests and commits to `develop` and `main`, then verifies that Docker images build successfully.

## Development workflow

- `main` contains reviewed, release-ready code.
- `develop` is the integration branch for completed changes.
- Create feature and fix branches from `develop`, then open a merge request back to `develop`.
- Merge `develop` into `main` through a reviewed merge request after all CI jobs pass.

Direct pushes to `main` and `develop` must be disabled with GitHub branch protection rules.

## Project structure

```text
.
├── FastApiApp/          # FastAPI application and API routers
├── ML/                  # dataset, preprocessing, training, and model utilities
├── DataBase/            # SQLAlchemy models and SQLite configuration
├── models/              # saved regressors and encoder
├── react-app/           # React + TypeScript client
├── requirements.txt     # Python dependencies
└── main.py              # backend entry point
```

## Current limitations

- SQLite is used for the current local demo build.
- Model artifacts are versioned directly in Git; Git LFS may be appropriate if they grow substantially.

## Possible next steps

- Add automated backend and frontend test suites.
- Add CI checks for formatting, tests, and production builds.
- Move API configuration to environment variables.
- Add model-quality metrics and dataset versioning to the interface.

## License

Released under the [MIT License](LICENSE).
