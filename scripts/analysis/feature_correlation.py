"""
Analise de Correlacao de Features por Genero
Identifica quais features realmente predizem hits
"""
import pandas as pd
import numpy as np
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

def analyze_genre(genre_name, dataset_path):
    """Analisa correlacoes para um genero"""
    print(f"\n{'='*70}")
    print(f"ANALISE: {genre_name.upper()}")
    print(f"{'='*70}\n")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset nao encontrado: {dataset_path}")
        return None
    
    df = pd.read_csv(dataset_path)
    
    # Features para analisar
    features = ['bpm', 'energy', 'danceability', 'valence', 
                'acousticness', 'instrumentalness', 'liveness',
                'speechiness', 'loudness']
    
    # Filtra apenas features que existem
    available_features = [f for f in features if f in df.columns]
    
    print(f"Total de musicas: {len(df)}")
    print(f"Hits: {df['is_hit'].sum()} ({df['is_hit'].mean()*100:.1f}%)")
    print(f"Nao-hits: {(1-df['is_hit']).sum()}")
    
    # Calcula correlacoes
    print(f"\n[CORRELACOES COM IS_HIT]")
    print(f"{'Feature':<20} {'Correlacao':<12} {'Interpretacao'}")
    print(f"{'-'*70}")
    
    correlations = {}
    for feature in available_features:
        corr = df[feature].corr(df['is_hit'])
        correlations[feature] = corr
        
        # Interpretacao
        if abs(corr) < 0.05:
            interp = "SEM EFEITO (ignorar)"
        elif abs(corr) < 0.1:
            interp = "Efeito FRACO"
        elif abs(corr) < 0.2:
            interp = "Efeito MODERADO"
        else:
            interp = "Efeito FORTE"
        
        if corr < 0:
            interp += " (NEGATIVO)"
        
        print(f"{feature:<20} {corr:>+7.3f}      {interp}")
    
    # Estatisticas por grupo (Hit vs Nao-Hit)
    print(f"\n[COMPARACAO HITS vs NAO-HITS]")
    print(f"{'Feature':<20} {'Hits (Avg)':<15} {'Nao-Hits (Avg)':<15} {'Diferenca'}")
    print(f"{'-'*70}")
    
    insights = {}
    for feature in available_features:
        hit_mean = df[df['is_hit'] == 1][feature].mean()
        non_hit_mean = df[df['is_hit'] == 0][feature].mean()
        diff = hit_mean - non_hit_mean
        
        insights[feature] = {
            'hit_mean': hit_mean,
            'non_hit_mean': non_hit_mean,
            'diff': diff
        }
        
        print(f"{feature:<20} {hit_mean:>10.2f}      {non_hit_mean:>10.2f}         {diff:>+7.2f}")
    
    # Top 3 features mais importantes
    sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    print(f"\n[TOP 3 FEATURES MAIS IMPORTANTES]")
    for i, (feature, corr) in enumerate(sorted_corr[:3], 1):
        print(f"{i}. {feature}: {corr:+.3f}")
        hit_avg = insights[feature]['hit_mean']
        non_hit_avg = insights[feature]['non_hit_mean']
        
        if corr > 0:
            print(f"   -> Hits tem MAIS {feature} ({hit_avg:.2f} vs {non_hit_avg:.2f})")
        else:
            print(f"   -> Hits tem MENOS {feature} ({hit_avg:.2f} vs {non_hit_avg:.2f})")
    
    # Features inuteis (correlacao quase zero)
    useless = [(f, c) for f, c in correlations.items() if abs(c) < 0.05]
    if useless:
        print(f"\n[FEATURES INUTEIS (Correlacao < 0.05)]")
        for feature, corr in useless:
            print(f"   - {feature} ({corr:+.3f}) - pode REMOVER dos pesos")
    
    # Sugestao de ranges ideais (95% dos hits)
    print(f"\n[RANGES IDEAIS SUGERIDOS (95% dos hits)]")
    print(f"{'Feature':<20} {'Min':<10} {'Max':<10} {'Nota'}")
    print(f"{'-'*70}")
    
    hit_data = df[df['is_hit'] == 1]
    for feature in available_features:
        p2_5 = hit_data[feature].quantile(0.025)
        p97_5 = hit_data[feature].quantile(0.975)
        
        # Arredonda para facilitar
        if feature == 'bpm':
            p2_5 = round(p2_5)
            p97_5 = round(p97_5)
        else:
            p2_5 = round(p2_5, 2)
            p97_5 = round(p97_5, 2)
        
        print(f"{feature:<20} {p2_5!s:<10} {p97_5!s:<10} Cobre 95% dos hits")
    
    return {
        'genre': genre_name,
        'correlations': correlations,
        'insights': insights,
        'top_features': sorted_corr[:3]
    }

def main():
    print("="*70)
    print("ANALISE DE CORRELACAO - TODOS OS GENEROS")
    print("="*70)
    
    datasets_dir = os.path.join(project_root, 'ml', 'datasets')
    
    genres = {
        'mpb': 'kaggle_mpb_ml.csv',
        'brazil': 'kaggle_pop_urban_brasil_ml.csv',
        'sertanejo': 'kaggle_sertanejo_ml.csv',
        'pagode': 'kaggle_pagode_ml.csv',
        'samba': 'kaggle_samba_ml.csv',
        'forro': 'kaggle_forro_ml.csv'
    }
    
    all_results = []
    
    for genre_id, filename in genres.items():
        dataset_path = os.path.join(datasets_dir, filename)
        result = analyze_genre(genre_id, dataset_path)
        if result:
            all_results.append(result)
    
    # Resumo comparativo
    print(f"\n\n{'='*70}")
    print("RESUMO COMPARATIVO - TOP FEATURE POR GENERO")
    print(f"{'='*70}\n")
    
    print(f"{'Genero':<15} {'Top Feature':<20} {'Correlacao':<12} {'Acao Sugerida'}")
    print(f"{'-'*70}")
    
    for result in all_results:
        top_feature, top_corr = result['top_features'][0]
        
        if abs(top_corr) < 0.1:
            action = "ML fraco, usar heuristica"
        elif abs(top_corr) < 0.2:
            action = "Aumentar peso desta feature"
        else:
            action = "PRIORIZAR esta feature!"
        
        print(f"{result['genre']:<15} {top_feature:<20} {top_corr:>+7.3f}      {action}")
    
    # Identificar features universalmente inuteis
    print(f"\n[FEATURES FRACAS EM TODOS OS GENEROS]")
    
    feature_names = ['bpm', 'energy', 'danceability', 'valence', 
                     'acousticness', 'instrumentalness', 'liveness',
                     'speechiness', 'loudness']
    
    for feature in feature_names:
        avg_corr = np.mean([r['correlations'].get(feature, 0) for r in all_results])
        max_corr = max([abs(r['correlations'].get(feature, 0)) for r in all_results])
        
        if max_corr < 0.1:
            print(f"   - {feature}: Correlacao media {avg_corr:+.3f}, max {max_corr:.3f} - CONSIDERE REMOVER")

if __name__ == "__main__":
    main()
