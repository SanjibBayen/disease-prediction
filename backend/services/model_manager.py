"""
Model Manager Service - Handles ML model loading, caching, and prediction logic

This module provides centralized management of all machine learning models,
including loading, validation, caching, and metadata tracking.
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path
import logging
from datetime import datetime
from functools import lru_cache
import hashlib
import json

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

class ModelType:
    """Model type constants"""
    PICKLE = "pickle"
    JOBLIB = "joblib"


class ModelStatus:
    """Model loading status"""
    LOADED = "loaded"
    FAILED = "failed"
    NOT_FOUND = "not_found"


# Model configuration with all necessary details
MODEL_CONFIGS = [
    {
        'name': 'diabetes',
        'file': 'diabetes/diabetes_model.sav',
        'alt_files': [],
        'type': ModelType.PICKLE,
        'preprocessor': None,
        'alt_preprocessors': [],
        'encoder': None,
        'accuracy': 0.85,
        'description': 'SVC model for diabetes prediction',
        'version': '1.0',
        'required_features': ['pregnancies', 'glucose', 'blood_pressure', 
                              'skin_thickness', 'insulin', 'bmi', 
                              'diabetes_pedigree', 'age']
    },
    {
        'name': 'asthma',
        'file': 'asthma/model.pkl',
        'alt_files': ['asthama/model.pkl'],
        'type': ModelType.JOBLIB,
        'preprocessor': 'asthma/preprocessor.pkl',
        'alt_preprocessors': ['asthama/preprocessor.pkl'],
        'encoder': None,
        'accuracy': 0.83,
        'description': 'Random Forest model for asthma prediction',
        'version': '1.0',
        'required_features': ['gender_male', 'smoking_ex', 'smoking_non', 'age', 'peak_flow']
    },
    {
        'name': 'cardio',
        'file': 'cardio_vascular/xgboost_cardiovascular_model.pkl',
        'alt_files': [],
        'type': ModelType.PICKLE,
        'preprocessor': None,
        'alt_preprocessors': [],
        'encoder': None,
        'accuracy': 0.78,
        'description': 'XGBoost model for cardiovascular disease',
        'version': '1.0',
        'required_features': ['age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 
                              'smoke', 'alco', 'active', 'weight']
    },
    {
        'name': 'stroke',
        'file': 'stroke/finalized_model.pkl',
        'alt_files': [],
        'type': ModelType.JOBLIB,
        'preprocessor': None,
        'alt_preprocessors': [],
        'encoder': None,
        'accuracy': 0.80,
        'description': 'Ensemble model for stroke prediction',
        'version': '1.0',
        'required_features': ['age', 'hypertension', 'heart_disease', 'ever_married', 
                              'avg_glucose_level', 'bmi', 'smoking_status']
    },
    {
        'name': 'hypertension',
        'file': 'hypertension/extratrees_model.pkl',
        'alt_files': [],
        'type': ModelType.PICKLE,
        'preprocessor': 'hypertension/scaler.pkl',
        'alt_preprocessors': [],
        'encoder': None,
        'accuracy': 0.82,
        'description': 'Extra Trees model for hypertension',
        'version': '1.0',
        'required_features': ['male', 'age', 'cigsPerDay', 'BPMeds', 'totChol', 
                              'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
    },
    {
        'name': 'sleep',
        'file': 'sleep_health/svc_model.pkl',
        'alt_files': [],
        'type': ModelType.PICKLE,
        'preprocessor': 'sleep_health/scaler.pkl',
        'alt_preprocessors': [],
        'encoder': 'sleep_health/label_encoders.pkl',
        'accuracy': 0.76,
        'description': 'SVC model for sleep disorder detection',
        'version': '1.0',
        'required_features': ['gender', 'age', 'occupation', 'sleep_duration', 
                              'quality_of_sleep', 'stress_level', 'bmi_category', 
                              'blood_pressure', 'heart_rate', 'daily_steps']
    },
    {
        'name': 'mental_health',
        'file': 'mental/MentalH.pkl',
        'alt_files': ['mental/mental_health_model.pkl'],
        'type': ModelType.JOBLIB,
        'preprocessor': None,
        'alt_preprocessors': [],
        'encoder': None,
        'accuracy': 0.75,  # Lower accuracy for fallback / ALT 0.82
        'description': 'Mental health assessment (fallback mode - no ML)', #'Transformer-based model for depression and anxiety detection from text'
        'version': '1.0',
        'required_features': ['text']
    },
]


# ============================================================================
# MODEL MANAGER CLASS
# ============================================================================

class ModelManager:
    """
    Centralized model management service
    
    Handles:
    - Loading models from multiple paths
    - Caching loaded models
    - Preprocessor management
    - Model metadata tracking
    - Health checks and validation
    """
    
    def __init__(self, models_path: str = "models", auto_load: bool = True):
        """
        Initialize ModelManager
        
        Args:
            models_path: Path to directory containing model files
            auto_load: Whether to automatically load all models on initialization
        
        Raises:
            ValueError: If models_path is invalid
        """
        if not models_path:
            raise ValueError("models_path cannot be empty")
        
        self.models_path = Path(models_path)
        self.models: Dict[str, Any] = {}
        self.preprocessors: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict] = {}
        self._load_errors: Dict[str, str] = {}
        
        # Create models directory if it doesn't exist
        if not self.models_path.exists():
            logger.warning(f"Models directory not found: {self.models_path}")
            self.models_path.mkdir(parents=True, exist_ok=True)
        
        if auto_load:
            self.load_all_models()
    
    # ============================================================================
    # MENTAL HEALTH PREDICTION METHODS
    # ============================================================================
    
    def predict_mental_health(self, text: str) -> Dict[str, Any]:
        """
        Predict depression and anxiety risk from text
        
        Args:
            text: User's description of mental state
        
        Returns:
            Dictionary with depression_risk, anxiety_risk, and recommendations
        """
        try:
            model = self.models.get('mental_health')
            if model is None:
                logger.warning("Mental health model not loaded, using fallback")
                return self._fallback_mental_health_prediction(text)
            
            # For transformer models, the prediction method may vary
            if hasattr(model, '__call__'):
                result = model(text)
                return self._parse_model_output(result)
            elif hasattr(model, 'predict'):
                result = model.predict([text])
                return self._parse_model_output(result)
            else:
                return self._fallback_mental_health_prediction(text)
                
        except Exception as e:
            logger.error(f"Mental health prediction error: {str(e)}")
            return self._fallback_mental_health_prediction(text)
    
    def _parse_model_output(self, result: Any) -> Dict[str, Any]:
        """
        Parse model output to extract depression and anxiety scores
        
        Args:
            result: Raw model output
        
        Returns:
            Dictionary with parsed scores
        """
        # Format 1: Dictionary with 'depression', 'anxiety' keys
        if isinstance(result, dict):
            depression = result.get('depression', 50.0)
            anxiety = result.get('anxiety', 50.0)
        
        # Format 2: List/tuple with 2 values [depression, anxiety]
        elif isinstance(result, (list, tuple)) and len(result) >= 2:
            depression = float(result[0]) * 100 if result[0] <= 1 else float(result[0])
            anxiety = float(result[1]) * 100 if result[1] <= 1 else float(result[1])
        
        # Format 3: Single value with classification
        else:
            return self._fallback_mental_health_prediction(None)
        
        return {
            'depression_risk': min(100, max(0, depression)),
            'anxiety_risk': min(100, max(0, anxiety))
        }
    
    def _fallback_mental_health_prediction(self, text: str = None) -> Dict[str, Any]:
        """
        Fallback rule-based mental health prediction when ML model unavailable
        
        Args:
            text: User's text (optional)
        
        Returns:
            Dictionary with calculated scores
        """
        depression_score = 50.0
        anxiety_score = 50.0
        
        if text:
            text_lower = text.lower()
            
            # Depression keywords
            depression_keywords = ['hopeless', 'worthless', 'empty', 'sad', 'depressed', 
                                   'no energy', 'fatigue', 'sleep', 'tired', 'lonely',
                                   'cry', 'crying', 'numb', 'dark', 'suicidal', 'death']
            
            # Anxiety keywords
            anxiety_keywords = ['anxious', 'anxiety', 'worry', 'nervous', 'panic', 'scared',
                                'fear', 'overwhelmed', 'stress', 'racing thoughts', 
                                'heart racing', 'sweating', 'restless', 'tense']
            
            # Count keyword matches
            depression_count = sum(1 for word in depression_keywords if word in text_lower)
            anxiety_count = sum(1 for word in anxiety_keywords if word in text_lower)
            
            # Calculate scores (base 50 + 5 per keyword, max 95)
            depression_score = min(95, 50 + (depression_count * 5))
            anxiety_score = min(95, 50 + (anxiety_count * 5))
            
            # Adjust based on text length (more text = more confidence)
            word_count = len(text_lower.split())
            if word_count > 50:
                confidence_boost = min(10, word_count // 10)
                depression_score = min(95, depression_score + confidence_boost)
                anxiety_score = min(95, anxiety_score + confidence_boost)
        
        return {
            'depression_risk': depression_score,
            'anxiety_risk': anxiety_score
        }
    
    # ============================================================================
    # PUBLIC METHODS
    # ============================================================================
    
    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all machine learning models with metadata
        
        Returns:
            Dictionary with model names and loading success status
        """
        results = {}
        
        for config in MODEL_CONFIGS:
            success = self._load_model_with_config(config)
            results[config['name']] = success
        
        loaded_count = len(self.models)
        logger.info(f"Model loading complete: {loaded_count}/{len(MODEL_CONFIGS)} models loaded")
        
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
            logger.error(f"Cannot reload: Model '{model_name}' not found in configuration")
            return False
        
        # Remove existing model if present
        if model_name in self.models:
            del self.models[model_name]
        if model_name in self.preprocessors:
            del self.preprocessors[model_name]
        if model_name in self.model_metadata:
            del self.model_metadata[model_name]
        
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
        """
        Get a preprocessor by name
        
        Args:
            name: Preprocessor name (model name or specific preprocessor key)
        
        Returns:
            Preprocessor object or None if not found
        """
        return self.preprocessors.get(name)
    
    def get_model_info(self, name: str) -> Optional[Dict]:
        """
        Get model metadata
        
        Args:
            name: Model name
        
        Returns:
            Dictionary with model metadata or None
        """
        return self.model_metadata.get(name)
    
    def list_models(self) -> List[str]:
        """
        List all loaded model names
        
        Returns:
            List of loaded model names
        """
        return list(self.models.keys())
    
    def list_available_models(self) -> List[Dict]:
        """
        List all configured models with their status
        
        Returns:
            List of dictionaries with model information
        """
        available = []
        for config in MODEL_CONFIGS:
            available.append({
                'name': config['name'],
                'description': config['description'],
                'accuracy': config['accuracy'],
                'is_loaded': config['name'] in self.models,
                'version': config.get('version', 'unknown')
            })
        return available
    
    def is_model_loaded(self, name: str) -> bool:
        """
        Check if a specific model is loaded
        
        Args:
            name: Model name
        
        Returns:
            True if model is loaded, False otherwise
        """
        return name in self.models
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Get comprehensive model status
        
        Returns:
            Dictionary with model status information
        """
        return {
            'total_models': len(MODEL_CONFIGS),
            'loaded_models': len(self.models),
            'models': self.list_available_models(),
            'load_errors': self._load_errors,
            'models_path': str(self.models_path),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def validate_model(self, name: str, sample_input: Dict) -> Tuple[bool, str]:
        """
        Validate that a model can make predictions
        
        Args:
            name: Model name
            sample_input: Sample input data for testing
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        model = self.get_model(name)
        if model is None:
            return False, f"Model '{name}' not loaded"
        
        config = self._find_model_config(name)
        if config is None:
            return False, f"No configuration found for '{name}'"
        
        # Check required features
        missing_features = [f for f in config['required_features'] if f not in sample_input]
        if missing_features:
            return False, f"Missing required features: {missing_features}"
        
        try:
            # Try to make a prediction with sample data
            features = np.array([[sample_input[f] for f in config['required_features']]])
            model.predict(features)
            return True, "Model validation successful"
        except Exception as e:
            return False, f"Model prediction failed: {str(e)}"
    
    def get_model_hash(self, name: str) -> Optional[str]:
        """
        Get MD5 hash of model file for integrity checking
        
        Args:
            name: Model name
        
        Returns:
            MD5 hash string or None if model not found
        """
        config = self._find_model_config(name)
        if config is None:
            return None
        
        file_path = self._find_model_file(config)
        if file_path is None or not file_path.exists():
            return None
        
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to hash model {name}: {e}")
            return None
    
    # ============================================================================
    # PRIVATE METHODS
    # ============================================================================
    
    def _find_model_config(self, model_name: str) -> Optional[Dict]:
        """Find model configuration by name"""
        for config in MODEL_CONFIGS:
            if config['name'] == model_name:
                return config
        return None
    
    def _find_model_file(self, config: Dict) -> Optional[Path]:
        """Find existing model file from configured paths"""
        # Try main file
        main_path = self.models_path / config['file']
        if main_path.exists():
            return main_path
        
        # Try alternative files
        for alt_file in config.get('alt_files', []):
            alt_path = self.models_path / alt_file
            if alt_path.exists():
                return alt_path
        
        return None
    
    def _find_preprocessor_file(self, config: Dict, preprocessor_key: str) -> Optional[Path]:
        """Find existing preprocessor file"""
        # Try main preprocessor
        if config.get(preprocessor_key):
            main_path = self.models_path / config[preprocessor_key]
            if main_path.exists():
                return main_path
        
        # Try alternative preprocessors
        alt_key = f'alt_{preprocessor_key}'
        for alt_file in config.get(alt_key, []):
            alt_path = self.models_path / alt_file
            if alt_path.exists():
                return alt_path
        
        return None
    
    def _load_model_with_config(self, config: Dict) -> bool:
        """
        Load a single model with its configuration
        
        Args:
            config: Model configuration dictionary
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        name = config['name']
        
        try:
            # Find and load model file
            model_path = self._find_model_file(config)
            if model_path is None:
                self._load_errors[name] = f"Model file not found: {config['file']}"
                logger.warning(f"Model '{name}' not found at any configured path")
                return False
            
            # Load model based on type
            model = self._load_file(model_path, config['type'])
            if model is None:
                self._load_errors[name] = f"Failed to load model from {model_path}"
                return False
            
            self.models[name] = model
            logger.info(f"✓ Loaded {name} model from {model_path}")
            
            # Load preprocessor if exists
            if config.get('preprocessor'):
                prep_path = self._find_preprocessor_file(config, 'preprocessor')
                if prep_path and prep_path.exists():
                    preprocessor = self._load_file(prep_path, config['type'])
                    if preprocessor is not None:
                        self.preprocessors[name] = preprocessor
                        logger.info(f"  ✓ Loaded preprocessor for {name}")
            
            # Load encoder if exists
            if config.get('encoder'):
                encoder_path = self.models_path / config['encoder']
                if encoder_path.exists():
                    encoder = self._load_file(encoder_path, ModelType.PICKLE)
                    if encoder is not None:
                        self.preprocessors[f"{name}_encoder"] = encoder
                        logger.info(f"  ✓ Loaded encoder for {name}")
            
            # Store metadata
            self.model_metadata[name] = {
                'accuracy': config['accuracy'],
                'description': config['description'],
                'loaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'model_path': str(model_path),
                'model_type': config['type'],
                'version': config.get('version', 'unknown'),
                'features': config.get('required_features', []),
                'file_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2)
            }
            
            return True
            
        except Exception as e:
            self._load_errors[name] = str(e)
            logger.error(f"Failed to load {name}: {str(e)}", exc_info=True)
            return False
    
    def _load_file(self, file_path: Path, file_type: str) -> Optional[Any]:
        """
        Load a file using pickle or joblib
        
        Args:
            file_path: Path to the file
            file_type: Either 'pickle' or 'joblib'
        
        Returns:
            Loaded object or None if failed
        """
        try:
            if file_type == ModelType.PICKLE:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            elif file_type == ModelType.JOBLIB:
                return joblib.load(file_path)
            else:
                raise ValueError(f"Unknown file type: {file_type}")
        except (pickle.PickleError, EOFError, ValueError) as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return None
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def get_model_summary(self) -> str:
        """
        Get a human-readable summary of loaded models
        
        Returns:
            Formatted string with model information
        """
        summary_lines = [
            "=" * 60,
            "Model Manager Summary",
            "=" * 60,
            f"Models Directory: {self.models_path}",
            f"Total Models Configured: {len(MODEL_CONFIGS)}",
            f"Models Loaded: {len(self.models)}",
            "",
            "Loaded Models:"
        ]
        
        for name in self.models.keys():
            metadata = self.model_metadata.get(name, {})
            accuracy = metadata.get('accuracy', 'unknown')
            loaded_at = metadata.get('loaded_at', 'unknown')[:19]
            summary_lines.append(f"  ✓ {name} (accuracy: {accuracy}, loaded: {loaded_at})")
        
        if self._load_errors:
            summary_lines.append("")
            summary_lines.append("Loading Errors:")
            for name, error in self._load_errors.items():
                summary_lines.append(f"  ✗ {name}: {error}")
        
        summary_lines.append("=" * 60)
        
        return "\n".join(summary_lines)
    
    def save_model_status(self, output_path: str) -> bool:
        """
        Save model status to JSON file
        
        Args:
            output_path: Path to save the status file
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            status = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'models_path': str(self.models_path),
                'total_models': len(MODEL_CONFIGS),
                'loaded_models': len(self.models),
                'models': self.list_available_models(),
                'load_errors': self._load_errors,
                'model_metadata': self.model_metadata
            }
            
            with open(output_path, 'w') as f:
                json.dump(status, f, indent=2, default=str)
            
            logger.info(f"Model status saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model status: {e}")
            return False


