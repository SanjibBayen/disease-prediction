"""
Model Manager Service - Handles ML model loading and prediction logic
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelManager:
    """Centralized model management service"""
    
    def __init__(self, models_path: str = "models"):
        self.models_path = models_path
        self.models: Dict[str, Any] = {}
        self.preprocessors: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        self.load_all_models()
    
    def load_all_models(self):
        """Load all machine learning models with metadata"""
        
        # Define model configurations
        model_configs = [
            {
                'name': 'diabetes',
                'file': 'diabetes/diabetes_model.sav',
                'type': 'pickle',
                'preprocessor': None,
                'accuracy': 0.85,
                'description': 'SVC model for diabetes prediction'
            },
            {
                'name': 'asthma',
                'file': 'asthma/model.pkl',
                'alt_file': 'asthama/model.pkl',
                'type': 'joblib',
                'preprocessor': 'asthma/preprocessor.pkl',
                'alt_preprocessor': 'asthama/preprocessor.pkl',
                'accuracy': 0.83,
                'description': 'Random Forest model for asthma prediction'
            },
            {
                'name': 'cardio',
                'file': 'cardio_vascular/xgboost_cardiovascular_model.pkl',
                'type': 'pickle',
                'preprocessor': None,
                'accuracy': 0.78,
                'description': 'XGBoost model for cardiovascular disease'
            },
            {
                'name': 'stroke',
                'file': 'stroke/finalized_model.pkl',
                'type': 'joblib',
                'preprocessor': None,
                'accuracy': 0.80,
                'description': 'Ensemble model for stroke prediction'
            },
            {
                'name': 'hypertension',
                'file': 'hypertension/extratrees_model.pkl',
                'type': 'pickle',
                'preprocessor': 'hypertension/scaler.pkl',
                'accuracy': 0.82,
                'description': 'Extra Trees model for hypertension'
            },
            {
                'name': 'sleep',
                'file': 'sleep_health/svc_model.pkl',
                'type': 'pickle',
                'preprocessor': 'sleep_health/scaler.pkl',
                'encoder': 'sleep_health/label_encoders.pkl',
                'accuracy': 0.76,
                'description': 'SVC model for sleep disorder detection'
            }
        ]
        
        for config in model_configs:
            self._load_model_with_config(config)
        
        logger.info(f"Successfully loaded {len(self.models)} models")
    
    def _load_model_with_config(self, config: Dict):
        """Load a single model with its configuration"""
        try:
            # Load main model
            model_path = os.path.join(self.models_path, config['file'])
            if not os.path.exists(model_path) and 'alt_file' in config:
                model_path = os.path.join(self.models_path, config['alt_file'])
            
            if os.path.exists(model_path):
                if config['type'] == 'pickle':
                    with open(model_path, 'rb') as f:
                        model = pickle.load(f)
                else:
                    model = joblib.load(model_path)
                
                self.models[config['name']] = model
                
                # Load preprocessor if exists
                if config.get('preprocessor'):
                    prep_path = os.path.join(self.models_path, config['preprocessor'])
                    if 'alt_preprocessor' in config and not os.path.exists(prep_path):
                        prep_path = os.path.join(self.models_path, config['alt_preprocessor'])
                    
                    if os.path.exists(prep_path):
                        if config['type'] == 'pickle':
                            with open(prep_path, 'rb') as f:
                                preprocessor = pickle.load(f)
                        else:
                            preprocessor = joblib.load(prep_path)
                        self.preprocessors[config['name']] = preprocessor
                
                # Load encoder if exists
                if config.get('encoder'):
                    encoder_path = os.path.join(self.models_path, config['encoder'])
                    if os.path.exists(encoder_path):
                        with open(encoder_path, 'rb') as f:
                            encoder = pickle.load(f)
                        self.preprocessors[f"{config['name']}_encoder"] = encoder
                
                # Store metadata
                self.model_metadata[config['name']] = {
                    'accuracy': config['accuracy'],
                    'description': config['description'],
                    'loaded_at': datetime.now().isoformat(),
                    'features': self._get_model_features(config['name'])
                }
                
                logger.info(f"✓ Loaded {config['name']} model")
            else:
                logger.warning(f"Model not found: {config['name']}")
                
        except Exception as e:
            logger.error(f"Failed to load {config['name']}: {str(e)}")
    
    def _get_model_features(self, model_name: str) -> List[str]:
        """Get expected features for a model"""
        features_map = {
            'diabetes': ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                        'insulin', 'bmi', 'diabetes_pedigree', 'age'],
            'asthma': ['gender_male', 'smoking_ex', 'smoking_non', 'age', 'peak_flow'],
            'cardio': ['age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'weight'],
            'stroke': ['age', 'hypertension', 'heart_disease', 'ever_married', 'avg_glucose_level', 'bmi', 'smoking_status'],
            'hypertension': ['male', 'age', 'cigsPerDay', 'BPMeds', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        }
        return features_map.get(model_name, [])
    
    def get_model(self, name: str) -> Optional[Any]:
        """Get a loaded model by name"""
        return self.models.get(name)
    
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