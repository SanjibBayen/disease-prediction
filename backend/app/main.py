"""
HealthPredict AI - Main Application
FastAPI Backend for Disease Prediction System
By Sanjib Bayen
Version: 3.0.0
"""

import logging
import sys
import uuid
import os
from datetime import datetime
from typing import Dict, Any, Tuple, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.model_manager import get_model_manager
# Rate limiting
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
except ImportError:
    SLOWAPI_AVAILABLE = False
    print("Warning: slowapi not installed. Rate limiting disabled.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log')
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# REQUEST ID MIDDLEWARE
# ============================================================================

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ============================================================================
# REQUEST LOGGING MIDDLEWARE
# ============================================================================

async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.now()
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path} - Request ID: {getattr(request.state, 'request_id', 'N/A')}")
    
    response = await call_next(request)
    
    # Log response
    process_time = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(f"← {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events"""
    logger.info("=" * 60)
    logger.info("HealthPredict AI API Starting...")
    logger.info(f"Version: 3.0.0")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info("=" * 60)
    
    # Load models on startup
    from services.model_manager import get_model_manager
    model_manager = get_model_manager()
    logger.info(f"Models loaded: {list(model_manager.models.keys())}")
    
    yield
    
    logger.info("HealthPredict AI API Shutting down...")


# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Disease Prediction AI API",
    version="3.0.0",
    description=""""
    ## Advanced Disease Prediction System
    
    This API provides machine learning-powered predictions for various health conditions.
    
    ### Features
    - Diabetes Risk Prediction
    - Asthma Risk Assessment
    - Cardiovascular Disease Prediction
    - Stroke Risk Analysis
    - Hypertension Risk Evaluation
    - Sleep Health Analysis
    - Mental Health Assessment
    
    ### Rate Limits
    - 100 requests per minute per IP
    - 1000 requests per hour per IP
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "Sanjib Bayen",
        "email": "sanjibbayen@gmail.com",
        "url": "https://github.com/SanjibBayen/disease-prediction"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Register request logging middleware after app instantiation
app.middleware("http")(log_requests)

# Add request ID middleware
app.add_middleware(RequestIDMiddleware)

# ============================================================================
# RATE LIMITING SETUP
# ============================================================================

if SLOWAPI_AVAILABLE:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Rate limiting enabled")
else:
    logger.warning("Rate limiting disabled - install slowapi for production")

# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-Request-ID"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
    max_age=3600,
)


# ============================================================================
# IMPORT MODELS (after app creation to avoid circular imports)
# ============================================================================

from app.models import (
    DiabetesInput, AsthmaInput, CardioInput, StrokeInput, 
    HypertensionInput, MentalHealthInput, PredictionResponse,
    MentalHealthResponse, HealthResponse, ErrorResponse
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_diabetes_risk(data: DiabetesInput) -> Tuple[int, float, str, str]:
    """Calculate diabetes risk based on input values"""
    risk_score = 0
    
    if data.glucose > 140:
        risk_score += 30
    elif data.glucose > 125:
        risk_score += 20
    elif data.glucose > 100:
        risk_score += 10
    
    if data.bmi > 30:
        risk_score += 25
    elif data.bmi > 25:
        risk_score += 15
    
    if data.age > 45:
        risk_score += 15
    elif data.age > 35:
        risk_score += 5
    
    if data.pregnancies > 5:
        risk_score += 10
    elif data.pregnancies > 2:
        risk_score += 5
    
    if data.blood_pressure > 140:
        risk_score += 10
    
    if data.diabetes_pedigree > 0.8:
        risk_score += 15
    elif data.diabetes_pedigree > 0.5:
        risk_score += 5
    
    if risk_score >= 50:
        return 1, min(85 + (risk_score - 50) / 2, 98), "High", "High risk of diabetes detected"
    elif risk_score >= 30:
        return 0, 65 + (risk_score - 30) / 2, "Moderate", "Moderate risk of diabetes"
    else:
        return 0, max(60, 75 - (30 - risk_score) / 2), "Low", "No signs of diabetes detected"


def get_diabetes_recommendations(data: DiabetesInput, risk_level: str) -> List[str]:
    """Generate personalized recommendations"""
    recs = []
    
    if risk_level == "High":
        recs.extend([
            "Consult a healthcare provider for proper diabetes management",
            "Monitor blood sugar levels daily"
        ])
    elif risk_level == "Moderate":
        recs.extend([
            "Schedule a diabetes screening test",
            "Monitor your blood sugar levels periodically"
        ])
    
    if data.glucose > 140:
        recs.append("Reduce intake of sugary foods and refined carbohydrates")
    if data.bmi > 25:
        recs.append("Aim to lose 5-10% of body weight through diet and exercise")
    if data.age > 45:
        recs.append("Schedule regular diabetes screening every 6 months")
    
    if not recs:
        recs.extend([
            "Continue maintaining a healthy balanced diet",
            "Exercise regularly - at least 150 minutes per week"
        ])
    
    return recs


def calculate_other_risks(data, disease: str) -> Tuple[int, float, str, str, List[str]]:
    """Generic risk calculator for other diseases"""
    risk_score = 0
    
    if disease == "asthma":
        if data.smoking_ex == 1:
            risk_score += 25
        if data.peak_flow < 0.4:
            risk_score += 35
        elif data.peak_flow < 0.6:
            risk_score += 20
        if data.age > 0.7:
            risk_score += 15
        
        recs = ["Avoid smoking", "Maintain good indoor air quality"]
        if data.peak_flow < 0.5:
            recs.append("Monitor peak flow readings regularly")
    
    elif disease == "cardio":
        if data.ap_hi > 140:
            risk_score += 30
        if data.cholesterol == 3:
            risk_score += 25
        if data.smoke == 1:
            risk_score += 20
        if data.active == 0:
            risk_score += 15
        
        recs = ["Exercise 30 minutes daily", "Maintain healthy blood pressure"]
        if data.smoke == 1:
            recs.append("Consider quitting smoking")
    
    elif disease == "stroke":
        if data.hypertension == 1:
            risk_score += 30
        if data.heart_disease == 1:
            risk_score += 25
        if data.avg_glucose_level > 140:
            risk_score += 20
        if data.age > 60:
            risk_score += 15
        
        recs = ["Monitor blood pressure regularly", "Control blood sugar levels"]
        if data.hypertension == 1:
            recs.append("Strict blood pressure control is essential")
    
    else:  # hypertension
        if data.sysBP > 140:
            risk_score += 35
        if data.diaBP > 90:
            risk_score += 25
        if data.BMI > 30:
            risk_score += 20
        if data.age > 55:
            risk_score += 15
        
        recs = ["Reduce sodium intake", "Regular blood pressure monitoring"]
        if data.BMI > 25:
            recs.append("Weight loss can significantly reduce BP")
    
    if risk_score >= 50:
        return 1, min(85 + (risk_score - 50) / 2, 95), "High", f"High risk of {disease}", recs
    else:
        return 0, 80 - risk_score / 3, "Low", f"Low risk of {disease}", recs


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_model=Dict[str, Any], tags=["System"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "HealthPredict AI API is running",
        "version": "3.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            {"path": "/docs", "method": "GET", "description": "API documentation"},
            {"path": "/api/health", "method": "GET", "description": "Health check"},
            {"path": "/api/predict/diabetes", "method": "POST", "description": "Diabetes prediction"},
            {"path": "/api/predict/asthma", "method": "POST", "description": "Asthma prediction"},
            {"path": "/api/predict/cardio", "method": "POST", "description": "Cardiovascular prediction"},
            {"path": "/api/predict/stroke", "method": "POST", "description": "Stroke prediction"},
            {"path": "/api/predict/hypertension", "method": "POST", "description": "Hypertension prediction"},
            {"path": "/api/predict/mental-health", "method": "POST", "description": "Mental health assessment"}
        ]
    }


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint with model status"""
    try:
        # Try different import paths
        try:
            from app.dependencies import get_model_manager
        except ImportError:
            from services.model_manager import get_model_manager
        
        model_manager = get_model_manager()
        
        return HealthResponse(
            status="healthy",
            models_loaded=len(model_manager.models),
            models=list(model_manager.models.keys()),
            version="3.0.0",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="degraded",
            models_loaded=0,
            models=[],
            version="3.0.0",
            timestamp=datetime.now().isoformat()
        )


@app.post("/api/predict/diabetes", response_model=PredictionResponse, tags=["Predictions"])
async def predict_diabetes(data: DiabetesInput):
    """Predict diabetes risk"""
    try:
        logger.info(f"Diabetes prediction request")
        prediction, probability, risk_level, message = calculate_diabetes_risk(data)
        recommendations = get_diabetes_recommendations(data, risk_level)
        
        return PredictionResponse(
            success=True,
            prediction=prediction,
            probability=round(probability, 1),
            risk_level=risk_level,
            message=message,
            recommendations=recommendations
        )
    except Exception as e:
        logger.error(f"Diabetes prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/predict/asthma", response_model=PredictionResponse, tags=["Predictions"])
async def predict_asthma(data: AsthmaInput):
    """Predict asthma risk"""
    try:
        pred, prob, risk, msg, recs = calculate_other_risks(data, "asthma")
        return PredictionResponse(
            success=True,
            prediction=pred,
            probability=round(prob, 1),
            risk_level=risk,
            message=msg,
            recommendations=recs
        )
    except Exception as e:
        logger.error(f"Asthma prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/predict/cardio", response_model=PredictionResponse, tags=["Predictions"])
async def predict_cardio(data: CardioInput):
    """Predict cardiovascular disease risk"""
    try:
        pred, prob, risk, msg, recs = calculate_other_risks(data, "cardio")
        return PredictionResponse(
            success=True,
            prediction=pred,
            probability=round(prob, 1),
            risk_level=risk,
            message=msg,
            recommendations=recs
        )
    except Exception as e:
        logger.error(f"Cardiovascular prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/predict/stroke", response_model=PredictionResponse, tags=["Predictions"])
async def predict_stroke(data: StrokeInput):
    """Predict stroke risk"""
    try:
        pred, prob, risk, msg, recs = calculate_other_risks(data, "stroke")
        return PredictionResponse(
            success=True,
            prediction=pred,
            probability=round(prob, 1),
            risk_level=risk,
            message=msg,
            recommendations=recs
        )
    except Exception as e:
        logger.error(f"Stroke prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/predict/hypertension", response_model=PredictionResponse, tags=["Predictions"])
async def predict_hypertension(data: HypertensionInput):
    """Predict hypertension risk"""
    try:
        pred, prob, risk, msg, recs = calculate_other_risks(data, "hypertension")
        return PredictionResponse(
            success=True,
            prediction=pred,
            probability=round(prob, 1),
            risk_level=risk,
            message=msg,
            recommendations=recs
        )
    except Exception as e:
        logger.error(f"Hypertension prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/predict/mental-health", response_model=MentalHealthResponse, tags=["Predictions"])
async def predict_mental_health(data: MentalHealthInput):
    """Predict depression and anxiety risk from text"""
    try:
        logger.info(f"Mental health prediction request (text length: {len(data.text)})")
        
        from services.model_manager import get_model_manager
        model_manager = get_model_manager()
        
        result = model_manager.predict_mental_health(data.text)
        
        avg_risk = (result['depression_risk'] + result['anxiety_risk']) / 2
        if avg_risk >= 70:
            risk_level = "High"
        elif avg_risk >= 40:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        if risk_level == "High":
            message = "High risk of depression and/or anxiety detected"
        elif risk_level == "Moderate":
            message = "Moderate risk of depression and/or anxiety detected"
        else:
            message = "Low risk of depression and anxiety detected"
        
        recommendations = [
            "Consider speaking with a mental health professional",
            "Practice regular self-care and stress management",
            "Maintain healthy sleep and exercise habits"
        ]
        
        return MentalHealthResponse(
            success=True,
            depression_risk=result['depression_risk'],
            anxiety_risk=result['anxiety_risk'],
            risk_level=risk_level,
            message=message,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Mental health prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation Error",
            "message": "Invalid input data",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": "Request Error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info")
    )