"""
Estrategia especifica para melhorar MPB e R&B Brasil
Problema: Features derivadas nao ajudaram (ou pioraram)
Solucao: Feature selection + XGBoost + Dataset quality
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_selection import SelectKBest, f_classif, RFE
import joblib
from datetime import datetime

def analyze_feature_importance(df, genre):
    """Analisa quais features realmente importam para o genero"""
    print(f"\n{'='*70}")
    print(f"ANALISE DE FEATURES - {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Separa features e target
    # Remove colunas nao-numericas e target
    cols_to_drop = ['is_hit', 'track_name', 'artist', 'artist_name', 'artists', 
                    'genre', 'id', 'artist_names', 'name', 'genres', 'artists_ids',
                    'Unnamed: 0']
    X = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    
    # Garante que todas as colunas sao numericas
    X = X.select_dtypes(include=[np.number])
    y = df['is_hit']
    
    # Remove linhas onde target eh NaN
    valid_idx = y.notna()
    X = X[valid_idx]
    y = y[valid_idx]
    
    # Remove NaN values em features
    X = X.fillna(X.median())
    
    print(f"Total de features: {len(X.columns)}")
    print(f"Samples validos: {len(X)}")
    print(f"Features: {list(X.columns)}\n")
    
    # 1. SelectKBest (ANOVA F-test)
    print("1. SelectKBest (Top 10 features):")
    selector = SelectKBest(f_classif, k=min(10, len(X.columns)))
    selector.fit(X, y)
    
    scores = pd.DataFrame({
        'feature': X.columns,
        'score': selector.scores_
    }).sort_values('score', ascending=False)
    
    print(scores.head(10).to_string(index=False))
    
    # 2. Random Forest Feature Importance
    print("\n2. Random Forest Feature Importance (Top 10):")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(importance.head(10).to_string(index=False))
    
    # 3. Retorna top features
    top_features = importance.head(12)['feature'].tolist()
    
    return top_features

def train_with_selected_features(df, genre, top_features):
    """Treina modelo usando apenas top features"""
    print(f"\n{'='*70}")
    print(f"TREINAMENTO COM FEATURES SELECIONADAS - {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Prepara dados com features selecionadas
    feature_cols = [f for f in top_features if f in df.columns]
    X = df[feature_cols]
    y = df['is_hit']
    
    print(f"Features usadas ({len(feature_cols)}): {feature_cols}\n")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"Treino: {len(X_train)}, Teste: {len(X_test)}\n")
    
    # Treina Random Forest otimizado
    print("Treinando Random Forest (features selecionadas)...")
    rf = RandomForestClassifier(
        n_estimators=300,  # Mais arvores
        max_depth=20,      # Mais profundidade
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    
    # Avalia
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    cv_scores = cross_val_score(rf, X_train, y_train, cv=5)
    
    print(f"\nResultados:")
    print(f"  Train Accuracy: {train_score:.1%}")
    print(f"  Test Accuracy:  {test_score:.1%}")
    print(f"  CV Mean:        {cv_scores.mean():.1%} (+/- {cv_scores.std():.1%})")
    
    # Salva modelo
    models_dir = Path(__file__).parent / 'models'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_RF_selected_{timestamp}.pkl"
    model_path = models_dir / model_filename
    
    joblib.dump(rf, model_path)
    print(f"\nModelo salvo: {model_filename}")
    
    return {
        'model': rf,
        'test_accuracy': test_score,
        'cv_mean': cv_scores.mean(),
        'features_used': feature_cols
    }

def train_xgboost_model(df, genre):
    """Treina modelo XGBoost como alternativa"""
    try:
        from xgboost import XGBClassifier
    except ImportError:
        print("\nXGBoost nao instalado. Pulando...")
        print("Instale com: pip install xgboost")
        return None
    
    print(f"\n{'='*70}")
    print(f"TREINAMENTO XGBOOST - {genre.upper()}")
    print(f"{'='*70}\n")
    
    # Prepara dados (sem features derivadas complexas)
    basic_features = ['bpm', 'energy', 'danceability', 'valence', 
                     'acousticness', 'instrumentalness', 'liveness', 
                     'speechiness', 'loudness']
    
    feature_cols = [f for f in basic_features if f in df.columns]
    X = df[feature_cols]
    y = df['is_hit']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Treina XGBoost
    print("Treinando XGBoost...")
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    xgb.fit(X_train, y_train)
    
    # Avalia
    test_score = xgb.score(X_test, y_test)
    cv_scores = cross_val_score(xgb, X_train, y_train, cv=5)
    
    print(f"\nResultados XGBoost:")
    print(f"  Test Accuracy: {test_score:.1%}")
    print(f"  CV Mean:       {cv_scores.mean():.1%} (+/- {cv_scores.std():.1%})")
    
    # Salva modelo
    models_dir = Path(__file__).parent / 'models'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{genre}_XGBoost_{timestamp}.pkl"
    model_path = models_dir / model_filename
    
    joblib.dump(xgb, model_path)
    print(f"\nModelo XGBoost salvo: {model_filename}")
    
    return {
        'model': xgb,
        'test_accuracy': test_score,
        'cv_mean': cv_scores.mean()
    }

def improve_mpb_rnb():
    """Pipeline completo para melhorar MPB e R&B"""
    
    ml_ready_dir = Path(__file__).parent / 'datasets' / 'ml_ready'
    
    genres_to_improve = {
        'mpb': ml_ready_dir / 'mpb_ml_ready_enhanced.csv',
        'rnb_brasil': ml_ready_dir / 'rnb_brasil_ml_ready_enhanced.csv'
    }
    
    results = {}
    
    for genre, filepath in genres_to_improve.items():
        print(f"\n\n{'#'*70}")
        print(f"# MELHORANDO: {genre.upper()}")
        print(f"{'#'*70}")
        
        # Carrega dataset
        df = pd.read_csv(filepath)
        print(f"\nDataset: {len(df)} musicas")
        print(f"Hits: {df['is_hit'].sum()}, Nao-hits: {len(df) - df['is_hit'].sum()}")
        
        # 1. Analisa features
        top_features = analyze_feature_importance(df, genre)
        
        # 2. Treina com features selecionadas
        rf_result = train_with_selected_features(df, genre, top_features)
        
        # 3. Treina XGBoost
        xgb_result = train_xgboost_model(df, genre)
        
        results[genre] = {
            'rf_selected': rf_result,
            'xgboost': xgb_result
        }
    
    # Resumo final
    print(f"\n\n{'='*70}")
    print("RESUMO FINAL - MPB E R&B BRASIL")
    print(f"{'='*70}\n")
    
    for genre, res in results.items():
        print(f"\n{genre.upper()}:")
        print(f"  RF (features selecionadas): {res['rf_selected']['test_accuracy']:.1%}")
        if res['xgboost']:
            print(f"  XGBoost (features basicas):  {res['xgboost']['test_accuracy']:.1%}")
    
    print(f"\n{'='*70}")
    print("CONCLUIDO!")
    print(f"{'='*70}")

if __name__ == "__main__":
    improve_mpb_rnb()
