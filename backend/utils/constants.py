"""
Application constants
"""

# Disease Categories
DISEASE_CATEGORIES = {
    'diabetes': {
        'name': 'Diabetes',
        'icon': '🩸',
        'color': '#3b82f6',
        'description': 'Metabolic disorder affecting blood sugar regulation'
    },
    'hypertension': {
        'name': 'Hypertension',
        'icon': '❤️',
        'color': '#ef4444',
        'description': 'High blood pressure condition'
    },
    'cardiovascular': {
        'name': 'Cardiovascular Disease',
        'icon': '💓',
        'color': '#8b5cf6',
        'description': 'Heart and blood vessel disorders'
    },
    'stroke': {
        'name': 'Stroke',
        'icon': '🧠',
        'color': '#10b981',
        'description': 'Brain blood flow interruption'
    },
    'asthma': {
        'name': 'Asthma',
        'icon': '🌬️',
        'color': '#f59e0b',
        'description': 'Chronic respiratory condition'
    },
    'sleep': {
        'name': 'Sleep Disorder',
        'icon': '🌙',
        'color': '#6366f1',
        'description': 'Sleep pattern abnormalities'
    }
}

# Risk Levels
RISK_LEVELS = {
    'low': {
        'name': 'Low Risk',
        'color': '#10b981',
        'bg_color': '#d1fae5',
        'icon': '✅',
        'description': 'Minimal risk factors detected'
    },
    'moderate': {
        'name': 'Moderate Risk',
        'color': '#f59e0b',
        'bg_color': '#fed7aa',
        'icon': '⚠️',
        'description': 'Some risk factors present'
    },
    'high': {
        'name': 'High Risk',
        'color': '#ef4444',
        'bg_color': '#fee2e2',
        'icon': '🔴',
        'description': 'Significant risk factors detected'
    }
}

# BMI Categories
BMI_CATEGORIES = {
    'underweight': {'min': 0, 'max': 18.5, 'label': 'Underweight', 'color': '#3b82f6'},
    'normal': {'min': 18.5, 'max': 25, 'label': 'Normal weight', 'color': '#10b981'},
    'overweight': {'min': 25, 'max': 30, 'label': 'Overweight', 'color': '#f59e0b'},
    'obese': {'min': 30, 'max': 100, 'label': 'Obese', 'color': '#ef4444'}
}

# Blood Pressure Categories
BLOOD_PRESSURE_CATEGORIES = {
    'normal': {'systolic_min': 90, 'systolic_max': 120, 'diastolic_min': 60, 'diastolic_max': 80, 'label': 'Normal'},
    'elevated': {'systolic_min': 120, 'systolic_max': 129, 'diastolic_min': 80, 'diastolic_max': 80, 'label': 'Elevated'},
    'hypertension_stage1': {'systolic_min': 130, 'systolic_max': 139, 'diastolic_min': 80, 'diastolic_max': 89, 'label': 'Stage 1 Hypertension'},
    'hypertension_stage2': {'systolic_min': 140, 'systolic_max': 180, 'diastolic_min': 90, 'diastolic_max': 120, 'label': 'Stage 2 Hypertension'},
    'hypertensive_crisis': {'systolic_min': 180, 'systolic_max': 300, 'diastolic_min': 120, 'diastolic_max': 200, 'label': 'Hypertensive Crisis'}
}

# Glucose Categories
GLUCOSE_CATEGORIES = {
    'normal': {'min': 70, 'max': 99, 'label': 'Normal', 'color': '#10b981'},
    'prediabetes': {'min': 100, 'max': 125, 'label': 'Prediabetes', 'color': '#f59e0b'},
    'diabetes': {'min': 126, 'max': 500, 'label': 'Diabetes', 'color': '#ef4444'}
}

# Cholesterol Categories (mg/dL)
CHOLESTEROL_CATEGORIES = {
    'desirable': {'min': 0, 'max': 200, 'label': 'Desirable', 'color': '#10b981'},
    'borderline': {'min': 200, 'max': 239, 'label': 'Borderline High', 'color': '#f59e0b'},
    'high': {'min': 240, 'max': 500, 'label': 'High', 'color': '#ef4444'}
}

# Activity Levels
ACTIVITY_LEVELS = {
    'sedentary': {'label': 'Sedentary', 'minutes': 0, 'color': '#ef4444'},
    'light': {'label': 'Light', 'minutes': 30, 'color': '#f59e0b'},
    'moderate': {'label': 'Moderate', 'minutes': 60, 'color': '#3b82f6'},
    'active': {'label': 'Active', 'minutes': 90, 'color': '#10b981'},
    'very_active': {'label': 'Very Active', 'minutes': 120, 'color': '#8b5cf6'}
}

# Smoking Status
SMOKING_STATUS = {
    0: 'Never Smoked',
    1: 'Former Smoker',
    2: 'Current Smoker',
    3: 'Unknown'
}

# Alcohol Consumption
ALCOHOL_LEVELS = {
    'none': 'No Alcohol',
    'moderate': 'Moderate (1-2 drinks/day)',
    'heavy': 'Heavy (>2 drinks/day)'
}

# API Response Messages
API_MESSAGES = {
    'success': 'Operation completed successfully',
    'error': 'An error occurred',
    'not_found': 'Resource not found',
    'invalid_input': 'Invalid input provided',
    'unauthorized': 'Unauthorized access',
    'model_not_loaded': 'Model not loaded',
    'prediction_failed': 'Prediction failed'
}

# Cache Settings
CACHE_SETTINGS = {
    'default_ttl': 3600,  # 1 hour
    'model_cache_ttl': 86400,  # 24 hours
    'data_cache_ttl': 1800,  # 30 minutes
    'max_cache_size': 100  # Maximum number of cached items
}

# Pagination Settings
PAGINATION = {
    'default_page': 1,
    'default_page_size': 20,
    'max_page_size': 100
}

# File Upload Settings
FILE_UPLOAD = {
    'max_size_mb': 10,
    'allowed_extensions': ['.csv', '.xlsx', '.json'],
    'allowed_mime_types': ['text/csv', 'application/json', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
}