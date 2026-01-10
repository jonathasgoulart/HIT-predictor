
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.hit_predictor import HitPredictor

def check_artists():
    print("=== CHECK ARTISTAS ESPECIFICOS ===")
    genre = 'mpb' # As duas estao no MPB/RnB
    datasets = {
        'mpb_kaggle': 'ml/datasets/kaggle_mpb_ml.csv',
        'rnb_kaggle': 'ml/datasets/kaggle_rnb_ml.csv',
        'mpb_massive': 'ml/datasets/ml_ready/massive_mpb.csv'
    }
    
    targets = ['Liniker', 'Luedji']
    
    for d_name, path in datasets.items():
        if not os.path.exists(path): 
            print(f"Skipping {d_name} (not found)")
            continue
        
        print(f"\n>> Buscando em {d_name}...")
        try:
            df = pd.read_csv(path)
        except:
            print(f"Erro ao ler {path}")
            continue

        local_genre = 'mpb' if 'mpb' in d_name else 'rnb_brasil'
        predictor = HitPredictor(genre=local_genre)
        
        for idx, row in df.iterrows():
            track = str(row.get('track_name', '')).lower()
            # Tenta 'artist' ou 'artist_name'
            artist = str(row.get('artist', row.get('artist_name', ''))).lower()
            
            is_target = False
            for t in targets:
                if t.lower() in track or t.lower() in artist:
                    is_target = True
            
            if is_target:
                features = {
                    'bpm': row.get('bpm', 120),
                    'energy': row.get('energy', 0.5),
                    'danceability': row.get('danceability', 0.5),
                    'loudness': row.get('loudness', -8.0),
                    'valence': row.get('valence', 0.5),
                    'acousticness': row.get('acousticness', 0.1),
                    'liveness': row.get('liveness', 0.1),
                    'speechiness': row.get('speechiness', 0.05),
                    'brightness': 2500,
                    'dynamic_variation': 0.2,
                }
                result = predictor.predict(features)
                s = result['hit_score']
                ml_prob = result.get('ml_prediction', {}).get('probability', 0) * 100
                is_hit_truth = row.get('is_hit', -1)
                
                print(f"   [{'HIT' if is_hit_truth==1 else 'NON'}] {row.get('track_name', 'Unknown')} - {artist}")
                print(f"     -> Final Score: {s} (ML: {ml_prob:.1f}%)")
                if s < 60 and is_hit_truth == 1:
                    print(f"     -> PENALTIES: {result.get('breakdown', [])}")

if __name__ == "__main__":
    check_artists()
