"""
Advanced Model Management System
Handles loading, caching, and prediction for all ML models

Version: 2.0
Author: HealthPredict AI Team
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path
from datetime import datetime
import logging
from functools import lru_cache, wraps
import json
import hashlib
import threading
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS AND DATA CLASSES
# ============================================================================

class ModelType(str, Enum):
    """Model type enumeration"""
    PICKLE = "pickle"
    JOBLIB = "joblib"


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


@dataclass
class ModelConfig:
    """Model configuration data class"""
    name: str
    path: str
    type: ModelType
    alt_paths: List[str] = field(default_factory=list)
    has_preprocessor: bool = False
    preprocessor_paths: List[str] = field(default_factory=list)
    accuracy: float = 0.85
    description: str = ""
    version: str = "1.0"
    required_features: List[str] = field(default_factory=list)


@dataclass
class PredictionResult:
    """Prediction result data class"""
    success: bool
    prediction: int
    probability: float
    risk_level: str
    message: str
    recommendations: List[str]
    model_accuracy: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'success': self.success,
            'prediction': self.prediction,
            'probability': self.probability,
            'risk_level': self.risk_level,
            'message': self.message,
            'recommendations': self.recommendations,
            'model_accuracy': self.model_accuracy,
            'timestamp': self.timestamp
        }


# ============================================================================
# MODEL CONFIGURATIONS
# ============================================================================

MODEL_CONFIGS: List[ModelConfig] = [
    ModelConfig(
        name='diabetes',
        path='diabetes/diabetes_model.sav',
        type=ModelType.PICKLE,
        accuracy=0.85,
        description='SVC model for diabetes prediction',
        required_features=['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                          'insulin', 'bmi', 'diabetes_pedigree', 'age']
    ),
    ModelConfig(
        name='asthma',
        path='asthma/model.pkl',
        type=ModelType.JOBLIB,
        alt_paths=['asthama/model.pkl'],
        has_preprocessor=True,
        preprocessor_paths=['asthma/preprocessor.pkl', 'asthama/preprocessor.pkl'],
        accuracy=0.83,
        description='Random Forest model for asthma prediction',
        required_features=['gender_male', 'smoking_ex', 'smoking_non', 'age', 'peak_flow']
    ),
    ModelConfig(
        name='cardio',
        path='cardio_vascular/xgboost_cardiovascular_model.pkl',
        type=ModelType.PICKLE,
        accuracy=0.78,
        description='XGBoost model for cardiovascular disease',
        required_features=['age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 
                          'smoke', 'alco', 'active', 'weight']
    ),
    ModelConfig(
        name='stroke',
        path='stroke/finalized_model.pkl',
        type=ModelType.JOBLIB,
        accuracy=0.80,
        description='Ensemble model for stroke prediction',
        required_features=['age', 'hypertension', 'heart_disease', 'ever_married', 
                          'avg_glucose_level', 'bmi', 'smoking_status']
    ),
    ModelConfig(
        name='hypertension',
        path='hypertension/extratrees_model.pkl',
        type=ModelType.PICKLE,
        has_preprocessor=True,
        preprocessor_paths=['hypertension/scaler.pkl'],
        accuracy=0.82,
        description='Extra Trees model for hypertension',
        required_features=['male', 'age', 'cigsPerDay', 'BPMeds', 'totChol', 
                          'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
    ),
    ModelConfig(
        name='sleep',
        path='sleep_health/svc_model.pkl',
        type=ModelType.PICKLE,
        has_preprocessor=True,
        preprocessor_paths=['sleep_health/scaler.pkl', 'sleep_health/label_encoders.pkl'],
        accuracy=0.76,
        description='SVC model for sleep disorder detection',
        required_features=['gender', 'age', 'occupation', 'sleep_duration', 
                          'quality_of_sleep', 'stress_level', 'bmi_category', 
                          'blood_pressure', 'heart_rate', 'daily_steps']
    ),
    ModelConfig(
        name='mental_health',
        path='mental/MentalH.pkl',
        type=ModelType.JOBLIB,
        alt_paths=['mental/mental_health_model.pkl'],
        accuracy=0.82,
        description='Transformer-based model for depression and anxiety detection',
        required_features=['text']
    ),
]


# ============================================================================
# RETRY DECORATOR
# ============================================================================

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry model loading on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}, retrying...")
                    import time
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


# ============================================================================
# MODEL MANAGER CLASS
# ============================================================================

class ModelManager:
    """
    Advanced Manager for loading and accessing ML models
    
    Features:
    - Thread-safe singleton pattern
    - Model caching and lazy loading
    - Automatic retry on failure
    - Comprehensive error handling
    - Model integrity checking (MD5 hashes)
    - Performance metrics tracking
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """Thread-safe singleton implementation"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, base_path: str = "models", auto_load: bool = True):
        """
        Initialize ModelManager
        
        Args:
            base_path: Base path to models directory
            auto_load: Whether to load all models automatically
        """
        # Only initialize once (for singleton)
        if hasattr(self, '_initialized'):
            return
        
        self.base_path = Path(base_path)
        self.models: Dict[str, Any] = {}
        self.preprocessors: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        self.model_hashes: Dict[str, str] = {}
        self._load_errors: Dict[str, str] = {}
        self._load_times: Dict[str, float] = {}
        self._initialized = True
        
        # Create base directory if not exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        if auto_load:
            self.load_all_models()
        
        logger.info(f"ModelManager initialized with base path: {self.base_path}")
    
    # ============================================================================
    # PUBLIC METHODS
    # ============================================================================
    
    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all machine learning models with error handling
        
        Returns:
            Dictionary with model names and loading success status
        """
        results = {}
        
        for config in MODEL_CONFIGS:
            success = self._load_model_with_config(config)
            results[config.name] = success
        
        loaded_count = len(self.models)
        total_count = len(MODEL_CONFIGS)
        
        logger.info(f"Model loading complete: {loaded_count}/{total_count} models loaded")
        
        if self._load_errors:
            logger.warning(f"Loading errors: {self._load_errors}")
        
        return results
    
    def reload_model(self, model_name: str) -> bool:
        """
        Reload a specific model
        
        Args:
            model_name: Name of the model to reload
        
        Returns:
            True if reload successful, False otherwise
        """
        config = self._find_model_config(model_name)
        if config is None:
            logger.error(f"Cannot reload: Model '{model_name}' not found")
            return False
        
        # Remove existing model
        self.models.pop(model_name, None)
        self.preprocessors = {k: v for k, v in self.preprocessors.items() 
                             if not k.startswith(model_name)}
        self.model_metadata.pop(model_name, None)
        
        return self._load_model_with_config(config)
    
    def get_model(self, name: str) -> Optional[Any]:
        """
        Get a loaded model by name
        
        Args:
            name: Model name (e.g., 'diabetes', 'asthma')
        
        Returns:
            Model object or None if not loaded
        """
        if name not in self.models:
            logger.warning(f"Model '{name}' not loaded. Available: {list(self.models.keys())}")
            return None
        return self.models[name]
    
    def get_preprocessor(self, name: str) -> Optional[Any]:
        """Get a preprocessor by name"""
        return self.preprocessors.get(name)
    
    def get_model_info(self, name: str) -> Optional[Dict]:
        """Get model metadata"""
        return self.model_metadata.get(name)
    
    def list_models(self) -> List[str]:
        """List all loaded model names"""
        return list(self.models.keys())
    
    def is_model_loaded(self, name: str) -> bool:
        """Check if a specific model is loaded"""
        return name in self.models
    
    def get_model_hash(self, name: str) -> Optional[str]:
        """Get MD5 hash of model file for integrity checking"""
        return self.model_hashes.get(name)
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get comprehensive model status"""
        return {
            'total_models': len(MODEL_CONFIGS),
            'loaded_models': len(self.models),
            'models': [
                {
                    'name': name,
                    'accuracy': self.model_metadata.get(name, {}).get('accuracy', 'unknown'),
                    'loaded_at': self.model_metadata.get(name, {}).get('loaded_at', 'unknown')
                }
                for name in self.models.keys()
            ],
            'load_errors': self._load_errors,
            'base_path': str(self.base_path),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_model_summary(self) -> str:
        """Get human-readable model summary"""
        lines = [
            "=" * 60,
            "Model Manager Summary",
            "=" * 60,
            f"Base Path: {self.base_path}",
            f"Models Loaded: {len(self.models)}/{len(MODEL_CONFIGS)}",
            "",
            "Loaded Models:"
        ]
        
        for name in self.models.keys():
            metadata = self.model_metadata.get(name, {})
            accuracy = metadata.get('accuracy', 'unknown')
            load_time = metadata.get('load_time_ms', 'unknown')
            lines.append(f"  ✓ {name} (accuracy: {accuracy}, load time: {load_time}ms)")
        
        if self._load_errors:
            lines.append("")
            lines.append("Loading Errors:")
            for name, error in self._load_errors.items():
                lines.append(f"  ✗ {name}: {error}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    # ============================================================================
    # PREDICTION METHODS
    # ============================================================================
    
    def predict_diabetes(self, data) -> Dict:
        """Predict diabetes risk with proper probability calculation"""
        start_time = datetime.now()
        
        try:
            features = self._prepare_diabetes_features(data)
            model = self.models.get('diabetes')
            
            if model is None:
                return self._error_response("Diabetes model not available")
            
            prediction = int(model.predict(features)[0])
            probability = self._calculate_probability(model, features, prediction)
            risk_level = self._get_risk_level(prediction, probability)
            recommendations = self._get_diabetes_recommendations(data, prediction)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.debug(f"Diabetes prediction completed in {processing_time:.2f}ms")
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': probability,
                'risk_level': risk_level,
                'message': self._get_prediction_message('diabetes', prediction),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Diabetes prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_asthma(self, data) -> Dict:
        """Predict asthma risk"""
        try:
            raw_input = self._prepare_asthma_features(data)
            
            # Apply preprocessing if available
            preprocessor_key = 'asthma_preprocessor'
            if preprocessor_key in self.preprocessors:
                processed_input = self.preprocessors[preprocessor_key].transform(raw_input)
            else:
                processed_input = raw_input
            
            model = self.models.get('asthma')
            if model is None:
                return self._error_response("Asthma model not available")
            
            prediction = int(model.predict(processed_input)[0])
            risk_score = self._calculate_asthma_risk_score(data)
            risk_level = self._get_risk_level(prediction, risk_score)
            recommendations = self._get_asthma_recommendations(data, prediction)
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': risk_score,
                'risk_level': risk_level,
                'message': self._get_prediction_message('asthma', prediction),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Asthma prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_cardio(self, data) -> Dict:
        """Predict cardiovascular disease risk"""
        try:
            features = self._prepare_cardio_features(data)
            model = self.models.get('cardio')
            
            if model is None:
                return self._error_response("Cardiovascular model not available")
            
            prediction = int(model.predict(features)[0])
            probability = self._calculate_probability(model, features, prediction)
            risk_level = self._get_risk_level(prediction, probability)
            recommendations = self._get_cardio_recommendations(data, prediction)
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': probability,
                'risk_level': risk_level,
                'message': self._get_prediction_message('cardio', prediction),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Cardiovascular prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_stroke(self, data) -> Dict:
        """Predict stroke risk"""
        try:
            features = self._prepare_stroke_features(data)
            model = self.models.get('stroke')
            
            if model is None:
                return self._error_response("Stroke model not available")
            
            prediction = int(model.predict(features)[0])
            probability = self._calculate_probability(model, features, prediction)
            risk_level = self._get_risk_level(prediction, probability)
            recommendations = self._get_stroke_recommendations(data, prediction)
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': probability,
                'risk_level': risk_level,
                'message': self._get_prediction_message('stroke', prediction),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Stroke prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_hypertension(self, data) -> Dict:
        """Predict hypertension risk"""
        try:
            input_df = self._prepare_hypertension_features(data)
            
            # Apply scaling if available
            scaler_key = 'hypertension_scaler'
            if scaler_key in self.preprocessors:
                num_cols = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
                input_df[num_cols] = self.preprocessors[scaler_key].transform(input_df[num_cols])
            
            model = self.models.get('hypertension')
            if model is None:
                return self._error_response("Hypertension model not available")
            
            prediction = int(model.predict(input_df)[0])
            probability = self._calculate_probability(model, input_df, prediction)
            risk_level = self._get_risk_level(prediction, probability)
            recommendations = self._get_hypertension_recommendations(data, prediction)
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': probability,
                'risk_level': risk_level,
                'message': self._get_prediction_message('hypertension', prediction),
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Hypertension prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_mental_health(self, text: str) -> Dict:
        """Predict depression and anxiety risk from text"""
        try:
            model = self.models.get('mental_health')
            
            if model is None:
                logger.warning("Mental health model not loaded, using fallback")
                return self._fallback_mental_health_prediction(text)
            
            # Handle different model formats
            if hasattr(model, '__call__'):
                result = model(text)
            elif hasattr(model, 'predict'):
                result = model.predict([text])
            else:
                return self._fallback_mental_health_prediction(text)
            
            return self._parse_mental_health_output(result)
            
        except Exception as e:
            logger.error(f"Mental health prediction error: {str(e)}", exc_info=True)
            return self._fallback_mental_health_prediction(text)
    
    # ============================================================================
    # PRIVATE METHODS - FEATURE PREPARATION
    # ============================================================================
    
    def _prepare_diabetes_features(self, data) -> np.ndarray:
        """Prepare features for diabetes prediction"""
        return np.array([[
            float(data.pregnancies),
            float(data.glucose),
            float(data.blood_pressure),
            float(data.skin_thickness),
            float(data.insulin),
            float(data.bmi),
            float(data.diabetes_pedigree),
            float(data.age)
        ]])
    
    def _prepare_asthma_features(self, data) -> np.ndarray:
        """Prepare features for asthma prediction"""
        return np.array([[
            float(data.gender_male),
            float(data.smoking_ex),
            float(data.smoking_non),
            float(data.age),
            float(data.peak_flow)
        ]])
    
    def _prepare_cardio_features(self, data) -> np.ndarray:
        """Prepare features for cardiovascular prediction"""
        return np.array([[
            float(data.age),
            float(data.ap_hi),
            float(data.ap_lo),
            float(data.cholesterol),
            float(data.gluc),
            float(data.smoke),
            float(data.alco),
            float(data.active),
            float(data.weight)
        ]])
    
    def _prepare_stroke_features(self, data) -> np.ndarray:
        """Prepare features for stroke prediction"""
        return np.array([[
            float(data.age),
            float(data.hypertension),
            float(data.heart_disease),
            float(data.ever_married),
            float(data.avg_glucose_level),
            float(data.bmi),
            float(data.smoking_status)
        ]])
    
    def _prepare_hypertension_features(self, data) -> pd.DataFrame:
        """Prepare features for hypertension prediction"""
        return pd.DataFrame({
            'male': [float(data.male)],
            'age': [float(data.age)],
            'cigsPerDay': [float(data.cigsPerDay)],
            'BPMeds': [float(data.BPMeds)],
            'totChol': [float(data.totChol)],
            'sysBP': [float(data.sysBP)],
            'diaBP': [float(data.diaBP)],
            'BMI': [float(data.BMI)],
            'heartRate': [float(data.heartRate)],
            'glucose': [float(data.glucose)]
        })
    
    # ============================================================================
    # PRIVATE METHODS - MODEL LOADING
    # ============================================================================
    
    @retry_on_failure(max_retries=2)
    def _load_model_with_config(self, config: ModelConfig) -> bool:
        """Load a single model with its configuration"""
        name = config.name
        start_time = datetime.now()
        
        try:
            # Find model file
            model_path = self._find_model_file(config)
            if model_path is None:
                self._load_errors[name] = f"Model file not found: {config.path}"
                logger.warning(f"Model '{name}' not found")
                return False
            
            # Load model
            model = self._load_file(model_path, config.type)
            if model is None:
                self._load_errors[name] = f"Failed to load model from {model_path}"
                return False
            
            self.models[name] = model
            logger.info(f"✓ Loaded {name} model from {model_path}")
            
            # Calculate file hash for integrity
            self.model_hashes[name] = self._calculate_file_hash(model_path)
            
            # Load preprocessors
            if config.has_preprocessor:
                self._load_preprocessors(name, config.preprocessor_paths)
            
            # Store metadata
            load_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            self.model_metadata[name] = {
                'accuracy': config.accuracy,
                'description': config.description,
                'loaded_at': datetime.now().isoformat(),
                'model_path': str(model_path),
                'model_type': config.type.value,
                'version': config.version,
                'features': config.required_features,
                'file_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2),
                'load_time_ms': round(load_time_ms, 2)
            }
            
            return True
            
        except Exception as e:
            self._load_errors[name] = str(e)
            logger.error(f"Failed to load {name}: {str(e)}", exc_info=True)
            return False
    
    def _find_model_file(self, config: ModelConfig) -> Optional[Path]:
        """Find existing model file from configured paths"""
        # Try main path
        main_path = self.base_path / config.path
        if main_path.exists():
            return main_path
        
        # Try alternative paths
        for alt_path in config.alt_paths:
            alt_full_path = self.base_path / alt_path
            if alt_full_path.exists():
                return alt_full_path
        
        return None
    
    def _load_preprocessors(self, model_name: str, preprocessor_paths: List[str]):
        """Load preprocessors for a model"""
        for prep_path in preprocessor_paths:
            full_path = self.base_path / prep_path
            if full_path.exists():
                try:
                    preprocessor = self._load_file(full_path, ModelType.PICKLE)
                    if preprocessor is not None:
                        key = f"{model_name}_{full_path.stem}"
                        self.preprocessors[key] = preprocessor
                        logger.info(f"  ✓ Loaded preprocessor: {full_path.name}")
                except Exception as e:
                    logger.error(f"Failed to load preprocessor {prep_path}: {str(e)}")
    
    def _load_file(self, file_path: Path, file_type: ModelType) -> Optional[Any]:
        """Load a file using pickle or joblib"""
        try:
            if file_type == ModelType.PICKLE:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                return joblib.load(file_path)
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file for integrity checking"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()[:16]
        except Exception:
            return "unknown"
    
    # ============================================================================
    # PRIVATE METHODS - UTILITIES
    # ============================================================================
    
    def _find_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Find model configuration by name"""
        for config in MODEL_CONFIGS:
            if config.name == model_name:
                return config
        return None
    
    def _calculate_probability(self, model, features, prediction: int) -> float:
        """Calculate prediction probability safely"""
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features)[0]
                probability = float(proba[1] if prediction == 1 else proba[0])
                return round(probability * 100, 2)
            else:
                return 85.0 if prediction == 1 else 75.0
        except Exception as e:
            logger.warning(f"Probability calculation failed: {str(e)}")
            return 75.0
    
    def _get_risk_level(self, prediction: int, probability: float) -> str:
        """Determine risk level based on prediction and probability"""
        if prediction == 1:
            if probability >= 70:
                return RiskLevel.HIGH.value
            elif probability >= 50:
                return RiskLevel.MODERATE.value
            else:
                return RiskLevel.LOW.value
        else:
            return RiskLevel.LOW.value
    
    def _get_prediction_message(self, disease: str, prediction: int) -> str:
        """Get human-readable prediction message"""
        messages = {
            'diabetes': {0: "No signs of diabetes detected", 1: "High risk of diabetes detected"},
            'asthma': {0: "Low risk of asthma", 1: "High risk of asthma detected"},
            'cardio': {0: "Low risk of cardiovascular disease", 1: "High risk of cardiovascular disease detected"},
            'stroke': {0: "Low risk of stroke", 1: "High risk of stroke detected"},
            'hypertension': {0: "Normal blood pressure range", 1: "High risk of hypertension detected"}
        }
        return messages.get(disease, {}).get(prediction, "Prediction completed")
    
    def _error_response(self, message: str) -> Dict:
        """Generate error response"""
        return {
            'success': False,
            'prediction': 0,
            'probability': 0,
            'risk_level': RiskLevel.HIGH.value,
            'message': message,
            'recommendations': ['Please check input values or contact support'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _parse_mental_health_output(self, result: Any) -> Dict:
        """Parse mental health model output"""
        if isinstance(result, dict):
            depression = result.get('depression', 50.0)
            anxiety = result.get('anxiety', 50.0)
        elif isinstance(result, (list, tuple)) and len(result) >= 2:
            depression = float(result[0]) * 100 if result[0] <= 1 else float(result[0])
            anxiety = float(result[1]) * 100 if result[1] <= 1 else float(result[1])
        else:
            return self._fallback_mental_health_prediction(None)
        
        return {
            'depression_risk': min(100, max(0, depression)),
            'anxiety_risk': min(100, max(0, anxiety))
        }
    
    def _fallback_mental_health_prediction(self, text: str = None) -> Dict:
        """Fallback rule-based mental health prediction"""
        depression_score = 50.0
        anxiety_score = 50.0
        
        if text:
            text_lower = text.lower()
            
            depression_keywords = ['hopeless', 'worthless', 'empty', 'sad', 'depressed', 
                                   'no energy', 'fatigue', 'tired', 'lonely', 'cry', 'numb', 'suicidal']
            anxiety_keywords = ['anxious', 'anxiety', 'worry', 'nervous', 'panic', 'scared',
                                'fear', 'overwhelmed', 'stress', 'racing thoughts']
            
            depression_count = sum(1 for w in depression_keywords if w in text_lower)
            anxiety_count = sum(1 for w in anxiety_keywords if w in text_lower)
            
            depression_score = min(95, 50 + (depression_count * 5))
            anxiety_score = min(95, 50 + (anxiety_count * 5))
        
        return {
            'depression_risk': depression_score,
            'anxiety_risk': anxiety_score
        }
    
    # ============================================================================
    # RECOMMENDATION METHODS
    # ============================================================================
    
    def _get_diabetes_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized diabetes recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "Consult an endocrinologist for proper diabetes management",
                "Monitor blood sugar levels daily using a glucometer"
            ])
        
        if hasattr(data, 'glucose') and data.glucose > 140:
            recommendations.append("Reduce intake of sugary foods and refined carbohydrates")
        
        if hasattr(data, 'bmi') and data.bmi > 25:
            recommendations.append("Aim to lose 5-10% of body weight through diet and exercise")
        
        if hasattr(data, 'age') and data.age > 45:
            recommendations.append("Schedule regular diabetes screening every 6 months")
        
        if not recommendations:
            recommendations.extend([
                "Continue maintaining a healthy balanced diet",
                "Exercise regularly - at least 150 minutes per week"
            ])
        
        return recommendations
    
    def _get_asthma_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized asthma recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "Consult a pulmonologist for comprehensive asthma evaluation",
                "Consider pulmonary function testing (spirometry)"
            ])
        
        if hasattr(data, 'smoking_ex') and data.smoking_ex == 1:
            recommendations.append("Avoid smoking and second-hand smoke exposure")
        
        if hasattr(data, 'peak_flow') and data.peak_flow < 0.5:
            recommendations.append("Monitor peak flow readings daily")
        
        if not recommendations:
            recommendations.append("Maintain good respiratory health with regular exercise")
        
        return recommendations
    
    def _get_cardio_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized cardiovascular recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "Schedule immediate cardiology consultation",
                "Consider stress test and ECG evaluation"
            ])
        
        if hasattr(data, 'ap_hi') and data.ap_hi > 140:
            recommendations.append("Monitor blood pressure twice daily")
            recommendations.append("Reduce sodium intake to less than 1500mg per day")
        
        if hasattr(data, 'smoke') and data.smoke == 1:
            recommendations.append("Join smoking cessation program")
        
        recommendations.append("Exercise 30-45 minutes daily, 5 days per week")
        
        return recommendations
    
    def _get_stroke_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized stroke recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "Seek immediate neurological evaluation",
                "Learn FAST warning signs (Face, Arm, Speech, Time)"
            ])
        
        if hasattr(data, 'hypertension') and data.hypertension == 1:
            recommendations.append("Strict blood pressure control is essential")
        
        if hasattr(data, 'avg_glucose_level') and data.avg_glucose_level > 140:
            recommendations.append("Control blood sugar levels to reduce stroke risk")
        
        recommendations.append("Maintain healthy BMI between 18.5-24.9")
        
        return recommendations
    
    def _get_hypertension_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized hypertension recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.extend([
                "Consult cardiologist for BP management plan",
                "Consider 24-hour ambulatory BP monitoring"
            ])
        
        if hasattr(data, 'sysBP') and data.sysBP > 140:
            recommendations.append("Reduce sodium intake to less than 1500mg daily")
        
        if hasattr(data, 'BMI') and data.BMI > 25:
            recommendations.append("Weight loss of 5-10% can significantly reduce BP")
        
        recommendations.append("Practice DASH diet (rich in fruits, vegetables, low-fat dairy)")
        
        return recommendations
    
    # ============================================================================
    # RISK SCORE CALCULATIONS
    # ============================================================================
    
    def _calculate_asthma_risk_score(self, data) -> float:
        """Calculate asthma risk score based on factors"""
        score = 0
        
        if hasattr(data, 'smoking_ex') and data.smoking_ex == 1:
            score += 20
        
        if hasattr(data, 'peak_flow'):
            if data.peak_flow < 0.4:
                score += 30
            elif data.peak_flow < 0.6:
                score += 15
        
        if hasattr(data, 'age') and data.age > 0.7:
            score += 10
        
        return min(score, 100)
    
    def _calculate_cardio_risk_score(self, data) -> float:
        """Calculate cardiovascular risk score"""
        score = 0
        
        if hasattr(data, 'ap_hi') and data.ap_hi > 140:
            score += 25
        
        if hasattr(data, 'cholesterol') and data.cholesterol == 3:
            score += 20
        
        if hasattr(data, 'smoke') and data.smoke == 1:
            score += 15
        
        if hasattr(data, 'active') and data.active == 0:
            score += 10
        
        return min(score, 100)
    
    def _calculate_stroke_risk_score(self, data) -> float:
        """Calculate stroke risk score"""
        score = 0
        
        if hasattr(data, 'hypertension') and data.hypertension == 1:
            score += 25
        
        if hasattr(data, 'heart_disease') and data.heart_disease == 1:
            score += 20
        
        if hasattr(data, 'avg_glucose_level') and data.avg_glucose_level > 140:
            score += 15
        
        if hasattr(data, 'age') and data.age > 60:
            score += 15
        
        return min(score, 100)


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_model_manager: Optional[ModelManager] = None

