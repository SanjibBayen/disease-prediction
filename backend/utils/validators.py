"""
Validation utility functions

This module provides comprehensive validation functions for various data types
used throughout the HealthPredict AI system. Includes email, phone, medical
parameters, and general validation utilities.
"""

import re
from typing import Any, Optional, Tuple, Union, List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

class ValidationConstants:
    """Constants for validation ranges and patterns"""
    
    # Age ranges
    MIN_AGE = 0
    MAX_AGE = 120
    MIN_ADULT_AGE = 18
    MAX_ADULT_AGE = 100
    
    # BMI ranges
    MIN_BMI = 10
    MAX_BMI = 60
    UNDERWEIGHT_BMI = 18.5
    NORMAL_BMI_MAX = 24.9
    OVERWEIGHT_BMI_MAX = 29.9
    
    # Blood pressure ranges
    MIN_SYSTOLIC = 70
    MAX_SYSTOLIC = 220
    MIN_DIASTOLIC = 40
    MAX_DIASTOLIC = 130
    NORMAL_SYSTOLIC_MAX = 120
    NORMAL_DIASTOLIC_MAX = 80
    HYPERTENSION_SYSTOLIC = 140
    HYPERTENSION_DIASTOLIC = 90
    
    # Heart rate ranges
    MIN_HEART_RATE = 40
    MAX_HEART_RATE = 150
    RESTING_HEART_RATE_MIN = 60
    RESTING_HEART_RATE_MAX = 100
    
    # Glucose ranges
    MIN_GLUCOSE = 40
    MAX_GLUCOSE = 400
    NORMAL_GLUCOSE_MAX = 99
    PREDIABETES_GLUCOSE_MAX = 125
    
    # Cholesterol ranges (mg/dL)
    MIN_CHOLESTEROL = 100
    MAX_CHOLESTEROL = 500
    DESIRABLE_CHOLESTEROL_MAX = 200
    BORDERLINE_CHOLESTEROL_MAX = 239
    
    # Other ranges
    MIN_HEIGHT_CM = 50
    MAX_HEIGHT_CM = 250
    MIN_WEIGHT_KG = 10
    MAX_WEIGHT_KG = 300


class ValidationMessages:
    """Validation error messages"""
    INVALID_EMAIL = "Invalid email format"
    INVALID_PHONE = "Invalid phone number format"
    INVALID_AGE = "Age must be between {min} and {max}"
    INVALID_BMI = "BMI must be between {min} and {max}"
    INVALID_BP = "Invalid blood pressure: systolic={systolic}, diastolic={diastolic}"
    INVALID_HEART_RATE = "Heart rate must be between {min} and {max}"
    INVALID_GLUCOSE = "Glucose level must be between {min} and {max}"
    INVALID_RANGE = "Value must be between {min} and {max}"
    INVALID_CHOICE = "Value must be one of: {choices}"
    REQUIRED_FIELD = "Required field '{field}' is missing"
    INVALID_NUMERIC = "Value must be numeric"
    INVALID_STRING = "Value must be a non-empty string"
    INVALID_DATE = "Invalid date format. Use YYYY-MM-DD"


# ============================================================================
# STRING VALIDATORS
# ============================================================================

def is_valid_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if email format is valid, False otherwise
    
    Examples:
        >>> is_valid_email("user@example.com")
        True
        >>> is_valid_email("invalid-email")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format (international)
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if phone format is valid, False otherwise
    
    Examples:
        >>> is_valid_phone("+1-555-123-4567")
        True
        >>> is_valid_phone("12345")
        False
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Supports various international formats
    pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{3,4}$'
    return bool(re.match(pattern, phone.strip()))


def is_valid_username(username: str, min_length: int = 3, max_length: int = 50) -> bool:
    """
    Validate username format
    
    Args:
        username: Username to validate
        min_length: Minimum length
        max_length: Maximum length
    
    Returns:
        True if username is valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    username = username.strip()
    if len(username) < min_length or len(username) > max_length:
        return False
    
    # Alphanumeric, underscore, dot, hyphen
    pattern = r'^[a-zA-Z0-9_.-]+$'
    return bool(re.match(pattern, username))


def is_valid_password(password: str, min_length: int = 8) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        min_length: Minimum length requirement
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*(),.?":{}|<>' for c in password)
    
    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_lower:
        return False, "Password must contain at least one lowercase letter"
    if not has_digit:
        return False, "Password must contain at least one digit"
    if not has_special:
        return False, "Password must contain at least one special character"
    
    return True, None


# ============================================================================
# MEDICAL PARAMETER VALIDATORS
# ============================================================================

def is_valid_age(age: int, min_age: int = ValidationConstants.MIN_AGE, 
                 max_age: int = ValidationConstants.MAX_AGE) -> Tuple[bool, Optional[str]]:
    """
    Validate age range
    
    Args:
        age: Age in years
        min_age: Minimum allowed age
        max_age: Maximum allowed age
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(age, (int, float)):
        return False, f"Age must be a number, got {type(age).__name__}"
    
    if age < min_age:
        return False, ValidationMessages.INVALID_AGE.format(min=min_age, max=max_age)
    if age > max_age:
        return False, ValidationMessages.INVALID_AGE.format(min=min_age, max=max_age)
    
    return True, None


