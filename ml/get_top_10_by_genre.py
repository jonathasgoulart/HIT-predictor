"""
Script para gerar as TOP 10 músicas de cada gênero
usando os modelos treinados e datasets disponíveis
"""
import pandas as pd
import joblib
import os
from pathlib import Path
import numpy as np

# Features usadas pelos modelos ML
ML_FEATURES = ['bpm', 'energy', 'danceability', 'valence',
               'acousticness', 'instrumentalness', 'liveness',
               'speechiness', 'loudness']

def load_latest_model(genre):
    """Carrega o modelo mais recente para um gênero"""
    models_dir = Path(__file__).parent / 'models'
    pattern = f"{genre}_*.pkl"
    model_files = list(models_dir.glob(pattern))
    
    if not model_files:
        return None
    
    # Pega o mais recente
    latest_model = sorted(model_files)[-1]
    try:
        model = joblib.load(latest_model)
        return model, latest_model.name
    except Exception as e:
        print(f"Erro ao carregar modelo {latest_model.name}: {e}")
        return None

def get_genre_dataset_path(genre):
    """Retorna o caminho do dataset para o gênero"""
    datasets_dir = Path(__file__).parent / 'datasets'
    
    # Mapeamento de gêneros para arquivos de dataset
    dataset_map = {
        'mpb': 'master_mpb.csv',
        'rnb_brasil': 'master_rnb_brasil.csv',
        'brazil': 'kaggle_pop_urban_brasil_ml.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml.csv',
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv'
    }
    
    dataset_file = dataset_map.get(genre)
    if not dataset_file:
        return None
    
    dataset_path = datasets_dir / dataset_file
    if dataset_path.exists():
        return dataset_path
    else:
        print(f"Dataset não encontrado: {dataset_path}")
        return None

def prepare_features(df):
    """Prepara as features para predição"""
    # Verifica se todas as features necessárias estão presentes
    missing_features = [f for f in ML_FEATURES if f not in df.columns]
    
    if missing_features:
        print(f"  [AVISO] Features faltando: {missing_features}")
        # Preenche com valores padrão
        for feature in missing_features:
            if feature == 'bpm':
                df[feature] = 120
            elif feature in ['energy', 'danceability', 'valence', 'acousticness', 
                            'instrumentalness', 'liveness', 'speechiness']:
                df[feature] = 0.5
            elif feature == 'loudness':
                df[feature] = -8.0
    
    return df[ML_FEATURES].values

def get_top_10_for_genre(genre):
    """Retorna as top 10 músicas para um gênero específico"""
    print(f"\n{'='*60}")
    print(f"Processando gênero: {genre.upper()}")
    print(f"{'='*60}")
    
    # 1. Carrega o modelo
    model_result = load_latest_model(genre)
    if not model_result:
        print(f"  [ERRO] Nenhum modelo encontrado para {genre}")
        return None
    
    model, model_name = model_result
    print(f"  Modelo: {model_name}")
    
    # 2. Carrega o dataset
    dataset_path = get_genre_dataset_path(genre)
    if not dataset_path:
        print(f"  [ERRO] Dataset não encontrado para {genre}")
        return None
    
    print(f"  Dataset: {dataset_path.name}")
    
    try:
        df = pd.read_csv(dataset_path)
        print(f"  Total de músicas: {len(df)}")
    except Exception as e:
        print(f"  [ERRO] Erro ao ler dataset: {e}")
        return None
    
    # 3. Prepara features
    X = prepare_features(df.copy())
    
    # 4. Faz predições
    try:
        predictions = model.predict_proba(X)[:, 1]  # Probabilidade de ser hit
        df['hit_probability'] = predictions
        df['hit_score'] = (predictions * 100).astype(int)
    except Exception as e:
        print(f"  [ERRO] Erro ao fazer predições: {e}")
        return None
    
    # 5. Ordena por score e pega top 10
    top_10 = df.nlargest(10, 'hit_score')
    
    # 6. Seleciona colunas relevantes para exibir
    display_cols = []
    
    # Identifica colunas de identificação disponíveis
    if 'track_name' in top_10.columns:
        display_cols.append('track_name')
    elif 'name' in top_10.columns:
        display_cols.append('name')
    
    if 'artist_name' in top_10.columns:
        display_cols.append('artist_name')
    elif 'artist' in top_10.columns:
        display_cols.append('artist')
    elif 'artists' in top_10.columns:
        display_cols.append('artists')
    
    # Adiciona features principais
    feature_cols = ['bpm', 'energy', 'danceability', 'valence', 'loudness']
    for col in feature_cols:
        if col in top_10.columns:
            display_cols.append(col)
    
    # Sempre adiciona o score
    display_cols.extend(['hit_score', 'hit_probability'])
    
    # Remove duplicatas mantendo ordem
    display_cols = list(dict.fromkeys(display_cols))
    
    top_10_display = top_10[display_cols].copy()
    
    return top_10_display

def main():
    """Processa todos os gêneros e gera relatório"""
    
    # Lista de gêneros disponíveis
    genres = [
        'mpb',
        'rnb_brasil', 
        'brazil',  # Pop Urban Brasil
        'sertanejo',
        'pagode',
        'samba',
        'forro'
    ]
    
    print("=" * 80)
    print("TOP 10 MÚSICAS POR GÊNERO - USANDO MODELOS ML")
    print("=" * 80)
    
    results = {}
    
    for genre in genres:
        top_10 = get_top_10_for_genre(genre)
        
        if top_10 is not None:
            results[genre] = top_10
            
            # Exibe resultados
            print(f"\n  TOP 10 para {genre.upper()}:")
            print("  " + "-" * 58)
            
            for idx, row in top_10.iterrows():
                # Identifica nome da música e artista
                track_name = row.get('track_name') or row.get('name', 'Desconhecido')
                artist = row.get('artist_name') or row.get('artist') or row.get('artists', 'Desconhecido')
                score = row['hit_score']
                prob = row['hit_probability']
                
                print(f"  {len(results[genre]) - list(top_10.index).index(idx)}. {track_name[:40]:<40} | {artist[:25]:<25}")
                print(f"     Score: {score}/100 ({prob:.1%} probabilidade)")
                
                # Mostra features principais
                features_str = ""
                if 'bpm' in row:
                    features_str += f"BPM:{int(row['bpm'])} "
                if 'energy' in row:
                    features_str += f"Energy:{row['energy']:.2f} "
                if 'danceability' in row:
                    features_str += f"Dance:{row['danceability']:.2f}"
                
                if features_str:
                    print(f"     {features_str}")
                print()
    
    # Salva resultados em CSV
    output_dir = Path(__file__).parent / 'datasets'
    
    print("\n" + "=" * 80)
    print("SALVANDO RESULTADOS")
    print("=" * 80)
    
    for genre, top_10 in results.items():
        output_file = output_dir / f'top_10_{genre}.csv'
        top_10.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"  [OK] {genre.upper()}: {output_file}")
    
    # Cria também um arquivo consolidado
    all_results = []
    for genre, top_10 in results.items():
        top_10_copy = top_10.copy()
        top_10_copy['genre'] = genre
        all_results.append(top_10_copy)
    
    if all_results:
        consolidated = pd.concat(all_results, ignore_index=True)
        consolidated_file = output_dir / 'top_10_all_genres.csv'
        consolidated.to_csv(consolidated_file, index=False, encoding='utf-8-sig')
        print(f"\n  [OK] CONSOLIDADO: {consolidated_file}")
    
    print("\n" + "=" * 80)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 80)

if __name__ == "__main__":
    main()
