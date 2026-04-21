"""
Hypertension Prediction Dataset Preprocessing
Source: Hypertension Risk Dataset
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ============================================================================
# DATA LOADING
# ============================================================================

def load_hypertension_data():
    """Load Hypertension dataset"""
    
    df = pd.read_csv('data_csv/Hypertension-risk-model-main.csv')
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Features: {df.shape[1] - 1}")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_hypertension_data(df):
    """Clean hypertension data"""
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove outliers
    df = df[df['sysBP'] <= 250]
    df = df[df['diaBP'] <= 140]
    df = df[df['BMI'] <= 50]
    df = df[df['glucose'] <= 300]
    
    # Handle missing values
    df = df.fillna(df.median())
    
    print(f"✓ Cleaned data - remaining records: {len(df)}")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_hypertension(df):
    """Create new features for hypertension prediction"""
    
    # Pulse pressure
    df['pulse_pressure'] = df['sysBP'] - df['diaBP']
    
    # Mean arterial pressure
    df['map'] = df['diaBP'] + (df['pulse_pressure'] / 3)
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['BMI'],
                                  bins=[0, 18.5, 25, 30, 60],
                                  labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Age groups
    df['age_group'] = pd.cut(df['age'],
                              bins=[0, 40, 50, 60, 80],
                              labels=['Young', 'Middle', 'Senior', 'Elderly'])
    
    # BP categories
    df['bp_category'] = 'Normal'
    df.loc[df['sysBP'] >= 140, 'bp_category'] = 'High'
    df.loc[df['sysBP'] >= 180, 'bp_category'] = 'Severe'
    
    # Hypertension risk score
    df['hypertension_risk'] = (
        (df['sysBP'] > 140).astype(int) * 35 +
        (df['diaBP'] > 90).astype(int) * 25 +
        (df['BMI'] > 30).astype(int) * 20 +
        (df['age'] > 55).astype(int) * 15 +
        (df['cigsPerDay'] > 10).astype(int) * 10
    )
    
    print(f"✓ Created {df.shape[1] - 10} new features")
    
    return df


# ============================================================================
# FEATURE SELECTION
# ============================================================================

def select_hypertension_features(df):
    """Select features for model training"""
    
    feature_cols = [
        'male', 'age', 'cigsPerDay', 'BPMeds', 'totChol',
        'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose',
        'pulse_pressure', 'map'
    ]
    
    X = df[feature_cols].copy()
    y = df['TenYearCHD'].copy() if 'TenYearCHD' in df.columns else df['target'].copy()
    
    print(f"✓ Selected {len(feature_cols)} features for training")
    
    return X, y


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_hypertension_features(X, y):
    """Scale features and split data"""
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42, stratify=y
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
    joblib.dump(scaler, 'models/hypertension/scaler.pkl')
    
    return X_train, X_val, X_test, y_train, y_val, y_test, scaler


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def hypertension_preprocessing_pipeline():
    """Complete preprocessing pipeline for hypertension data"""
    
    print("\n" + "="*60)
    print("HYPERTENSION DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_hypertension_data()
    
    # Clean data
    df = clean_hypertension_data(df)
    
    # Feature engineering
    df = feature_engineering_hypertension(df)
    
    # Select features
    X, y = select_hypertension_features(df)
    
    # Transform
    X_train, X_val, X_test, y_train, y_val, y_test, scaler = transform_hypertension_features(X, y)
    
    # Save processed data
    import joblib
    np.savez('data/processed/hypertension_processed.npz',
             X_train=X_train, X_val=X_val, X_test=X_test,
             y_train=y_train, y_val=y_val, y_test=y_test)
    
    print(f"\n✓ Processed data saved to data/processed/hypertension_processed.npz")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    hypertension_preprocessing_pipeline()