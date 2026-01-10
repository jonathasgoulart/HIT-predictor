"""
Validação Retroativa do Modelo Hit Predictor
Testa o modelo com as top 50 e bottom 50 músicas de cada gênero
"""
import pandas as pd
import os
import sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Adiciona backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from hit_predictor import HitPredictor

# Configurações
GENRES = {
    'MPB': 'ml/datasets/kaggle_mpb_ml.csv',
    'R&B Brasil': 'ml/datasets/kaggle_rnb_ml.csv'
}

TOP_N = 50
BOTTOM_N = 50

def load_dataset(file_path):
    """Carrega dataset e retorna top/bottom músicas"""
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return None, None
    
    df = pd.read_csv(file_path)
    
    # Ordena por popularidade ou score (assumindo que existe uma coluna de ranking)
    # Se não houver, usa is_hit como proxy
    if 'popularity' in df.columns:
        df_sorted = df.sort_values('popularity', ascending=False)
    elif 'streams' in df.columns:
        df_sorted = df.sort_values('streams', ascending=False)
    else:
        # Separa hits e não-hits
        hits = df[df['is_hit'] == 1]
        non_hits = df[df['is_hit'] == 0]
        
        # Pega amostras aleatórias
        top_songs = hits.sample(min(TOP_N, len(hits)), random_state=42)
        bottom_songs = non_hits.sample(min(BOTTOM_N, len(non_hits)), random_state=42)
        
        return top_songs, bottom_songs
    
    # Pega top e bottom
    top_songs = df_sorted.head(TOP_N)
    bottom_songs = df_sorted.tail(BOTTOM_N)
    
    return top_songs, bottom_songs

def predict_songs(songs, genre_id):
    """Faz predição para um conjunto de músicas"""
    predictor = HitPredictor(genre=genre_id)
    
    results = []
    for idx, row in songs.iterrows():
        # Extrai TODAS as 9 features
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
        
        # Faz predição
        prediction = predictor.predict(features)
        
        results.append({
            'track_name': row.get('track_name', row.get('name', 'Unknown')),
            'artist': row.get('artist_name', row.get('artist', 'Unknown')),
            'actual_hit': row.get('is_hit', 0),
            'predicted_score': prediction['hit_score'],
            'predicted_hit': 1 if prediction['hit_score'] >= 50 else 0
        })
    
    return pd.DataFrame(results)

def calculate_metrics(results_df):
    """Calcula métricas de performance"""
    y_true = results_df['actual_hit']
    y_pred = results_df['predicted_hit']
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }

def print_results(genre, top_results, bottom_results, top_metrics, bottom_metrics):
    """Imprime resultados formatados"""
    print("\n" + "="*80)
    print(f"VALIDAÇÃO RETROATIVA - {genre}")
    print("="*80)
    
    # Top 50
    print(f"\nTOP {TOP_N} MUSICAS (Esperado: HITS)")
    print("-"*80)
    print(f"Acuracia:  {top_metrics['accuracy']:.2%}")
    print(f"Precisao:  {top_metrics['precision']:.2%}")
    print(f"Recall:    {top_metrics['recall']:.2%}")
    print(f"F1-Score:  {top_metrics['f1_score']:.2%}")
    print(f"\nMatriz de Confusao:")
    print(f"  TN: {top_metrics['confusion_matrix'][0][0]:3d}  FP: {top_metrics['confusion_matrix'][0][1]:3d}")
    print(f"  FN: {top_metrics['confusion_matrix'][1][0]:3d}  TP: {top_metrics['confusion_matrix'][1][1]:3d}")
    
    # Exemplos de erros
    errors = top_results[top_results['actual_hit'] != top_results['predicted_hit']]
    if len(errors) > 0:
        print(f"\nERROS ({len(errors)} musicas):")
        for idx, row in errors.head(5).iterrows():
            print(f"  - {row['track_name']} ({row['artist']}): Score {row['predicted_score']:.0f}")
    
    # Bottom 50
    print(f"\nBOTTOM {BOTTOM_N} MUSICAS (Esperado: NAO-HITS)")
    print("-"*80)
    print(f"Acuracia:  {bottom_metrics['accuracy']:.2%}")
    print(f"Precisao:  {bottom_metrics['precision']:.2%}")
    print(f"Recall:    {bottom_metrics['recall']:.2%}")
    print(f"F1-Score:  {bottom_metrics['f1_score']:.2%}")
    print(f"\nMatriz de Confusao:")
    print(f"  TN: {bottom_metrics['confusion_matrix'][0][0]:3d}  FP: {bottom_metrics['confusion_matrix'][0][1]:3d}")
    print(f"  FN: {bottom_metrics['confusion_matrix'][1][0]:3d}  TP: {bottom_metrics['confusion_matrix'][1][1]:3d}")
    
    # Exemplos de erros
    errors = bottom_results[bottom_results['actual_hit'] != bottom_results['predicted_hit']]
    if len(errors) > 0:
        print(f"\nERROS ({len(errors)} musicas):")
        for idx, row in errors.head(5).iterrows():
            print(f"  - {row['track_name']} ({row['artist']}): Score {row['predicted_score']:.0f}")

def main():
    print("="*80)
    print("VALIDAÇÃO RETROATIVA DO MODELO HIT PREDICTOR")
    print("="*80)
    print(f"\nTestando Top {TOP_N} e Bottom {BOTTOM_N} de cada gênero\n")
    
    all_results = {}
    
    for genre_name, file_path in GENRES.items():
        print(f"\nProcessando {genre_name}...")
        
        # Carrega dados
        top_songs, bottom_songs = load_dataset(file_path)
        
        if top_songs is None:
            continue
        
        # Determina genre_id para o predictor
        genre_id = 'mpb' if 'mpb' in file_path.lower() else 'rnb_brasil'
        
        # Faz predições
        print(f"  - Predizendo top {len(top_songs)} músicas...")
        top_results = predict_songs(top_songs, genre_id)
        
        print(f"  - Predizendo bottom {len(bottom_songs)} músicas...")
        bottom_results = predict_songs(bottom_songs, genre_id)
        
        # Calcula métricas
        top_metrics = calculate_metrics(top_results)
        bottom_metrics = calculate_metrics(bottom_results)
        
        # Imprime resultados
        print_results(genre_name, top_results, bottom_results, top_metrics, bottom_metrics)
        
        all_results[genre_name] = {
            'top_results': top_results,
            'bottom_results': bottom_results,
            'top_metrics': top_metrics,
            'bottom_metrics': bottom_metrics
        }
    
    # Resumo geral
    print("\n" + "="*80)
    print("RESUMO GERAL")
    print("="*80)
    
    for genre_name, results in all_results.items():
        top_acc = results['top_metrics']['accuracy']
        bottom_acc = results['bottom_metrics']['accuracy']
        avg_acc = (top_acc + bottom_acc) / 2
        
        print(f"\n{genre_name}:")
        print(f"  Top {TOP_N}:    {top_acc:.2%} acurácia")
        print(f"  Bottom {BOTTOM_N}: {bottom_acc:.2%} acurácia")
        print(f"  Média:      {avg_acc:.2%}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
