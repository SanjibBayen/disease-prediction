"""
Diabetes Dataset Preprocessing
Source: PIMA Indians Diabetes Database
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer

# ============================================================================
# DATA LOADING
# ============================================================================

def load_diabetes_data():
    """Load PIMA Indians Diabetes dataset"""
    
    # Dataset columns
    columns = [
        'pregnancies',      # Number of pregnancies
        'glucose',          # Plasma glucose concentration
        'blood_pressure',   # Diastolic blood pressure (mm Hg)
        'skin_thickness',   # Triceps skin fold thickness (mm)
        'insulin',          # 2-Hour serum insulin (mu U/ml)
        'bmi',              # Body mass index
        'diabetes_pedigree', # Diabetes pedigree function
        'age',              # Age (years)
        'outcome'           # Class variable (0 or 1)
    ]
    
    # Load data (assuming CSV format)
    df = pd.read_csv('data_csv/diabetes.csv', names=columns, header=0)
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Features: {df.shape[1] - 1}")
    print(f"✓ Target distribution:\n{df['outcome'].value_counts()}")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_diabetes_data(df):
    """Clean and preprocess diabetes data"""
    
    # Replace zero values with NaN for medical measurements (zero is impossible)
    zero_columns = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
    
    for col in zero_columns:
        df[col] = df[col].replace(0, np.nan)
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            print(f"  - {col}: {missing_count} zero values replaced with NaN")
    
    # Impute missing values with median
    imputer = SimpleImputer(strategy='median')
    df[zero_columns] = imputer.fit_transform(df[zero_columns])
    
    print(f"✓ Missing values imputed with median")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_diabetes(df):
    """Create new features for diabetes prediction"""
    
    # Age groups
    df['age_group'] = pd.cut(df['age'], 
                              bins=[0, 30, 45, 60, 120],
                              labels=['Young', 'Middle', 'Senior', 'Elderly'])
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['bmi'],
                                  bins=[0, 18.5, 25, 30, 100],
                                  labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Glucose categories
    df['glucose_category'] = pd.cut(df['glucose'],
                                     bins=[0, 70, 100, 126, 300],
                                     labels=['Low', 'Normal', 'Prediabetes', 'Diabetes'])
    
    # Risk score (simple weighted sum)
    df['risk_score'] = (
        (df['glucose'] > 140).astype(int) * 30 +
        (df['bmi'] > 30).astype(int) * 25 +
        (df['age'] > 45).astype(int) * 15 +
        (df['blood_pressure'] > 140).astype(int) * 10 +
        (df['diabetes_pedigree'] > 0.8).astype(int) * 15
    )
    
    print(f"✓ Created {df.shape[1] - 9} new features")
    
    return df


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_diabetes_features(df, scaler_type='standard'):
    """Transform features for model training"""
    
    # Select features for training
    feature_cols = ['pregnancies', 'glucose', 'blood_pressure', 
                    'skin_thickness', 'insulin', 'bmi', 
                    'diabetes_pedigree', 'age']
    
    X = df[feature_cols].copy()
    y = df['outcome'].copy()
    
    # Scale features
    if scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()
    
    X_scaled = scaler.fit_transform(X)
    
    # Save scaler for later use
    import joblib
    joblib.dump(scaler, 'models/diabetes/scaler.pkl')
    
    print(f"✓ Features scaled using {scaler_type} scaler")
    print(f"✓ Scaler saved to models/diabetes/scaler.pkl")
    
    return X_scaled, y, scaler


# ============================================================================
# DATA SPLIT
# ============================================================================

def split_diabetes_data(X, y, test_size=0.2, random_state=42):
    """Split data into train, validation, test sets"""
    
    # First split: train+val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Second split: train vs validation
    val_size = test_size / (1 - test_size)  # 0.25 of remaining
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=random_state, stratify=y_temp
    )
    
    print(f"\n✓ Data Split Complete:")
    print(f"  - Training: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  - Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  - Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def diabetes_preprocessing_pipeline():
    """Complete preprocessing pipeline for diabetes data"""
    
    print("\n" + "="*60)
    print("DIABETES DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_diabetes_data()
    
    # Clean data
    df = clean_diabetes_data(df)
    
    # Feature engineering
    df = feature_engineering_diabetes(df)
    
    # Transform features
    X, y, scaler = transform_diabetes_features(df)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = split_diabetes_data(X, y)
    
    # Save processed data
    np.savez('data/processed/diabetes_processed.npz',
             X_train=X_train, X_val=X_val, X_test=X_test,
             y_train=y_train, y_val=y_val, y_test=y_test)
    
    print(f"\n✓ Processed data saved to data/processed/diabetes_processed.npz")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    diabetes_preprocessing_pipeline()