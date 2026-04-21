"""
Sleep Health Dataset Preprocessing
Source: Sleep Health and Lifestyle Dataset
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# ============================================================================
# DATA LOADING
# ============================================================================

def load_sleep_data():
    """Load Sleep Health dataset"""
    
    df = pd.read_csv('data_csv/Sleep_health_and_lifestyle_dataset.csv')
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Features: {df.shape[1] - 1}")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_sleep_data(df):
    """Clean sleep health data"""
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Split blood pressure into systolic and diastolic
    df[['systolic_bp', 'diastolic_bp']] = df['Blood Pressure'].str.split('/', expand=True).astype(float)
    
    # Remove outliers
    df = df[df['Sleep Duration'] >= 4]
    df = df[df['Sleep Duration'] <= 10]
    df = df[df['Stress Level'] <= 10]
    df = df[df['Heart Rate'] <= 120]
    
    print(f"✓ Cleaned data - remaining records: {len(df)}")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_sleep(df):
    """Create new features for sleep health prediction"""
    
    # Sleep efficiency (quality / duration)
    df['sleep_efficiency'] = df['Quality of Sleep'] / df['Sleep Duration']
    
    # Stress impact score
    df['stress_impact'] = df['Stress Level'] * df['Quality of Sleep'] / 10
    
    # Activity score
    df['activity_score'] = df['Physical Activity Level'] / 100 * df['Daily Steps'] / 10000
    
    # Age groups
    df['age_group'] = pd.cut(df['Age'],
                              bins=[0, 30, 40, 50, 60],
                              labels=['Young', 'Adult', 'Middle', 'Senior'])
    
    # Sleep score (0-100)
    df['sleep_score'] = (
        df['Sleep Duration'] / 8 * 30 +
        df['Quality of Sleep'] / 10 * 30 +
        (10 - df['Stress Level']) / 10 * 20 +
        df['Physical Activity Level'] / 100 * 20
    )
    
    print(f"✓ Created {df.shape[1] - 11} new features")
    
    return df


# ============================================================================
# ENCODE CATEGORICAL FEATURES
# ============================================================================

def encode_sleep_features(df):
    """Encode categorical features for sleep data"""
    
    # Label encode categorical columns
    categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'age_group']
    
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    # One-hot encode for some columns
    df = pd.get_dummies(df, columns=['BMI Category'], prefix='bmi')
    
    print(f"✓ Encoded {len(categorical_cols)} categorical features")
    
    return df, encoders


# ============================================================================
# FEATURE SELECTION
# ============================================================================

def select_sleep_features(df):
    """Select features for model training"""
    
    feature_cols = [
        'Age', 'Sleep Duration', 'Quality of Sleep', 'Stress Level',
        'Physical Activity Level', 'Heart Rate', 'Daily Steps',
        'systolic_bp', 'diastolic_bp', 'sleep_efficiency', 'stress_impact',
        'activity_score', 'Gender_encoded', 'Occupation_encoded'
    ]
    
    # Add BMI dummy columns
    bmi_cols = [col for col in df.columns if col.startswith('bmi_')]
    feature_cols.extend(bmi_cols)
    
    X = df[feature_cols].copy()
    y = (df['Sleep Disorder'].notna() & (df['Sleep Disorder'] != 'None')).astype(int)
    
    print(f"✓ Selected {len(feature_cols)} features for training")
    
    return X, y


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_sleep_features(X, y):
    """Scale features and split data"""
    
    # Scale numerical features
    numerical_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    scaler = StandardScaler()
    
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"\n✓ Data Split Complete:")
    print(f"  - Training: {len(X_train)} samples")
    print(f"  - Validation: {len(X_val)} samples")
    print(f"  - Test: {len(X_test)} samples")
    
    # Save scaler
    import joblib
    joblib.dump(scaler, 'models/sleep_health/scaler.pkl')
    
    return X_train, X_val, X_test, y_train, y_val, y_test, scaler


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def sleep_preprocessing_pipeline():
    """Complete preprocessing pipeline for sleep data"""
    
    print("\n" + "="*60)
    print("SLEEP HEALTH DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_sleep_data()
    
    # Clean data
    df = clean_sleep_data(df)
    
    # Feature engineering
    df = feature_engineering_sleep(df)
    
    # Encode features
    df, encoders = encode_sleep_features(df)
    
    # Select features
    X, y = select_sleep_features(df)
    
    # Transform
    X_train, X_val, X_test, y_train, y_val, y_test, scaler = transform_sleep_features(X, y)
    
    # Save processed data
    import joblib
    np.savez('data/processed/sleep_processed.npz',
             X_train=X_train, X_val=X_val, X_test=X_test,
             y_train=y_train, y_val=y_val, y_test=y_test)
    
    # Save encoders
    joblib.dump(encoders, 'models/sleep_health/label_encoders.pkl')
    
    print(f"\n✓ Processed data saved to data/processed/sleep_processed.npz")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    sleep_preprocessing_pipeline()