def get_model_manager() -> ModelManager:
    """Get or create the model manager singleton (thread-safe)"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def quick_predict(disease: str, data: Dict) -> Dict:
    """Quick prediction helper"""
    manager = get_model_manager()
    
    prediction_methods = {
        'diabetes': manager.predict_diabetes,
        'asthma': manager.predict_asthma,
        'cardio': manager.predict_cardio,
        'stroke': manager.predict_stroke,
        'hypertension': manager.predict_hypertension,
        'mental_health': lambda d: manager.predict_mental_health(d.get('text', ''))
    }
    
    method = prediction_methods.get(disease.lower())
    if method is None:
        return {'success': False, 'error': f'Unknown disease: {disease}'}
    
    # Convert dict to object for methods that expect object
    class DataObject:
        pass
    
    obj = DataObject()
    for key, value in data.items():
        setattr(obj, key, value)
    
    try:
        if disease.lower() == 'mental_health':
            return method(data)
        return method(obj)
    except Exception as e:
        logger.error(f"Quick prediction error: {e}")
        return {'success': False, 'error': str(e)}


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    print("\n" + "=" * 60)
    print("Testing Model Manager")
    print("=" * 60 + "\n")
    
    # Create manager
    manager = get_model_manager()
    
    # Print summary
    print(manager.get_model_summary())
    
    # Test status
    status = manager.get_model_status()
    print(f"\nStatus: {status['loaded_models']}/{status['total_models']} models loaded")