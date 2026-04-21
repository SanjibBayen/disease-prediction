"""
Cardiovascular Model Training
Algorithm: XGBoost
"""

import numpy as np
import joblib
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report

def train_cardio_model():
    """Train XGBoost model for cardiovascular prediction"""
    
    print("\n" + "="*60)
    print("CARDIOVASCULAR MODEL TRAINING")
    print("="*60 + "\n")
    
    # Load processed data
    data = np.load('data/processed/cardio_processed.npz')
    X_train, X_val, X_test = data['X_train'], data['X_val'], data['X_test']
    y_train, y_val, y_test = data['y_train'], data['y_val'], data['y_test']
    
    # Initialize model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    # Train model
    print("Training XGBoost model...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"✓ Test Accuracy: {accuracy*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No CVD', 'CVD']))
    
    # Save model
    joblib.dump(model, 'models/cardio_vascular/xgboost_cardiovascular_model.pkl')
    print(f"\n✓ Model saved to models/cardio_vascular/xgboost_cardiovascular_model.pkl")
    
    return model

if __name__ == "__main__":
    train_cardio_model()