"""
Quick Win #3: Retreinar modelos com dados limpos
Usa os datasets _clean.csv para retreinar os modelos
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.train_enhanced_models import train_genre_model
import pandas as pd

def retrain_with_clean_data():
    """Retreina modelos que tiveram dados limpos"""
    print("\n" + "="*70)
    print("RETREINANDO MODELOS COM DADOS LIMPOS")
    print("="*70 + "\n")
    
    # Modelos que tiveram dados limpos
    clean_datasets = {
        'mpb': 'ml/datasets/kaggle_mpb_ml_clean.csv',
        'rnb_brasil': 'ml/datasets/kaggle_rnb_ml_clean.csv',
        'pop_urban_brasil': 'ml/datasets/kaggle_pop_urban_brasil_ml_clean.csv',
        'samba': 'ml/datasets/kaggle_samba_ml_clean.csv'
    }
    
    results = {}
    
    for genre, dataset_path in clean_datasets.items():
        print(f"\n{'='*70}")
        print(f"TREINANDO: {genre.upper()}")
        print(f"{'='*70}\n")
        
        try:
            # Verifica se dataset existe
            if not Path(dataset_path).exists():
                print(f"AVISO: Dataset nao encontrado: {dataset_path}")
                continue
            
            # Carrega dataset
            df = pd.read_csv(dataset_path)
            print(f"Dataset: {len(df)} musicas")
            print(f"Hit ratio: {df['is_hit'].mean():.1%}")
            
            # Treina modelo
            print(f"\nTreinando modelo...")
            accuracy, model_path = train_genre_model(genre, dataset_path)
            
            results[genre] = {
                'accuracy': accuracy,
                'model_path': model_path,
                'dataset_size': len(df)
            }
            
            print(f"\nOK: Modelo treinado!")
            print(f"  Accuracy: {accuracy:.2%}")
            print(f"  Modelo: {model_path}")
            
        except Exception as e:
            print(f"ERRO ao treinar {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    # Relatório final
    print("\n" + "="*70)
    print("RELATORIO FINAL")
    print("="*70 + "\n")
    
    for genre, result in results.items():
        print(f"{genre.upper()}:")
        print(f"  Accuracy: {result['accuracy']:.2%}")
        print(f"  Dataset: {result['dataset_size']} musicas")
        print(f"  Modelo: {Path(result['model_path']).name}")
        print()
    
    print("="*70)
    print("OK: RETREINAMENTO CONCLUIDO!")
    print("="*70)
    
    return results

if __name__ == "__main__":
    retrain_with_clean_data()
