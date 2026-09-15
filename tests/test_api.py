from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

SAMPLE_HOUSING = {
    "MedInc": 8.3252,
    "HouseAge": 41,
    "AveRooms": 6.984127,
    "AveBedrms": 1.023810,
    "Population": 322,
    "AveOccup": 2.264706,
    "Latitude": 37.88,
    "Longitude": -122.23,
}


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prediction_returns_a_value() -> None:
    response = client.post("/predict/linear_regression", json=SAMPLE_HOUSING)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["prediction"], float)


def test_unknown_model_is_rejected() -> None:
    response = client.post("/predict/unknown", json=SAMPLE_HOUSING)

    assert response.status_code == 404


def test_training_history_is_a_list() -> None:
    response = client.get("/train/history")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
