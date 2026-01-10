"""
Analisa se músicas marcadas como HIT estão realmente recebendo notas altas
"""
import pandas as pd
import os
import sys

# Adiciona backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from hit_predictor import HitPredictor

GENRES = {
    'Sertanejo': ('ml/datasets/kaggle_sertanejo_ml.csv', 'sertanejo'),
    'Pop/Urban': ('ml/datasets/kaggle_pop_urban_brasil_ml.csv', 'pop_urban_brasil'),
    'Forró': ('ml/datasets/kaggle_forro_ml.csv', 'forro'),
    'Pagode': ('ml/datasets/kaggle_pagode_ml.csv', 'pagode'),
    'Samba': ('ml/datasets/kaggle_samba_ml.csv', 'samba'),
    'MPB': ('ml/datasets/kaggle_mpb_ml.csv', 'mpb'),
    'R&B Brasil': ('ml/datasets/kaggle_rnb_ml.csv', 'rnb_brasil')
}

def analyze_genre(genre_name, file_path, genre_id):
    if not os.path.exists(file_path):
        return None
        
    print(f"\nAnalyzando {genre_name}...")
    df = pd.read_csv(file_path)
    
    predictor = HitPredictor(genre=genre_id)
    
    hit_scores = []
    non_hit_scores = []
    
    for idx, row in df.iterrows():
        try:
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
            
            result = predictor.predict(features)
            score = result['hit_score']
            
            if row['is_hit'] == 1:
                hit_scores.append(score)
            else:
                non_hit_scores.append(score)
        except Exception as e:
            continue
            
    avg_hit = sum(hit_scores) / len(hit_scores) if hit_scores else 0
    avg_non_hit = sum(non_hit_scores) / len(non_hit_scores) if non_hit_scores else 0
    
    return {
        'avg_hit': avg_hit,
        'avg_non_hit': avg_non_hit,
        'count_hit': len(hit_scores),
        'count_non_hit': len(non_hit_scores),
        'min_hit': min(hit_scores) if hit_scores else 0,
        'max_non_hit': max(non_hit_scores) if non_hit_scores else 0
    }

def main():
    print("="*80)
    print("ANALISE DE NOTAS: HITS vs NAO-HITS")
    print("="*80)
    print(f"{'GENERO':<15} | {'MEDIA HIT':<10} | {'MEDIA NAO-HIT':<15} | {'DIFERENCA':<10}")
    print("-" * 60)
    
    for genre_name, (file_path, genre_id) in GENRES.items():
        stats = analyze_genre(genre_name, file_path, genre_id)
        
        if stats:
            hit_avg = stats['avg_hit']
            non_hit_avg = stats['avg_non_hit']
            diff = hit_avg - non_hit_avg
            
            diff = hit_avg - non_hit_avg
            
            status = "BOM" if diff > 15 else "ATENCAO" if diff > 5 else "RUIM"
            
            print(f"{genre_name:<15} | {hit_avg:<10.1f} | {non_hit_avg:<15.1f} | {diff:<+10.1f} {status}")
            
    print("-" * 60)
    print("\nDETALHES:")
    print("- BOM: Hits tem nota media > 15 pontos acima dos nao-hits")
    print("- ATENCAO: Diferenca pequena entre hits e nao-hits")
    print("- RUIM: Nao-hits estao com notas iguais ou maiores que hits")

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    main()
