"""
Prediction Service - Handles all prediction logic and result formatting

This module provides comprehensive disease prediction services using machine learning models.
It includes risk calculation, recommendation generation, and result formatting for various diseases.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
import logging
from functools import wraps
from dataclasses import dataclass
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class DiseaseType(str, Enum):
    """Disease type enumeration"""
    DIABETES = "diabetes"
    ASTHMA = "asthma"
    CARDIO = "cardio"
    STROKE = "stroke"
    HYPERTENSION = "hypertension"


@dataclass
class PredictionResult:
    """Prediction result data class"""
    prediction: int
    probability: float
    risk_level: str
    message: str
    recommendations: List[str]
    risk_factors: List[Dict[str, Any]]
    model_accuracy: float
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'prediction': self.prediction,
            'probability': self.probability,
            'risk_level': self.risk_level,
            'message': self.message,
            'recommendations': self.recommendations,
            'risk_factors': self.risk_factors,
            'model_accuracy': self.model_accuracy,
            'timestamp': self.timestamp
        }


# ============================================================================
# DECORATORS FOR ERROR HANDLING AND LOGGING
# ============================================================================

def log_prediction(func):
    """Decorator to log prediction attempts"""
    @wraps(func)
    def wrapper(self, data: Dict, *args, **kwargs):
        disease = func.__name__.replace('predict_', '')
        logger.info(f"Starting {disease} prediction with data: {data}")
        
        try:
            result = func(self, data, *args, **kwargs)
            logger.info(f"{disease} prediction completed successfully: {result.get('risk_level', 'Unknown')} risk")
            return result
        except Exception as e:
            logger.error(f"{disease} prediction failed: {str(e)}", exc_info=True)
            raise
    return wrapper


def validate_input_data(required_fields: List[str]):
    """Decorator to validate input data has required fields"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, data: Dict, *args, **kwargs):
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            # Validate numeric fields
            for field in required_fields:
                if field in data and data[field] is not None:
                    try:
                        float(data[field])
                    except (ValueError, TypeError):
                        raise ValueError(f"Field '{field}' must be numeric, got {data[field]}")
            
            return func(self, data, *args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# PREDICTION SERVICE CLASS
# ============================================================================

class PredictionService:
    """
    Service for making predictions and formatting results
    
    This service handles predictions for multiple diseases using pre-trained ML models.
    It includes comprehensive error handling, input validation, and result formatting.
    """
    
    # Default model accuracies (fallback if not available from model_manager)
    DEFAULT_ACCURACIES = {
        'diabetes': 0.85,
        'asthma': 0.83,
        'cardio': 0.78,
        'stroke': 0.80,
        'hypertension': 0.82
    }
    
    # Risk score thresholds
    RISK_THRESHOLDS = {
        'high': 60,
        'moderate': 30
    }
    
    def __init__(self, model_manager):
        """
        Initialize prediction service
        
        Args:
            model_manager: ModelManager instance for accessing ML models
        """
        if model_manager is None:
            raise ValueError("ModelManager cannot be None")
        
        self.model_manager = model_manager
        logger.info("PredictionService initialized successfully")


def predict_mental_health(self, data: Dict) -> Dict:
    """
    Make mental health prediction from text
    
    Args:
        data: Dictionary containing 'text' field
    
    Returns:
        Dictionary with depression_risk, anxiety_risk, risk_level, message, recommendations
    """
    try:
        text = data.get('text', '')
        if not text or not text.strip():
            raise ValueError("Text input is required")
        
        # Get prediction from model manager
        result = self.model_manager.predict_mental_health(text)
        
        depression_risk = result.get('depression_risk', 50.0)
        anxiety_risk = result.get('anxiety_risk', 50.0)
        
        # Determine overall risk level
        avg_risk = (depression_risk + anxiety_risk) / 2
        if avg_risk >= 70:
            risk_level = "High"
        elif avg_risk >= 40:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        # Generate message
        if risk_level == "High":
            message = "High risk of depression and/or anxiety detected"
        elif risk_level == "Moderate":
            message = "Moderate risk of depression and/or anxiety detected"
        else:
            message = "Low risk of depression and anxiety detected"
        
        # Generate recommendations
        recommendations = self._get_mental_health_recommendations(depression_risk, anxiety_risk, text)
        
        return {
            'success': True,
            'depression_risk': round(depression_risk, 1),
            'anxiety_risk': round(anxiety_risk, 1),
            'risk_level': risk_level,
            'message': message,
            'recommendations': recommendations,
            'model_accuracy': self.model_manager.get_model_info('mental_health', {}).get('accuracy', 0.82)
        }
        
    except Exception as e:
        logger.error(f"Mental health prediction error: {str(e)}")
        return self._mental_health_error_response(f"Mental health prediction failed: {str(e)}")

def _get_mental_health_recommendations(self, depression_risk: float, anxiety_risk: float, text: str = None) -> List[str]:
    """
    Generate personalized mental health recommendations
    
    Args:
        depression_risk: Depression risk percentage
        anxiety_risk: Anxiety risk percentage
        text: Original user text (for keyword-specific recommendations)
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    # Risk-based recommendations
    if depression_risk >= 70:
        recommendations.append("Please consider speaking with a mental health professional")
        recommendations.append("Contact a crisis helpline if you're having thoughts of self-harm")
        recommendations.append("Share your feelings with a trusted friend or family member")
    elif depression_risk >= 40:
        recommendations.append("Consider talking to a counselor or therapist")
        recommendations.append("Practice self-care activities that you enjoy")
    
    if anxiety_risk >= 70:
        recommendations.append("Deep breathing exercises can help manage acute anxiety")
        recommendations.append("Consider speaking with a psychiatrist about medication options")
    elif anxiety_risk >= 40:
        recommendations.append("Try meditation or mindfulness apps like Headspace or Calm")
        recommendations.append("Limit caffeine and alcohol consumption")
    
    # General recommendations for all risk levels
    if "sleep" in text.lower() or "insomnia" in text.lower():
        recommendations.append("Maintain a consistent sleep schedule (7-9 hours per night)")
    
    if "stress" in text.lower() or "overwhelmed" in text.lower():
        recommendations.append("Break large tasks into smaller, manageable steps")
        recommendations.append("Set boundaries and learn to say no")
    
    if "anxious" in text.lower() or "worry" in text.lower():
        recommendations.append("Practice grounding techniques (5-4-3-2-1 method)")
    
    if "sad" in text.lower() or "hopeless" in text.lower():
        recommendations.append("Engage in physical activity - even a 10-minute walk helps")
        recommendations.append("Connect with others, even if you don't feel like it")
    
    # Default recommendations if none were added
    if not recommendations:
        recommendations.extend([
            "Regular exercise (30 minutes, 3-5 times per week) improves mental health",
            "Maintain a balanced diet rich in omega-3 fatty acids",
            "Limit social media use and screen time before bed",
            "Stay connected with supportive friends and family"
        ])
    
    return recommendations

def _mental_health_error_response(self, error_message: str) -> Dict:
    """Generate error response"""
    return {
        'success': False,
        'depression_risk': 0,
        'anxiety_risk': 0,
        'risk_level': 'Error',
        'message': error_message,
        'recommendations': ['Please try again or consult a professional directly'],
        'model_accuracy': 0.0
    }

# ============================================================================
    # PUBLIC PREDICTION METHODS
    # ============================================================================
    
    @log_prediction
    @validate_input_data([
        'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
        'insulin', 'bmi', 'diabetes_pedigree', 'age'
    ])
    def predict_diabetes(self, data: Dict) -> Dict:
        """
        Make diabetes prediction
        
        Args:
            data: Dictionary containing diabetes risk factors
        
        Returns:
            Dictionary with prediction results
            
        Raises:
            ValueError: If model is not loaded or input validation fails
        """
        try:
            # Extract and validate features
            features = self._prepare_diabetes_features(data)
            
            # Get model
            model = self.model_manager.get_model('diabetes')
            if model is None:
                logger.warning("Diabetes model not loaded, using fallback calculation")
                return self._fallback_diabetes_prediction(data)
            
            # Make prediction
            prediction = int(model.predict(features)[0])
            
            # Calculate probability
            probability = self._calculate_probability(model, features, prediction)
            
            # Generate recommendations and risk factors
            recommendations = self._get_diabetes_recommendations(data, prediction)
            risk_factors = self._analyze_diabetes_risk_factors(data)
            
            # Get model accuracy
            accuracy = self._get_model_accuracy('diabetes')
            
            return {
                'prediction': prediction,
                'probability': round(probability, 2),
                'risk_level': self._get_risk_level_from_prediction(prediction, probability),
                'message': self._get_prediction_message(DiseaseType.DIABETES, prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Diabetes prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Diabetes prediction failed: {str(e)}")
    
    @log_prediction
    @validate_input_data(['gender_male', 'smoking_ex', 'smoking_non', 'age', 'peak_flow'])
    def predict_asthma(self, data: Dict) -> Dict:
        """Make asthma prediction"""
        try:
            # Prepare input
            raw_input = self._prepare_asthma_features(data)
            
            # Apply preprocessing if available
            preprocessor = self.model_manager.get_preprocessor('asthma')
            if preprocessor is not None:
                processed_input = preprocessor.transform(raw_input)
            else:
                processed_input = raw_input
                logger.debug("No preprocessor found for asthma model")
            
            # Get model
            model = self.model_manager.get_model('asthma')
            if model is None:
                logger.warning("Asthma model not loaded, using fallback calculation")
                return self._fallback_asthma_prediction(data)
            
            # Make prediction
            prediction = int(model.predict(processed_input)[0])
            
            # Calculate risk score
            risk_score = self._calculate_asthma_risk_score(data)
            probability = risk_score
            
            # Generate response
            recommendations = self._get_asthma_recommendations(data, prediction)
            risk_factors = self._analyze_asthma_risk_factors(data)
            accuracy = self._get_model_accuracy('asthma')
            
            return {
                'prediction': prediction,
                'probability': round(probability, 2),
                'risk_level': self._get_risk_level_from_score(probability),
                'message': self._get_prediction_message(DiseaseType.ASTHMA, prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Asthma prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Asthma prediction failed: {str(e)}")
    
    @log_prediction
    @validate_input_data(['age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'weight'])
    def predict_cardio(self, data: Dict) -> Dict:
        """Make cardiovascular disease prediction"""
        try:
            features = self._prepare_cardio_features(data)
            
            model = self.model_manager.get_model('cardio')
            if model is None:
                logger.warning("Cardiovascular model not loaded, using fallback calculation")
                return self._fallback_cardio_prediction(data)
            
            prediction = int(model.predict(features)[0])
            probability = self._calculate_probability(model, features, prediction)
            
            recommendations = self._get_cardio_recommendations(data, prediction)
            risk_factors = self._analyze_cardio_risk_factors(data)
            accuracy = self._get_model_accuracy('cardio')
            
            return {
                'prediction': prediction,
                'probability': round(probability, 2),
                'risk_level': self._get_risk_level_from_prediction(prediction, probability),
                'message': self._get_prediction_message(DiseaseType.CARDIO, prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Cardiovascular prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Cardiovascular prediction failed: {str(e)}")
    
    @log_prediction
    @validate_input_data(['age', 'hypertension', 'heart_disease', 'ever_married', 'avg_glucose_level', 'bmi', 'smoking_status'])
    def predict_stroke(self, data: Dict) -> Dict:
        """Make stroke prediction"""
        try:
            features = self._prepare_stroke_features(data)
            
            model = self.model_manager.get_model('stroke')
            if model is None:
                logger.warning("Stroke model not loaded, using fallback calculation")
                return self._fallback_stroke_prediction(data)
            
            prediction = int(model.predict(features)[0])
            probability = self._calculate_probability(model, features, prediction)
            
            recommendations = self._get_stroke_recommendations(data, prediction)
            risk_factors = self._analyze_stroke_risk_factors(data)
            accuracy = self._get_model_accuracy('stroke')
            
            return {
                'prediction': prediction,
                'probability': round(probability, 2),
                'risk_level': self._get_risk_level_from_prediction(prediction, probability),
                'message': self._get_prediction_message(DiseaseType.STROKE, prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Stroke prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Stroke prediction failed: {str(e)}")
    
    @log_prediction
    @validate_input_data(['male', 'age', 'cigsPerDay', 'BPMeds', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'])
    def predict_hypertension(self, data: Dict) -> Dict:
        """Make hypertension prediction"""
        try:
            input_df = self._prepare_hypertension_features(data)
            
            # Scale features if preprocessor exists
            preprocessor = self.model_manager.get_preprocessor('hypertension')
            if preprocessor is not None:
                num_cols = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
                try:
                    input_df[num_cols] = preprocessor.transform(input_df[num_cols])
                except Exception as e:
                    logger.warning(f"Feature scaling failed: {e}, using raw values")
            
            model = self.model_manager.get_model('hypertension')
            if model is None:
                logger.warning("Hypertension model not loaded, using fallback calculation")
                return self._fallback_hypertension_prediction(data)
            
            prediction = int(model.predict(input_df)[0])
            probability = self._calculate_probability(model, input_df, prediction)
            
            recommendations = self._get_hypertension_recommendations(data, prediction)
            risk_factors = self._analyze_hypertension_risk_factors(data)
            accuracy = self._get_model_accuracy('hypertension')
            
            return {
                'prediction': prediction,
                'probability': round(probability, 2),
                'risk_level': self._get_risk_level_from_prediction(prediction, probability),
                'message': self._get_prediction_message(DiseaseType.HYPERTENSION, prediction),
                'recommendations': recommendations,
                'risk_factors': risk_factors,
                'model_accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Hypertension prediction error: {str(e)}", exc_info=True)
            return self._error_response(f"Hypertension prediction failed: {str(e)}")
    
    # ============================================================================
    # FEATURE PREPARATION METHODS
    # ============================================================================
    
    def _prepare_diabetes_features(self, data: Dict) -> np.ndarray:
        """Prepare feature array for diabetes prediction"""
        try:
            features = np.array([[
                float(data['pregnancies']),
                float(data['glucose']),
                float(data['blood_pressure']),
                float(data['skin_thickness']),
                float(data['insulin']),
                float(data['bmi']),
                float(data['diabetes_pedigree']),
                float(data['age'])
            ]], dtype=np.float64)
            
            # Validate feature ranges
            self._validate_diabetes_ranges(data)
            
            return features
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid diabetes input data: {str(e)}")
    
    def _prepare_asthma_features(self, data: Dict) -> np.ndarray:
        """Prepare feature array for asthma prediction"""
        try:
            return np.array([[
                float(data['gender_male']),
                float(data['smoking_ex']),
                float(data['smoking_non']),
                float(data['age']),
                float(data['peak_flow'])
            ]], dtype=np.float64)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid asthma input data: {str(e)}")
    
    def _prepare_cardio_features(self, data: Dict) -> np.ndarray:
        """Prepare feature array for cardiovascular prediction"""
        try:
            return np.array([[
                float(data['age']),
                float(data['ap_hi']),
                float(data['ap_lo']),
                float(data['cholesterol']),
                float(data['gluc']),
                float(data['smoke']),
                float(data['alco']),
                float(data['active']),
                float(data['weight'])
            ]], dtype=np.float64)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid cardiovascular input data: {str(e)}")
    
    def _prepare_stroke_features(self, data: Dict) -> np.ndarray:
        """Prepare feature array for stroke prediction"""
        try:
            return np.array([[
                float(data['age']),
                float(data['hypertension']),
                float(data['heart_disease']),
                float(data['ever_married']),
                float(data['avg_glucose_level']),
                float(data['bmi']),
                float(data['smoking_status'])
            ]], dtype=np.float64)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid stroke input data: {str(e)}")
    
    def _prepare_hypertension_features(self, data: Dict) -> pd.DataFrame:
        """Prepare DataFrame for hypertension prediction"""
        try:
            return pd.DataFrame({
                'male': [float(data['male'])],
                'age': [float(data['age'])],
                'cigsPerDay': [float(data['cigsPerDay'])],
                'BPMeds': [float(data['BPMeds'])],
                'totChol': [float(data['totChol'])],
                'sysBP': [float(data['sysBP'])],
                'diaBP': [float(data['diaBP'])],
                'BMI': [float(data['BMI'])],
                'heartRate': [float(data['heartRate'])],
                'glucose': [float(data['glucose'])]
            })
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid hypertension input data: {str(e)}")
    
    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================
    
    def _validate_diabetes_ranges(self, data: Dict) -> None:
        """Validate diabetes feature ranges"""
        validations = [
            (data['glucose'], 0, 300, "Glucose"),
            (data['blood_pressure'], 0, 200, "Blood pressure"),
            (data['bmi'], 0, 70, "BMI"),
            (data['age'], 1, 120, "Age")
        ]
        
        for value, min_val, max_val, name in validations:
            if value < min_val or value > max_val:
                raise ValueError(f"{name} value {value} is outside valid range [{min_val}, {max_val}]")
    
    # ============================================================================
    # PROBABILITY AND RISK CALCULATION METHODS
    # ============================================================================
    
    def _calculate_probability(self, model, features: Union[np.ndarray, pd.DataFrame], prediction: int) -> float:
        """
        Calculate prediction probability safely
        
        Args:
            model: ML model with predict_proba method
            features: Input features
            prediction: Model prediction (0 or 1)
        
        Returns:
            Probability percentage (0-100)
        """
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features)[0]
                probability = float(proba[1] if prediction == 1 else proba[0])
                # Convert to percentage
                return min(max(probability * 100, 0), 100)
            else:
                # Default confidence based on prediction
                return 85.0 if prediction == 1 else 75.0
        except Exception as e:
            logger.warning(f"Probability calculation failed: {str(e)}")
            return 75.0
    
    def _get_risk_level_from_prediction(self, prediction: int, probability: float) -> str:
        """
        Determine risk level based on prediction and probability
        
        Args:
            prediction: Model prediction (0 or 1)
            probability: Confidence probability (0-100)
        
        Returns:
            Risk level string
        """
        if prediction == 1:
            return RiskLevel.HIGH.value
        else:
            if probability >= 70:
                return RiskLevel.LOW.value
            elif probability >= 50:
                return RiskLevel.MODERATE.value
            else:
                return RiskLevel.LOW.value
    
    def _get_risk_level_from_score(self, score: float) -> str:
        """
        Determine risk level from risk score
        
        Args:
            score: Risk score (0-100)
        
        Returns:
            Risk level string
        """
        if score >= self.RISK_THRESHOLDS['high']:
            return RiskLevel.HIGH.value
        elif score >= self.RISK_THRESHOLDS['moderate']:
            return RiskLevel.MODERATE.value
        else:
            return RiskLevel.LOW.value
    
    def _get_model_accuracy(self, disease: str) -> float:
        """
        Get model accuracy from model manager or use default
        
        Args:
            disease: Disease name
        
        Returns:
            Accuracy value (0-1)
        """
        try:
            info = self.model_manager.get_model_info(disease)
            if info and 'accuracy' in info:
                return info['accuracy']
        except Exception:
            pass
        return self.DEFAULT_ACCURACIES.get(disease, 0.80)
    
    # ============================================================================
    # PREDICTION MESSAGES
    # ============================================================================
    
    def _get_prediction_message(self, disease: DiseaseType, prediction: int) -> str:
        """Get human-readable prediction message"""
        messages = {
            DiseaseType.DIABETES: {
                0: "No signs of diabetes detected",
                1: "High risk of diabetes detected"
            },
            DiseaseType.ASTHMA: {
                0: "Low risk of asthma",
                1: "High risk of asthma detected"
            },
            DiseaseType.CARDIO: {
                0: "Low risk of cardiovascular disease",
                1: "High risk of cardiovascular disease detected"
            },
            DiseaseType.STROKE: {
                0: "Low risk of stroke",
                1: "High risk of stroke detected"
            },
            DiseaseType.HYPERTENSION: {
                0: "Normal blood pressure range",
                1: "High risk of hypertension detected"
            }
        }
        return messages.get(disease, {}).get(prediction, "Prediction completed")
    
    def _error_response(self, error_message: str) -> Dict:
        """Generate error response"""
        return {
            'prediction': 0,
            'probability': 0.0,
            'risk_level': RiskLevel.HIGH.value,
            'message': f"Prediction error: {error_message}",
            'recommendations': ['Please check your input values and try again'],
            'risk_factors': [],
            'model_accuracy': 0.0
        }
    
    # ============================================================================
    # FALLBACK PREDICTIONS (When ML models are not available)
    # ============================================================================
    
    def _fallback_diabetes_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based diabetes prediction when ML model is unavailable"""
        risk_score = 0
        
        if data.get('glucose', 0) > 140:
            risk_score += 30
        if data.get('bmi', 0) > 30:
            risk_score += 25
        if data.get('age', 0) > 45:
            risk_score += 15
        if data.get('diabetes_pedigree', 0) > 0.8:
            risk_score += 15
        
        prediction = 1 if risk_score >= 50 else 0
        probability = min(85 + (risk_score - 50) / 2, 95) if prediction == 1 else max(60, 75 - risk_score / 3)
        
        return {
            'prediction': prediction,
            'probability': round(probability, 2),
            'risk_level': self._get_risk_level_from_score(risk_score),
            'message': self._get_prediction_message(DiseaseType.DIABETES, prediction),
            'recommendations': self._get_diabetes_recommendations(data, prediction),
            'risk_factors': self._analyze_diabetes_risk_factors(data),
            'model_accuracy': 0.75
        }
    
    def _fallback_asthma_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based asthma prediction"""
        risk_score = 0
        if data.get('smoking_ex', 0) == 1:
            risk_score += 25
        if data.get('peak_flow', 0) < 0.4:
            risk_score += 35
        prediction = 1 if risk_score >= 50 else 0
        probability = 80 - risk_score / 2 if prediction == 0 else 85 + (risk_score - 50) / 2
        
        return {
            'prediction': prediction,
            'probability': round(min(probability, 95), 2),
            'risk_level': self._get_risk_level_from_score(risk_score),
            'message': self._get_prediction_message(DiseaseType.ASTHMA, prediction),
            'recommendations': self._get_asthma_recommendations(data, prediction),
            'risk_factors': self._analyze_asthma_risk_factors(data),
            'model_accuracy': 0.70
        }
    
    def _fallback_cardio_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based cardiovascular prediction"""
        risk_score = 0
        if data.get('ap_hi', 0) > 140:
            risk_score += 30
        if data.get('cholesterol', 1) == 3:
            risk_score += 25
        if data.get('smoke', 0) == 1:
            risk_score += 20
        prediction = 1 if risk_score >= 50 else 0
        
        return {
            'prediction': prediction,
            'probability': round(82 - risk_score / 3 if prediction == 0 else 85 + (risk_score - 50) / 2, 2),
            'risk_level': self._get_risk_level_from_score(risk_score),
            'message': self._get_prediction_message(DiseaseType.CARDIO, prediction),
            'recommendations': self._get_cardio_recommendations(data, prediction),
            'risk_factors': self._analyze_cardio_risk_factors(data),
            'model_accuracy': 0.70
        }
    
    def _fallback_stroke_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based stroke prediction"""
        risk_score = 0
        if data.get('hypertension', 0) == 1:
            risk_score += 30
        if data.get('heart_disease', 0) == 1:
            risk_score += 25
        if data.get('age', 0) > 60:
            risk_score += 15
        prediction = 1 if risk_score >= 50 else 0
        
        return {
            'prediction': prediction,
            'probability': round(85 - risk_score / 3 if prediction == 0 else 85 + (risk_score - 50) / 2, 2),
            'risk_level': self._get_risk_level_from_score(risk_score),
            'message': self._get_prediction_message(DiseaseType.STROKE, prediction),
            'recommendations': self._get_stroke_recommendations(data, prediction),
            'risk_factors': self._analyze_stroke_risk_factors(data),
            'model_accuracy': 0.70
        }
    
    def _fallback_hypertension_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based hypertension prediction"""
        risk_score = 0
        if data.get('sysBP', 0) > 140:
            risk_score += 35
        if data.get('diaBP', 0) > 90:
            risk_score += 25
        if data.get('BMI', 0) > 30:
            risk_score += 20
        prediction = 1 if risk_score >= 50 else 0
        
        return {
            'prediction': prediction,
            'probability': round(78 - risk_score / 3 if prediction == 0 else 85 + (risk_score - 50) / 2, 2),
            'risk_level': self._get_risk_level_from_score(risk_score),
            'message': self._get_prediction_message(DiseaseType.HYPERTENSION, prediction),
            'recommendations': self._get_hypertension_recommendations(data, prediction),
            'risk_factors': self._analyze_hypertension_risk_factors(data),
            'model_accuracy': 0.70
        }
    
    # ============================================================================
    # RECOMMENDATION METHODS (Keep your existing implementation)
    # ============================================================================
    
    def _get_diabetes_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized diabetes recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult an endocrinologist for proper diabetes management")
            recommendations.append("Monitor blood sugar levels daily using a glucometer")
            recommendations.append("Follow prescribed medication schedule strictly")
        
        if data.get('glucose', 0) > 140:
            recommendations.append("Reduce intake of sugary foods and refined carbohydrates")
            recommendations.append("Consider consulting a nutritionist for meal planning")
        
        if data.get('bmi', 0) > 25:
            recommendations.append("Aim to lose 5-10% of body weight through diet and exercise")
            recommendations.append("Incorporate 30 minutes of moderate exercise daily")
        
        if data.get('age', 0) > 45:
            recommendations.append("Schedule regular diabetes screening every 6 months")
        
        if data.get('blood_pressure', 0) > 140:
            recommendations.append("Monitor blood pressure regularly and reduce sodium intake")
        
        if not recommendations:
            recommendations.extend([
                "Continue maintaining a healthy balanced diet",
                "Exercise regularly - at least 150 minutes per week",
                "Get annual health check-ups including blood sugar testing"
            ])
        
        return recommendations
    
    def _get_asthma_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized asthma recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult a pulmonologist for comprehensive asthma evaluation")
            recommendations.append("Consider pulmonary function testing (spirometry)")
            recommendations.append("Keep rescue inhaler accessible at all times")
        
        if data.get('smoking_ex', 0) == 1 or data.get('smoking_non', 0) == 0:
            recommendations.append("Avoid smoking and second-hand smoke exposure")
        
        if data.get('peak_flow', 0) < 0.5:
            recommendations.append("Monitor peak flow readings daily")
            recommendations.append("Create an asthma action plan with your doctor")
        
        recommendations.append("Identify and avoid personal asthma triggers")
        recommendations.append("Keep home environment dust-free and well-ventilated")
        
        return recommendations
    
    def _get_cardio_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized cardiovascular recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Schedule immediate cardiology consultation")
            recommendations.append("Consider stress test and ECG evaluation")
        
        if data.get('ap_hi', 0) > 140 or data.get('ap_lo', 0) > 90:
            recommendations.append("Monitor blood pressure twice daily")
            recommendations.append("Reduce sodium intake to less than 1500mg per day")
        
        if data.get('cholesterol', 1) > 1:
            recommendations.append("Adopt heart-healthy Mediterranean diet")
            recommendations.append("Include more omega-3 fatty acids in diet")
        
        if data.get('smoke', 0) == 1:
            recommendations.append("Join smoking cessation program")
        
        recommendations.append("Exercise 30-45 minutes daily, 5 days per week")
        recommendations.append("Manage stress through meditation or yoga")
        
        return recommendations
    
    def _get_stroke_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized stroke recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Seek immediate neurological evaluation")
            recommendations.append("Learn FAST warning signs (Face, Arm, Speech, Time)")
        
        if data.get('hypertension', 0) == 1:
            recommendations.append("Strict blood pressure control is essential")
        
        if data.get('avg_glucose_level', 0) > 140:
            recommendations.append("Control blood sugar levels to reduce stroke risk")
        
        recommendations.append("Maintain healthy BMI between 18.5-24.9")
        recommendations.append("Exercise regularly to improve cardiovascular health")
        
        return recommendations
    
    def _get_hypertension_recommendations(self, data: Dict, prediction: int) -> List[str]:
        """Generate personalized hypertension recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult cardiologist for BP management plan")
            recommendations.append("Consider 24-hour ambulatory BP monitoring")
        
        if data.get('sysBP', 0) > 140 or data.get('diaBP', 0) > 90:
            recommendations.append("Reduce sodium intake to less than 1500mg daily")
            recommendations.append("Limit alcohol consumption")
        
        if data.get('BMI', 0) > 25:
            recommendations.append("Weight loss of 5-10% can significantly reduce BP")
        
        if data.get('cigsPerDay', 0) > 0:
            recommendations.append("Smoking cessation is critical for BP control")
        
        recommendations.append("Practice DASH diet (rich in fruits, vegetables, low-fat dairy)")
        recommendations.append("Regular aerobic exercise - walking, swimming, cycling")
        
        return recommendations
    
    # ============================================================================
    # RISK FACTOR ANALYSIS METHODS
    # ============================================================================
    
    def _analyze_diabetes_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return diabetes risk factors"""
        risk_factors = []
        
        if data.get('glucose', 0) > 140:
            risk_factors.append({
                'factor': 'Elevated Glucose',
                'value': f"{data['glucose']} mg/dL",
                'risk': 'High',
                'recommendation': 'Monitor blood sugar and reduce sugar intake'
            })
        
        if data.get('bmi', 0) > 25:
            risk_factors.append({
                'factor': 'Overweight/Obese',
                'value': f"BMI {data['bmi']}",
                'risk': 'Moderate',
                'recommendation': 'Weight management through diet and exercise'
            })
        
        if data.get('age', 0) > 45:
            risk_factors.append({
                'factor': 'Age',
                'value': f"{data['age']} years",
                'risk': 'Moderate',
                'recommendation': 'Regular diabetes screening'
            })
        
        return risk_factors
    
    def _analyze_asthma_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return asthma risk factors"""
        risk_factors = []
        
        if data.get('smoking_ex', 0) == 1:
            risk_factors.append({
                'factor': 'Smoking History',
                'value': 'Former Smoker',
                'risk': 'Moderate',
                'recommendation': 'Avoid smoke exposure and monitor symptoms'
            })
        
        if data.get('peak_flow', 0) < 0.5:
            risk_factors.append({
                'factor': 'Reduced Peak Flow',
                'value': f"{data['peak_flow']} L/sec",
                'risk': 'High',
                'recommendation': 'Pulmonary function evaluation recommended'
            })
        
        return risk_factors
    
    def _analyze_cardio_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return cardiovascular risk factors"""
        risk_factors = []
        
        if data.get('ap_hi', 0) > 140:
            risk_factors.append({
                'factor': 'High Systolic BP',
                'value': f"{data['ap_hi']} mmHg",
                'risk': 'High',
                'recommendation': 'Blood pressure management required'
            })
        
        if data.get('cholesterol', 1) > 1:
            risk_factors.append({
                'factor': 'Abnormal Cholesterol',
                'value': 'Above Normal',
                'risk': 'Moderate',
                'recommendation': 'Dietary modification and possible medication'
            })
        
        return risk_factors
    
    def _analyze_stroke_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return stroke risk factors"""
        risk_factors = []
        
        if data.get('hypertension', 0) == 1:
            risk_factors.append({
                'factor': 'Hypertension',
                'value': 'Present',
                'risk': 'High',
                'recommendation': 'Strict blood pressure control'
            })
        
        if data.get('avg_glucose_level', 0) > 140:
            risk_factors.append({
                'factor': 'High Glucose',
                'value': f"{data['avg_glucose_level']} mg/dL",
                'risk': 'Moderate',
                'recommendation': 'Diabetes management to reduce stroke risk'
            })
        
        return risk_factors
    
    def _analyze_hypertension_risk_factors(self, data: Dict) -> List[Dict]:
        """Analyze and return hypertension risk factors"""
        risk_factors = []
        
        if data.get('sysBP', 0) > 140:
            risk_factors.append({
                'factor': 'Elevated Systolic BP',
                'value': f"{data['sysBP']} mmHg",
                'risk': 'High',
                'recommendation': 'Immediate lifestyle modification'
            })
        
        if data.get('BMI', 0) > 25:
            risk_factors.append({
                'factor': 'High BMI',
                'value': f"{data['BMI']}",
                'risk': 'Moderate',
                'recommendation': 'Weight loss program recommended'
            })
        
        return risk_factors
    
    # ============================================================================
    # RISK SCORE CALCULATION METHODS
    # ============================================================================
    
    def _calculate_asthma_risk_score(self, data: Dict) -> float:
        """Calculate asthma risk score based on factors"""
        score = 0
        
        if data.get('smoking_ex', 0) == 1:
            score += 20
        
        peak_flow = data.get('peak_flow', 0.5)
        if peak_flow < 0.4:
            score += 30
        elif peak_flow < 0.6:
            score += 15
        
        if data.get('age', 0) > 0.7:
            score += 10
        
        return min(score, 100)
    
    def _calculate_cardio_risk_score(self, data: Dict) -> float:
        """Calculate cardiovascular risk score"""
        score = 0
        
        ap_hi = data.get('ap_hi', 0)
        if ap_hi > 140:
            score += 25
        elif ap_hi > 130:
            score += 15
        
        cholesterol = data.get('cholesterol', 1)
        if cholesterol == 3:
            score += 20
        elif cholesterol == 2:
            score += 10
        
        if data.get('smoke', 0) == 1:
            score += 15
        
        if data.get('active', 0) == 0:
            score += 10
        
        return min(score, 100)
    
    def _calculate_stroke_risk_score(self, data: Dict) -> float:
        """Calculate stroke risk score"""
        score = 0
        
        if data.get('hypertension', 0) == 1:
            score += 25
        
        if data.get('heart_disease', 0) == 1:
            score += 20
        
        if data.get('avg_glucose_level', 0) > 140:
            score += 15
        
        if data.get('bmi', 0) > 30:
            score += 10
        
        age = data.get('age', 0)
        if age > 60:
            score += 15
        elif age > 50:
            score += 10
        
        return min(score, 100)


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def create_prediction_service(model_manager) -> PredictionService:
    """
    Factory function to create a PredictionService instance
    
    Args:
        model_manager: ModelManager instance
    
    Returns:
        Configured PredictionService instance
    """
    if model_manager is None:
        raise ValueError("ModelManager is required to create PredictionService")
    
    return PredictionService(model_manager)