from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from services.ml_service import ml_service

router = APIRouter(prefix="/predict", tags=["ML Predictions"])

class CKDInput(BaseModel):
    # Flexible input to match web_app.py logic
    # We use a dict to accept whatever the frontend sends, 
    # as the model handling is done dynamically in the service
    data: Dict[str, Any]

class HeartInput(BaseModel):
    age_years: float
    bmi: float
    ap_hi: float
    ap_lo: float
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int

class FitbitInput(BaseModel):
    # Core features needed for prediction
    TotalSteps: float = Field(..., description="Daily total steps")
    TotalDistance: float
    TrackerDistance: float
    LoggedActivitiesDistance: float
    VeryActiveDistance: float
    ModeratelyActiveDistance: float
    LightActiveDistance: float
    SedentaryActiveDistance: float
    VeryActiveMinutes: float
    FairlyActiveMinutes: float
    LightlyActiveMinutes: float
    SedentaryMinutes: float
    Calories: float
    TotalSleepRecords: float
    TotalMinutesAsleep: float
    TotalTimeInBed: float
    # Optional date for improved feature engineering
    date: Optional[str] = None 

@router.post("/ckd")
async def predict_ckd(input_data: Dict[str, Any]):
    """
    Predict Chronic Kidney Disease risk
    """
    result = ml_service.predict_ckd(input_data)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/heart")
async def predict_heart(input_data: HeartInput):
    """
    Predict Heart Disease / Cardiovascular anomaly risk
    """
    result = ml_service.predict_heart(input_data.dict())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/fitbit")
async def predict_fitbit(input_data: FitbitInput):
    """
    Predict anomaly pattern in Fitbit daily activity/health data
    """
    result = ml_service.predict_fitbit(input_data.dict())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
