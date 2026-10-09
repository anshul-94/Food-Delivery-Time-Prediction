from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_food_delivery_model.pkl"


# Load the complete ML pipeline
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

model_pipeline = joblib.load(MODEL_PATH)


# FastAPI application
app = FastAPI(
    title="Food Delivery Time Prediction API",
    description=(
        "Predict food delivery time using a trained "
        "Random Forest machine learning pipeline."
    ),
    version="1.0.0",
)


FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static",
)

# Request schema: exactly 16 model features
class DeliveryInput(BaseModel):
    Delivery_person_Age: float = Field(gt=0, le=100)
    Delivery_person_Ratings: float = Field(ge=0, le=5)

    Weatherconditions: str
    Road_traffic_density: str
    Vehicle_condition: int = Field(ge=0, le=10)

    Type_of_order: str
    Type_of_vehicle: str

    multiple_deliveries: float = Field(ge=0)
    Festival: str
    City: str

    Delivery_Distance: float = Field(gt=0)
    Order_Hour: int = Field(ge=0, le=23)
    Order_Minute: int = Field(ge=0, le=59)
    Day_of_Week: str
    Month: int = Field(ge=1, le=12)
    Is_Weekend: int = Field(ge=0, le=1)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model_pipeline is not None,
    }


@app.post("/predict")
def predict_delivery_time(data: DeliveryInput):
    try:
        input_df = pd.DataFrame(
            [data.model_dump()]
        )

        # Preserve the exact training feature order
        expected_features = list(
            model_pipeline.feature_names_in_
        )

        input_df = input_df[expected_features]

        prediction = model_pipeline.predict(input_df)[0]

        return {
            "predicted_delivery_time_minutes": round(
                max(0.0, float(prediction)), 2
            ),
            "unit": "minutes",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=(
                "Invalid input category or feature value. "
                f"Check your training categories. Details: {exc}"
            ),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the server logs.",
        ) from exc
