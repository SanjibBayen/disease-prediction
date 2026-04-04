"""
Advanced Model Management System
Handles loading, caching, and prediction for all ML models
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging
from functools import lru_cache
import json

logger = logging.getLogger(__name__)

class ModelManager:
    """Advanced Manager for loading and accessing ML models"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.preprocessors: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        self.base_path = "models"
        self.load_all_models()
    
    def load_all_models(self):
        """Load all machine learning models with error handling"""
        
        # Define model configurations
        model_configs = [
            {
                'name': 'diabetes',
                'path': 'diabetes/diabetes_model.sav',
                'type': 'pickle',
                'alt_paths': [],
                'has_preprocessor': False
            },
            {
                'name': 'asthma',
                'path': 'asthma/model.pkl',
                'type': 'joblib',
                'alt_paths': ['asthama/model.pkl'],
                'has_preprocessor': True,
                'preprocessor_paths': ['asthma/preprocessor.pkl', 'asthama/preprocessor.pkl']
            },
            {
                'name': 'cardio',
                'path': 'cardio_vascular/xgboost_cardiovascular_model.pkl',
                'type': 'pickle',
                'alt_paths': [],
                'has_preprocessor': False
            },
            {
                'name': 'stroke',
                'path': 'stroke/finalized_model.pkl',
                'type': 'joblib',
                'alt_paths': [],
                'has_preprocessor': False
            },
            {
                'name': 'hypertension',
                'path': 'hypertension/extratrees_model.pkl',
                'type': 'pickle',
                'alt_paths': [],
                'has_preprocessor': True,
                'preprocessor_paths': ['hypertension/scaler.pkl']
            },
            {
                'name': 'sleep',
                'path': 'sleep_health/svc_model.pkl',
                'type': 'pickle',
                'alt_paths': [],
                'has_preprocessor': True,
                'preprocessor_paths': ['sleep_health/scaler.pkl', 'sleep_health/label_encoders.pkl']
            }
        ]
        
        for config in model_configs:
            self._load_model_with_config(config)
        
        logger.info(f"✓ Total models loaded: {len(self.models)}")
        if self.models:
            logger.info(f"  Models: {', '.join(self.models.keys())}")
    
    def _load_model_with_config(self, config: Dict):
        """Load a single model with its configuration"""
        name = config['name']
        
        # Try main path and alternative paths
        paths_to_try = [config['path']] + config.get('alt_paths', [])
        
        for path in paths_to_try:
            full_path = os.path.join(self.base_path, path)
            if os.path.exists(full_path):
                try:
                    # Load model
                    if config['type'] == 'pickle':
                        with open(full_path, 'rb') as f:
                            model = pickle.load(f)
                    else:  # joblib
                        model = joblib.load(full_path)
                    
                    self.models[name] = model
                    logger.info(f"✓ {name.capitalize()} model loaded from {path}")
                    
                    # Load preprocessors if they exist
                    if config.get('has_preprocessor'):
                        self._load_preprocessors(name, config.get('preprocessor_paths', []))
                    
                    # Store metadata
                    self.model_metadata[name] = {
                        'loaded_at': datetime.now().isoformat(),
                        'model_path': path,
                        'model_type': config['type']
                    }
                    break  # Success, exit the loop
                    
                except Exception as e:
                    logger.error(f"Failed to load {name} model from {path}: {str(e)}")
                    continue  # Try next path
        
        if name not in self.models:
            logger.warning(f"⚠ {name.capitalize()} model not found in any path")
    
    def _load_preprocessors(self, model_name: str, preprocessor_paths: List[str]):
        """Load preprocessors for a model"""
        for prep_path in preprocessor_paths:
            full_path = os.path.join(self.base_path, prep_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'rb') as f:
                        preprocessor = pickle.load(f)
                    
                    # Store with appropriate key
                    key = f"{model_name}_{os.path.basename(prep_path).replace('.pkl', '')}"
                    self.preprocessors[key] = preprocessor
                    logger.info(f"  ✓ Loaded preprocessor: {os.path.basename(prep_path)}")
                except Exception as e:
                    logger.error(f"Failed to load preprocessor {prep_path}: {str(e)}")
    
    def predict_diabetes(self, data) -> Dict:
        """Predict diabetes risk with proper probability calculation"""
        try:
            # Prepare features
            features = np.array([[
                float(data.pregnancies),
                float(data.glucose),
                float(data.blood_pressure),
                float(data.skin_thickness),
                float(data.insulin),
                float(data.bmi),
                float(data.diabetes_pedigree),
                float(data.age)
            ]])
            
            model = self.models.get('diabetes')
            if model is None:
                return self._error_response("Diabetes model not available")
            
            # Make prediction
            prediction = int(model.predict(features)[0])
            
            # Calculate probability correctly
            probability = self._calculate_probability(model, features, prediction)
            
            # Generate recommendations
            recommendations = self._get_diabetes_recommendations(data, prediction)
            
            # Determine risk level based on BOTH prediction and probability
            risk_level = self._get_risk_level(prediction, probability)
            
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
            logger.error(f"Diabetes prediction error: {str(e)}")
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_asthma(self, data) -> Dict:
        """Predict asthma risk"""
        try:
            # Prepare features
            raw_input = np.array([[
                float(data.gender_male),
                float(data.smoking_ex),
                float(data.smoking_non),
                float(data.age),
                float(data.peak_flow)
            ]])
            
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
            
            # Calculate risk score based on factors
            risk_score = self._calculate_asthma_risk_score(data)
            
            recommendations = self._get_asthma_recommendations(data, prediction)
            risk_level = self._get_risk_level(prediction, risk_score)
            
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
            logger.error(f"Asthma prediction error: {str(e)}")
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_cardio(self, data) -> Dict:
        """Predict cardiovascular disease risk"""
        try:
            features = np.array([[
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
            
            model = self.models.get('cardio')
            if model is None:
                return self._error_response("Cardiovascular model not available")
            
            prediction = int(model.predict(features)[0])
            
            # Calculate risk score
            risk_score = self._calculate_cardio_risk_score(data)
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
            logger.error(f"Cardiovascular prediction error: {str(e)}")
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_stroke(self, data) -> Dict:
        """Predict stroke risk"""
        try:
            features = np.array([[
                float(data.age),
                float(data.hypertension),
                float(data.heart_disease),
                float(data.ever_married),
                float(data.avg_glucose_level),
                float(data.bmi),
                float(data.smoking_status)
            ]])
            
            model = self.models.get('stroke')
            if model is None:
                return self._error_response("Stroke model not available")
            
            prediction = int(model.predict(features)[0])
            
            # Calculate risk score
            risk_score = self._calculate_stroke_risk_score(data)
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
            logger.error(f"Stroke prediction error: {str(e)}")
            return self._error_response(f"Prediction error: {str(e)}")
    
    def predict_hypertension(self, data) -> Dict:
        """Predict hypertension risk"""
        try:
            # Create DataFrame
            input_df = pd.DataFrame({
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
            
            # Apply scaling if available
            scaler_key = 'hypertension_scaler'
            if scaler_key in self.preprocessors:
                num_cols = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
                input_df[num_cols] = self.preprocessors[scaler_key].transform(input_df[num_cols])
            
            model = self.models.get('hypertension')
            if model is None:
                return self._error_response("Hypertension model not available")
            
            prediction = int(model.predict(input_df)[0])
            
            # Calculate probability
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
            logger.error(f"Hypertension prediction error: {str(e)}")
            return self._error_response(f"Prediction error: {str(e)}")
    
    def _calculate_probability(self, model, features, prediction: int) -> float:
        """Calculate prediction probability safely"""
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features)[0]
                probability = float(proba[1] if prediction == 1 else proba[0])
                # Convert to percentage and round to 2 decimal places
                return round(probability * 100, 2)
            else:
                # Default confidence scores
                return 85.0 if prediction == 1 else 75.0
        except Exception as e:
            logger.warning(f"Probability calculation failed: {str(e)}")
            return 75.0
    
    def _get_risk_level(self, prediction: int, probability: float) -> str:
        """
        Determine risk level based on prediction and probability
        FIXED: For prediction=0 (negative), risk should be Low
        For prediction=1 (positive), risk should be High
        """
        if prediction == 1:
            # Positive prediction - High risk
            if probability >= 70:
                return "High"
            elif probability >= 50:
                return "Moderate"
            else:
                return "Low"
        else:
            # Negative prediction - Low risk
            if probability >= 70:
                return "Low"
            elif probability >= 50:
                return "Low"
            else:
                return "Low"
    
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
            'risk_level': 'Error',
            'message': message,
            'recommendations': ['Please check model files or contact support'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_diabetes_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized diabetes recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult an endocrinologist for proper diabetes management")
            recommendations.append("Monitor blood sugar levels daily using a glucometer")
        
        if hasattr(data, 'glucose') and data.glucose > 140:
            recommendations.append("Reduce intake of sugary foods and refined carbohydrates")
        
        if hasattr(data, 'bmi') and data.bmi > 25:
            recommendations.append("Aim to lose 5-10% of body weight through diet and exercise")
        
        if hasattr(data, 'age') and data.age > 45:
            recommendations.append("Schedule regular diabetes screening every 6 months")
        
        if not recommendations:
            recommendations.append("Continue maintaining a healthy balanced diet")
            recommendations.append("Exercise regularly - at least 150 minutes per week")
        
        return recommendations
    
    def _get_asthma_recommendations(self, data, prediction: int) -> List[str]:
        """Generate personalized asthma recommendations"""
        recommendations = []
        
        if prediction == 1:
            recommendations.append("Consult a pulmonologist for comprehensive asthma evaluation")
            recommendations.append("Consider pulmonary function testing (spirometry)")
        
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
            recommendations.append("Schedule immediate cardiology consultation")
            recommendations.append("Consider stress test and ECG evaluation")
        
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
            recommendations.append("Seek immediate neurological evaluation")
            recommendations.append("Learn FAST warning signs (Face, Arm, Speech, Time)")
        
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
            recommendations.append("Consult cardiologist for BP management plan")
            recommendations.append("Consider 24-hour ambulatory BP monitoring")
        
        if hasattr(data, 'sysBP') and data.sysBP > 140:
            recommendations.append("Reduce sodium intake to less than 1500mg daily")
        
        if hasattr(data, 'BMI') and data.BMI > 25:
            recommendations.append("Weight loss of 5-10% can significantly reduce BP")
        
        recommendations.append("Practice DASH diet (rich in fruits, vegetables, low-fat dairy)")
        
        return recommendations
    
    def _calculate_asthma_risk_score(self, data) -> float:
        """Calculate asthma risk score based on factors"""
        score = 0
        
        if hasattr(data, 'smoking_ex') and data.smoking_ex == 1:
            score += 20
        
        if hasattr(data, 'peak_flow') and data.peak_flow < 0.4:
            score += 30
        elif hasattr(data, 'peak_flow') and data.peak_flow < 0.6:
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
    
    def get_model(self, name: str):
        """Get a loaded model"""
        return self.models.get(name)
    
    def get_preprocessor(self, name: str):
        """Get a preprocessor"""
        return self.preprocessors.get(name)
    
    def list_models(self) -> List[str]:
        """List all loaded models"""
        return list(self.models.keys())
    
    def is_model_loaded(self, name: str) -> bool:
        """Check if a specific model is loaded"""
        return name in self.models
    
    def get_model_info(self, name: str) -> Optional[Dict]:
        """Get metadata for a specific model"""
        return self.model_metadata.get(name)


# Singleton instance with caching
_model_manager = None

def get_model_manager() -> ModelManager:
    """Get or create the model manager singleton"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager


# Convenience function for quick predictions
def quick_predict(disease: str, data: Dict) -> Dict:
    """Quick prediction helper"""
    manager = get_model_manager()
    prediction_methods = {
        'diabetes': manager.predict_diabetes,
        'asthma': manager.predict_asthma,
        'cardio': manager.predict_cardio,
        'stroke': manager.predict_stroke,
        'hypertension': manager.predict_hypertension
    }
    
    method = prediction_methods.get(disease)
    if method:
        # Convert dict to object
        class DataObject:
            pass
        
        obj = DataObject()
        for key, value in data.items():
            setattr(obj, key, value)
        
        return method(obj)
    
    return {'success': False, 'error': f'Unknown disease: {disease}'}