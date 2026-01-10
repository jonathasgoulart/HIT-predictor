"""
TOP 10 Músicas por Gênero - Modelo Calibrado
"""
import sys
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from backend.hit_predictor import HitPredictor

def get_top_10(genre_id, dataset_path):
    """Retorna TOP 10 músicas do gênero"""
    print(f"\n{'='*80}")
    print(f"TOP 10 - {genre_id.upper()}")
    print(f"{'='*80}\n")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset não encontrado: {dataset_path}")
        return None
    
    df = pd.read_csv(dataset_path)
    print(f"Total de músicas analisadas: {len(df)}")
    
    predictor = HitPredictor(genre=genre_id)
    
    def get_score(row):
        features = {
            'bpm': row.get('bpm', 120),
            'energy': row.get('energy', 0.5),
            'danceability': row.get('danceability', 0.5),
            'valence': row.get('valence', 0.5),
            'acousticness': row.get('acousticness', 0.5),
            'instrumentalness': row.get('instrumentalness', 0.1),
            'liveness': row.get('liveness', 0.1),
            'speechiness': row.get('speechiness', 0.1),
            'loudness': row.get('loudness', -7.0),
        }
        pred = predictor.predict(features)
        return pred['hit_score']
    
    print("Calculando scores...")
    df['predicted_score'] = df.apply(get_score, axis=1)
    
    # TOP 10
    top_10 = df.nlargest(10, 'predicted_score')
    
    # Estratégia usada
    strategy = predictor.GENRE_STRATEGY.get(genre_id, 'ml')
    print(f"Estratégia: {strategy.upper()}\n")
    
    print(f"{'#':<4} {'Score':<8} {'Música':<50} {'Artista':<30}")
    print(f"{'-'*80}")
    
    for idx, (i, row) in enumerate(top_10.iterrows(), 1):
        track = row.get('track_name', row.get('name', 'Unknown'))[:48]
        artist = row.get('artist', row.get('artist_name', row.get('artists', 'Unknown')))
        if isinstance(artist, str):
            artist = artist[:28]
        else:
            artist = 'Unknown'
        
        score = row['predicted_score']
        print(f"{idx:<4} {score:<8.1f} {track:<50} {artist:<30}")
    
    return top_10

def main():
    print("="*80)
    print("TOP 10 MÚSICAS POR GÊNERO - MODELO CALIBRADO")
    print("="*80)
    
    datasets_dir = os.path.join(project_root, 'ml', 'datasets')
    
    # Todos os gêneros
    genres = {
        'R&B Brasil': ('rnb_brasil', 'master_rnb_brasil.csv'),
        'Pop Urban Brasil': ('brazil', 'kaggle_pop_urban_brasil_ml.csv'),
        'MPB': ('mpb', 'master_mpb.csv'),
        'Sertanejo': ('sertanejo', 'kaggle_sertanejo_ml.csv'),
        'Forró': ('forro', 'kaggle_forro_ml.csv'),
        'Samba': ('samba', 'kaggle_samba_ml.csv'),
        'Pagode': ('pagode', 'kaggle_pagode_ml.csv')
    }
    
    all_tops = {}
    
    for genre_name, (genre_id, filename) in genres.items():
        dataset_path = os.path.join(datasets_dir, filename)
        top_10 = get_top_10(genre_id, dataset_path)
        if top_10 is not None:
            all_tops[genre_name] = top_10
    
    print(f"\n\n{'='*80}")
    print("RESUMO FINAL")
    print(f"{'='*80}\n")
    print(f"Total de gêneros analisados: {len(all_tops)}")
    print("\nPara ver detalhes, consulte a saída acima!")

if __name__ == "__main__":
    main()
