"""
Helper utility functions

This module provides common utility functions for data formatting,
calculations, string manipulation, and general helper operations.
"""

from datetime import datetime, date
from typing import Optional, Any, List, Dict, Union
import re
import hashlib
import json
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTS
# ============================================================================

class BMICategories:
    """BMI category thresholds"""
    UNDERWEIGHT = 18.5
    NORMAL = 25
    OVERWEIGHT = 30
    OBESE = 30

BMI_CATEGORY_NAMES = {
    'underweight': 'Underweight',
    'normal': 'Normal weight',
    'overweight': 'Overweight',
    'obese': 'Obese'
}


# ============================================================================
# DATE AND TIME HELPERS
# ============================================================================

def format_date(date_obj: Any, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a date object to string
    
    Args:
        date_obj: Date object, datetime object, or string
        format_str: Desired output format
    
    Returns:
        Formatted date string or empty string if invalid
    
    Examples:
        >>> format_date(datetime(2024, 1, 1), "%Y-%m-%d")
        '2024-01-01'
    """
    if date_obj is None:
        return ""
    
    if isinstance(date_obj, str):
        try:
            # Try parsing ISO format first
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            try:
                # Try common formats
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]:
                    try:
                        date_obj = datetime.strptime(date_obj, fmt)
                        break
                    except ValueError:
                        continue
            except Exception:
                return date_obj
    
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime(format_str)
    
    return str(date_obj)


def parse_date(date_str: str, formats: Optional[List[str]] = None) -> Optional[date]:
    """
    Parse a date string into a date object
    
    Args:
        date_str: Date string to parse
        formats: List of possible formats (default: common formats)
    
    Returns:
        Date object or None if parsing fails
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    if formats is None:
        formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y"]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    
    return None


def calculate_age(birth_date: date) -> int:
    """
    Calculate age from birth date
    
    Args:
        birth_date: Date of birth
    
    Returns:
        Age in years, or 0 if invalid
    
    Examples:
        >>> calculate_age(date(1990, 1, 1))
        34  # (assuming current year is 2024)
    """
    if birth_date is None:
        return 0
    
    if not isinstance(birth_date, date):
        try:
            birth_date = parse_date(str(birth_date))
            if birth_date is None:
                return 0
        except Exception:
            return 0
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return max(0, age)


def get_age_group(age: int) -> str:
    """
    Get age group category
    
    Args:
        age: Age in years
    
    Returns:
        Age group string
    """
    if age < 18:
        return "Minor"
    elif age < 30:
        return "Young Adult"
    elif age < 50:
        return "Adult"
    elif age < 65:
        return "Middle Age"
    else:
        return "Senior"


def time_execution(func):
    """
    Decorator to measure function execution time
    
    Args:
        func: Function to decorate
    
    Returns:
        Wrapped function with timing
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.debug(f"{func.__name__} executed in {execution_time:.2f}ms")
        return result
    return wrapper


# ============================================================================
# HEALTH METRIC HELPERS
# ============================================================================

def get_bmi_category(bmi: float) -> str:
    """
    Get BMI category based on value
    
    Args:
        bmi: Body Mass Index value
    
    Returns:
        BMI category string
    
    Examples:
        >>> get_bmi_category(22.5)
        'Normal weight'
        >>> get_bmi_category(32.0)
        'Obese'
    """
    if not isinstance(bmi, (int, float)):
        return "Unknown"
    
    if bmi < BMICategories.UNDERWEIGHT:
        return BMI_CATEGORY_NAMES['underweight']
    elif bmi < BMICategories.NORMAL:
        return BMI_CATEGORY_NAMES['normal']
    elif bmi < BMICategories.OVERWEIGHT:
        return BMI_CATEGORY_NAMES['overweight']
    else:
        return BMI_CATEGORY_NAMES['obese']


def get_bmi_range(bmi: float) -> Dict[str, Any]:
    """
    Get detailed BMI information including range and health recommendations
    
    Args:
        bmi: Body Mass Index value
    
    Returns:
        Dictionary with BMI category, range, and recommendations
    """
    category = get_bmi_category(bmi)
    
    ranges = {
        'Underweight': {'min': 0, 'max': 18.5, 'color': 'blue', 'risk': 'Low weight'},
        'Normal weight': {'min': 18.5, 'max': 25, 'color': 'green', 'risk': 'Healthy'},
        'Overweight': {'min': 25, 'max': 30, 'color': 'orange', 'risk': 'Increased'},
        'Obese': {'min': 30, 'max': 100, 'color': 'red', 'risk': 'High'}
    }
    
    info = ranges.get(category, {})
    
    return {
        'category': category,
        'bmi': round(bmi, 1),
        'min_range': info.get('min', 0),
        'max_range': info.get('max', 0),
        'color': info.get('color', 'gray'),
        'risk_level': info.get('risk', 'Unknown')
    }


def get_blood_pressure_category(systolic: int, diastolic: int) -> Dict[str, Any]:
    """
    Get blood pressure category and recommendations
    
    Args:
        systolic: Systolic blood pressure (mmHg)
        diastolic: Diastolic blood pressure (mmHg)
    
    Returns:
        Dictionary with BP category and recommendations
    """
    if systolic < 120 and diastolic < 80:
        category = "Normal"
        color = "green"
        recommendation = "Maintain healthy lifestyle"
    elif 120 <= systolic < 130 and diastolic < 80:
        category = "Elevated"
        color = "yellow"
        recommendation = "Monitor regularly, consider lifestyle changes"
    elif 130 <= systolic < 140 or 80 <= diastolic < 90:
        category = "Stage 1 Hypertension"
        color = "orange"
        recommendation = "Consult doctor, lifestyle modifications needed"
    elif systolic >= 140 or diastolic >= 90:
        category = "Stage 2 Hypertension"
        color = "red"
        recommendation = "Medical consultation recommended"
    else:
        category = "Hypertensive Crisis"
        color = "darkred"
        recommendation = "Seek immediate medical attention"
    
    return {
        'category': category,
        'systolic': systolic,
        'diastolic': diastolic,
        'color': color,
        'recommendation': recommendation
    }


# ============================================================================
# STRING HELPERS
# ============================================================================

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum allowed length
        suffix: String to append when truncated
    
    Returns:
        Truncated text
    
    Examples:
        >>> truncate_text("This is a very long string", 10)
        'This is...'
    """
    if not text or not isinstance(text, str):
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug
    
    Args:
        text: Text to slugify
    
    Returns:
        URL-friendly slug
    
    Examples:
        >>> slugify("Hello World!")
        'hello-world'
    """
    if not text or not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML by escaping special characters
    
    Args:
        text: Text to sanitize
    
    Returns:
        HTML-safe string
    """
    if not text:
        return ""
    
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    
    return "".join(html_escape_table.get(c, c) for c in text)


def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from a string
    
    Args:
        text: String to extract numbers from
    
    Returns:
        List of extracted numbers
    """
    if not text:
        return []
    
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(n) for n in numbers]


# ============================================================================
# NUMBER AND MATH HELPERS
# ============================================================================

def format_currency(amount: float, currency: str = "$", decimal_places: int = 2) -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        decimal_places: Number of decimal places
    
    Returns:
        Formatted currency string
    
    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
    """
    if not isinstance(amount, (int, float)):
        return f"{currency}0.00"
    
    return f"{currency}{amount:,.{decimal_places}f}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safe division to avoid division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero
    
    Returns:
        Division result or default value
    
    Examples:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        0.0
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def round_to_nearest(value: float, nearest: float = 0.5) -> float:
    """
    Round a number to the nearest specified value
    
    Args:
        value: Number to round
        nearest: Nearest value to round to
    
    Returns:
        Rounded number
    
    Examples:
        >>> round_to_nearest(1.2, 0.5)
        1.0
        >>> round_to_nearest(1.3, 0.5)
        1.5
    """
    if not isinstance(value, (int, float)):
        return 0.0
    
    return round(value / nearest) * nearest


def get_percentage(value: float, total: float, decimal_places: int = 1) -> float:
    """
    Calculate percentage safely
    
    Args:
        value: Part value
        total: Total value
        decimal_places: Number of decimal places to round to
    
    Returns:
        Percentage value
    
    Examples:
        >>> get_percentage(25, 100)
        25.0
    """
    if total == 0:
        return 0.0
    
    percentage = (value / total) * 100
    return round(percentage, decimal_places)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
    
    Returns:
        Percentage change (negative for decrease)
    """
    if old_value == 0:
        return 0.0
    
    change = ((new_value - old_value) / abs(old_value)) * 100
    return round(change, 2)


# ============================================================================
# DATA STRUCTURE HELPERS
# ============================================================================

def generate_id(prefix: str = "", length: int = 8) -> str:
    """
    Generate a unique ID
    
    Args:
        prefix: Optional prefix for the ID
        length: Length of the random part
    
    Returns:
        Unique ID string
    
    Examples:
        >>> generate_id("user_")
        'user_a1b2c3d4'
    """
    from uuid import uuid4
    unique_id = str(uuid4())[:length]
    return f"{prefix}{unique_id}" if prefix else unique_id


def generate_hash(data: Any, algorithm: str = "md5") -> str:
    """
    Generate hash of data
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm (md5, sha1, sha256)
    
    Returns:
        Hash string
    """
    # Convert data to string if needed
    if not isinstance(data, str):
        data = json.dumps(data, sort_keys=True, default=str)
    
    data_bytes = data.encode('utf-8')
    
    if algorithm == "md5":
        return hashlib.md5(data_bytes).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data_bytes).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(data_bytes).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def flatten_dict(data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """
    Flatten a nested dictionary
    
    Args:
        data: Nested dictionary
        parent_key: Parent key for recursion
        sep: Separator for nested keys
    
    Returns:
        Flattened dictionary
    
    Examples:
        >>> flatten_dict({'a': {'b': 1, 'c': 2}})
        {'a_b': 1, 'a_c': 2}
    """
    if not data:
        return {}
    
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Handle lists by converting to string
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    
    return dict(items)


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    Split a list into chunks of specified size
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    
    Examples:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    if not lst:
        return []
    
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_get(data: Dict, key: str, default: Any = None, keys: List[str] = None) -> Any:
    """
    Safely get nested dictionary value
    
    Args:
        data: Dictionary to search
        key: Key to look up
        default: Default value if key not found
        keys: List of keys for nested lookup
    
    Returns:
        Value or default
    
    Examples:
        >>> safe_get({'a': {'b': 1}}, keys=['a', 'b'])
        1
    """
    if keys:
        current = data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current
    
    return data.get(key, default)


def merge_dicts(dict1: Dict, dict2: Dict, deep: bool = True) -> Dict:
    """
    Merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        deep: Whether to perform deep merge
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    if deep:
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value, deep)
            else:
                result[key] = value
    else:
        result.update(dict2)
    
    return result


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def is_valid_email(email: str) -> bool:
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


