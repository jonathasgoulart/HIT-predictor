
import sys
import os
import pandas as pd
import numpy as np

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.hit_predictor import HitPredictor

def test_pop_urban_alignment():
    print("=== BACKTEST FOCADO: POP/URBAN BRASIL ===")
    
    # 1. Load Dataset
    df_path = os.path.join('ml', 'datasets', 'kaggle_pop_urban_brasil_ml.csv')
    try:
        df = pd.read_csv(df_path)
    except FileNotFoundError:
        print("Erro: Dataset não encontrado.")
        return

    # Filter Hits
    hits = df[df['is_hit'] == 1]
    print(f"Total de Hits no Banco de Dados: {len(hits)}")
    
    predictor = HitPredictor('pop_urban_brasil')
    
    scores = []
    print("\n--- Verificação de Alinhamento (Amostra de 15 Hits) ---")
    print(f"{'ARTISTA - MUSICA':<40} | {'BPM':<5} | {'ENERGY':<5} | {'SCORE APP'}")
    print("-" * 70)
    
    # Sample 15 random hits
    sample_hits = hits.sample(n=min(15, len(hits)), random_state=42)
    
    for _, row in sample_hits.iterrows():
        # Construct features dict (simulating app input)
        features = {
            'bpm': row['bpm'],
            'energy': row['energy'],
            'danceability': row['danceability'],
            'valence': row.get('valence', 0.5),
            'acousticness': row.get('acousticness', 0.5),
            'loudness': row.get('loudness', -8.0),
            'speechiness': row.get('speechiness', 0.05),
            'instrumentalness': row.get('instrumentalness', 0.0),
            'liveness': row.get('liveness', 0.1),
            # Mock spectral features matching the energy
            'brightness': row['energy'] * 3000 + 1000, 
            'dynamic_variation': 0.5
        }
        
        result = predictor.predict(features)
        score = result['hit_score']
        scores.append(score)
        
        name = f"{row['artist_name']} - {row['track_name']}"[:38]
        print(f"{name:<40} | {int(row['bpm']):<5} | {row['energy']:.2f}  | {score}")

    avg_score = np.mean(scores)
    print("-" * 70)
    print(f"\nMÉDIA DOS HITS 'POP URBAN': {avg_score:.1f} / 100")
    
    if avg_score > 75:
        print("✅ CONCLUSÃO: O App está ALTAMENTE ALINHADO com os Hits.")
    elif avg_score > 60:
        print("⚠️ CONCLUSÃO: O App está MODERADAMENTE ALINHADO (alguns hits penalizados).")
    else:
        print("❌ CONCLUSÃO: O App está DESALINHADO (rejeitando hits).")

if __name__ == "__main__":
    test_pop_urban_alignment()
