"""
Stroke Prediction Model Training
Algorithm: Ensemble (Random Forest + XGBoost + Logistic Regression)
"""

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore')

def train_stroke_model():
    """Train ensemble model for stroke prediction"""
    
    print("\n" + "="*60)
    print("STROKE PREDICTION MODEL TRAINING (ENSEMBLE)")
    print("="*60 + "\n")
    
    # Load processed data
    data = np.load('data/processed/stroke_processed.npz')
    X_train, X_val, X_test = data['X_train'], data['X_val'], data['X_test']
    y_train, y_val, y_test = data['y_train'], data['y_val'], data['y_test']
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    # Check class distribution
    unique, counts = np.unique(y_train, return_counts=True)
    class_ratio = counts[0] / counts[1]
    print(f"Class ratio (neg:pos): {class_ratio:.2f}:1")
    
    # Combine train and validation for final training
    X_train_full = np.vstack([X_train, X_val])
    y_train_full = np.hstack([y_train, y_val])
    
    print("\n" + "-"*60)
    print("TRAINING MODELS")
    print("-"*60)
    
    # 1. Random Forest
    print("\n1. Training Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train_full, y_train_full)
    
    # 2. XGBoost
    print("2. Training XGBoost...")
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        scale_pos_weight=class_ratio,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    xgb.fit(X_train_full, y_train_full)
    
    # 3. Logistic Regression
    print("3. Training Logistic Regression...")
    lr = LogisticRegression(
        C=1.0,
        class_weight='balanced',
        random_state=42,
        max_iter=1000
    )
    lr.fit(X_train_full, y_train_full)
    
    # 4. Ensemble Model
    print("4. Creating Ensemble Model...")
    ensemble = VotingClassifier(
        estimators=[
            ('rf', rf),
            ('xgb', xgb),
            ('lr', lr)
        ],
        voting='soft',
        weights=[0.4, 0.4, 0.2]
    )
    ensemble.fit(X_train_full, y_train_full)
    
    print("\n" + "-"*60)
    print("MODEL EVALUATION ON TEST SET")
    print("-"*60)
    
    # Test set evaluation
    y_test_pred = ensemble.predict(X_test)
    y_test_proba = ensemble.predict_proba(X_test)[:, 1]
    
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred)
    test_recall = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    test_roc_auc = roc_auc_score(y_test, y_test_proba)
    
    print(f"\nTest Set Metrics:")
    print(f"  • Accuracy:  {test_accuracy*100:.2f}%")
    print(f"  • Precision: {test_precision*100:.2f}%")
    print(f"  • Recall:    {test_recall*100:.2f}%")
    print(f"  • F1-Score:  {test_f1*100:.2f}%")
    print(f"  • ROC-AUC:   {test_roc_auc:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp)
    
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives:  {tn:5d}  |  False Positives: {fp:5d}")
    print(f"  False Negatives: {fn:5d}  |  True Positives:  {tp:5d}")
    print(f"  Specificity: {specificity*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred, 
                               target_names=['No Stroke', 'Stroke']))
    
    # Save models
    joblib.dump(ensemble, 'models/stroke/stroke_ensemble_model.pkl')
    joblib.dump(rf, 'models/stroke/stroke_rf_model.pkl')
    joblib.dump(xgb, 'models/stroke/stroke_xgb_model.pkl')
    
    print(f"\n✓ Models saved to models/stroke/")
    
    return ensemble

if __name__ == "__main__":
    train_stroke_model()