def is_valid_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    
    pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{3,4}$'
    return bool(re.match(pattern, phone.strip()))


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    print("Testing Helper Functions...")
    print("=" * 60)
    
    # Test date formatting
    print("\n1. Date Formatting:")
    print(f"  format_date(datetime.now()): {format_date(datetime.now())}")
    
    # Test age calculation
    print("\n2. Age Calculation:")
    test_date = date(1990, 1, 1)
    print(f"  Age for {test_date}: {calculate_age(test_date)}")
    print(f"  Age group: {get_age_group(calculate_age(test_date))}")
    
    # Test BMI functions
    print("\n3. BMI Functions:")
    print(f"  BMI 22.5 category: {get_bmi_category(22.5)}")
    bmi_info = get_bmi_range(28.5)
    print(f"  BMI 28.5 info: {bmi_info}")
    
    # Test blood pressure
    print("\n4. Blood Pressure:")
    bp_info = get_blood_pressure_category(125, 85)
    print(f"  BP 125/85: {bp_info}")
    
    # Test string functions
    print("\n5. String Functions:")
    print(f"  truncate_text: {truncate_text('This is a very long string', 15)}")
    print(f"  slugify: {slugify('Hello World!')}")
    
    # Test math functions
    print("\n6. Math Functions:")
    print(f"  format_currency(1234.56): {format_currency(1234.56)}")
    print(f"  safe_divide(10, 0): {safe_divide(10, 0)}")
    print(f"  get_percentage(25, 100): {get_percentage(25, 100)}%")
    
    # Test data structure functions
    print("\n7. Data Structure Functions:")
    print(f"  generate_id('user_'): {generate_id('user_')}")
    
    nested_dict = {'a': {'b': 1, 'c': 2}, 'd': 3}
    print(f"  flatten_dict: {flatten_dict(nested_dict)}")
    
    print(f"  chunk_list: {chunk_list([1, 2, 3, 4, 5], 2)}")
    
    print("\n" + "=" * 60)
    print("Helper Functions Test Complete!")


def clean_text(text: str) -> str:
    """
    Clean and normalize text for mental health analysis
    
    Args:
        text: Raw input text
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Keep only letters, numbers, and basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\']', '', text)
    
    return text.strip()


def detect_crisis_keywords(text: str) -> List[str]:
    """
    Detect crisis-related keywords in text
    
    Args:
        text: Input text
    
    Returns:
        List of detected crisis keywords
    """
    crisis_keywords = [
        'suicide', 'kill myself', 'end my life', 'want to die',
        'better off dead', 'no reason to live', 'hurt myself',
        'self harm', 'emergency', 'crisis'
    ]
    
    text_lower = text.lower()
    detected = [kw for kw in crisis_keywords if kw in text_lower]
    
    return detected


def get_mental_health_disclaimer() -> str:
    """
    Get disclaimer for mental health predictions
    
    Returns:
        Disclaimer text
    """
    return """
    **Important Note:** This is an AI-powered screening tool only.
    It is not a substitute for professional mental health diagnosis or treatment.
    If you're experiencing a mental health crisis, please contact:
    - National Suicide Prevention Lifeline: 988
    - Crisis Text Line: Text HOME to 741741
    - Emergency Services: 911
    """