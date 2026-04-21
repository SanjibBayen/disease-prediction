"""
Train All Models - Master Script
Runs training for all disease prediction models
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def train_all_models():
    """Train all models sequentially"""
    
    print("\n" + "="*70)
    print("COMPLETE MODEL TRAINING PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # List of training scripts
    training_scripts = [
        ('train_diabetes.py', 'Diabetes'),
        ('train_cardio.py', 'Cardiovascular'),
        ('train_stroke.py', 'Stroke'),
        ('train_asthma.py', 'Asthma'),
        ('train_hypertension.py', 'Hypertension'),
        ('train_sleep.py', 'Sleep Health')
    ]
    
    results = {}
    start_time = time.time()
    
    for script, name in training_scripts:
        print(f"\n{'='*70}")
        print(f"TRAINING {name.upper()} MODEL")
        print(f"{'='*70}")
        
        try:
            # Run the training script
            result = subprocess.run(
                [sys.executable, script],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # Print output
            print(result.stdout)
            
            if result.returncode == 0:
                print(f"\n✓ {name} model training completed successfully")
                results[name] = 'SUCCESS'
            else:
                print(f"\n✗ {name} model training failed")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                results[name] = 'FAILED'
                
        except Exception as e:
            print(f"\n✗ Error running {script}: {str(e)}")
            results[name] = 'ERROR'
    
    # Summary
    elapsed_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("TRAINING SUMMARY")
    print("="*70)
    
    for name, status in results.items():
        symbol = "✓" if status == 'SUCCESS' else "✗"
        print(f"{symbol} {name:20s}: {status}")
    
    print(f"\nTotal time: {elapsed_time/60:.2f} minutes")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Count successes
    successes = sum(1 for v in results.values() if v == 'SUCCESS')
    print(f"\n✓ {successes}/{len(training_scripts)} models trained successfully")

if __name__ == "__main__":
    train_all_models()