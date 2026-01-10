"""
Retreina MPB com dataset MASTER (labels reais)
"""
import sys
sys.path.insert(0, '.')

from ml.train_model import ModelTrainer

print("="*70)
print("RETREINANDO MPB - DATASET MASTER (LABELS REAIS)")
print("="*70)

trainer = ModelTrainer('ml/datasets/master_mpb.csv')
trainer.load_dataset()
trainer.prepare_data(test_size=0.2)

# Treina
trainer.train_random_forest(n_estimators=150, max_depth=12)
metrics = trainer.evaluate()

# Salva
model_path = trainer.save_model(output_dir='ml/models')
print(f"\n[OK] Modelo MPB MASTER salvo!")
print(f"Path: {model_path}")
