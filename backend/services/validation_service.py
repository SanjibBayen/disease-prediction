"""
Validation Service - Handles input validation and sanitization

This module provides comprehensive validation for all disease prediction inputs,
including range checks, type validation, and business rule validation.
"""

from typing import Dict, Any, List, Tuple, Optional, Union
import re
from datetime import datetime
import pytz
import logging
import math

# Try to import numpy, but don't fail if not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Create dummy np for compatibility
    class DummyNP:
        @staticmethod
        def isnan(x):
            return False
        @staticmethod
        def isinf(x):
            return False
    np = DummyNP()
    HAS_NUMPY = False

logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

class ValidationRanges:
    """Validation ranges for all input fields"""
    
    # Diabetes ranges
    DIABETES = {
        'pregnancies': (0, 20),
        'glucose': (0, 300),
        'blood_pressure': (0, 200),
        'skin_thickness': (0, 100),
        'insulin': (0, 900),
        'bmi': (0, 70),
        'diabetes_pedigree': (0, 2.5),
        'age': (1, 120)
    }
    
    # Asthma ranges
    ASTHMA = {
        'gender_male': (0, 1),
        'smoking_ex': (0, 1),
        'smoking_non': (0, 1),
        'age': (0, 1),
        'peak_flow': (0.1, 1)
    }
    
    # Cardiovascular ranges
    CARDIO = {
        'age': (29, 65),
        'ap_hi': (90, 200),
        'ap_lo': (60, 140),
        'cholesterol': (1, 3),
        'gluc': (1, 3),
        'smoke': (0, 1),
        'alco': (0, 1),
        'active': (0, 1),
        'weight': (30, 200)
    }
    
    # Stroke ranges
    STROKE = {
        'age': (0, 82),
        'hypertension': (0, 1),
        'heart_disease': (0, 1),
        'ever_married': (0, 1),
        'avg_glucose_level': (55, 270),
        'bmi': (13.5, 98),
        'smoking_status': (0, 3)
    }
    
    # Hypertension ranges
    HYPERTENSION = {
        'male': (0, 1),
        'age': (32, 70),
        'cigsPerDay': (0, 70),
        'BPMeds': (0, 1),
        'totChol': (107, 500),
        'sysBP': (83.5, 295),
        'diaBP': (48, 142.5),
        'BMI': (15.54, 56.8),
        'heartRate': (44, 143),
        'glucose': (40, 394)
    }


class ValidationMessages:
    """Validation error messages"""
    MISSING_FIELD = "Missing required field: {field}"
    OUT_OF_RANGE = "{field} must be between {min} and {max}, got {value}"
    INVALID_BINARY = "{field} must be 0 or 1, got {value}"
    INVALID_CHOICE = "{field} must be one of {choices}, got {value}"
    INVALID_BP_RELATION = "Systolic BP ({systolic}) must be greater than diastolic BP ({diastolic})"
    INVALID_SMOKING = "Exactly one of smoking_ex or smoking_non must be 1"
    INVALID_NUMERIC = "{field} must be a number, got {value}"
    INVALID_EMAIL = "Invalid email format"
    INVALID_PHONE = "Invalid phone number format"


# ============================================================================
# VALIDATION SERVICE
# ============================================================================

