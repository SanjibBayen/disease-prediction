"""
Health check endpoints
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.dependencies import get_model_manager
from app.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Check the health status of the API and models
    """
    try:
        model_manager = get_model_manager()
        
        return HealthResponse(
            status="healthy",
            models_loaded=len(model_manager.models),
            models=list(model_manager.models.keys()),
            version="3.0.0",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/models", tags=["Health"])
async def get_models():
    """
    Get list of available models
    """
    try:
        model_manager = get_model_manager()
        return {
            "success": True,
            "models": list(model_manager.models.keys()),
            "count": len(model_manager.models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))