def is_valid_bmi(bmi: float, allow_extreme: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate BMI value with category information
    
    Args:
        bmi: BMI value
        allow_extreme: Allow extreme values (for clinical use)
    
    Returns:
        Tuple of (is_valid, error_message or category)
    """
    if not isinstance(bmi, (int, float)):
        return False, f"BMI must be a number, got {type(bmi).__name__}"
    
    min_bmi = ValidationConstants.MIN_BMI
    max_bmi = ValidationConstants.MAX_BMI
    
    if allow_extreme:
        min_bmi = 5
        max_bmi = 80
    
    if bmi < min_bmi or bmi > max_bmi:
        return False, ValidationMessages.INVALID_BMI.format(min=min_bmi, max=max_bmi)
    
    # Return BMI category as message for valid values
    if bmi < ValidationConstants.UNDERWEIGHT_BMI:
        return True, "Underweight"
    elif bmi <= ValidationConstants.NORMAL_BMI_MAX:
        return True, "Normal weight"
    elif bmi <= ValidationConstants.OVERWEIGHT_BMI_MAX:
        return True, "Overweight"
    else:
        return True, "Obese"


def is_valid_blood_pressure(systolic: int, diastolic: int) -> Tuple[bool, Optional[str]]:
    """
    Validate blood pressure values and return category
    
    Args:
        systolic: Systolic blood pressure (mmHg)
        diastolic: Diastolic blood pressure (mmHg)
    
    Returns:
        Tuple of (is_valid, error_message or category)
    """
    if not isinstance(systolic, (int, float)) or not isinstance(diastolic, (int, float)):
        return False, "Blood pressure values must be numbers"
    
    # Range validation
    if systolic < ValidationConstants.MIN_SYSTOLIC or systolic > ValidationConstants.MAX_SYSTOLIC:
        return False, ValidationMessages.INVALID_BP.format(systolic=systolic, diastolic=diastolic)
    
    if diastolic < ValidationConstants.MIN_DIASTOLIC or diastolic > ValidationConstants.MAX_DIASTOLIC:
        return False, ValidationMessages.INVALID_BP.format(systolic=systolic, diastolic=diastolic)
    
    # Relationship validation
    if systolic <= diastolic:
        return False, f"Systolic ({systolic}) must be greater than diastolic ({diastolic})"
    
    # Pulse pressure validation
    pulse_pressure = systolic - diastolic
    if pulse_pressure < 20:
        return False, f"Pulse pressure ({pulse_pressure} mmHg) is abnormally low"
    if pulse_pressure > 100:
        return False, f"Pulse pressure ({pulse_pressure} mmHg) is abnormally high"
    
    # Return BP category
    if systolic < ValidationConstants.NORMAL_SYSTOLIC_MAX and diastolic < ValidationConstants.NORMAL_DIASTOLIC_MAX:
        return True, "Normal"
    elif systolic < ValidationConstants.HYPERTENSION_SYSTOLIC and diastolic < ValidationConstants.HYPERTENSION_DIASTOLIC:
        return True, "Elevated"
    elif systolic < 160 or diastolic < 100:
        return True, "Stage 1 Hypertension"
    else:
        return True, "Stage 2 Hypertension"


def is_valid_heart_rate(rate: int, is_resting: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate heart rate
    
    Args:
        rate: Heart rate (beats per minute)
        is_resting: Whether this is a resting heart rate
    
    Returns:
        Tuple of (is_valid, error_message or category)
    """
    if not isinstance(rate, (int, float)):
        return False, f"Heart rate must be a number, got {type(rate).__name__}"
    
    if rate < ValidationConstants.MIN_HEART_RATE or rate > ValidationConstants.MAX_HEART_RATE:
        return False, ValidationMessages.INVALID_HEART_RATE.format(
            min=ValidationConstants.MIN_HEART_RATE, 
            max=ValidationConstants.MAX_HEART_RATE
        )
    
    if is_resting:
        if rate < ValidationConstants.RESTING_HEART_RATE_MIN:
            return True, "Bradycardia (slow heart rate)"
        elif rate > ValidationConstants.RESTING_HEART_RATE_MAX:
            return True, "Tachycardia (fast heart rate)"
        else:
            return True, "Normal resting heart rate"
    
    return True, "Normal"


def is_valid_glucose(glucose: float, fasting: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate glucose level
    
    Args:
        glucose: Glucose level (mg/dL)
        fasting: Whether this is a fasting glucose test
    
    Returns:
        Tuple of (is_valid, error_message or category)
    """
    if not isinstance(glucose, (int, float)):
        return False, f"Glucose must be a number, got {type(glucose).__name__}"
    
    if glucose < ValidationConstants.MIN_GLUCOSE or glucose > ValidationConstants.MAX_GLUCOSE:
        return False, ValidationMessages.INVALID_GLUCOSE.format(
            min=ValidationConstants.MIN_GLUCOSE,
            max=ValidationConstants.MAX_GLUCOSE
        )
    
    if fasting:
        if glucose <= ValidationConstants.NORMAL_GLUCOSE_MAX:
            return True, "Normal fasting glucose"
        elif glucose <= ValidationConstants.PREDIABETES_GLUCOSE_MAX:
            return True, "Prediabetes"
        else:
            return True, "Diabetes range"
    else:
        if glucose < 140:
            return True, "Normal random glucose"
        elif glucose < 200:
            return True, "Impaired glucose tolerance"
        else:
            return True, "Diabetes range"


def is_valid_cholesterol(cholesterol: float) -> Tuple[bool, Optional[str]]:
    """
    Validate cholesterol level
    
    Args:
        cholesterol: Total cholesterol (mg/dL)
    
    Returns:
        Tuple of (is_valid, error_message or category)
    """
    if not isinstance(cholesterol, (int, float)):
        return False, f"Cholesterol must be a number, got {type(cholesterol).__name__}"
    
    if cholesterol < ValidationConstants.MIN_CHOLESTEROL or cholesterol > ValidationConstants.MAX_CHOLESTEROL:
        return False, ValidationMessages.INVALID_RANGE.format(
            min=ValidationConstants.MIN_CHOLESTEROL,
            max=ValidationConstants.MAX_CHOLESTEROL
        )
    
    if cholesterol <= ValidationConstants.DESIRABLE_CHOLESTEROL_MAX:
        return True, "Desirable"
    elif cholesterol <= ValidationConstants.BORDERLINE_CHOLESTEROL_MAX:
        return True, "Borderline high"
    else:
        return True, "High"


# ============================================================================
# GENERAL VALIDATION FUNCTIONS
# ============================================================================

def sanitize_string(text: str, allow_spaces: bool = True, allow_special: bool = False) -> str:
    """
    Sanitize string by removing unwanted characters
    
    Args:
        text: Input string
        allow_spaces: Whether to allow spaces
        allow_special: Whether to allow special characters
    
    Returns:
        Sanitized string
    """
    if not text or not isinstance(text, str):
        return ""
    
    if allow_special:
        if allow_spaces:
            pattern = r'[^\w\s\-.,!?()]'
        else:
            pattern = r'[^\w\-.,!?()]'
    else:
        if allow_spaces:
            pattern = r'[^\w\s-]'
        else:
            pattern = r'[^\w-]'
    
    return re.sub(pattern, '', text.strip())


def validate_range(value: Union[int, float], min_val: Union[int, float], 
                   max_val: Union[int, float]) -> Tuple[bool, Optional[str]]:
    """
    Validate if value is within range
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(value, (int, float)):
        return False, f"Value must be a number, got {type(value).__name__}"
    
    if value < min_val or value > max_val:
        return False, ValidationMessages.INVALID_RANGE.format(min=min_val, max=max_val)
    
    return True, None


def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate required fields in dictionary
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    
    Returns:
        Tuple of (is_valid, list_of_missing_fields)
    """
    if not data or not isinstance(data, dict):
        return False, ["Data is empty or invalid"]
    
    missing = [field for field in required_fields if field not in data or data[field] is None]
    return len(missing) == 0, missing


def validate_numeric(value: Any, allow_zero: bool = True, allow_negative: bool = False) -> Tuple[bool, Optional[float]]:
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
        return False, ValidationMessages.INVALID_NUMERIC


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
    
    return False, ValidationMessages.INVALID_CHOICE.format(choices=choices)


def validate_date(date_str: str, format_str: str = "%Y-%m-%d") -> Tuple[bool, Optional[datetime]]:
    """
    Validate date string format
    
    Args:
        date_str: Date string to validate
        format_str: Expected date format
    
    Returns:
        Tuple of (is_valid, datetime_object or error_message)
    """
    if not date_str or not isinstance(date_str, str):
        return False, "Date string cannot be empty"
    
    try:
        date_obj = datetime.strptime(date_str.strip(), format_str)
        return True, date_obj
    except ValueError:
        return False, ValidationMessages.INVALID_DATE


def validate_percentage(value: float) -> Tuple[bool, Optional[str]]:
    """
    Validate percentage value (0-100)
    
    Args:
        value: Percentage value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    return validate_range(value, 0, 100)


# ============================================================================
# COMPOSITE VALIDATORS
# ============================================================================

def validate_patient_demographics(age: int, bmi: float, heart_rate: int) -> Dict[str, Any]:
    """
    Validate complete patient demographics
    
    Args:
        age: Age in years
        bmi: Body Mass Index
        heart_rate: Heart rate in bpm
    
    Returns:
        Dictionary with validation results
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate age
    age_valid, age_msg = is_valid_age(age)
    if not age_valid:
        results["valid"] = False
        results["errors"].append(age_msg)
    
    # Validate BMI
    bmi_valid, bmi_msg = is_valid_bmi(bmi)
    if not bmi_valid:
        results["valid"] = False
        results["errors"].append(bmi_msg)
    elif bmi_msg:
        results["warnings"].append(f"BMI Category: {bmi_msg}")
    
    # Validate heart rate
    hr_valid, hr_msg = is_valid_heart_rate(heart_rate)
    if not hr_valid:
        results["valid"] = False
        results["errors"].append(hr_msg)
    elif hr_msg and hr_msg != "Normal":
        results["warnings"].append(f"Heart Rate: {hr_msg}")
    
    return results


def validate_metabolic_panel(glucose: float, cholesterol: float, 
                             systolic: int, diastolic: int) -> Dict[str, Any]:
    """
    Validate complete metabolic panel
    
    Args:
        glucose: Glucose level
        cholesterol: Total cholesterol
        systolic: Systolic blood pressure
        diastolic: Diastolic blood pressure
    
    Returns:
        Dictionary with validation results
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Validate glucose
    glucose_valid, glucose_msg = is_valid_glucose(glucose)
    if not glucose_valid:
        results["valid"] = False
        results["errors"].append(glucose_msg)
    elif glucose_msg:
        results["warnings"].append(f"Glucose: {glucose_msg}")
    
    # Validate cholesterol
    chol_valid, chol_msg = is_valid_cholesterol(cholesterol)
    if not chol_valid:
        results["valid"] = False
        results["errors"].append(chol_msg)
    elif chol_msg:
        results["warnings"].append(f"Cholesterol: {chol_msg}")
    
    # Validate blood pressure
    bp_valid, bp_msg = is_valid_blood_pressure(systolic, diastolic)
    if not bp_valid:
        results["valid"] = False
        results["errors"].append(bp_msg)
    elif bp_msg:
        results["warnings"].append(f"Blood Pressure: {bp_msg}")
    
    return results


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_validator():
    """Factory function to create validator instance"""
    return Validator()


class Validator:
    """Validator class for object-oriented validation"""
    
    @staticmethod
    def email(email: str) -> bool:
        return is_valid_email(email)
    
    @staticmethod
    def phone(phone: str) -> bool:
        return is_valid_phone(phone)
    
    @staticmethod
    def age(age: int) -> Tuple[bool, Optional[str]]:
        return is_valid_age(age)
    
    @staticmethod
    def bmi(bmi: float) -> Tuple[bool, Optional[str]]:
        return is_valid_bmi(bmi)
    
    @staticmethod
    def blood_pressure(systolic: int, diastolic: int) -> Tuple[bool, Optional[str]]:
        return is_valid_blood_pressure(systolic, diastolic)
    
    @staticmethod
    def heart_rate(rate: int) -> Tuple[bool, Optional[str]]:
        return is_valid_heart_rate(rate)
    
    @staticmethod
    def glucose(glucose: float) -> Tuple[bool, Optional[str]]:
        return is_valid_glucose(glucose)
    
    @staticmethod
    def cholesterol(cholesterol: float) -> Tuple[bool, Optional[str]]:
        return is_valid_cholesterol(cholesterol)


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Test the validation functions
    print("Testing Validators...")
    print("=" * 50)
    
    # Test email
    print(f"Email 'test@example.com': {is_valid_email('test@example.com')}")
    print(f"Email 'invalid': {is_valid_email('invalid')}")
    
    # Test BMI
    valid, result = is_valid_bmi(22.5)
    print(f"BMI 22.5: valid={valid}, category={result}")
    
    valid, result = is_valid_bmi(32.0)
    print(f"BMI 32.0: valid={valid}, category={result}")
    
    # Test blood pressure
    valid, result = is_valid_blood_pressure(120, 80)
    print(f"BP 120/80: valid={valid}, category={result}")
    
    # Test glucose
    valid, result = is_valid_glucose(95)
    print(f"Glucose 95: valid={valid}, category={result}")