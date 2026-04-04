"""
Prediction endpoints for all diseases
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.dependencies import get_model_manager
from pydantic import BaseModel, Field

router = APIRouter()

# Define input models
class DiabetesInput(BaseModel):
    pregnancies: float = Field(0, ge=0, le=20)
    glucose: float = Field(100, ge=0, le=300)
    blood_pressure: float = Field(80, ge=0, le=200)
    skin_thickness: float = Field(20, ge=0, le=100)
    insulin: float = Field(79, ge=0, le=900)
    bmi: float = Field(25, ge=0, le=70)
    diabetes_pedigree: float = Field(0.5, ge=0, le=2.5)
    age: float = Field(30, ge=1, le=120)


@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesInput):
    """
    Predict diabetes risk using SVC model
    """
    try:
        model_manager = get_model_manager()
        result = model_manager.predict_diabetes(data)
        return {
            "success": True,
            **result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    model_manager = get_model_manager()
    return {
        "status": "healthy",
        "models_loaded": len(model_manager.models),
        "models": list(model_manager.models.keys()),
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }