"""
Calcula médias dos hits por gênero musical
"""
import pandas as pd
import os

genres = {
    'MPB': 'ml/datasets/kaggle_mpb_ml.csv',
    'R&B Brasil': 'ml/datasets/kaggle_rnb_ml.csv'
}

features = ['bpm', 'energy', 'danceability', 'valence', 
            'acousticness', 'instrumentalness', 'liveness', 
            'speechiness', 'loudness']

print('='*70)
print('MEDIAS DOS HITS POR GENERO MUSICAL')
print('='*70)

for genre, path in genres.items():
    if not os.path.exists(path):
        print(f'\n{genre}: Arquivo nao encontrado')
        continue
    
    df = pd.read_csv(path)
    hits = df[df['is_hit'] == 1]
    
    print(f'\n{genre}:')
    print('-'*70)
    print(f'Total de hits: {len(hits)}')
    print()
    
    for feat in features:
        if feat in hits.columns:
            mean_val = hits[feat].mean()
            print(f'  {feat:20s}: {mean_val:.3f}')

print('\n' + '='*70)
