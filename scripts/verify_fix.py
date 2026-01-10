
import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.api import get_hit_averages_by_genre
    from backend.hit_predictor import HitPredictor
    
    print("=== TESTE DE INTEGRIDADE DO BACKEND ===")
    
    # 1. Test Chart Data (Empty Charts Bug)
    print("\n[1] Testando dados do gráfico (get_hit_averages_by_genre)...")
    try:
        averages = get_hit_averages_by_genre('brazil')
        if averages:
            print("    ✅ SUCESSO! Dados retornados:", list(averages.keys()))
            print(f"    Energia Média: {averages.get('energy'):.2f}")
        else:
            print("    ❌ FALHA! Retornou None (Gráfico ficará vazio)")
    except Exception as e:
        print(f"    ❌ CRASH! Erro ao chamar função: {e}")

    # 2. Test HitPredictor Logic (Low Scores Bug)
    print("\n[2] Testando HitPredictor ('brazil')...")
    predictor = HitPredictor('brazil')
    print(f"    Gênero resolvido: {predictor.genre}")
    
    # Check Ranges
    bpm_range = predictor.ideal_ranges.get('bpm')
    print(f"    Range BPM: {bpm_range}")
    
    if predictor.genre == 'pop_urban_brasil' and bpm_range == (90, 150):
        print("    ✅ SUCESSO! Mapeamento 'brazil' -> 'pop_urban_brasil' funcionando.")
    else:
        print("    ❌ FALHA! HitPredictor não assumiu as regras do Pop Urban.")
        
    # 3. Test Prediction
    print("\n[3] Testando Predição (Simulada)...")
    dummy_features = {
        'bpm': 130, 'energy': 0.8, 'danceability': 0.8, 
        'valence': 0.8, 'loudness': -5.0,
        'acousticness': 0.1, 'instrumentalness': 0.0,
        'liveness': 0.1, 'speechiness': 0.05,
        'brightness': 3000, 'dynamic_variation': 0.2
    }
    result = predictor.predict(dummy_features)
    print(f"    Score Simulado: {result['hit_score']}")
    print(f"    Método usado: {result['prediction_method']}")
    
    if result['hit_score'] > 70:
        print("    ✅ SUCESSO! Predição alta para dados de hit.")
    else:
        print("    ❌ FALHA! Score baixo mesmo com features boas.")
        
except ImportError as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: {e}")
    print("O backend parece estar quebrado ou incompleto.")
