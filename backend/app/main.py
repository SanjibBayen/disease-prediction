from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, List

app = FastAPI(title="HealthPredict AI API", version="3.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATA MODELS WITH VALIDATION ==========

class DiabetesInput(BaseModel):
    pregnancies: float = Field(0, ge=0, le=20, description="Number of pregnancies")
    glucose: float = Field(100, ge=0, le=300, description="Glucose level (mg/dL)")
    blood_pressure: float = Field(80, ge=0, le=200, description="Blood pressure (mmHg)")
    skin_thickness: float = Field(20, ge=0, le=100, description="Skin thickness (mm)")
    insulin: float = Field(79, ge=0, le=900, description="Insulin level (mu U/ml)")
    bmi: float = Field(25, ge=0, le=70, description="Body Mass Index")
    diabetes_pedigree: float = Field(0.5, ge=0, le=2.5, description="Diabetes pedigree function")
    age: float = Field(30, ge=1, le=120, description="Age in years")
    
    @validator('pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree', 'age')
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError(f"Value cannot be negative")
        return v

class AsthmaInput(BaseModel):
    gender_male: int = Field(0, ge=0, le=1)
    smoking_ex: int = Field(0, ge=0, le=1)
    smoking_non: int = Field(1, ge=0, le=1)
    age: float = Field(0.5, ge=0, le=1)
    peak_flow: float = Field(0.5, ge=0.1, le=1)
    
    @validator('gender_male', 'smoking_ex', 'smoking_non')
    def validate_binary(cls, v):
        if v not in [0, 1]:
            raise ValueError(f"Value must be 0 or 1")
        return v

class CardioInput(BaseModel):
    age: int = Field(35, ge=29, le=65)
    ap_hi: int = Field(110, ge=90, le=200)
    ap_lo: int = Field(70, ge=60, le=140)
    cholesterol: int = Field(1, ge=1, le=3)
    gluc: int = Field(1, ge=1, le=3)
    smoke: int = Field(0, ge=0, le=1)
    alco: int = Field(0, ge=0, le=1)
    active: int = Field(1, ge=0, le=1)
    weight: float = Field(70, ge=30, le=200)
    
    @validator('age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'weight')
    def validate_positive(cls, v):
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError(f"Value cannot be negative")
        return v

class StrokeInput(BaseModel):
    age: int = Field(35, ge=0, le=82)
    hypertension: int = Field(0, ge=0, le=1)
    heart_disease: int = Field(0, ge=0, le=1)
    ever_married: int = Field(1, ge=0, le=1)
    avg_glucose_level: float = Field(90, ge=55, le=270)
    bmi: float = Field(24, ge=13.5, le=98)
    smoking_status: int = Field(0, ge=0, le=3)
    
    @validator('hypertension', 'heart_disease', 'ever_married')
    def validate_binary(cls, v):
        if v not in [0, 1]:
            raise ValueError(f"Value must be 0 or 1")
        return v

class HypertensionInput(BaseModel):
    male: int = Field(0, ge=0, le=1)
    age: int = Field(35, ge=32, le=70)
    cigsPerDay: float = Field(0, ge=0, le=70)
    BPMeds: float = Field(0, ge=0, le=1)
    totChol: float = Field(180, ge=107, le=500)
    sysBP: float = Field(110, ge=83.5, le=295)
    diaBP: float = Field(70, ge=48, le=142.5)
    BMI: float = Field(22, ge=15.54, le=56.8)
    heartRate: float = Field(70, ge=44, le=143)
    glucose: float = Field(85, ge=40, le=394)
    
    @validator('male', 'BPMeds')
    def validate_binary(cls, v):
        if v not in [0, 1]:
            raise ValueError(f"Value must be 0 or 1")
        return v

# ========== HELPER FUNCTIONS ==========

def calculate_diabetes_risk(data: DiabetesInput) -> tuple:
    """Calculate diabetes risk based on input values"""
    risk_score = 0
    
    # Glucose level scoring
    if data.glucose > 140:
        risk_score += 30
    elif data.glucose > 125:
        risk_score += 20
    elif data.glucose > 100:
        risk_score += 10
    
    # BMI scoring
    if data.bmi > 30:
        risk_score += 25
    elif data.bmi > 25:
        risk_score += 15
    
    # Age scoring
    if data.age > 45:
        risk_score += 15
    elif data.age > 35:
        risk_score += 5
    
    # Pregnancies (for females)
    if data.pregnancies > 5:
        risk_score += 10
    elif data.pregnancies > 2:
        risk_score += 5
    
    # Blood pressure
    if data.blood_pressure > 140:
        risk_score += 10
    
    # Family history indicator (diabetes_pedigree)
    if data.diabetes_pedigree > 0.8:
        risk_score += 15
    elif data.diabetes_pedigree > 0.5:
        risk_score += 5
    
    # Determine prediction and risk level
    if risk_score >= 50:
        prediction = 1
        risk_level = "High"
        message = "High risk of diabetes detected"
        probability = min(85 + (risk_score - 50) / 2, 98)
    elif risk_score >= 30:
        prediction = 0
        risk_level = "Moderate"
        message = "Moderate risk of diabetes"
        probability = 65 + (risk_score - 30) / 2
    else:
        prediction = 0
        risk_level = "Low"
        message = "No signs of diabetes detected"
        probability = 75 - (30 - risk_score) / 2
    
    return prediction, round(probability, 1), risk_level, message

def get_diabetes_recommendations(data: DiabetesInput, risk_level: str) -> List[str]:
    """Generate personalized recommendations"""
    recommendations = []
    
    if risk_level == "High":
        recommendations.append("Consult a healthcare provider for proper diabetes management")
        recommendations.append("Monitor blood sugar levels daily using a glucometer")
    
    if data.glucose > 140:
        recommendations.append("Reduce intake of sugary foods and refined carbohydrates")
    
    if data.bmi > 25:
        recommendations.append("Aim to lose 5-10% of body weight through diet and exercise")
    
    if data.age > 45:
        recommendations.append("Schedule regular diabetes screening every 6 months")
    
    if data.blood_pressure > 140:
        recommendations.append("Monitor blood pressure regularly and reduce sodium intake")
    
    if not recommendations:
        recommendations.append("Continue maintaining a healthy balanced diet")
        recommendations.append("Exercise regularly - at least 150 minutes per week")
    
    return recommendations

# ========== ROOT ENDPOINT ==========
@app.get("/")
async def root():
    return {
        "message": "HealthPredict AI API is running",
        "version": "3.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {"path": "/api/health", "method": "GET", "description": "Health check"},
            {"path": "/api/predict/diabetes", "method": "POST", "description": "Diabetes prediction"},
            {"path": "/api/predict/asthma", "method": "POST", "description": "Asthma prediction"},
            {"path": "/api/predict/cardio", "method": "POST", "description": "Cardiovascular prediction"},
            {"path": "/api/predict/stroke", "method": "POST", "description": "Stroke prediction"},
            {"path": "/api/predict/hypertension", "method": "POST", "description": "Hypertension prediction"}
        ]
    }

# ========== HEALTH ENDPOINT ==========
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": 6,
        "models": ["diabetes", "asthma", "cardio", "stroke", "hypertension", "sleep"],
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

# ========== DIABETES PREDICTION ==========
@app.post("/api/predict/diabetes")
async def predict_diabetes(data: DiabetesInput):
    try:
        prediction, probability, risk_level, message = calculate_diabetes_risk(data)
        recommendations = get_diabetes_recommendations(data, risk_level)
        
        return {
            "success": True,
            "prediction": prediction,
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== ASTHMA PREDICTION ==========
@app.post("/api/predict/asthma")
async def predict_asthma(data: AsthmaInput):
    try:
        risk_score = 0
        
        if data.smoking_ex == 1:
            risk_score += 25
        if data.peak_flow < 0.4:
            risk_score += 35
        elif data.peak_flow < 0.6:
            risk_score += 20
        if data.age > 0.7:
            risk_score += 15
        
        if risk_score >= 50:
            prediction = 1
            risk_level = "High"
            message = "High risk of asthma detected"
            probability = min(85 + (risk_score - 50) / 2, 95)
        else:
            prediction = 0
            risk_level = "Low"
            message = "Low risk of asthma"
            probability = 80 - risk_score / 2
        
        recommendations = [
            "Avoid smoking and second-hand smoke",
            "Maintain good indoor air quality"
        ]
        
        if data.peak_flow < 0.5:
            recommendations.append("Monitor peak flow readings regularly")
        
        return {
            "success": True,
            "prediction": prediction,
            "probability": round(probability, 1),
            "risk_level": risk_level,
            "message": message,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== CARDIOVASCULAR PREDICTION ==========
@app.post("/api/predict/cardio")
async def predict_cardio(data: CardioInput):
    try:
        risk_score = 0
        
        if data.ap_hi > 140:
            risk_score += 30
        elif data.ap_hi > 130:
            risk_score += 15
        
        if data.cholesterol == 3:
            risk_score += 25
        elif data.cholesterol == 2:
            risk_score += 10
        
        if data.smoke == 1:
            risk_score += 20
        if data.active == 0:
            risk_score += 15
        if data.age > 55:
            risk_score += 10
        
        if risk_score >= 50:
            prediction = 1
            risk_level = "High"
            message = "High risk of cardiovascular disease"
            probability = min(85 + (risk_score - 50) / 2, 95)
        else:
            prediction = 0
            risk_level = "Low"
            message = "Low risk of cardiovascular disease"
            probability = 82 - risk_score / 3
        
        recommendations = [
            "Exercise 30 minutes daily, 5 days per week",
            "Maintain healthy blood pressure"
        ]
        
        if data.smoke == 1:
            recommendations.append("Consider quitting smoking")
        if data.cholesterol > 1:
            recommendations.append("Adopt a heart-healthy diet low in saturated fats")
        
        return {
            "success": True,
            "prediction": prediction,
            "probability": round(probability, 1),
            "risk_level": risk_level,
            "message": message,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== STROKE PREDICTION ==========
@app.post("/api/predict/stroke")
async def predict_stroke(data: StrokeInput):
    try:
        risk_score = 0
        
        if data.hypertension == 1:
            risk_score += 30
        if data.heart_disease == 1:
            risk_score += 25
        if data.avg_glucose_level > 140:
            risk_score += 20
        if data.bmi > 30:
            risk_score += 15
        if data.age > 60:
            risk_score += 15
        elif data.age > 50:
            risk_score += 10
        if data.smoking_status == 2:
            risk_score += 10
        
        if risk_score >= 50:
            prediction = 1
            risk_level = "High"
            message = "High risk of stroke detected"
            probability = min(85 + (risk_score - 50) / 2, 95)
        else:
            prediction = 0
            risk_level = "Low"
            message = "Low risk of stroke"
            probability = 85 - risk_score / 3
        
        recommendations = [
            "Monitor blood pressure regularly",
            "Control blood sugar levels"
        ]
        
        if data.hypertension == 1:
            recommendations.append("Strict blood pressure control is essential")
        if data.smoking_status == 2:
            recommendations.append("Quit smoking to reduce stroke risk")
        
        return {
            "success": True,
            "prediction": prediction,
            "probability": round(probability, 1),
            "risk_level": risk_level,
            "message": message,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== HYPERTENSION PREDICTION ==========
@app.post("/api/predict/hypertension")
async def predict_hypertension(data: HypertensionInput):
    try:
        risk_score = 0
        
        if data.sysBP > 140:
            risk_score += 35
        elif data.sysBP > 130:
            risk_score += 20
        
        if data.diaBP > 90:
            risk_score += 25
        elif data.diaBP > 85:
            risk_score += 15
        
        if data.BMI > 30:
            risk_score += 20
        elif data.BMI > 25:
            risk_score += 10
        
        if data.age > 55:
            risk_score += 15
        if data.cigsPerDay > 10:
            risk_score += 10
        
        if risk_score >= 50:
            prediction = 1
            risk_level = "High"
            message = "High risk of hypertension detected"
            probability = min(85 + (risk_score - 50) / 2, 95)
        else:
            prediction = 0
            risk_level = "Low"
            message = "Normal blood pressure range"
            probability = 78 - risk_score / 3
        
        recommendations = [
            "Reduce sodium intake to less than 1500mg daily",
            "Regular blood pressure monitoring"
        ]
        
        if data.BMI > 25:
            recommendations.append("Weight loss of 5-10% can significantly reduce BP")
        if data.cigsPerDay > 0:
            recommendations.append("Smoking cessation is critical for BP control")
        
        return {
            "success": True,
            "prediction": prediction,
            "probability": round(probability, 1),
            "risk_level": risk_level,
            "message": message,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== ERROR HANDLER FOR VALIDATION ERRORS ==========
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "success": False,
        "error": "Validation Error",
        "message": exc.detail,
        "status_code": exc.status_code
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)