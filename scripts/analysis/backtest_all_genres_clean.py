"""
Backtest Completo de Calibrao - Todos os Gneros
Valida se o modelo est bem calibrado usando a base de dados completa
"""
import sys
import os
import pandas as pd
import numpy as np

# Adiciona projeto ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from backend.hit_predictor import HitPredictor

def backtest_genre(genre_id, dataset_path):
    """Testa um gnero especfico"""
    print(f"\n{'='*70}")
    print(f"BACKTEST: {genre_id.upper()}")
    print(f"{'='*70}")
    
    # Carrega dataset
    if not os.path.exists(dataset_path):
        print(f" Dataset no encontrado: {dataset_path}")
        return None
    
    df = pd.read_csv(dataset_path)
    print(f"[INFO] Total de musicas: {len(df)}")
    
    # Separa hits vs no-hits
    hits = df[df['is_hit'] == 1].copy()
    non_hits = df[df['is_hit'] == 0].copy()
    
    print(f"   [+] Hits: {len(hits)}")
    print(f"   [-] Nao-Hits: {len(non_hits)}")
    
    if len(hits) == 0 or len(non_hits) == 0:
        print(" Dataset desbalanceado (falta hits ou no-hits)")
        return None
    
    # Inicializa preditor
    predictor = HitPredictor(genre=genre_id)
    
    # Funo para calcular score
    def get_score(row):
        features = {
            'bpm': row['bpm'],
            'energy': row['energy'],
            'danceability': row['danceability'],
            'loudness': row.get('loudness', -7.0),
            'valence': row.get('valence', 0.5),
            'acousticness': row.get('acousticness', 0.5),
            'instrumentalness': row.get('instrumentalness', 0.1),
            'liveness': row.get('liveness', 0.1),
            'speechiness': row.get('speechiness', 0.1),
        }
        pred = predictor.predict(features)
        return pred['hit_score']
    
    # Calcula scores
    print("\n Calculando scores...")
    hits['predicted_score'] = hits.apply(get_score, axis=1)
    non_hits['predicted_score'] = non_hits.apply(get_score, axis=1)
    
    # Estatsticas
    hit_mean = hits['predicted_score'].mean()
    hit_std = hits['predicted_score'].std()
    hit_min = hits['predicted_score'].min()
    hit_max = hits['predicted_score'].max()
    
    non_hit_mean = non_hits['predicted_score'].mean()
    non_hit_std = non_hits['predicted_score'].std()
    non_hit_min = non_hits['predicted_score'].min()
    non_hit_max = non_hits['predicted_score'].max()
    
    print(f"\n RESULTADOS:")
    print(f"\n   HITS:")
    print(f"      Mdia: {hit_mean:.1f}  {hit_std:.1f}")
    print(f"      Range: [{hit_min:.1f} - {hit_max:.1f}]")
    
    print(f"\n   NO-HITS:")
    print(f"      Mdia: {non_hit_mean:.1f}  {non_hit_std:.1f}")
    print(f"      Range: [{non_hit_min:.1f} - {non_hit_max:.1f}]")
    
    # Separao (quanto maior, melhor)
    separation = hit_mean - non_hit_mean
    print(f"\n    Separao: {separation:.1f} pontos")
    
    # Threshold ideal (ponto de corte timo)
    threshold = (hit_mean + non_hit_mean) / 2
    print(f"    Threshold Ideal: {threshold:.1f}")
    
    # Acurcia usando threshold
    hits_corretos = (hits['predicted_score'] >= threshold).sum()
    non_hits_corretos = (non_hits['predicted_score'] < threshold).sum()
    
    accuracy = (hits_corretos + non_hits_corretos) / (len(hits) + len(non_hits))
    precision = hits_corretos / ((hits['predicted_score'] >= threshold).sum() + (non_hits['predicted_score'] >= threshold).sum())
    recall = hits_corretos / len(hits)
    
    print(f"\n    Acurcia: {accuracy*100:.1f}%")
    print(f"    Preciso: {precision*100:.1f}%")
    print(f"    Recall: {recall*100:.1f}%")
    
    # Anlise de calibrao
    print(f"\n{''*70}")
    print(" ANLISE DE CALIBRAO:")
    
    if separation < 10:
        print("    PROBLEMA: Separao muito baixa (< 10 pontos)")
        print("       Modelo no consegue diferenciar hits de no-hits")
        status = "RUIM"
    elif separation < 20:
        print("    ATENO: Separao moderada (10-20 pontos)")
        print("       Modelo diferencia, mas pode melhorar")
        status = "REGULAR"
    else:
        print("    BOM: Separao adequada (> 20 pontos)")
        status = "BOM"
    
    if hit_mean < 60:
        print("    PROBLEMA: Mdia de hits muito baixa (< 60)")
        print("       Modelo muito crtico, vai rejeitar hits verdadeiros")
    
    if non_hit_mean > 50:
        print("    PROBLEMA: Mdia de no-hits muito alta (> 50)")
        print("       Modelo muito permissivo, vai aprovar no-hits")
    
    # Top/Bottom 5 msicas HITS (para verificao manual)
    print(f"\n{''*70}")
    print(" TOP 5 HITS (Scores Mais Altos):")
    top_hits = hits.nlargest(5, 'predicted_score')[['track_name', 'artist', 'predicted_score']]
    for idx, row in top_hits.iterrows():
        print(f"   {row['predicted_score']:.1f} - {row['track_name']} ({row['artist']})")
    
    print(f"\n BOTTOM 5 HITS (Scores Mais Baixos - Possveis Falsos Negativos):")
    bottom_hits = hits.nsmallest(5, 'predicted_score')[['track_name', 'artist', 'predicted_score']]
    for idx, row in bottom_hits.iterrows():
        print(f"   {row['predicted_score']:.1f} - {row['track_name']} ({row['artist']})")
    
    return {
        'genre': genre_id,
        'hit_mean': hit_mean,
        'non_hit_mean': non_hit_mean,
        'separation': separation,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'status': status,
        'threshold': threshold
    }

