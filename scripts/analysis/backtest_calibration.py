
import os
import sys
import pandas as pd
import numpy as np

# Adicionar raiz do projeto ao path para importar backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.hit_predictor import HitPredictor

def run_backtest():
    print("=== INICIANDO BACKTEST DE CALIBRAÇÃO ===")
    
    # Gêneros para testar
    genres = ['mpb', 'rnb_brasil', 'pop_urban_brasil', 'sertanejo', 'pagode']
    
    datasets_path = os.path.join('ml', 'datasets')
    
    results = []

    for genre in genres:
        print(f"\n>> Analisando Genero: {genre.upper()}")
        
        # Mapear nome do arquivo
        if genre == 'pop_urban_brasil':
            filename = 'kaggle_pop_urban_brasil_ml.csv'
        elif genre == 'rnb_brasil':
            filename = 'kaggle_rnb_ml.csv'
        else:
            filename = f'kaggle_{genre}_ml.csv'
            
        filepath = os.path.join(datasets_path, filename)
        
        if not os.path.exists(filepath):
            print(f"   [WARN] Dataset nao encontrado: {filepath}")
            continue
            
        try:
            df = pd.read_csv(filepath)
            
            # Filtrar apenas HITS reais (is_hit = 1)
            hits = df[df['is_hit'] == 1]
            print(f"   Total de Hits no Dataset: {len(hits)}")
            
            if len(hits) == 0:
                continue
                
            predictor = HitPredictor(genre=genre)
            
            # --- ANALISE DE HITS (RECALL) ---
            print(f"   [HITS REAIS] (Target: > 75)")
            scores_hits = []
            hit_penalties = []
            
            # Busca específica por artistas
            target_artists = ['Liniker', 'Luedji']
            
            for idx, row in hits.iterrows():
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
                scores_hits.append(s)
                
                # Check for target artists
                track_name = str(row.get('track_name', '')).lower()
                artist_name = str(row.get('artist_name', '')).lower()
                
                for target in target_artists:
                    if target.lower() in track_name or target.lower() in artist_name:
                        print(f"   >>> DESTAQUE: {row.get('track_name', 'Unknown')} ({row.get('artist_name', 'Unknown')})")
                        print(f"       Score: {s} | ML: {result.get('ml_prediction', {}).get('probability', 0)*100:.1f}%")
                        print(f"       Breakdown: {result.get('breakdown', [])}")

                if s < 60:
                    hit_penalties.extend(result.get('breakdown', []))

            avg_hit = np.mean(scores_hits) if scores_hits else 0
            min_hit = np.min(scores_hits) if scores_hits else 0
            
            success_hits = sum(1 for s in scores_hits if s >= 70)
            recall = (success_hits / len(scores_hits) * 100) if scores_hits else 0
            
            print(f"   - Média: {avg_hit:.1f} | Mín: {min_hit:.1f}")
            print(f"   - Taxa de Aprovação (Score >= 70): {recall:.1f}%")
            
            # Carregar NÃO-HITS
            non_hits = df[df['is_hit'] == 0]
            if len(non_hits) > 0:
                print(f"   [NÃO-HITS] (Target: < 50)")
                scores_nohits = []
                for idx, row in non_hits.iterrows():
                    # Amostras aleatórias (limitado a 50 para não demorar)
                    if idx > 50 and len(non_hits) > 50: break
                    
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
                    scores_nohits.append(result['hit_score'])
                
                avg_nohit = np.mean(scores_nohits) if scores_nohits else 0
                success_nohits = sum(1 for s in scores_nohits if s < 60)
                specificity = (success_nohits / len(scores_nohits) * 100) if scores_nohits else 0
                
                print(f"   - Média: {avg_nohit:.1f}")
                print(f"   - Taxa de Rejeição (Score < 60): {specificity:.1f}%")
                
                # --- DIAGNÓSTICO GERAL ---
                if recall < 70:
                    print("   [ALERTA] Muitos hits legitimos sendo penalizados (Recall Baixo)")
                if specificity < 60:
                    print("   [ALERTA] Muitos nao-hits passando como sucesso (Especificidade Baixa)")
            
            if hit_penalties:
                print("   Principais Queixas (Top 3):")
                from collections import Counter
                # Extraindo apenas texto simples
                penalty_texts = [str(p) for p in hit_penalties]
                ctr = Counter(penalty_texts)
                for item, count in ctr.most_common(3):
                    print(f"     -> {item} ({count}x)")
            
            results.append({
                'genre': genre,
                'avg_hit': avg_hit,
                'recall': recall,
                'specificity': specificity if len(non_hits) > 0 else 0
            })
            
        except Exception as e:
            print(f"   [ERROR] Falha ao processar {genre}: {e}")

    print("\n=== RESUMO FINAL ===")
    print(f"{'GENERO'.ljust(20)} | {'AVG HIT'.ljust(10)} | {'RECALL'.ljust(10)} | {'REJEICAO'.ljust(10)}")
    for r in results:
        print(f"{r['genre'].ljust(20)} | {r['avg_hit']:.1f}       | {r['recall']:.1f}%     | {r['specificity']:.1f}%")

if __name__ == "__main__":
    run_backtest()
