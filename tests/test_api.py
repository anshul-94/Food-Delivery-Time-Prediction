
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def valid_payload():
    """Return a valid example request for the prediction API."""
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
        result["predicted_delivery_time_minutes"],
        (int, float),
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