def main():
    """Executa backtest para todos os gneros"""
    print("="*70)
    print("BACKTEST COMPLETO DE CALIBRAO - TODOS OS GNEROS")
    print("="*70)
    
    datasets_dir = os.path.join(project_root, 'ml', 'datasets')
    
    # Define gneros e seus datasets
    genres = {
        'mpb': 'kaggle_mpb_ml.csv',
        'pop_urban_brasil': 'kaggle_pop_urban_brasil_ml.csv',
        'rnb_brasil': 'kaggle_rnb_ml.csv',
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv'
    }
    
    results = []
    
    for genre_id, filename in genres.items():
        dataset_path = os.path.join(datasets_dir, filename)
        result = backtest_genre(genre_id, dataset_path)
        if result:
            results.append(result)
    
    # Resumo geral
    print(f"\n\n{'='*70}")
    print(" RESUMO GERAL - CALIBRAO POR GNERO")
    print(f"{'='*70}\n")
    
    df_results = pd.DataFrame(results)
    
    print(f"{'Gnero':<20} {'Hit Avg':<10} {'Non-Hit':<10} {'Sep':<8} {'Acc':<8} {'Status':<10}")
    print(f"{'-'*70}")
    
    for idx, row in df_results.iterrows():
        print(f"{row['genre']:<20} {row['hit_mean']:>6.1f}    {row['non_hit_mean']:>6.1f}    "
              f"{row['separation']:>6.1f}  {row['accuracy']*100:>6.1f}%  {row['status']:<10}")
    
    # Diagnstico geral
    print(f"\n{'='*70}")
    print(" DIAGNSTICO GERAL:")
    print(f"{'='*70}\n")
    
    avg_separation = df_results['separation'].mean()
    avg_accuracy = df_results['accuracy'].mean()
    
    problemas = df_results[df_results['status'] == 'RUIM']
    regulares = df_results[df_results['status'] == 'REGULAR']
    
    if len(problemas) > 0:
        print(f" {len(problemas)} gnero(s) com PROBLEMAS:")
        for idx, row in problemas.iterrows():
            print(f"   - {row['genre']}: Separao de apenas {row['separation']:.1f} pontos")
    
    if len(regulares) > 0:
        print(f" {len(regulares)} gnero(s) REGULARES (podem melhorar):")
        for idx, row in regulares.iterrows():
            print(f"   - {row['genre']}: Separao de {row['separation']:.1f} pontos")
    
    print(f"\n Mdia Geral:")
    print(f"   Separao: {avg_separation:.1f} pontos")
    print(f"   Acurcia: {avg_accuracy*100:.1f}%")
    
    if avg_separation < 15:
        print(f"\n RECOMENDAO: Modelo precisa de AJUSTES URGENTES")
        print("    Separao mdia muito baixa")
        print("    Revisar pesos e ranges heursticos")
    elif avg_separation < 25:
        print(f"\n RECOMENDAO: Modelo OK, mas pode ser refinado")
        print("    Ajustar gneros especficos com problemas")
    else:
        print(f"\n MODELO BEM CALIBRADO!")
        print("    Separao adequada em todos os gneros")

if __name__ == "__main__":
    main()
