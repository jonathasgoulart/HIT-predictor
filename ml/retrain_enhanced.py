"""
Retreina modelos usando datasets enhanced (com feature engineering)
Compara performance antes vs depois
"""
import pandas as pd
import numpy as np
from pathlib import Path
from train_model import ModelTrainer
import joblib
from datetime import datetime

def train_enhanced_models():
    """Treina modelos com datasets enhanced"""
    
    ml_ready_dir = Path(__file__).parent / 'datasets' / 'ml_ready'
    models_dir = Path(__file__).parent / 'models'
    
    print("="*70)
    print("RETREINAMENTO COM FEATURES MELHORADAS")
    print("="*70 + "\n")
    
    # Datasets enhanced
    enhanced_files = list(ml_ready_dir.glob('*_enhanced.csv'))
    
    if not enhanced_files:
        print("Nenhum dataset enhanced encontrado!")
        print("Execute: python engineer_features.py")
        return
    
    print(f"Encontrados {len(enhanced_files)} datasets enhanced\n")
    
    results = []
    
    for enhanced_file in sorted(enhanced_files):
        # Extrai nome do genero
        genre = enhanced_file.stem.replace('_ml_ready_enhanced', '')
        
        print(f"\n{'='*70}")
        print(f"TREINANDO: {genre.upper()}")
        print(f"{'='*70}\n")
        
        try:
            # Carrega dataset
            trainer = ModelTrainer(str(enhanced_file))
            trainer.load_dataset()
            
            # Prepara dados
            trainer.prepare_data(test_size=0.25, random_state=42)
            
            # Treina Random Forest otimizado
            print("\nTreinando Random Forest...")
            trainer.train_random_forest(
                n_estimators=200,  # Mais arvores
                max_depth=15       # Mais profundidade
            )
            
            # Avalia
            metrics = trainer.evaluate()
            
            # Salva modelo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_filename = f"{genre}_RandomForest_enhanced_{timestamp}.pkl"
            model_path = models_dir / model_filename
            
            joblib.dump(trainer.model, model_path)
            print(f"\nModelo salvo: {model_filename}")
            
            # Salva metadata
            metadata = {
                'genre': genre,
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1': metrics['f1'],
                'cv_mean': metrics['cv_scores'].mean(),
                'cv_std': metrics['cv_scores'].std(),
                'n_samples': len(trainer.df),
                'n_features': trainer.X_train.shape[1],
                'timestamp': timestamp,
                'enhanced': True
            }
            
            metadata_file = models_dir / f"{genre}_RandomForest_enhanced_{timestamp}_metadata.txt"
            with open(metadata_file, 'w') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
            
            results.append(metadata)
            
            print(f"\n[OK] {genre.upper()} - Accuracy: {metrics['accuracy']:.1%}")
            
        except Exception as e:
            print(f"\n[ERRO] {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    # Resumo comparativo
    print(f"\n\n{'='*70}")
    print("RESUMO - MODELOS COM FEATURES MELHORADAS")
    print(f"{'='*70}\n")
    
    print(f"{'Genero':<20} {'Accuracy':<12} {'CV Mean':<12} {'Features':<10}")
    print("-"*70)
    
    for result in sorted(results, key=lambda x: x['accuracy'], reverse=True):
        print(f"{result['genre']:<20} {result['accuracy']:<12.1%} "
              f"{result['cv_mean']:<12.1%} {result['n_features']:<10}")
    
    # Salva resumo
    summary_df = pd.DataFrame(results)
    summary_file = models_dir / 'enhanced_models_summary.csv'
    summary_df.to_csv(summary_file, index=False)
    print(f"\nResumo salvo: {summary_file}")
    
    print(f"\n{'='*70}")
    print("RETREINAMENTO CONCLUIDO!")
    print(f"{'='*70}")
    
    print("\nProximo passo:")
    print("  Comparar com modelos anteriores:")
    print("  python ml/compare_models.py")

if __name__ == "__main__":
    train_enhanced_models()
