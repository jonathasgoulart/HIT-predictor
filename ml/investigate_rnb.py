"""
Investigacao de performance do R&B Brasil
Compara dataset pequeno vs grande e testa Gradient Boosting
"""
import pandas as pd
import numpy as np
import sys
from train_model import ModelTrainer

def run_investigation():
    print("="*60)
    print("INVESTIGACAO R&B BRASIL")
    print("="*60)
    
    # 1. Baseline Pequeno
    print("\n1. BASELINE: Dataset Pequeno (rnb_brasil_dataset.csv)")
    try:
        trainer_small = ModelTrainer(r'c:\Users\jonat\Documents\Novo HIT\ml\datasets\rnb_brasil_dataset.csv')
        trainer_small.load_dataset()
        trainer_small.prepare_data(test_size=0.3)
        trainer_small.train_random_forest(n_estimators=100)
        metrics_small = trainer_small.evaluate()
        print(f"   Accuracy: {metrics_small['accuracy']:.2%}")
    except Exception as e:
        print(f"   Erro: {e}")

    # 2. Baseline Grande
    print("\n2. BASELINE: Dataset Grande (consolidated_knn/rnb_brasil_consolidated.csv)")
    try:
        trainer_large = ModelTrainer(r'c:\Users\jonat\Documents\Novo HIT\ml\datasets\consolidated_knn\rnb_brasil_consolidated.csv')
        trainer_large.load_dataset()
        trainer_large.prepare_data(test_size=0.2)
        trainer_large.train_random_forest(n_estimators=150, max_depth=12)
        metrics_large = trainer_large.evaluate()
        print(f"   Accuracy: {metrics_large['accuracy']:.2%}")
    except Exception as e:
        print(f"   Erro: {e}")

    # 3. Teste Gradient Boosting (Grande)
    print("\n3. EXPERIMENTO: Gradient Boosting (Dataset Grande)")
    try:
        trainer_gb = ModelTrainer(r'c:\Users\jonat\Documents\Novo HIT\ml\datasets\consolidated_knn\rnb_brasil_consolidated.csv')
        trainer_gb.load_dataset()
        trainer_gb.prepare_data(test_size=0.2)
        trainer_gb.train_gradient_boosting(n_estimators=200, learning_rate=0.1)
        metrics_gb = trainer_gb.evaluate()
        print(f"   Accuracy: {metrics_gb['accuracy']:.2%}")

    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    run_investigation()
