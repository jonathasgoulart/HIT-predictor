"""
Retreinamento com Datasets Finais
Treina modelos RandomForest para todos os gêneros com dados limpos + hits verificados
"""
import sys
import os
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

def train_genre_model(genre, dataset_path):
    """Treina modelo para um gênero específico"""
    print(f"\n{'='*70}")
    print(f"TREINANDO: {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Carrega dataset
    df = pd.read_csv(dataset_path)
    print(f"Dataset: {len(df)} musicas")
    print(f"Hit ratio: {df['is_hit'].mean():.1%}")
    
    # Features para ML
    ml_features = ['bpm', 'energy', 'danceability', 'loudness', 'valence',
                   'acousticness', 'instrumentalness', 'liveness', 'speechiness']
    
    # Filtra apenas features disponíveis
    available_features = [f for f in ml_features if f in df.columns]
    print(f"Features disponiveis: {len(available_features)}")
    
    if len(available_features) < 3:
        print(f"ERRO: Poucas features disponiveis ({len(available_features)})")
        return None, None
    
    # Prepara dados
    X = df[available_features].fillna(df[available_features].mean())
    y = df['is_hit']
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")
    
    # Treina Random Forest
    print("\nTreinando Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Avalia
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    cv_mean = cv_scores.mean()
    
    print(f"\nRESULTADOS:")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  CV Mean: {cv_mean:.2%}")
    print(f"  CV Std: {cv_scores.std():.2%}")
    
    # Salva modelo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RandomForest_enhanced_{timestamp}.pkl"
    model_path = Path(__file__).parent / 'models' / model_filename
    model_path.parent.mkdir(exist_ok=True)
    
    joblib.dump(model, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return accuracy, str(model_path)

def retrain_all_models():
    """Retreina todos os modelos com datasets finais"""
    print("\n" + "="*70)
    print("RETREINAMENTO COM DATASETS FINAIS")
    print("="*70)
    
    datasets_dir = Path(__file__).parent / 'datasets'
    
    genres = {
        'mpb': 'kaggle_mpb_ml_final.csv',
        'rnb_brasil': 'kaggle_rnb_ml_final.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml_final.csv',
        'sertanejo': 'kaggle_sertanejo_ml_final.csv',
        'samba': 'kaggle_samba_ml_final.csv',
        'pagode': 'kaggle_pagode_ml_final.csv'
    }
    
    results = {}
    
    for genre, filename in genres.items():
        dataset_path = datasets_dir / filename
        
        if not dataset_path.exists():
            print(f"\nAVISO: Dataset nao encontrado: {filename}")
            continue
        
        try:
            accuracy, model_path = train_genre_model(genre, str(dataset_path))
            if accuracy is not None:
                results[genre] = {
                    'accuracy': accuracy,
                    'model_path': model_path,
                    'dataset': filename
                }
        except Exception as e:
            print(f"\nERRO ao treinar {genre}: {e}")
            import traceback
            traceback.print_exc()
    
    # Relatório final
    print("\n" + "="*70)
    print("RELATORIO FINAL DE RETREINAMENTO")
    print("="*70 + "\n")
    
    for genre, result in results.items():
        print(f"{genre.upper()}:")
        print(f"  Accuracy: {result['accuracy']:.2%}")
        print(f"  Dataset: {result['dataset']}")
        print(f"  Modelo: {Path(result['model_path']).name}")
        print()
    
    print("="*70)
    print("RETREINAMENTO CONCLUIDO!")
    print("="*70)
    
    return results

if __name__ == "__main__":
    retrain_all_models()
