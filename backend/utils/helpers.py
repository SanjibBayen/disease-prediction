"""
Helper utility functions
"""

from datetime import datetime, date
from typing import Optional, Any
import re

def format_date(date_obj: Any, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a date object to string"""
    if date_obj is None:
        return ""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj)
        except:
            return date_obj
    return date_obj.strftime(format_str) if hasattr(date_obj, 'strftime') else str(date_obj)

def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    if birth_date is None:
        return 0
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_bmi_category(bmi: float) -> str:
    """Get BMI category based on value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def format_currency(amount: float, currency: str = "$") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division to avoid division by zero"""
    if denominator == 0:
        return default
    return numerator / denominator

def round_to_nearest(value: float, nearest: float = 0.5) -> float:
    """Round a number to the nearest specified value"""
    return round(value / nearest) * nearest

def get_percentage(value: float, total: float) -> float:
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return (value / total) * 100

def generate_id(prefix: str = "") -> str:
    """Generate a unique ID"""
    from uuid import uuid4
    unique_id = str(uuid4())[:8]
    return f"{prefix}{unique_id}" if prefix else unique_id

def flatten_dict(data: dict, parent_key: str = '', sep: str = '_') -> dict:
    """Flatten a nested dictionary"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def chunk_list(lst: list, chunk_size: int) -> list:
    """Split a list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]