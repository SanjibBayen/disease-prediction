"""
Pydantic models for request/response validation

This module defines all data models used for API request validation
and response formatting for the HealthPredict AI system.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

class RiskLevel:
    """Risk level constants"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class ValidationMessages:
    """Validation error messages"""
    INVALID_RANGE = "Value must be between {min} and {max}"
    INVALID_BINARY = "Value must be 0 or 1"
    INVALID_POSITIVE = "Value cannot be negative"
    INVALID_SMOKING = "Smoking status values are inconsistent"
    INVALID_BP = "Systolic pressure must be greater than diastolic pressure"
    REQUIRED_FIELD = "This field is required"


# ============================================================================
# BASE MODEL WITH COMMON FUNCTIONALITY
# ============================================================================

class BaseHealthModel(BaseModel):
    """Base model with common validation methods"""
    
    model_config = {
        "validate_assignment": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


# ============================================================================
# INPUT MODELS
# ============================================================================

class DiabetesInput(BaseHealthModel):
    """
    Input data for diabetes prediction
    """
    pregnancies: float = Field(
        default=0, 
        ge=0, 
        le=20,
        description="Number of pregnancies",
        examples=[1]
    )
    glucose: float = Field(
        default=100, 
        ge=0, 
        le=300,
        description="Glucose level (mg/dL)",
        examples=[120]
    )
    blood_pressure: float = Field(
        default=80, 
        ge=0, 
        le=200,
        description="Blood pressure (mmHg)",
        examples=[80]
    )
    skin_thickness: float = Field(
        default=20, 
        ge=0, 
        le=100,
        description="Skin thickness (mm)",
        examples=[20]
    )
    insulin: float = Field(
        default=79, 
        ge=0, 
        le=900,
        description="Insulin level (mu U/ml)",
        examples=[79]
    )
    bmi: float = Field(
        default=25, 
        ge=0, 
        le=70,
        description="Body Mass Index",
        examples=[25.5]
    )
    diabetes_pedigree: float = Field(
        default=0.5, 
        ge=0, 
        le=2.5,
        description="Diabetes pedigree function",
        examples=[0.5]
    )
    age: float = Field(
        default=30, 
        ge=1, 
        le=120,
        description="Age in years",
        examples=[35]
    )
    
    @field_validator('pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                     'insulin', 'bmi', 'diabetes_pedigree', 'age')
    @classmethod
    def validate_non_negative(cls, v: float, info) -> float:
        """Validate that values are non-negative"""
        if v < 0:
            raise ValueError(f"{info.field_name} cannot be negative. Got: {v}")
        return v
    
    @field_validator('glucose')
    @classmethod
    def validate_glucose(cls, v: float) -> float:
        """Additional glucose-specific validation"""
        if 0 < v < 50:
            raise ValueError(f"Glucose value {v} mg/dL is unusually low. Please verify.")
        if v > 250:
            raise ValueError(f"Glucose value {v} mg/dL is very high. Please verify.")
        return v
    
    @field_validator('bmi')
    @classmethod
    def validate_bmi(cls, v: float) -> float:
        """Additional BMI validation"""
        if v < 15:
            raise ValueError(f"BMI {v} is severely underweight. Please verify.")
        if v > 50:
            raise ValueError(f"BMI {v} is extremely high. Please verify.")
        return v
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v: float) -> float:
        """Validate age is reasonable"""
        if v < 18:
            raise ValueError(f"Age {v} is below 18. This model is designed for adults.")
        return v
    
    model_config = {
        "json_schema_extra": {
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
    }


class AsthmaInput(BaseHealthModel):
    """
    Input data for asthma prediction
    """
    gender_male: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Gender (1 for Male, 0 for Female)",
        examples=[1]
    )
    smoking_ex: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Ex-smoker status (1 for Yes)",
        examples=[0]
    )
    smoking_non: int = Field(
        default=1, 
        ge=0, 
        le=1,
        description="Non-smoker status (1 for Yes)",
        examples=[1]
    )
    age: float = Field(
        default=0.5, 
        ge=0, 
        le=1,
        description="Normalized age (0-1)",
        examples=[0.5]
    )
    peak_flow: float = Field(
        default=0.5, 
        ge=0.1, 
        le=1,
        description="Peak flow rate (L/sec)",
        examples=[0.6]
    )
    
    @field_validator('gender_male', 'smoking_ex', 'smoking_non')
    @classmethod
    def validate_binary_values(cls, v: int, info) -> int:
        """Validate binary fields (0 or 1)"""
        if v not in [0, 1]:
            raise ValueError(f"{info.field_name} must be 0 or 1. Got: {v}")
        return v
    
    @model_validator(mode='after')
    def validate_smoking_status(self) -> 'AsthmaInput':
        """Ensure smoking status is consistent"""
        if self.smoking_ex + self.smoking_non != 1:
            raise ValueError("Exactly one of smoking_ex or smoking_non must be 1")
        return self
    
    @field_validator('peak_flow')
    @classmethod
    def validate_peak_flow(cls, v: float) -> float:
        """Validate peak flow value"""
        if v < 0.2:
            raise ValueError(f"Peak flow {v} L/sec is very low. Please verify.")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "gender_male": 1,
                "smoking_ex": 0,
                "smoking_non": 1,
                "age": 0.5,
                "peak_flow": 0.6
            }
        }
    }


