"""
Feature Engineering Pipeline
Adiciona features derivadas para melhorar performance do modelo ML
"""
import pandas as pd
import numpy as np
from pathlib import Path

def engineer_features(df):
    """
    Adiciona features derivadas ao dataset
    
    Args:
        df: DataFrame com features básicas
        
    Returns:
        DataFrame com features adicionais
    """
    df_enhanced = df.copy()
    
    # 1. Groove Factor (combinação de danceability, energy e BPM)
    # Músicas com bom groove têm danceability alta, energy moderada-alta e BPM adequado
    if all(col in df.columns for col in ['danceability', 'energy', 'bpm']):
        # Normaliza BPM para 0-1 (assumindo range 60-180)
        bpm_normalized = (df['bpm'].clip(60, 180) - 60) / 120
        df_enhanced['groove_factor'] = (
            df['danceability'] * 0.5 + 
            df['energy'] * 0.3 + 
            bpm_normalized * 0.2
        )
    
    # 2. Commercial Appeal (loudness + valence)
    # Músicas comerciais tendem a ser mais altas e positivas
    if all(col in df.columns for col in ['loudness', 'valence']):
        # Normaliza loudness de -60 a 0 dB para 0-1
        loudness_normalized = (df['loudness'].clip(-60, 0) + 60) / 60
        df_enhanced['commercial_appeal'] = (
            loudness_normalized * 0.6 + 
            df['valence'] * 0.4
        )
    
    # 3. Energy-Dance Ratio
    # Relação entre energia e danceability (detecta músicas energéticas mas não dançantes)
    if all(col in df.columns for col in ['energy', 'danceability']):
        # Evita divisão por zero
        df_enhanced['energy_dance_ratio'] = df['energy'] / (df['danceability'] + 0.01)
    
    # 4. Vocal Presence (inverso de instrumentalness)
    if 'instrumentalness' in df.columns:
        df_enhanced['vocal_presence'] = 1 - df['instrumentalness']
    
    # 5. BPM Category (categórico -> numérico)
    if 'bpm' in df.columns:
        df_enhanced['bpm_category'] = pd.cut(
            df['bpm'], 
            bins=[0, 90, 120, 140, 200],
            labels=[0, 1, 2, 3]  # slow, medium, fast, very_fast
        ).astype(float)
    
    # 6. Loudness Normalized (0-1)
    if 'loudness' in df.columns:
        df_enhanced['loudness_normalized'] = (df['loudness'].clip(-60, 0) + 60) / 60
    
    # 7. Spectral Complexity (se tivermos brightness e dynamic_variation)
    # Nota: Esses campos podem não existir em todos os datasets
    if all(col in df.columns for col in ['brightness', 'dynamic_variation']):
        # Normaliza brightness (assumindo range 1000-4000 Hz)
        brightness_norm = (df['brightness'].clip(1000, 4000) - 1000) / 3000
        df_enhanced['spectral_complexity'] = brightness_norm * df['dynamic_variation']
    
    # 8. Hit Potential Score (combinação heurística)
    # Baseado nas correlações conhecidas
    if all(col in df.columns for col in ['energy', 'danceability', 'valence']):
        df_enhanced['hit_potential_score'] = (
            df['energy'] * 0.3 +
            df['danceability'] * 0.4 +
            df['valence'] * 0.2 +
            df_enhanced.get('commercial_appeal', 0.5) * 0.1
        )
    
    # 9. Acoustic-Electric Balance
    if 'acousticness' in df.columns:
        df_enhanced['acoustic_electric_balance'] = 1 - abs(df['acousticness'] - 0.5) * 2
    
    # 10. Speech-Music Ratio
    if 'speechiness' in df.columns:
        # Músicas com muita fala (>0.33) são provavelmente podcasts/spoken word
        df_enhanced['is_music'] = (df['speechiness'] < 0.33).astype(float)
    
    return df_enhanced

def add_features_to_dataset(input_file, output_file=None):
    """
    Adiciona features a um dataset e salva
    
    Args:
        input_file: Caminho do CSV de entrada
        output_file: Caminho do CSV de saída (opcional)
    """
    print(f"Carregando {input_file.name}...")
    df = pd.read_csv(input_file)
    
    print(f"  Antes: {len(df.columns)} colunas")
    
    # Adiciona features
    df_enhanced = engineer_features(df)
    
    new_features = set(df_enhanced.columns) - set(df.columns)
    print(f"  Depois: {len(df_enhanced.columns)} colunas")
    print(f"  Novas features: {', '.join(sorted(new_features))}")
    
    # Salva
    if output_file is None:
        output_file = input_file.parent / f"{input_file.stem}_enhanced.csv"
    
    df_enhanced.to_csv(output_file, index=False, encoding='utf-8')
    print(f"  Salvo: {output_file.name}\n")
    
    return df_enhanced

def process_all_ml_ready_datasets():
    """Processa todos os datasets em ml_ready/"""
    ml_ready_dir = Path(__file__).parent / 'datasets' / 'ml_ready'
    
    if not ml_ready_dir.exists():
        print(f"Diretorio {ml_ready_dir} nao encontrado!")
        return
    
    print("="*70)
    print("FEATURE ENGINEERING - ADICIONAR FEATURES DERIVADAS")
    print("="*70 + "\n")
    
    csv_files = list(ml_ready_dir.glob('*_ml_ready.csv'))
    
    if not csv_files:
        print("Nenhum arquivo *_ml_ready.csv encontrado!")
        return
    
    print(f"Encontrados {len(csv_files)} datasets para processar\n")
    
    for csv_file in csv_files:
        add_features_to_dataset(csv_file)
    
    print("="*70)
    print("FEATURE ENGINEERING CONCLUIDO!")
    print("="*70)
    print("\nDatasets com features adicionadas estao em:")
    print("  ml/datasets/ml_ready/*_enhanced.csv")
    print("\nProximo passo:")
    print("  python ml/train_master_models.py --use-enhanced")

if __name__ == "__main__":
    process_all_ml_ready_datasets()
