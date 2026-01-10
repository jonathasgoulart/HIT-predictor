"""
Retreinamento dos modelos ML com as 9 features corretas do Spotify
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from datetime import datetime

# Features corretas que usamos
FEATURES = [
    'bpm', 'energy', 'danceability', 'valence',
    'acousticness', 'instrumentalness', 'liveness',
    'speechiness', 'loudness'
]

GENRES = {
    'mpb': 'ml/datasets/kaggle_mpb_ml.csv',
    'rnb_brasil': 'ml/datasets/kaggle_rnb_ml.csv',
    'pop_urban_brasil': 'ml/datasets/kaggle_pop_urban_brasil_ml.csv',
    'sertanejo': 'ml/datasets/kaggle_sertanejo_ml.csv',
    'forro': 'ml/datasets/kaggle_forro_ml.csv',
    'pagode': 'ml/datasets/kaggle_pagode_ml.csv',
    'samba': 'ml/datasets/kaggle_samba_ml.csv'
}

def load_and_prepare_data(file_path):
    """Carrega e prepara dados para treinamento"""
    print(f"  Carregando {file_path}...")
    df = pd.read_csv(file_path)
    
    # Verifica se todas as features existem
    missing_features = [f for f in FEATURES if f not in df.columns]
    if missing_features:
        print(f"  AVISO: Features faltando: {missing_features}")
        return None, None
    
    # Verifica se tem label
    if 'is_hit' not in df.columns:
        print(f"  ERRO: Coluna 'is_hit' nao encontrada!")
        return None, None
    
    # Prepara X e y
    X = df[FEATURES].copy()
    y = df['is_hit'].copy()
    
    # Remove NaN
    mask = ~(X.isna().any(axis=1) | y.isna())
    X = X[mask]
    y = y[mask]
    
    print(f"  Dataset: {len(X)} amostras")
    print(f"  Hits: {sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)")
    print(f"  Nao-hits: {sum(y==0)} ({sum(y==0)/len(y)*100:.1f}%)")
    
    return X, y

def train_model(X, y, genre_name):
    """Treina modelo Random Forest"""
    print(f"\n  Treinando modelo para {genre_name}...")
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Treina Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'  # Importante para dados desbalanceados
    )
    
    model.fit(X_train, y_train)
    
    # Avalia
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n  Resultados no conjunto de teste:")
    print(f"  Acuracia: {accuracy:.2%}")
    print(f"\n  Relatorio de Classificacao:")
    print(classification_report(y_test, y_pred, target_names=['Nao-Hit', 'Hit']))
    
    print(f"\n  Matriz de Confusao:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN: {cm[0][0]:3d}  FP: {cm[0][1]:3d}")
    print(f"  FN: {cm[1][0]:3d}  TP: {cm[1][1]:3d}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"\n  Cross-Validation (5-fold):")
    print(f"  Acuracia media: {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")
    
    # Feature importance
    print(f"\n  Importancia das Features:")
    feature_importance = pd.DataFrame({
        'feature': FEATURES,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        print(f"  {row['feature']:20s}: {row['importance']:.4f}")
    
    return model

def save_model(model, genre_id):
    """Salva modelo treinado"""
    models_dir = 'ml/models'
    os.makedirs(models_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{genre_id}_RandomForestClassifier_{timestamp}.pkl"
    filepath = os.path.join(models_dir, filename)
    
    joblib.dump(model, filepath)
    print(f"\n  Modelo salvo: {filepath}")
    
    return filepath

def main():
    print("="*80)
    print("RETREINAMENTO DE MODELOS ML - 9 FEATURES SPOTIFY")
    print("="*80)
    print(f"\nFeatures utilizadas: {', '.join(FEATURES)}")
    print(f"Total de features: {len(FEATURES)}")
    
    trained_models = {}
    
    for genre_id, file_path in GENRES.items():
        print(f"\n{'='*80}")
        print(f"GENERO: {genre_id.upper()}")
        print(f"{'='*80}")
        
        # Carrega dados
        X, y = load_and_prepare_data(file_path)
        
        if X is None:
            print(f"  ERRO: Nao foi possivel carregar dados para {genre_id}")
            continue
        
        # Treina modelo
        model = train_model(X, y, genre_id)
        
        # Salva modelo
        model_path = save_model(model, genre_id)
        
        trained_models[genre_id] = {
            'model': model,
            'path': model_path,
            'n_samples': len(X),
            'n_features': len(FEATURES)
        }
    
    # Resumo final
    print(f"\n{'='*80}")
    print("RESUMO DO TREINAMENTO")
    print(f"{'='*80}")
    
    for genre_id, info in trained_models.items():
        print(f"\n{genre_id}:")
        print(f"  Modelo: {os.path.basename(info['path'])}")
        print(f"  Amostras: {info['n_samples']}")
        print(f"  Features: {info['n_features']}")
    
    print(f"\n{'='*80}")
    print("TREINAMENTO CONCLUIDO!")
    print(f"{'='*80}")
    print("\nProximos passos:")
    print("1. Teste os novos modelos com: python validate_model.py")
    print("2. Se os resultados forem bons, delete os modelos antigos")
    print("3. Reinicie o servidor backend para usar os novos modelos")

if __name__ == "__main__":
    main()
