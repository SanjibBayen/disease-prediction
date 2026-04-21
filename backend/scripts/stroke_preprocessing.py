"""
Stroke Prediction Dataset Preprocessing
Source: Healthcare Dataset Stroke Data
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# ============================================================================
# DATA LOADING
# ============================================================================

def load_stroke_data():
    """Load Stroke Prediction dataset"""
    
    df = pd.read_csv('data_csv/healthcare-dataset-stroke-data.csv')
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Features: {df.shape[1] - 1}")
    print(f"✓ Stroke cases: {df['stroke'].sum()} ({df['stroke'].mean()*100:.2f}%)")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_stroke_data(df):
    """Clean stroke prediction data"""
    
    # Handle missing BMI values
    bmi_median = df['bmi'].median()
    df['bmi'] = df['bmi'].fillna(bmi_median)
    print(f"✓ BMI missing values filled with median: {bmi_median:.1f}")
    
    # Remove outliers in glucose level (>300)
    df = df[df['avg_glucose_level'] <= 300]
    
    # Remove outliers in BMI (>50)
    df = df[df['bmi'] <= 50]
    
    print(f"✓ Removed outliers - remaining records: {len(df)}")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_stroke(df):
    """Create new features for stroke prediction"""
    
    # Age groups
    df['age_group'] = pd.cut(df['age'],
                              bins=[0, 30, 45, 60, 85],
                              labels=['Young', 'Middle', 'Senior', 'Elderly'])
    
    # Glucose categories
    df['glucose_category'] = pd.cut(df['avg_glucose_level'],
                                      bins=[0, 70, 100, 126, 300],
                                      labels=['Low', 'Normal', 'Prediabetes', 'Diabetes'])
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['bmi'],
                                  bins=[0, 18.5, 25, 30, 50],
                                  labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Risk score
    df['stroke_risk'] = (
        df['hypertension'] * 25 +
        df['heart_disease'] * 25 +
        (df['age'] > 60).astype(int) * 20 +
        (df['avg_glucose_level'] > 140).astype(int) * 15 +
        (df['bmi'] > 30).astype(int) * 10 +
        (df['smoking_status'] == 2).astype(int) * 10
    )
    
    print(f"✓ Created {df.shape[1] - 10} new features")
    
    return df


# ============================================================================
# ENCODE CATEGORICAL FEATURES
# ============================================================================

def encode_stroke_features(df):
    """Encode categorical features for stroke data"""
    
    # Label encode categorical columns
    categorical_cols = ['gender', 'ever_married', 'work_type', 'Residence_type',
                        'smoking_status', 'age_group', 'glucose_category', 'bmi_category']
    
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    # Drop original categorical columns
    df = df.drop(columns=categorical_cols)
    
    print(f"✓ Encoded {len(categorical_cols)} categorical features")
    
    return df, encoders


# ============================================================================
# FEATURE SELECTION
# ============================================================================

def select_stroke_features(df):
    """Select features for model training"""
    
    # Selected features
    feature_cols = [
        'age', 'hypertension', 'heart_disease', 'ever_married_encoded',
        'avg_glucose_level', 'bmi', 'smoking_status_encoded',
        'gender_encoded', 'work_type_encoded', 'Residence_type_encoded',
        'age_group_encoded', 'glucose_category_encoded', 'bmi_category_encoded'
    ]
    
    X = df[feature_cols].copy()
    y = df['stroke'].copy()
    
    print(f"✓ Selected {len(feature_cols)} features for training")
    
    return X, y


# ============================================================================
# HANDLE CLASS IMBALANCE
# ============================================================================

def balance_stroke_data(X, y):
    """Handle class imbalance using SMOTE"""
    
    # Check imbalance
    stroke_count = y.sum()
    non_stroke_count = len(y) - stroke_count
    print(f"✓ Before SMOTE - Non-stroke: {non_stroke_count}, Stroke: {stroke_count}")
    
    # Apply SMOTE
    smote = SMOTE(random_state=42, sampling_strategy=0.3)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    new_stroke_count = y_resampled.sum()
    new_non_stroke_count = len(y_resampled) - new_stroke_count
    print(f"✓ After SMOTE - Non-stroke: {new_non_stroke_count}, Stroke: {new_stroke_count}")
    
    return X_resampled, y_resampled


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_stroke_features(X, y):
    """Scale features and split data"""
    
    # Scale numerical features
    numerical_cols = ['age', 'avg_glucose_level', 'bmi']
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
    joblib.dump(scaler, 'models/stroke/scaler.pkl')
    
    return X_train, X_val, X_test, y_train, y_val, y_test, scaler


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def stroke_preprocessing_pipeline():
    """Complete preprocessing pipeline for stroke data"""
    
    print("\n" + "="*60)
    print("STROKE DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_stroke_data()
    
    # Clean data
    df = clean_stroke_data(df)
    
    # Feature engineering
    df = feature_engineering_stroke(df)
    
    # Encode features
    df, encoders = encode_stroke_features(df)
    
    # Select features
    X, y = select_stroke_features(df)
    
    # Balance data (SMOTE)
    X, y = balance_stroke_data(X, y)
    
    # Transform and split
    X_train, X_val, X_test, y_train, y_val, y_test, scaler = transform_stroke_features(X, y)
    
    # Save processed data
    import joblib
    np.savez('data/processed/stroke_processed.npz',
             X_train=X_train, X_val=X_val, X_test=X_test,
             y_train=y_train, y_val=y_val, y_test=y_test)
    
    # Save encoders
    joblib.dump(encoders, 'models/stroke/encoders.pkl')
    
    print(f"\n✓ Processed data saved to data/processed/stroke_processed.npz")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    stroke_preprocessing_pipeline()