# ============================================================================
# SINGLETON INSTANCE AND CONVENIENCE FUNCTIONS
# ============================================================================

# Singleton instance
_model_manager_instance = None

def get_model_manager(models_path: str = "models") -> ModelManager:
    """
    Get or create the singleton ModelManager instance
    
    This is useful for avoiding duplicate model loading across the application.
    
    Args:
        models_path: Path to models directory
    
    Returns:
        Singleton ModelManager instance
    """
    global _model_manager_instance
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager(models_path=models_path)
    return _model_manager_instance


def create_model_manager(models_path: str = "models", auto_load: bool = True) -> ModelManager:
    """
    Factory function to create a ModelManager instance
    
    Args:
        models_path: Path to models directory
        auto_load: Whether to load models automatically
    
    Returns:
        Configured ModelManager instance
    """
    return ModelManager(models_path=models_path, auto_load=auto_load)


# ============================================================================
# MAIN EXECUTION (for testing)
# ============================================================================

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    # Test model manager
    print("\n" + "=" * 60)
    print("Testing Model Manager")
    print("=" * 60 + "\n")
    
    # Create manager
    manager = ModelManager(models_path="models", auto_load=True)
    
    # Print summary
    print(manager.get_model_summary())
    
    # Test individual model access
    print("\nTesting model access:")
    for model_name in manager.list_models():
        model = manager.get_model(model_name)
        info = manager.get_model_info(model_name)
        print(f"  {model_name}: {type(model).__name__}, accuracy: {info.get('accuracy', 'unknown')}")
    
    # Test status
    status = manager.get_model_status()
    print(f"\nStatus: {status['loaded_models']}/{status['total_models']} models loaded")