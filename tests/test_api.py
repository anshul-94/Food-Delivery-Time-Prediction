
from pathlib import Path
from unittest.mock import patch

import joblib
from fastapi.testclient import TestClient


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_food_delivery_model.pkl"

FEATURES = [
    "Delivery_person_Age",
    "Delivery_person_Ratings",
    "Weatherconditions",
    "Road_traffic_density",
    "Vehicle_condition",
    "Type_of_order",
    "Type_of_vehicle",
    "multiple_deliveries",
    "Festival",
    "City",
    "Delivery_Distance",
    "Order_Hour",
    "Order_Minute",
    "Day_of_Week",
    "Month",
    "Is_Weekend",
]


class FakePipeline:
    """Lightweight model used only when the real artifact is unavailable."""

    feature_names_in_ = FEATURES

    def predict(self, dataframe):
        return [25.0]


if MODEL_PATH.exists():
    # Local development: use the actual trained model.
    from app.main import app
else:
    # CI: mock model loading without needing the 210 MB artifact.
    original_exists = Path.exists

    def exists_for_ci(path):
        if path == MODEL_PATH:
            return True
        return original_exists(path)

    with (
        patch.object(Path, "exists", exists_for_ci),
        patch.object(joblib, "load", return_value=FakePipeline()),
    ):
        from app.main import app


client = TestClient(app)


def valid_payload():
    return {
        "Delivery_person_Age": 28,
        "Delivery_person_Ratings": 4.7,
        "Weatherconditions": "Sunny",
        "Road_traffic_density": "Low",
        "Vehicle_condition": 2,
        "Type_of_order": "Snack",
        "Type_of_vehicle": "motorcycle",
        "multiple_deliveries": 1,
        "Festival": "No",
        "City": "Urban",
        "Delivery_Distance": 5.5,
        "Order_Hour": 14,
        "Order_Minute": 30,
        "Day_of_Week": "Monday",
        "Month": 9,
        "Is_Weekend": 0,
    }


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "DeliveryTime" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


def test_prediction_success():
    response = client.post("/predict", json=valid_payload())
    assert response.status_code == 200

    result = response.json()
    assert isinstance(
        result["predicted_delivery_time_minutes"], (int, float)
    )
    assert result["predicted_delivery_time_minutes"] >= 0
    assert result["unit"] == "minutes"


def test_missing_required_field():
    payload = valid_payload()
    payload.pop("Delivery_Distance")

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_invalid_hour():
    payload = valid_payload()
    payload["Order_Hour"] = 25

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_frontend_css_is_served():
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert "font-family" in response.text