class ValidationService:
    """
    Service for validating input data for all disease predictions
    
    This class provides static methods for validating input data for
    diabetes, asthma, cardiovascular, stroke, and hypertension predictions.
    """
    
    @staticmethod
    def validate_diabetes_input(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate diabetes prediction input
        
        Args:
            data: Dictionary containing diabetes prediction parameters
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        
        Example:
            >>> valid, errors = ValidationService.validate_diabetes_input({
            ...     'pregnancies': 1,
            ...     'glucose': 120,
            ...     'blood_pressure': 80,
            ...     ...
            ... })
        """
        errors = []
        
        # Required fields check
        required_fields = list(ValidationRanges.DIABETES.keys())
        errors.extend(ValidationService._check_required_fields(data, required_fields))
        
        # Range validations
        for field, (min_val, max_val) in ValidationRanges.DIABETES.items():
            if field in data:
                error = ValidationService._validate_range(
                    data[field], min_val, max_val, field
                )
                if error:
                    errors.append(error)
        
        # Additional business logic validations
        if 'glucose' in data and data['glucose'] is not None:
            glucose = data['glucose']
            if 0 < glucose < 50:
                errors.append(f"Glucose value {glucose} mg/dL is unusually low. Please verify.")
            if glucose > 250:
                errors.append(f"Glucose value {glucose} mg/dL is very high. Please verify.")
        
        if 'bmi' in data and data['bmi'] is not None:
            bmi = data['bmi']
            if bmi < 15:
                errors.append(f"BMI {bmi} is severely underweight. Please verify.")
            if bmi > 50:
                errors.append(f"BMI {bmi} is extremely high. Please verify.")
        
        if 'age' in data and data['age'] is not None and data['age'] < 18:
            errors.append(f"Age {data['age']} is below 18. This model is designed for adults.")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_asthma_input(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate asthma prediction input
        
        Args:
            data: Dictionary containing asthma prediction parameters
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields check
        required_fields = list(ValidationRanges.ASTHMA.keys())
        errors.extend(ValidationService._check_required_fields(data, required_fields))
        
        # Range validations
        for field, (min_val, max_val) in ValidationRanges.ASTHMA.items():
            if field in data:
                error = ValidationService._validate_range(
                    data[field], min_val, max_val, field
                )
                if error:
                    errors.append(error)
        
        # Binary field validations
        binary_fields = ['gender_male', 'smoking_ex', 'smoking_non']
        for field in binary_fields:
            if field in data and data[field] is not None:
                if data[field] not in [0, 1]:
                    errors.append(ValidationMessages.INVALID_BINARY.format(
                        field=field, value=data[field]
                    ))
        
        # Smoking status consistency check
        if 'smoking_ex' in data and 'smoking_non' in data:
            smoking_ex = data.get('smoking_ex', 0)
            smoking_non = data.get('smoking_non', 1)
            if smoking_ex + smoking_non != 1:
                errors.append(ValidationMessages.INVALID_SMOKING)
        
        # Peak flow additional validation
        if 'peak_flow' in data and data['peak_flow'] is not None:
            peak_flow = data['peak_flow']
            if peak_flow < 0.2:
                errors.append(f"Peak flow {peak_flow} L/sec is very low. Please verify.")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_cardio_input(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate cardiovascular prediction input
        
        Args:
            data: Dictionary containing cardiovascular prediction parameters
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields check
        required_fields = list(ValidationRanges.CARDIO.keys())
        errors.extend(ValidationService._check_required_fields(data, required_fields))
        
        # Range validations
        for field, (min_val, max_val) in ValidationRanges.CARDIO.items():
            if field in data:
                error = ValidationService._validate_range(
                    data[field], min_val, max_val, field
                )
                if error:
                    errors.append(error)
        
        # Binary field validations
        binary_fields = ['smoke', 'alco', 'active']
        for field in binary_fields:
            if field in data and data[field] is not None:
                if data[field] not in [0, 1]:
                    errors.append(ValidationMessages.INVALID_BINARY.format(
                        field=field, value=data[field]
                    ))
        
        # Blood pressure relationship
        if 'ap_hi' in data and 'ap_lo' in data:
            systolic = data['ap_hi']
            diastolic = data['ap_lo']
            if systolic is not None and diastolic is not None:
                if systolic <= diastolic:
                    errors.append(ValidationMessages.INVALID_BP_RELATION.format(
                        systolic=systolic, diastolic=diastolic
                    ))
                
                # Pulse pressure validation
                pulse_pressure = systolic - diastolic
                if pulse_pressure < 20:
                    errors.append(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally low")
                if pulse_pressure > 100:
                    errors.append(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally high")
        
        # Cholesterol and glucose level validations
        for field in ['cholesterol', 'gluc']:
            if field in data and data[field] is not None:
                if data[field] not in [1, 2, 3]:
                    errors.append(ValidationMessages.INVALID_CHOICE.format(
                        field=field, choices=[1, 2, 3], value=data[field]
                    ))
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_stroke_input(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate stroke prediction input
        
        Args:
            data: Dictionary containing stroke prediction parameters
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields check
        required_fields = list(ValidationRanges.STROKE.keys())
        errors.extend(ValidationService._check_required_fields(data, required_fields))
        
        # Range validations
        for field, (min_val, max_val) in ValidationRanges.STROKE.items():
            if field in data:
                error = ValidationService._validate_range(
                    data[field], min_val, max_val, field
                )
                if error:
                    errors.append(error)
        
        # Binary field validations
        binary_fields = ['hypertension', 'heart_disease', 'ever_married']
        for field in binary_fields:
            if field in data and data[field] is not None:
                if data[field] not in [0, 1]:
                    errors.append(ValidationMessages.INVALID_BINARY.format(
                        field=field, value=data[field]
                    ))
        
        # Smoking status validation
        if 'smoking_status' in data and data['smoking_status'] is not None:
            if data['smoking_status'] not in [0, 1, 2, 3]:
                errors.append(ValidationMessages.INVALID_CHOICE.format(
                    field='smoking_status', choices=[0, 1, 2, 3], value=data['smoking_status']
                ))
        
        # Additional validations
        if 'avg_glucose_level' in data and data['avg_glucose_level'] is not None:
            glucose = data['avg_glucose_level']
            if glucose < 70:
                errors.append(f"Glucose level {glucose} mg/dL is very low. Please verify.")
            if glucose > 200:
                errors.append(f"Glucose level {glucose} mg/dL is very high. Please verify.")
        
        if 'bmi' in data and data['bmi'] is not None:
            bmi = data['bmi']
            if bmi < 16:
                errors.append(f"BMI {bmi} is severely underweight. Please verify.")
            if bmi > 40:
                errors.append(f"BMI {bmi} is very high. Please verify.")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_hypertension_input(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate hypertension prediction input
        
        Args:
            data: Dictionary containing hypertension prediction parameters
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields check
        required_fields = list(ValidationRanges.HYPERTENSION.keys())
        errors.extend(ValidationService._check_required_fields(data, required_fields))
        
        # Range validations
        for field, (min_val, max_val) in ValidationRanges.HYPERTENSION.items():
            if field in data:
                error = ValidationService._validate_range(
                    data[field], min_val, max_val, field
                )
                if error:
                    errors.append(error)
        
        # Binary field validations
        binary_fields = ['male', 'BPMeds']
        for field in binary_fields:
            if field in data and data[field] is not None:
                if data[field] not in [0, 1]:
                    errors.append(ValidationMessages.INVALID_BINARY.format(
                        field=field, value=data[field]
                    ))
        
        # Blood pressure relationship
        if 'sysBP' in data and 'diaBP' in data:
            systolic = data['sysBP']
            diastolic = data['diaBP']
            if systolic is not None and diastolic is not None:
                if systolic <= diastolic:
                    errors.append(ValidationMessages.INVALID_BP_RELATION.format(
                        systolic=systolic, diastolic=diastolic
                    ))
                
                pulse_pressure = systolic - diastolic
                if pulse_pressure < 20:
                    errors.append(f"Pulse pressure ({pulse_pressure} mmHg) is abnormally low")
        
        # Cigarettes validation
        if 'cigsPerDay' in data and data['cigsPerDay'] is not None:
            cigs = data['cigsPerDay']
            if cigs > 40:
                errors.append(f"Cigarettes per day ({cigs}) is very high. Please verify.")
        
        # Heart rate validation
        if 'heartRate' in data and data['heartRate'] is not None:
            hr = data['heartRate']
            if hr < 50:
                errors.append(f"Heart rate {hr} bpm is very low (bradycardia). Please verify.")
            if hr > 120:
                errors.append(f"Heart rate {hr} bpm is very high (tachycardia). Please verify.")
        
        return len(errors) == 0, errors
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    @staticmethod
    def _check_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
        """
        Check for missing required fields
        
        Args:
            data: Input dictionary
            required_fields: List of required field names
        
        Returns:
            List of error messages for missing fields
        """
        errors = []
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(ValidationMessages.MISSING_FIELD.format(field=field))
        return errors
    
    @staticmethod
    def _validate_range(value: Any, min_val: Union[int, float], 
                        max_val: Union[int, float], field_name: str) -> Optional[str]:
        """
        Validate that a value is within a specified range
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            field_name: Name of the field for error message
        
        Returns:
            Error message if validation fails, None otherwise
        """
        # Check if value is numeric
        if not isinstance(value, (int, float)):
            try:
                value = float(value)
            except (ValueError, TypeError):
                return ValidationMessages.INVALID_NUMERIC.format(field=field_name, value=value)
        
        # Check if value is within range
        if value < min_val or value > max_val:
            return ValidationMessages.OUT_OF_RANGE.format(
                field=field_name, min=min_val, max=max_val, value=value
            )
        
        return None
    
    @staticmethod
    def sanitize_input(data: Dict) -> Dict:
        """
        Sanitize input data by cleaning values
        
        Args:
            data: Input dictionary to sanitize
        
        Returns:
            Sanitized dictionary
        """
        if not data:
            return {}
        
        sanitized = {}
        
        for key, value in data.items():
            if value is None:
                sanitized[key] = None
            elif isinstance(value, str):
                # Remove extra whitespace
                value = value.strip()
                # Remove special characters if needed (keep basic punctuation)
                value = re.sub(r'[^\w\s\-\.]', '', value)
                # Convert empty strings to None
                if value == "":
                    value = None
                sanitized[key] = value
            elif isinstance(value, (int, float)):
                # Handle NaN and Infinity
                if HAS_NUMPY and (np.isnan(value) or np.isinf(value)):
                    sanitized[key] = 0.0
                else:
                    sanitized[key] = value
            elif isinstance(value, bool):
                sanitized[key] = 1 if value else 0
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not phone or not isinstance(phone, str):
            return False
        
        # Supports various international formats
        pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{3,4}$'
        return bool(re.match(pattern, phone.strip()))
    
    @staticmethod
    def validate_numeric(value: Any, allow_zero: bool = True, 
                         allow_negative: bool = False) -> Tuple[bool, Optional[float]]:
        """
        Validate and convert value to numeric
        
        Args:
            value: Value to validate
            allow_zero: Whether zero is allowed
            allow_negative: Whether negative values are allowed
        
        Returns:
            Tuple of (is_valid, numeric_value or error_message)
        """
        try:
            num = float(value)
            
            if not allow_zero and num == 0:
                return False, "Zero value is not allowed"
            
            if not allow_negative and num < 0:
                return False, "Negative values are not allowed"
            
            return True, num
        except (ValueError, TypeError):
            return False, ValidationMessages.INVALID_NUMERIC.format(field="value", value=value)
    
    @staticmethod
    def validate_choice(value: Any, choices: List[Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate if value is in allowed choices
        
        Args:
            value: Value to validate
            choices: List of allowed choices
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value in choices:
            return True, None
        
        return False, ValidationMessages.INVALID_CHOICE.format(
            field="value", choices=choices, value=value
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_input(disease_type: str, data: Dict) -> Tuple[bool, List[str]]:
    """
    Convenience function to validate input for any disease
    
    Args:
        disease_type: Type of disease ('diabetes', 'asthma', 'cardio', 'stroke', 'hypertension')
        data: Input data dictionary
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validators = {
        'diabetes': ValidationService.validate_diabetes_input,
        'asthma': ValidationService.validate_asthma_input,
        'cardio': ValidationService.validate_cardio_input,
        'stroke': ValidationService.validate_stroke_input,
        'hypertension': ValidationService.validate_hypertension_input
    }
    
    validator = validators.get(disease_type.lower())
    if validator is None:
        return False, [f"Unknown disease type: {disease_type}"]
    
    return validator(data)


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    print("Testing Validation Service...")
    print("=" * 60)
    
    # Test diabetes validation
    print("\n1. Testing Diabetes Validation:")
    test_data = {
        'pregnancies': 1,
        'glucose': 120,
        'blood_pressure': 80,
        'skin_thickness': 20,
        'insulin': 79,
        'bmi': 25.5,
        'diabetes_pedigree': 0.5,
        'age': 35
    }
    
    valid, errors = ValidationService.validate_diabetes_input(test_data)
    print(f"  Valid: {valid}")
    if errors:
        print(f"  Errors: {errors}")
    
    # Test with invalid data
    print("\n2. Testing Invalid Diabetes Data:")
    invalid_data = {
        'pregnancies': -1,
        'glucose': 500,
        'age': 15
    }
    
    valid, errors = ValidationService.validate_diabetes_input(invalid_data)
    print(f"  Valid: {valid}")
    print(f"  Errors: {errors}")
    
    # Test sanitization
    print("\n3. Testing Input Sanitization:")
    dirty_data = {
        'name': '  John Doe  ',
        'email': 'test@example.com',
        'value': float('nan')
    }
    
    cleaned = ValidationService.sanitize_input(dirty_data)
    print(f"  Original: {dirty_data}")
    print(f"  Cleaned: {cleaned}")
    
    print("\n" + "=" * 60)
    print("Validation Service Test Complete!")