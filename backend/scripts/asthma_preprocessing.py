"""
Asthma Prediction Dataset Preprocessing
Source: Asthma Analysis & Prediction Dataset
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# ============================================================================
# DATA LOADING
# ============================================================================

def load_asthma_data():
    """Load Asthma dataset"""
    
    df = pd.read_csv('data_csv/asthma_dataset.csv')
    
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Features: {df.shape[1] - 1}")
    
    return df


# ============================================================================
# DATA CLEANING
# ============================================================================

def clean_asthma_data(df):
    """Clean asthma data"""
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates()
    print(f"✓ Removed {initial_count - len(df)} duplicate records")
    
    # Remove outliers in peak flow
    df = df[(df['peak_flow'] >= 0.1) & (df['peak_flow'] <= 1.0)]
    
    # Handle missing values
    df = df.dropna()
    
    print(f"✓ Cleaned data - remaining records: {len(df)}")
    
    return df


# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def feature_engineering_asthma(df):
    """Create new features for asthma prediction"""
    
    # Normalize age (assuming original age 0-100)
    if 'age_years' in df.columns:
        df['age_normalized'] = df['age_years'] / 100
    
    # Create smoking risk score
    df['smoking_risk'] = df['smoking_ex'] * 1 + df['smoking_non'] * 0
    
    # Peak flow categories
    df['peak_flow_category'] = pd.cut(df['peak_flow'],
                                        bins=[0, 0.4, 0.6, 1.0],
                                        labels=['Low', 'Borderline', 'Normal'])
    
    # Asthma risk score
    df['asthma_risk'] = (
        df['smoking_ex'] * 25 +
        (df['peak_flow'] < 0.4).astype(int) * 35 +
        (df['peak_flow'] < 0.6).astype(int) * 20 +
        (df['age_normalized'] > 0.7).astype(int) * 15 if 'age_normalized' in df.columns else 0
    )
    
    print(f"✓ Created {df.shape[1] - 5} new features")
    
    return df


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_asthma_features(df):
    """Scale features and prepare for training"""
    
    # Select features
    feature_cols = ['gender_male', 'smoking_ex', 'smoking_non', 'age_normalized', 'peak_flow']
    
    # Ensure all features exist
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
    
    X = df[feature_cols].copy()
    y = df['asthma'].copy() if 'asthma' in df.columns else df['target'].copy()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n✓ Data Split Complete:")
    print(f"  - Training: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  - Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # Save scaler
    import joblib
    joblib.dump(scaler, 'models/asthma/scaler.pkl')
    
    return X_train, X_test, y_train, y_test, scaler


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def asthma_preprocessing_pipeline():
    """Complete preprocessing pipeline for asthma data"""
    
    print("\n" + "="*60)
    print("ASTHMA DATASET PREPROCESSING")
    print("="*60 + "\n")
    
    # Load data
    df = load_asthma_data()
    
    # Clean data
    df = clean_asthma_data(df)
    
    # Feature engineering
    df = feature_engineering_asthma(df)
    
    # Transform
    X_train, X_test, y_train, y_test, scaler = transform_asthma_features(df)
    
    # Save processed data
    import joblib
    np.savez('data/processed/asthma_processed.npz',
             X_train=X_train, X_test=X_test,
             y_train=y_train, y_test=y_test)
    
    # Save preprocessor (pipeline)
    from sklearn.pipeline import Pipeline
    preprocessor = Pipeline([
        ('scaler', scaler)
    ])
    joblib.dump(preprocessor, 'models/asthma/preprocessor.pkl')
    
    print(f"\n✓ Processed data saved to data/processed/asthma_processed.npz")
    print(f"✓ Preprocessor saved to models/asthma/preprocessor.pkl")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    asthma_preprocessing_pipeline()