class CardioInput(BaseHealthModel):
    """
    Input data for cardiovascular disease prediction
    """
    age: int = Field(
        default=40, 
        ge=29, 
        le=65,
        description="Age in years",
        examples=[45]
    )
    ap_hi: int = Field(
        default=120, 
        ge=90, 
        le=200,
        description="Systolic blood pressure (mmHg)",
        examples=[120]
    )
    ap_lo: int = Field(
        default=80, 
        ge=60, 
        le=140,
        description="Diastolic blood pressure (mmHg)",
        examples=[80]
    )
    cholesterol: int = Field(
        default=1, 
        ge=1, 
        le=3,
        description="Cholesterol level (1=Normal, 2=Above, 3=Well Above)",
        examples=[1]
    )
    gluc: int = Field(
        default=1, 
        ge=1, 
        le=3,
        description="Glucose level (1=Normal, 2=Above, 3=Well Above)",
        examples=[1]
    )
    smoke: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Smoking status (0=No, 1=Yes)",
        examples=[0]
    )
    alco: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Alcohol consumption (0=No, 1=Yes)",
        examples=[0]
    )
    active: int = Field(
        default=1, 
        ge=0, 
        le=1,
        description="Physical activity (0=No, 1=Yes)",
        examples=[1]
    )
    weight: float = Field(
        default=70, 
        ge=30, 
        le=200,
        description="Weight in kg",
        examples=[75]
    )
    
    @field_validator('age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'weight')
    @classmethod
    def validate_non_negative(cls, v, info) -> float:
        """Validate that values are non-negative"""
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative. Got: {v}")
        return v
    
    @model_validator(mode='after')
    def validate_bp_relationship(self) -> 'CardioInput':
        """Validate that systolic pressure > diastolic pressure"""
        if self.ap_hi <= self.ap_lo:
            raise ValueError(f"Systolic pressure ({self.ap_hi}) must be greater than diastolic pressure ({self.ap_lo})")
        
        pulse_pressure = self.ap_hi - self.ap_lo
        if pulse_pressure < 20:
            raise ValueError(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally low")
        if pulse_pressure > 100:
            raise ValueError(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally high")
        
        return self
    
    @field_validator('cholesterol', 'gluc')
    @classmethod
    def validate_level(cls, v: int, info) -> int:
        """Validate cholesterol and glucose levels"""
        if v not in [1, 2, 3]:
            raise ValueError(f"{info.field_name} must be 1, 2, or 3. Got: {v}")
        return v
    
    model_config = {
        "json_schema_extra": {
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
    }


class StrokeInput(BaseHealthModel):
    """
    Input data for stroke prediction
    """
    age: int = Field(
        default=50, 
        ge=0, 
        le=82,
        description="Age in years",
        examples=[55]
    )
    hypertension: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Hypertension (0=No, 1=Yes)",
        examples=[0]
    )
    heart_disease: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Heart disease (0=No, 1=Yes)",
        examples=[0]
    )
    ever_married: int = Field(
        default=1, 
        ge=0, 
        le=1,
        description="Marital status (0=No, 1=Yes)",
        examples=[1]
    )
    avg_glucose_level: float = Field(
        default=120, 
        ge=55, 
        le=270,
        description="Average glucose level (mg/dL)",
        examples=[120]
    )
    bmi: float = Field(
        default=25, 
        ge=13.5, 
        le=98,
        description="Body Mass Index",
        examples=[25.5]
    )
    smoking_status: int = Field(
        default=0, 
        ge=0, 
        le=3,
        description="Smoking status (0=Never,1=Former,2=Smokes,3=Unknown)",
        examples=[0]
    )
    
    @field_validator('hypertension', 'heart_disease', 'ever_married')
    @classmethod
    def validate_binary_fields(cls, v: int, info) -> int:
        """Validate binary fields (0 or 1)"""
        if v not in [0, 1]:
            raise ValueError(f"{info.field_name} must be 0 or 1. Got: {v}")
        return v
    
    @field_validator('smoking_status')
    @classmethod
    def validate_smoking_status(cls, v: int) -> int:
        """Validate smoking status is within range"""
        if v not in [0, 1, 2, 3]:
            raise ValueError(f"smoking_status must be 0, 1, 2, or 3. Got: {v}")
        return v
    
    @field_validator('avg_glucose_level')
    @classmethod
    def validate_glucose(cls, v: float) -> float:
        """Validate glucose level"""
        if v < 70:
            raise ValueError(f"Glucose level {v} mg/dL is very low. Please verify.")
        if v > 200:
            raise ValueError(f"Glucose level {v} mg/dL is very high. Please verify.")
        return v
    
    @field_validator('bmi')
    @classmethod
    def validate_bmi(cls, v: float) -> float:
        """Validate BMI"""
        if v < 16:
            raise ValueError(f"BMI {v} is severely underweight. Please verify.")
        if v > 40:
            raise ValueError(f"BMI {v} is very high. Please verify.")
        return v
    
    model_config = {
        "json_schema_extra": {
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
    }


class HypertensionInput(BaseHealthModel):
    """
    Input data for hypertension prediction
    """
    male: int = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Gender (0=Female, 1=Male)",
        examples=[1]
    )
    age: int = Field(
        default=49, 
        ge=32, 
        le=70,
        description="Age in years",
        examples=[50]
    )
    cigsPerDay: float = Field(
        default=0, 
        ge=0, 
        le=70,
        description="Cigarettes per day",
        examples=[0]
    )
    BPMeds: float = Field(
        default=0, 
        ge=0, 
        le=1,
        description="Blood pressure medication (0=No, 1=Yes)",
        examples=[0]
    )
    totChol: float = Field(
        default=200, 
        ge=107, 
        le=500,
        description="Total cholesterol (mg/dL)",
        examples=[200]
    )
    sysBP: float = Field(
        default=120, 
        ge=83.5, 
        le=295,
        description="Systolic blood pressure (mmHg)",
        examples=[120]
    )
    diaBP: float = Field(
        default=80, 
        ge=48, 
        le=142.5,
        description="Diastolic blood pressure (mmHg)",
        examples=[80]
    )
    BMI: float = Field(
        default=24, 
        ge=15.54, 
        le=56.8,
        description="Body Mass Index",
        examples=[24.5]
    )
    heartRate: float = Field(
        default=72, 
        ge=44, 
        le=143,
        description="Heart rate (beats per minute)",
        examples=[72]
    )
    glucose: float = Field(
        default=90, 
        ge=40, 
        le=394,
        description="Glucose level (mg/dL)",
        examples=[90]
    )
    
    @field_validator('male', 'BPMeds')
    @classmethod
    def validate_binary_fields(cls, v: float, info) -> float:
        """Validate binary fields (0 or 1)"""
        if v not in [0, 1]:
            raise ValueError(f"{info.field_name} must be 0 or 1. Got: {v}")
        return v
    
    @field_validator('cigsPerDay')
    @classmethod
    def validate_cigarettes(cls, v: float) -> float:
        """Validate cigarettes per day"""
        if v < 0:
            raise ValueError(f"Cigarettes per day cannot be negative. Got: {v}")
        if v > 40:
            raise ValueError(f"Cigarettes per day ({v}) is very high. Please verify.")
        return v
    
    @field_validator('totChol', 'glucose')
    @classmethod
    def validate_positive_values(cls, v: float, info) -> float:
        """Validate positive values"""
        if v <= 0:
            raise ValueError(f"{info.field_name} must be positive. Got: {v}")
        return v
    
    @model_validator(mode='after')
    def validate_blood_pressure(self) -> 'HypertensionInput':
        """Validate blood pressure relationship"""
        if self.sysBP <= self.diaBP:
            raise ValueError(f"Systolic BP ({self.sysBP}) must be greater than diastolic BP ({self.diaBP})")
        
        pulse_pressure = self.sysBP - self.diaBP
        if pulse_pressure < 20:
            raise ValueError(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally low")
        
        return self
    
    @field_validator('heartRate')
    @classmethod
    def validate_heart_rate(cls, v: float) -> float:
        """Validate heart rate"""
        if v < 50:
            raise ValueError(f"Heart rate {v} bpm is very low (bradycardia). Please verify.")
        if v > 120:
            raise ValueError(f"Heart rate {v} bpm is very high (tachycardia). Please verify.")
        return v
    
    model_config = {
        "json_schema_extra": {
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
    }



# ============================================================================
# RESPONSE MODELS
# ============================================================================

class PredictionResponse(BaseModel):
    """Standard prediction response model"""
    success: bool = Field(default=True, description="Whether the prediction was successful")
    prediction: int = Field(..., description="Prediction result (0=Low Risk, 1=High Risk)", example=0)
    probability: float = Field(..., description="Confidence probability (0-100)", example=85.5, ge=0, le=100)
    risk_level: str = Field(..., description="Risk level (Low/Moderate/High)", example="Low")
    message: str = Field(..., description="Human-readable prediction message", example="No signs of diabetes detected")
    recommendations: List[str] = Field(default_factory=list, description="Personalized recommendations")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Prediction timestamp")
    
    @field_validator('probability')
    @classmethod
    def validate_probability(cls, v: float) -> float:
        """Validate probability is within range"""
        if v < 0 or v > 100:
            raise ValueError(f"Probability must be between 0 and 100. Got: {v}")
        return v
    
    @field_validator('risk_level')
    @classmethod
    def validate_risk_level(cls, v: str) -> str:
        """Validate risk level is valid"""
        if v not in [RiskLevel.LOW, RiskLevel.MODERATE, RiskLevel.HIGH]:
            raise ValueError(f"Risk level must be Low, Moderate, or High. Got: {v}")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "prediction": 0,
                "probability": 85.5,
                "risk_level": "Low",
                "message": "No signs of diabetes detected",
                "recommendations": [
                    "Continue maintaining a healthy balanced diet",
                    "Exercise regularly - at least 150 minutes per week"
                ],
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Health status", example="healthy")
    models_loaded: int = Field(..., description="Number of loaded models", example=6)
    models: List[str] = Field(..., description="List of loaded model names", example=["diabetes", "asthma", "cardio"])
    version: str = Field(..., description="API version", example="3.0.0")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Response timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "models_loaded": 6,
                "models": ["diabetes", "asthma", "cardio", "stroke", "hypertension", "sleep"],
                "version": "3.0.0",
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type/code", example="ValidationError")
    message: str = Field(..., description="Human-readable error message", example="Invalid input data")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional detailed error information")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Error timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "glucose: value is not a valid float",
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    }


class MentalHealthInput(BaseModel):
    """Mental health prediction input - text-based analysis"""
    text: str = Field(
        min_length=10,
        max_length=5000,
        description="User's description of their mental state, symptoms, or feelings",
        examples=["I've been feeling very anxious lately and having trouble sleeping. I feel overwhelmed with work."]
    )
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate and clean text input"""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        if len(v.strip()) < 10:
            raise ValueError("Please provide more detail (at least 10 characters)")
        if len(v) > 5000:
            raise ValueError("Text is too long (maximum 5000 characters)")
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "I've been feeling very anxious lately and having trouble sleeping. I feel overwhelmed with work and can't concentrate."
            }
        }
    }


class MentalHealthResponse(BaseModel):
    """Mental health prediction response"""
    success: bool = True
    depression_risk: float = Field(ge=0, le=100, description="Depression risk percentage (0-100)")
    anxiety_risk: float = Field(ge=0, le=100, description="Anxiety risk percentage (0-100)")
    risk_level: str = Field(description="Overall risk level: Low, Moderate, or High")
    message: str = Field(description="Human-readable prediction message")
    recommendations: List[str] = Field(default_factory=list, description="Personalized recommendations")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "depression_risk": 65.5,
                "anxiety_risk": 72.3,
                "risk_level": "Moderate",
                "message": "Moderate risk of depression and anxiety detected",
                "recommendations": [
                    "Consider speaking with a mental health professional",
                    "Practice stress reduction techniques like meditation",
                    "Maintain regular sleep schedule"
                ],
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    }

class SleepHealthInput(BaseModel):
    """Input data for sleep health prediction"""
    gender: str = Field(
        default="Male",
        description="Gender (Male/Female)",
        examples=["Male", "Female"]
    )
    age: int = Field(
        default=35,
        ge=27,
        le=59,
        description="Age in years",
        examples=[35, 45, 55]
    )
    occupation: str = Field(
        default="Software Engineer",
        description="Occupation type",
        examples=["Software Engineer", "Doctor", "Teacher", "Business"]
    )
    sleep_duration: float = Field(
        default=7.0,
        ge=5.8,
        le=8.5,
        description="Sleep duration in hours",
        examples=[7.2, 6.5, 8.0]
    )
    quality_of_sleep: int = Field(
        default=7,
        ge=4,
        le=9,
        description="Quality of sleep (1-10 scale)",
        examples=[7, 5, 8]
    )
    physical_activity_level: int = Field(
        default=45,
        ge=30,
        le=90,
        description="Physical activity in minutes per day",
        examples=[45, 60, 30]
    )
    stress_level: int = Field(
        default=5,
        ge=3,
        le=8,
        description="Stress level (1-10 scale)",
        examples=[5, 7, 4]
    )
    bmi_category: str = Field(
        default="Normal",
        description="BMI category",
        examples=["Normal", "Overweight", "Obese"]
    )
    blood_pressure: str = Field(
        default="120/80",
        pattern="^\d{2,3}/\d{2,3}$",
        description="Blood pressure (systolic/diastolic)",
        examples=["120/80", "130/85", "140/90"]
    )
    heart_rate: int = Field(
        default=72,
        ge=65,
        le=86,
        description="Heart rate in beats per minute",
        examples=[72, 78, 68]
    )
    daily_steps: int = Field(
        default=7000,
        ge=3000,
        le=10000,
        description="Daily steps count",
        examples=[7000, 8500, 5000]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "gender": "Male",
                "age": 35,
                "occupation": "Software Engineer",
                "sleep_duration": 7.2,
                "quality_of_sleep": 7,
                "physical_activity_level": 45,
                "stress_level": 5,
                "bmi_category": "Normal",
                "blood_pressure": "120/80",
                "heart_rate": 72,
                "daily_steps": 7000
            }
        }

class SleepHealthResponse(BaseModel):
    """Sleep health prediction response model"""
    success: bool = Field(default=True, description="Whether the prediction was successful")
    prediction: int = Field(..., description="Prediction result (0=No Disorder, 1=Sleep Disorder)")
    probability: float = Field(..., description="Confidence probability (0-100)", ge=0, le=100)
    risk_level: str = Field(..., description="Risk level (Low/Moderate/High)")
    message: str = Field(..., description="Human-readable prediction message")
    recommendations: List[str] = Field(default_factory=list, description="Sleep hygiene recommendations")
    sleep_score: Optional[float] = Field(None, description="Overall sleep quality score (0-100)")
    factors_affected: Optional[List[str]] = Field(None, description="Sleep factors that need attention")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": 0,
                "probability": 78.5,
                "risk_level": "Low",
                "message": "Good sleep health detected",
                "recommendations": [
                    "Maintain consistent sleep schedule",
                    "Create relaxing bedtime routine"
                ],
                "sleep_score": 82,
                "factors_affected": [],
                "timestamp": "2024-01-01T12:00:00"
            }
        }

# ============================================================================
# BATCH PREDICTION MODELS
# ============================================================================

class BatchPredictionRequest(BaseModel):
    """Batch prediction request model"""
    requests: List[Dict[str, Any]] = Field(
        description="List of prediction requests",
        min_length=1,
        max_length=100
    )
    
    @field_validator('requests')
    @classmethod
    def validate_batch_size(cls, v: List) -> List:
        """Validate batch size is within limits"""
        if len(v) > 100:
            raise ValueError(f"Batch size cannot exceed 100. Got: {len(v)}")
        return v


class BatchPredictionResponse(BaseModel):
    """Batch prediction response model"""
    success: bool = Field(default=True, description="Whether all predictions were successful")
    results: List[PredictionResponse] = Field(..., description="List of individual prediction results")
    total_processed: int = Field(..., description="Total number of predictions processed")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Response timestamp")

    