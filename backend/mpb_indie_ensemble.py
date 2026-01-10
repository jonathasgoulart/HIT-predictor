"""
Ensemble MPB Indie: Heurística + ML
Combina regras especializadas com modelo ML para melhor accuracy
"""
import numpy as np

def calculate_indie_heuristic_score(features):
    """
    Calcula score heurístico específico para MPB Indie
    Baseado em características conhecidas do gênero
    """
    score = 50  # Base neutra
    
    # Feature 1: Acousticness (indie tende a ser mais acústico)
    acousticness = features.get('acousticness', 0.5)
    if acousticness > 0.6:
        score += 15  # Indie acústico tem mais chance de hit
    elif acousticness < 0.3:
        score -= 10  # Muito eletrônico = menos indie típico
    
    # Feature 2: Energy vs Valence (indie melancólico mas positivo)
    energy = features.get('energy', 0.5)
    valence = features.get('valence', 0.5)
    
    if energy < 0.6 and valence > 0.5:
        score += 15  # Indie melancólico mas otimista = hit
    elif energy > 0.7 and valence < 0.4:
        score -= 10  # Muito agressivo = menos indie
    
    # Feature 3: BPM (sweet spot indie)
    bpm = features.get('bpm', 110)
    if 95 <= bpm <= 125:
        score += 10  # BPM ideal para indie
    elif bpm < 80 or bpm > 140:
        score -= 10  # Muito lento ou rápido
    
    # Feature 4: Speechiness (indie tem letras, mas não é rap)
    speechiness = features.get('speechiness', 0.1)
    if 0.05 <= speechiness <= 0.2:
        score += 10  # Boa quantidade de letra
    elif speechiness > 0.3:
        score -= 15  # Muito rap/falado
    
    # Feature 5: Danceability (indie moderado)
    danceability = features.get('danceability', 0.5)
    if 0.4 <= danceability <= 0.7:
        score += 10  # Nem muito nem pouco
    elif danceability > 0.8:
        score -= 10  # Muito dançante = menos indie
    
    # Feature 6: Instrumentalness (indie tem vocal)
    instrumentalness = features.get('instrumentalness', 0.1)
    if instrumentalness < 0.2:
        score += 5  # Vocal presente
    elif instrumentalness > 0.5:
        score -= 10  # Muito instrumental
    
    # Feature 7: Loudness (indie tende a ser mais suave)
    loudness = features.get('loudness', -8)
    if -10 <= loudness <= -5:
        score += 5  # Loudness ideal indie
    elif loudness > -3:
        score -= 10  # Muito alto = menos indie
    
    # Normaliza para 0-100
    final_score = min(max(score, 0), 100)
    
    return final_score


def predict_mpb_indie_ensemble(features, ml_model=None):
    """
    Predição ensemble para MPB Indie
    Combina ML (40%) + Heurística (60%)
    
    Args:
        features: dict com features de áudio
        ml_model: modelo ML treinado (opcional)
    
    Returns:
        dict com score final e breakdown
    """
    # 1. Score Heurístico
    heuristic_score = calculate_indie_heuristic_score(features)
    
    # 2. Score ML (se modelo disponível)
    ml_score = 50  # Default neutro
    ml_available = False
    
    if ml_model is not None:
        try:
            # Prepara features para ML
            ml_features_order = ['bpm', 'energy', 'danceability', 'loudness', 'valence',
                                'acousticness', 'instrumentalness', 'liveness', 'speechiness']
            
            feature_vector = []
            for feat in ml_features_order:
                feature_vector.append(features.get(feat, 0.5))
            
            # Predição ML
            ml_proba = ml_model.predict_proba([feature_vector])[0][1]
            ml_score = ml_proba * 100
            ml_available = True
        except Exception as e:
            print(f"[ENSEMBLE] Erro no ML: {e}, usando apenas heurística")
            ml_score = heuristic_score
    
    # 3. Combinação Ensemble
    if ml_available:
        # 40% ML + 60% Heurística
        # (Mais peso na heurística porque ML não está funcionando bem)
        final_score = (0.4 * ml_score) + (0.6 * heuristic_score)
        method = 'ensemble_ml_heuristic'
    else:
        # Apenas heurística
        final_score = heuristic_score
        method = 'heuristic_only'
    
    # Arredonda
    final_score = int(round(final_score))
    
    # Breakdown detalhado
    breakdown = {
        'final_score': final_score,
        'method': method,
        'heuristic_score': int(round(heuristic_score)),
        'ml_score': int(round(ml_score)) if ml_available else None,
        'weights': {
            'ml': 0.4 if ml_available else 0,
            'heuristic': 0.6 if ml_available else 1.0
        },
        'heuristic_factors': {
            'acousticness': features.get('acousticness', 0.5),
            'energy_valence_balance': f"E:{features.get('energy', 0.5):.2f} V:{features.get('valence', 0.5):.2f}",
            'bpm': features.get('bpm', 110),
            'speechiness': features.get('speechiness', 0.1),
            'danceability': features.get('danceability', 0.5)
        }
    }
    
    return breakdown


# Exemplo de uso
if __name__ == "__main__":
    # Teste com música exemplo
    test_features = {
        'bpm': 110,
        'energy': 0.55,
        'danceability': 0.6,
        'loudness': -7,
        'valence': 0.65,
        'acousticness': 0.7,
        'instrumentalness': 0.1,
        'liveness': 0.15,
        'speechiness': 0.12
    }
    
    print("\n" + "="*70)
    print("TESTE ENSEMBLE MPB INDIE")
    print("="*70 + "\n")
    
    result = predict_mpb_indie_ensemble(test_features)
    
    print(f"Score Final: {result['final_score']}")
    print(f"Método: {result['method']}")
    print(f"Score Heurístico: {result['heuristic_score']}")
    print(f"Score ML: {result['ml_score']}")
    print(f"\nPesos:")
    print(f"  ML: {result['weights']['ml']:.0%}")
    print(f"  Heurística: {result['weights']['heuristic']:.0%}")
    print(f"\nFatores Heurísticos:")
    for factor, value in result['heuristic_factors'].items():
        print(f"  {factor}: {value}")
    
    print("\n" + "="*70)
