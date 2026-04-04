"""
Validation utility functions
"""

import re
from typing import Any, Optional, Tuple, Union

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_phone(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{3,4}$'
    return bool(re.match(pattern, phone))

def is_valid_age(age: int, min_age: int = 0, max_age: int = 120) -> bool:
    """Validate age range"""
    return min_age <= age <= max_age

def is_valid_bmi(bmi: float) -> bool:
    """Validate BMI value"""
    return 10 <= bmi <= 60

def is_valid_blood_pressure(systolic: int, diastolic: int) -> bool:
    """Validate blood pressure values"""
    return 70 <= systolic <= 220 and 40 <= diastolic <= 130 and systolic > diastolic

def is_valid_heart_rate(rate: int) -> bool:
    """Validate heart rate"""
    return 40 <= rate <= 150

def is_valid_glucose(glucose: float) -> bool:
    """Validate glucose level"""
    return 40 <= glucose <= 400

def sanitize_string(text: str, allow_spaces: bool = True) -> str:
    """Sanitize string by removing special characters"""
    if allow_spaces:
        pattern = r'[^\w\s-]'
    else:
        pattern = r'[^\w-]'
    return re.sub(pattern, '', text)

def validate_range(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> bool:
    """Validate if value is within range"""
    return min_val <= value <= max_val

def validate_required_fields(data: dict, required_fields: list) -> Tuple[bool, list]:
    """Validate required fields in dictionary"""
    missing = [field for field in required_fields if field not in data or data[field] is None]
    return len(missing) == 0, missing

def validate_numeric(value: Any, allow_zero: bool = True) -> bool:
    """Validate if value is numeric"""
    try:
        num = float(value)
        if not allow_zero and num == 0:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_choice(value: Any, choices: list) -> bool:
    """Validate if value is in allowed choices"""
    return value in choices