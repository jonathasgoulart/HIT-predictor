"""
Backtest FOCADO: R&B, MPB e Pop Urban (Prioridades)
"""
import sys
import os
import pandas as pd
import numpy as np

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from backend.hit_predictor import HitPredictor

def backtest_genre(genre_id, dataset_path):
    print(f"\n{'='*70}")
    print(f"BACKTEST: {genre_id.upper()}")
    print(f"{'='*70}")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset nao encontrado: {dataset_path}")
        return None
    
    df = pd.read_csv(dataset_path)
    print(f"[INFO] Total de musicas: {len(df)}")
    
    hits = df[df['is_hit'] == 1].copy()
    non_hits = df[df['is_hit'] == 0].copy()
    
    print(f"   [+] Hits: {len(hits)}")
    print(f"   [-] Nao-Hits: {len(non_hits)}")
    
    if len(hits) == 0 or len(non_hits) == 0:
        print("Dataset desbalanceado")
        return None
    
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
    
    print("\n[INFO] Calculando scores...")
    hits['predicted_score'] = hits.apply(get_score, axis=1)
    non_hits['predicted_score'] = non_hits.apply(get_score, axis=1)
    
    hit_mean = hits['predicted_score'].mean()
    hit_std = hits['predicted_score'].std()
    non_hit_mean = non_hits['predicted_score'].mean()
    non_hit_std = non_hits['predicted_score'].std()
    
    print(f"\n[RESULTADOS]:")
    print(f"   HITS: Avg={hit_mean:.1f}, Std={hit_std:.1f}")
    print(f"   NON-HITS: Avg={non_hit_mean:.1f}, Std={non_hit_std:.1f}")
    
    separation = hit_mean - non_hit_mean
    print(f"   Separacao: {separation:.1f} pontos")
    
    threshold = (hit_mean + non_hit_mean) / 2
    hits_corretos = (hits['predicted_score'] >= threshold).sum()
    non_hits_corretos = (non_hits['predicted_score'] < threshold).sum()
    accuracy = (hits_corretos + non_hits_corretos) / (len(hits) + len(non_hits))
    
    print(f"   Acuracia: {accuracy*100:.1f}%")
    
    # Estratégia usada
    strategy = predictor.GENRE_STRATEGY.get(genre_id, 'ml')
    print(f"   Estrategia: {strategy.upper()}")
    
    if separation < 10:
        status = "RUIM"
    elif separation < 20:
        status = "REGULAR"
    else:
        status = "BOM"
    
    print(f"   Status: {status}")
    
    return {
        'genre': genre_id,
        'hit_mean': hit_mean,
        'non_hit_mean': non_hit_mean,
        'separation': separation,
        'accuracy': accuracy,
        'status': status,
        'strategy': strategy
    }

def main():
    print("="*70)
    print("BACKTEST FOCADO - GENEROS PRIORITARIOS")
    print("="*70)
    
    datasets_dir = os.path.join(project_root, 'ml', 'datasets')
    
    # APENAS OS 3 PRIORITÁRIOS
    genres = {
        'rnb_brasil': 'kaggle_rnb_ml.csv',
        'mpb': 'master_mpb.csv',  # Dataset maior e mais confiável
        'brazil': 'kaggle_pop_urban_brasil_ml.csv'
    }
    
    results = []
    
    for genre_id, filename in genres.items():
        dataset_path = os.path.join(datasets_dir, filename)
        result = backtest_genre(genre_id, dataset_path)
        if result:
            results.append(result)
    
    print(f"\n\n{'='*70}")
    print("RESUMO - GENEROS PRIORITARIOS")
    print(f"{'='*70}\n")
    
    df_results = pd.DataFrame(results)
    
    print(f"{'Genero':<20} {'Hit':<8} {'Non-Hit':<8} {'Sep':<8} {'Acc':<8} {'Strat':<10} {'Status':<10}")
    print(f"{'-'*70}")
    
    for idx, row in df_results.iterrows():
        print(f"{row['genre']:<20} {row['hit_mean']:>6.1f}  {row['non_hit_mean']:>6.1f}  "
              f"{row['separation']:>6.1f}  {row['accuracy']*100:>6.1f}%  {row['strategy']:<10} {row['status']:<10}")
    
    print(f"\n[FINAL] Separacao Media: {df_results['separation'].mean():.1f} pontos")
    print(f"[FINAL] Acuracia Media: {df_results['accuracy'].mean()*100:.1f}%")
    
    # Identifica problemas
    problemas = df_results[df_results['separation'] < 10]
    if len(problemas) > 0:
        print(f"\n[ALERTA] {len(problemas)} genero(s) com PROBLEMAS:")
        for idx, row in problemas.iterrows():
            print(f"   - {row['genre']}: Sep={row['separation']:.1f}, Acc={row['accuracy']*100:.1f}%")

if __name__ == "__main__":
    main()
