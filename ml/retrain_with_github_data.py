"""
Retreina MPB e R&B com dataset GitHub (labels verificados)
Combina dados existentes + GitHub dataset
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
from datetime import datetime

def load_and_combine_datasets(genre):
    """Carrega e combina datasets existentes + GitHub"""
    print(f"\n{'='*70}")
    print(f"CARREGANDO DATASETS - {genre.upper()}")
    print(f"{'='*70}\n")
    
    datasets_dir = Path(__file__).parent / 'datasets'
    all_data = []
    
    # 1. Dataset atual (ml_ready)
    ml_ready = datasets_dir / 'ml_ready' / f'{genre}_ml_ready.csv'
    if ml_ready.exists():
        df1 = pd.read_csv(ml_ready)
        all_data.append(df1)
        print(f"[1] ml_ready: {len(df1)} musicas")
    
    # 2. GitHub dataset
    github_file = datasets_dir / 'github_labeled.csv'
    if github_file.exists():
        df_github = pd.read_csv(github_file)
        
        # Filtrar por genero
        if 'genre' in df_github.columns:
            # Mapear generos
            genre_map = {
                'mpb': ['mpb', 'bossa nova', 'bossanova'],
                'rnb_brasil': ['rnb', 'r&b', 'soul', 'r-n-b']
            }
            
            if genre in genre_map:
                df_genre = df_github[
                    df_github['genre'].str.lower().isin(genre_map[genre])
                ]
                if len(df_genre) > 0:
                    all_data.append(df_genre)
                    print(f"[2] GitHub: {len(df_genre)} musicas")
    
    if not all_data:
        print("ERRO: Nenhum dataset encontrado!")
        return None
    
    # Combina
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicatas
    if 'track_name' in df_combined.columns:
        before = len(df_combined)
        df_combined = df_combined.drop_duplicates(subset=['track_name'], keep='first')
        removed = before - len(df_combined)
        if removed > 0:
            print(f"\nRemovidas {removed} duplicatas")
    
    print(f"\nTotal combinado: {len(df_combined)} musicas")
    
    return df_combined

def train_with_combined_data(genre):
    """Treina modelo com dados combinados"""
    print(f"\n{'='*70}")
    print(f"TREINAMENTO - {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Carrega dados
    df = load_and_combine_datasets(genre)
    
    if df is None:
        return None
    
    # Features basicas
    basic_features = ['bpm', 'energy', 'danceability', 'valence', 
                     'acousticness', 'instrumentalness', 'liveness', 
                     'speechiness', 'loudness']
    
    available_features = [f for f in basic_features if f in df.columns]
    
    X = df[available_features]
    y = df['is_hit']
    
    # Remove NaN
    valid_idx = y.notna() & X.notna().all(axis=1)
    X = X[valid_idx]
    y = y[valid_idx]
    
    print(f"Samples validos: {len(X)}")
    print(f"Hits: {y.sum()}, Nao-hits: {len(y) - y.sum()}\n")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Treina Random Forest
    print("Treinando Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    
    rf.fit(X_train, y_train)
    
    # Avalia
    y_pred = rf.predict(X_test)
    
    test_acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    cv_scores = cross_val_score(rf, X_train, y_train, cv=5)
    
    print(f"\nResultados:")
    print(f"  Test Accuracy: {test_acc:.1%}")
    print(f"  Precision:     {precision:.1%}")
    print(f"  Recall:        {recall:.1%}")
    print(f"  F1 Score:      {f1:.1%}")
    print(f"  CV Mean:       {cv_scores.mean():.1%} (+/- {cv_scores.std():.1%})")
    
    # Salva modelo
    models_dir = Path(__file__).parent / 'models'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RF_github_{timestamp}.pkl"
    model_path = models_dir / model_filename
    
    joblib.dump(rf, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return {
        'accuracy': test_acc,
        'cv_mean': cv_scores.mean(),
        'n_samples': len(X)
    }

def main():
    print("="*70)
    print("RETREINAMENTO COM GITHUB DATASET")
    print("="*70)
    
    results = {}
    
    # MPB
    print("\n[1/2] MPB")
    results['mpb'] = train_with_combined_data('mpb')
    
    # R&B Brasil
    print("\n[2/2] R&B Brasil")
    results['rnb_brasil'] = train_with_combined_data('rnb_brasil')
    
    # Comparacao
    print(f"\n\n{'='*70}")
    print("COMPARACAO: BASELINE vs GITHUB")
    print(f"{'='*70}\n")
    
    baseline = {
        'mpb': 0.542,
        'rnb_brasil': 0.595
    }
    
    for genre, res in results.items():
        if res is None:
            continue
            
        print(f"{genre.upper()}:")
        print(f"  Baseline:      {baseline[genre]:.1%}")
        print(f"  Com GitHub:    {res['accuracy']:.1%}")
        print(f"  Samples:       {res['n_samples']}")
        
        improvement = res['accuracy'] - baseline[genre]
        if improvement > 0.02:
            print(f"  Melhoria:      +{improvement:.1%} OK!")
        elif improvement > -0.02:
            print(f"  Melhoria:      {improvement:.1%} ~ (similar)")
        else:
            print(f"  Melhoria:      {improvement:.1%} X")
        print()
    
    print(f"{'='*70}")
    print("RETREINAMENTO CONCLUIDO!")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
