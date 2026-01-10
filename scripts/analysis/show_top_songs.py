"""
Analisa datasets e mostra as músicas com maiores scores em cada gênero
"""
import pandas as pd
import os
import sys

# Adiciona backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from hit_predictor import HitPredictor

GENRES = {
    'MPB': ('ml/datasets/kaggle_mpb_ml.csv', 'mpb'),
    'R&B Brasil': ('ml/datasets/kaggle_rnb_ml.csv', 'rnb_brasil'),
    'Sertanejo': ('ml/datasets/kaggle_sertanejo_ml.csv', 'sertanejo'),
    'Forró': ('ml/datasets/kaggle_forro_ml.csv', 'forro'),
    'Pagode': ('ml/datasets/kaggle_pagode_ml.csv', 'pagode'),
    'Samba': ('ml/datasets/kaggle_samba_ml.csv', 'samba')
}

TOP_N = 10

def analyze_genre(genre_name, file_path, genre_id):
    """Analisa um gênero e retorna top músicas"""
    if not os.path.exists(file_path):
        print(f"  AVISO: Dataset nao encontrado: {file_path}")
        return None
    
    print(f"\nAnalisando {genre_name}...")
    df = pd.read_csv(file_path)
    
    # Cria predictor para o gênero
    predictor = HitPredictor(genre=genre_id)
    
    # Calcula score para cada música
    scores = []
    for idx, row in df.iterrows():
        features = {
            'bpm': row.get('bpm', 120),
            'energy': row.get('energy', 0.5),
            'danceability': row.get('danceability', 0.5),
            'valence': row.get('valence', 0.5),
            'acousticness': row.get('acousticness', 0.5),
            'instrumentalness': row.get('instrumentalness', 0.0),
            'liveness': row.get('liveness', 0.2),
            'speechiness': row.get('speechiness', 0.1),
            'loudness': row.get('loudness', -8.0)
        }
        
        prediction = predictor.predict(features)
        
        scores.append({
            'track_name': row.get('track_name', row.get('name', 'Unknown')),
            'artist': row.get('artist_name', row.get('artist', 'Unknown')),
            'score': prediction['hit_score'],
            'is_hit': row.get('is_hit', 0),
            'bpm': features['bpm'],
            'energy': features['energy'],
            'danceability': features['danceability']
        })
    
    # Ordena por score
    df_scores = pd.DataFrame(scores)
    df_scores = df_scores.sort_values('score', ascending=False)
    
    return df_scores

def main():
    print("="*80)
    print("TOP MUSICAS POR GENERO - MAIORES SCORES")
    print("="*80)
    
    all_results = {}
    
    for genre_name, (file_path, genre_id) in GENRES.items():
        df_scores = analyze_genre(genre_name, file_path, genre_id)
        
        if df_scores is None:
            continue
        
        all_results[genre_name] = df_scores
        
        # Mostra top N
        print(f"\n{'='*80}")
        print(f"TOP {TOP_N} - {genre_name.upper()}")
        print(f"{'='*80}")
        
        top_songs = df_scores.head(TOP_N)
        
        for i, (idx, row) in enumerate(top_songs.iterrows(), 1):
            hit_label = "HIT" if row['is_hit'] == 1 else "NAO-HIT"
            print(f"\n{i}. {row['track_name']}")
            print(f"   Artista: {row['artist']}")
            print(f"   Score: {row['score']:.0f}/100 ({hit_label})")
            print(f"   BPM: {row['bpm']:.0f} | Energia: {row['energy']:.2f} | Dancabilidade: {row['danceability']:.2f}")
    
    # Resumo geral
    print(f"\n{'='*80}")
    print("RESUMO GERAL")
    print(f"{'='*80}")
    
    for genre_name, df_scores in all_results.items():
        top_score = df_scores.iloc[0]['score']
        avg_score = df_scores['score'].mean()
        hits_in_top10 = sum(df_scores.head(TOP_N)['is_hit'])
        
        print(f"\n{genre_name}:")
        print(f"  Score maximo: {top_score:.0f}")
        print(f"  Score medio: {avg_score:.0f}")
        print(f"  Hits no top {TOP_N}: {hits_in_top10}/{TOP_N}")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
