"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

# ============================================================================
# Input Models
# ============================================================================

class DiabetesInput(BaseModel):
    """Input data for diabetes prediction"""
    pregnancies: float = Field(0, ge=0, le=20, description="Number of pregnancies")
    glucose: float = Field(100, ge=0, le=300, description="Glucose level (mg/dL)")
    blood_pressure: float = Field(80, ge=0, le=200, description="Blood pressure (mmHg)")
    skin_thickness: float = Field(20, ge=0, le=100, description="Skin thickness (mm)")
    insulin: float = Field(79, ge=0, le=900, description="Insulin level (mu U/ml)")
    bmi: float = Field(25, ge=0, le=70, description="Body Mass Index")
    diabetes_pedigree: float = Field(0.5, ge=0, le=2.5, description="Diabetes pedigree function")
    age: float = Field(30, ge=1, le=120, description="Age in years")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregnancies": 1,
                "glucose": 120,
                "blood_pressure": 80,
                "skin_thickness": 20,
                "insulin": 79,
                "bmi": 25.5,
                "diabetes_pedigree": 0.5,
                "age": 35
            }
        }

class AsthmaInput(BaseModel):
    """Input data for asthma prediction"""
    gender_male: int = Field(0, ge=0, le=1, description="Gender (1 for Male, 0 for Female)")
    smoking_ex: int = Field(0, ge=0, le=1, description="Ex-smoker status")
    smoking_non: int = Field(1, ge=0, le=1, description="Non-smoker status")
    age: float = Field(0.5, ge=0, le=1, description="Normalized age")
    peak_flow: float = Field(0.5, ge=0.1, le=1, description="Peak flow rate (L/sec)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gender_male": 1,
                "smoking_ex": 0,
                "smoking_non": 1,
                "age": 0.5,
                "peak_flow": 0.6
            }
        }

class CardioInput(BaseModel):
    """Input data for cardiovascular disease prediction"""
    age: int = Field(40, ge=29, le=65, description="Age in years")
    ap_hi: int = Field(120, ge=90, le=200, description="Systolic blood pressure")
    ap_lo: int = Field(80, ge=60, le=140, description="Diastolic blood pressure")
    cholesterol: int = Field(1, ge=1, le=3, description="Cholesterol level (1=Normal, 2=Above Normal, 3=Well Above Normal)")
    gluc: int = Field(1, ge=1, le=3, description="Glucose level (1=Normal, 2=Above Normal, 3=Well Above Normal)")
    smoke: int = Field(0, ge=0, le=1, description="Smoking status (0=No, 1=Yes)")
    alco: int = Field(0, ge=0, le=1, description="Alcohol consumption (0=No, 1=Yes)")
    active: int = Field(1, ge=0, le=1, description="Physical activity (0=No, 1=Yes)")
    weight: float = Field(70, ge=30, le=200, description="Weight in kg")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "ap_hi": 120,
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1,
                "weight": 75
            }
        }

class StrokeInput(BaseModel):
    """Input data for stroke prediction"""
    age: int = Field(50, ge=0, le=82, description="Age in years")
    hypertension: int = Field(0, ge=0, le=1, description="Hypertension (0=No, 1=Yes)")
    heart_disease: int = Field(0, ge=0, le=1, description="Heart disease (0=No, 1=Yes)")
    ever_married: int = Field(1, ge=0, le=1, description="Marital status (0=No, 1=Yes)")
    avg_glucose_level: float = Field(120, ge=55, le=270, description="Average glucose level")
    bmi: float = Field(25, ge=13.5, le=98, description="Body Mass Index")
    smoking_status: int = Field(0, ge=0, le=3, description="Smoking status (0=Never, 1=Former, 2=Smokes, 3=Unknown)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 55,
                "hypertension": 0,
                "heart_disease": 0,
                "ever_married": 1,
                "avg_glucose_level": 120,
                "bmi": 25.5,
                "smoking_status": 0
            }
        }

class HypertensionInput(BaseModel):
    """Input data for hypertension prediction"""
    male: int = Field(0, ge=0, le=1, description="Gender (0=Female, 1=Male)")
    age: int = Field(49, ge=32, le=70, description="Age in years")
    cigsPerDay: float = Field(0, ge=0, le=70, description="Cigarettes per day")
    BPMeds: float = Field(0, ge=0, le=1, description="Blood pressure medication (0=No, 1=Yes)")
    totChol: float = Field(200, ge=107, le=500, description="Total cholesterol")
    sysBP: float = Field(120, ge=83.5, le=295, description="Systolic blood pressure")
    diaBP: float = Field(80, ge=48, le=142.5, description="Diastolic blood pressure")
    BMI: float = Field(24, ge=15.54, le=56.8, description="Body Mass Index")
    heartRate: float = Field(72, ge=44, le=143, description="Heart rate")
    glucose: float = Field(90, ge=40, le=394, description="Glucose level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "male": 1,
                "age": 50,
                "cigsPerDay": 0,
                "BPMeds": 0,
                "totChol": 200,
                "sysBP": 120,
                "diaBP": 80,
                "BMI": 24.5,
                "heartRate": 72,
                "glucose": 90
            }
        }

# ============================================================================
# Response Models
# ============================================================================

class PredictionResponse(BaseModel):
    """Standard prediction response model"""
    success: bool = Field(True, description="Whether the prediction was successful")
    prediction: int = Field(..., description="Prediction result (0=Negative/Low Risk, 1=Positive/High Risk)")
    probability: float = Field(..., description="Confidence probability (0-100)")
    risk_level: str = Field(..., description="Risk level (Low/Moderate/High)")
    message: str = Field(..., description="Human-readable prediction message")
    recommendations: List[str] = Field(default_factory=list, description="Personalized recommendations")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Prediction timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": 0,
                "probability": 85.5,
                "risk_level": "Low",
                "message": "Not Diabetic",
                "recommendations": ["Maintain healthy lifestyle", "Regular exercise"],
                "timestamp": "2024-01-01T12:00:00"
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    models_loaded: int
    models: List[str]
    version: str
    timestamp: str

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    message: str
    timestamp: str