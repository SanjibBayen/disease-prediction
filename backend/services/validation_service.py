"""
Validation Service - Handles input validation and sanitization
"""

from typing import Dict, Any, List, Tuple, Optional
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    """Service for validating input data"""
    
    @staticmethod
    def validate_diabetes_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate diabetes prediction input"""
        errors = []
        
        # Required fields
        required_fields = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                          'insulin', 'bmi', 'diabetes_pedigree', 'age']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Range validations
        ranges = {
            'pregnancies': (0, 20),
            'glucose': (0, 300),
            'blood_pressure': (0, 200),
            'skin_thickness': (0, 100),
            'insulin': (0, 900),
            'bmi': (0, 70),
            'diabetes_pedigree': (0, 2.5),
            'age': (1, 120)
        }
        
        for field, (min_val, max_val) in ranges.items():
            if field in data:
                value = data[field]
                if value < min_val or value > max_val:
                    errors.append(f"{field} must be between {min_val} and {max_val}, got {value}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_asthma_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate asthma prediction input"""
        errors = []
        
        required_fields = ['gender_male', 'smoking_ex', 'smoking_non', 'age', 'peak_flow']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Gender validation
        if 'gender_male' in data and data['gender_male'] not in [0, 1]:
            errors.append("gender_male must be 0 or 1")
        
        # Smoking status validation
        if 'smoking_ex' in data and data['smoking_ex'] not in [0, 1]:
            errors.append("smoking_ex must be 0 or 1")
        
        if 'smoking_non' in data and data['smoking_non'] not in [0, 1]:
            errors.append("smoking_non must be 0 or 1")
        
        # Age validation (normalized)
        if 'age' in data and (data['age'] < 0 or data['age'] > 1):
            errors.append("age must be between 0 and 1 (normalized)")
        
        # Peak flow validation
        if 'peak_flow' in data and (data['peak_flow'] < 0.1 or data['peak_flow'] > 1):
            errors.append("peak_flow must be between 0.1 and 1.0")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_cardio_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate cardiovascular prediction input"""
        errors = []
        
        required_fields = ['age', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'weight']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Age validation
        if 'age' in data and (data['age'] < 29 or data['age'] > 65):
            errors.append("age must be between 29 and 65")
        
        # Blood pressure validation
        if 'ap_hi' in data and (data['ap_hi'] < 90 or data['ap_hi'] > 200):
            errors.append("systolic BP must be between 90 and 200")
        
        if 'ap_lo' in data and (data['ap_lo'] < 60 or data['ap_lo'] > 140):
            errors.append("diastolic BP must be between 60 and 140")
        
        # BP relationship
        if 'ap_hi' in data and 'ap_lo' in data and data['ap_hi'] <= data['ap_lo']:
            errors.append("systolic BP must be greater than diastolic BP")
        
        # Cholesterol validation
        if 'cholesterol' in data and data['cholesterol'] not in [1, 2, 3]:
            errors.append("cholesterol must be 1, 2, or 3")
        
        # Glucose validation
        if 'gluc' in data and data['gluc'] not in [1, 2, 3]:
            errors.append("glucose must be 1, 2, or 3")
        
        # Binary fields validation
        binary_fields = ['smoke', 'alco', 'active']
        for field in binary_fields:
            if field in data and data[field] not in [0, 1]:
                errors.append(f"{field} must be 0 or 1")
        
        # Weight validation
        if 'weight' in data and (data['weight'] < 30 or data['weight'] > 200):
            errors.append("weight must be between 30 and 200 kg")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_stroke_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate stroke prediction input"""
        errors = []
        
        required_fields = ['age', 'hypertension', 'heart_disease', 'ever_married', 
                          'avg_glucose_level', 'bmi', 'smoking_status']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Age validation
        if 'age' in data and (data['age'] < 0 or data['age'] > 82):
            errors.append("age must be between 0 and 82")
        
        # Binary fields validation
        binary_fields = ['hypertension', 'heart_disease', 'ever_married']
        for field in binary_fields:
            if field in data and data[field] not in [0, 1]:
                errors.append(f"{field} must be 0 or 1")
        
        # Glucose validation
        if 'avg_glucose_level' in data and (data['avg_glucose_level'] < 55 or data['avg_glucose_level'] > 270):
            errors.append("glucose level must be between 55 and 270")
        
        # BMI validation
        if 'bmi' in data and (data['bmi'] < 13.5 or data['bmi'] > 98):
            errors.append("BMI must be between 13.5 and 98")
        
        # Smoking status validation
        if 'smoking_status' in data and data['smoking_status'] not in [0, 1, 2, 3]:
            errors.append("smoking_status must be 0, 1, 2, or 3")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_hypertension_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate hypertension prediction input"""
        errors = []
        
        required_fields = ['male', 'age', 'cigsPerDay', 'BPMeds', 'totChol', 
                          'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Gender validation
        if 'male' in data and data['male'] not in [0, 1]:
            errors.append("male must be 0 or 1")
        
        # Age validation
        if 'age' in data and (data['age'] < 32 or data['age'] > 70):
            errors.append("age must be between 32 and 70")
        
        # Cigarettes validation
        if 'cigsPerDay' in data and (data['cigsPerDay'] < 0 or data['cigsPerDay'] > 70):
            errors.append("cigarettes per day must be between 0 and 70")
        
        # BP medication validation
        if 'BPMeds' in data and data['BPMeds'] not in [0, 1]:
            errors.append("BPMeds must be 0 or 1")
        
        # Cholesterol validation
        if 'totChol' in data and (data['totChol'] < 107 or data['totChol'] > 500):
            errors.append("total cholesterol must be between 107 and 500")
        
        # Blood pressure validation
        if 'sysBP' in data and (data['sysBP'] < 83.5 or data['sysBP'] > 295):
            errors.append("systolic BP must be between 83.5 and 295")
        
        if 'diaBP' in data and (data['diaBP'] < 48 or data['diaBP'] > 142.5):
            errors.append("diastolic BP must be between 48 and 142.5")
        
        # BMI validation
        if 'BMI' in data and (data['BMI'] < 15.54 or data['BMI'] > 56.8):
            errors.append("BMI must be between 15.54 and 56.8")
        
        # Heart rate validation
        if 'heartRate' in data and (data['heartRate'] < 44 or data['heartRate'] > 143):
            errors.append("heart rate must be between 44 and 143")
        
        # Glucose validation
        if 'glucose' in data and (data['glucose'] < 40 or data['glucose'] > 394):
            errors.append("glucose must be between 40 and 394")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(data: Dict) -> Dict:
        """Sanitize input data by removing special characters and trimming"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Remove extra whitespace
                value = value.strip()
                # Remove special characters if needed
                value = re.sub(r'[^\w\s\-\.]', '', value)
            elif isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                value = 0.0
            
            sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{3,4}$'
        return bool(re.match(pattern, phone))