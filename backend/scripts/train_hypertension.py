"""
Hypertension Prediction Model Training
Algorithm: Extra Trees Classifier
"""

import numpy as np
import joblib
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.model_selection import GridSearchCV, cross_val_score
import warnings
warnings.filterwarnings('ignore')

def train_hypertension_model():
    """Train Extra Trees model for hypertension prediction"""
    
    print("\n" + "="*60)
    print("HYPERTENSION PREDICTION MODEL TRAINING (EXTRA TREES)")
    print("="*60 + "\n")
    
    # Load processed data
    data = np.load('data/processed/hypertension_processed.npz')
    X_train, X_val, X_test = data['X_train'], data['X_val'], data['X_test']
    y_train, y_val, y_test = data['y_train'], data['y_val'], data['y_test']
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {X_train.shape[1]}")
    
    # Combine train and validation
    X_train_full = np.vstack([X_train, X_val])
    y_train_full = np.hstack([y_train, y_val])
    
    print(f"Combined training samples: {len(X_train_full)}")
    
    print("\n" + "-"*60)
    print("HYPERPARAMETER TUNING")
    print("-"*60)
    
    # Hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'class_weight': ['balanced', 'balanced_subsample', None],
        'max_features': ['sqrt', 'log2', None]
    }
    
    # Grid search
    etc = ExtraTreesClassifier(random_state=42, n_jobs=-1, bootstrap=True)
    grid_search = GridSearchCV(
        etc, param_grid, 
        cv=5, 
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )
    
    print("\nSearching for best parameters...")
    grid_search.fit(X_train_full, y_train_full)
    
    best_model = grid_search.best_estimator_
    
    print(f"\n✓ Best parameters: {grid_search.best_params_}")
    print(f"✓ Best CV score: {grid_search.best_score_:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(best_model, X_train_full, y_train_full, 
                                cv=10, scoring='roc_auc')
    print(f"✓ 10-fold CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    print("\n" + "-"*60)
    print("MODEL EVALUATION ON TEST SET")
    print("-"*60)
    
    # Test set evaluation
    y_test_pred = best_model.predict(X_test)
    y_test_proba = best_model.predict_proba(X_test)[:, 1]
    
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
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        print(f"\nConfusion Matrix:")
        print(f"  True Negatives:  {tn:5d}  |  False Positives: {fp:5d}")
        print(f"  False Negatives: {fn:5d}  |  True Positives:  {tp:5d}")
        print(f"  Specificity: {specificity*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred, 
                               target_names=['No Hypertension', 'Hypertension']))
    
    # Feature importance
    feature_importance = best_model.feature_importances_
    print("\nTop 10 Important Features:")
    top_indices = np.argsort(feature_importance)[-10:][::-1]
    for i, idx in enumerate(top_indices, 1):
        print(f"  {i:2d}. Feature_{idx:2d}: {feature_importance[idx]:.4f}")
    
    # Save model
    joblib.dump(best_model, 'models/hypertension/hypertension_extra_trees_model.pkl')
    print(f"\n✓ Model saved to models/hypertension/hypertension_extra_trees_model.pkl")
    
    return best_model

if __name__ == "__main__":
    train_hypertension_model()