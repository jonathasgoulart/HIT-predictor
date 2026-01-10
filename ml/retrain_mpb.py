"""
Retreina modelo MPB com dataset expandido
"""
import sys
sys.path.insert(0, '.')

from ml.train_model import ModelTrainer

print("="*70)
print("RETREINANDO MODELO MPB COM DATASET EXPANDIDO")
print("="*70)

trainer = ModelTrainer('ml/datasets/kaggle_mpb_ml_expanded.csv')
trainer.load_dataset()
trainer.prepare_data(test_size=0.2)

# Treina com parâmetros robustos
trainer.train_random_forest(n_estimators=150, max_depth=12)

# Avalia
metrics = trainer.evaluate()

# Salva se accuracy > 60%
if metrics['accuracy'] > 0.60:
    model_path = trainer.save_model(output_dir='ml/models')
    print(f"\n[OK] Modelo MPB expandido salvo!")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"F1 Score: {metrics['f1']:.2%}")
else:
    print(f"\n[AVISO] Accuracy baixa: {metrics['accuracy']:.2%}")
    print("Modelo não foi salvo.")
