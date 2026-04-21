"""
Cardiovascular Disease Dataset Preprocessing
Source: CardioVascular Disease dataset (Kaggle)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# ============================================================================
# DATA LOADING
# ============================================================================

def load_cardio_data():
    """Load Cardiovascular Disease dataset"""
    
    df = pd.read_csv('data_csv/cardio_train.csv', sep=';')
    
    # Convert age from days to years
    df['age'] = df['age'] / 365.25
    df['age'] = df['age'].astype(int)
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Age range: {df['age'].min()} - {df['age'].max()} years")
    print(f"✓ Target distribution:\n{df['cardio'].value_counts()}")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_cardio_data(df):
    """Clean cardiovascular data"""
    
    initial_count = len(df)
    
    # Remove unrealistic blood pressure values
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 200)]
    df = df[(df['ap_lo'] >= 50) & (df['ap_lo'] <= 140)]
    
    # Remove where systolic <= diastolic
    df = df[df['ap_hi'] > df['ap_lo']]
    
    # Remove unrealistic height (120-220 cm)
    df = df[(df['height'] >= 120) & (df['height'] <= 220)]
    
    # Remove unrealistic weight (30-200 kg)
    df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]
    
    removed = initial_count - len(df)
    print(f"✓ Removed {removed} invalid records ({removed/initial_count*100:.1f}%)")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_cardio(df):
    """Create new features for cardiovascular prediction"""
    
    # Calculate BMI
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['bmi'],
                                  bins=[0, 18.5, 25, 30, 60],
                                  labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Pulse pressure (difference between systolic and diastolic)
    df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']
    
    # Mean arterial pressure
    df['map'] = df['ap_lo'] + (df['pulse_pressure'] / 3)
    
    # Age groups
    df['age_group'] = pd.cut(df['age'],
                              bins=[0, 40, 50, 60, 70],
                              labels=['Young', 'Middle', 'Senior', 'Elderly'])
    
    # Risk score
    df['bp_risk'] = ((df['ap_hi'] > 140) | (df['ap_lo'] > 90)).astype(int) * 30
    df['chol_risk'] = (df['cholesterol'] > 1).astype(int) * 20
    df['smoke_risk'] = df['smoke'] * 15
    df['inactive_risk'] = (1 - df['active']) * 10
    
    df['cardio_risk_score'] = df['bp_risk'] + df['chol_risk'] + df['smoke_risk'] + df['inactive_risk']
    
    print(f"✓ Created {df.shape[1] - 11} new features")
    
    return df


# ============================================================================
# ENCODE CATEGORICAL FEATURES
# ============================================================================

def encode_cardio_features(df):
    """Encode categorical features"""
    
    # Label encode gender (1=male, 2=female)
    df['gender_encoded'] = df['gender'].map({1: 0, 2: 1})
    
    # One-hot encode categorical features
    categorical_cols = ['bmi_category', 'age_group']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    print(f"✓ Encoded categorical features")
    
    return df


# ============================================================================
# FEATURE SELECTION
# ============================================================================

def select_cardio_features(df):
    """Select features for model training"""
    
    # Feature columns for training
    feature_cols = [
        'age', 'gender_encoded', 'ap_hi', 'ap_lo', 
        'cholesterol', 'gluc', 'smoke', 'alco', 'active',
        'bmi', 'pulse_pressure', 'map'
    ]
    
    # Add encoded columns
    encoded_cols = [col for col in df.columns if col.startswith(('bmi_category_', 'age_group_'))]
    feature_cols.extend(encoded_cols)
    
    X = df[feature_cols].copy()
    y = df['cardio'].copy()
    
    print(f"✓ Selected {len(feature_cols)} features for training")
    
    return X, y


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_cardio_features(X, y):
    """Scale features and split data"""
    
    # Scale numerical features
    numerical_cols = ['age', 'ap_hi', 'ap_lo', 'bmi', 'pulse_pressure', 'map']
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
    print(f"  - Training: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  - Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"  - Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # Save scaler
    import joblib
    joblib.dump(scaler, 'models/cardio_vascular/scaler.pkl')
    
    return X_train, X_val, X_test, y_train, y_val, y_test, scaler


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def cardio_preprocessing_pipeline():
    """Complete preprocessing pipeline for cardiovascular data"""
    
    print("\n" + "="*60)
    print("CARDIOVASCULAR DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_cardio_data()
    
    # Clean data
    df = clean_cardio_data(df)
    
    # Feature engineering
    df = feature_engineering_cardio(df)
    
    # Encode features
    df = encode_cardio_features(df)
    
    # Select features
    X, y = select_cardio_features(df)
    
    # Transform and split
    X_train, X_val, X_test, y_train, y_val, y_test, scaler = transform_cardio_features(X, y)
    
    # Save processed data
    import joblib
    np.savez('data/processed/cardio_processed.npz',
             X_train=X_train, X_val=X_val, X_test=X_test,
             y_train=y_train, y_val=y_val, y_test=y_test)
    
    print(f"\n✓ Processed data saved to data/processed/cardio_processed.npz")
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    cardio_preprocessing_pipeline()