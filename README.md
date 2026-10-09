
# Food Delivery Time Prediction

## Overview
An end-to-end machine learning application that estimates
food delivery time using delivery, traffic, weather,
distance and order-time features.

## Tech Stack
- Python
- Pandas and NumPy
- Scikit-learn
- Random Forest Regressor
- FastAPI
- HTML, CSS and JavaScript
- Pytest
- Git and GitHub

## Application Features
- Saved preprocessing and model pipeline
- REST API for delivery time predictions
- Input validation using Pydantic
- Responsive web interface
- Automated API tests

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Open the web application:

http://127.0.0.1:8000/

API documentation:

http://127.0.0.1:8000/docs

## Run Tests

```bash
python -m pytest -v
```

## Model Evaluation
Add the actual MAE, RMSE and R² values from the
model evaluation notebook.

## Limitations
Predictions are estimates, not guaranteed delivery times.
Performance depends on training data quality and whether
prediction inputs match the training feature definitions.
