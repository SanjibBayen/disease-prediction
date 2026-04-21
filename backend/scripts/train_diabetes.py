"""
Diabetes Model Training
Algorithm: SVC (Support Vector Classifier)
"""

import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train_diabetes_model():
    """Train SVC model for diabetes prediction"""
    
    print("\n" + "="*60)
    print("DIABETES MODEL TRAINING")
    print("="*60 + "\n")
    
    # Load processed data
    data = np.load('data/processed/diabetes_processed.npz')
    X_train, X_val, X_test = data['X_train'], data['X_val'], data['X_test']
    y_train, y_val, y_test = data['y_train'], data['y_val'], data['y_test']
    
    # Initialize model
    model = SVC(
        C=1.0,
        kernel='rbf',
        gamma='scale',
        probability=True,
        random_state=42,
        class_weight='balanced'
    )
    
    # Train model
    print("Training SVC model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Model trained successfully!")
    print(f"✓ Test Accuracy: {accuracy*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Diabetes', 'Diabetes']))
    
    # Save model
    joblib.dump(model, 'models/diabetes/diabetes_model.sav')
    print(f"\n✓ Model saved to models/diabetes/diabetes_model.sav")
    
    return model

if __name__ == "__main__":
    train_diabetes_model()