import os
import pandas as pd
import sys
from pathlib import Path

# Adiciona o diretório atual ao path para permitir execução de qualquer lugar
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

try:
    from youtube_collector import YouTubeCollector
    from lastfm_collector import LastFMCollector
    from audio_feature_extractor import AudioFeatureExtractor
    from lyric_analyzer import LyricAnalyzer
except ImportError:
    from scripts.data_gen.youtube_collector import YouTubeCollector
    from scripts.data_gen.lastfm_collector import LastFMCollector
    from scripts.data_gen.audio_feature_extractor import AudioFeatureExtractor
    from scripts.data_gen.lyric_analyzer import LyricAnalyzer

class RobustDatabaseBuilder:
    """
    Construtor mestre da Base de Dados Brasileira v2.
    Orquestra a coleta de hits, verificação de gênero e extração de áudio.
    """
    def __init__(self):
        self.yt = YouTubeCollector()
        self.lfm = LastFMCollector()
        self.afe = AudioFeatureExtractor()
        self.la = LyricAnalyzer()
        
        self.output_path = 'ml/datasets/brazilian_hits_v2.csv'
        os.makedirs('ml/datasets', exist_ok=True)

    def run(self, target_count_per_genre=2000):
        print("\n" + "="*50)
        print("INICIANDO CONSTRUÇÃO DA BASE DE DADOS V2 (ULTRA ESCALA)")
        print(f"Meta: {target_count_per_genre} músicas por categoria (Total: {target_count_per_genre*3})")
        print("Foco: MPB, R&B, POP (2020-2025)")
        print("="*50 + "\n")

        # 1. Coleta do YouTube
        all_songs = []
        for genre in ['mpb', 'rnb', 'pop']:
            df_genre = self.yt.search_trending_hits(genre, target_count=target_count_per_genre)
            all_songs.append(df_genre)
        
        df = pd.concat(all_songs, ignore_index=True).drop_duplicates(subset=['track_name', 'artist'])
        print(f"\nTotal único coletado: {len(df)} músicas.")

        # 2. Enriquecimento com Last.fm e Analysis de Letra
        print("\nEnriquecendo dados com Last.fm e Análise de Letras...")
        enriched_data = []
        total = len(df)
        for i, (idx, row) in enumerate(df.iterrows()):
            if i > 0 and i % 100 == 0:
                print(f"  > Processadas {i} de {total} músicas...")
                
            info = self.lfm.get_track_info(row['artist'], row['track_name'])
            
            # Converter row para dict para permitir novos campos
            entry = row.to_dict()
            entry['listeners'] = info['listeners']
            entry['playcount'] = info['playcount']
            entry['tags'] = ",".join(info['tags']) if isinstance(info['tags'], list) else info['tags']
            
            # Nova: Análise de Letras
            lyric_info = self.la.analyze_track(row['artist'], row['track_name'])
            entry.update(lyric_info)
            
            enriched_data.append(entry)
        
        df = pd.DataFrame(enriched_data)

        # 3. Extração de Características de Áudio (se houver arquivo)
        # Nota: Em uma base real, os arquivos de áudio precisariam estar em 'uploads/'
        # com nomes padrão 'artista - musica.mp3'
        print("\nExtraindo características de áudio locais...")
        audio_features_list = []
        for _, row in df.iterrows():
            # Tenta encontrar o arquivo
            filename = f"{row['artist']} - {row['track_name']}.mp3"
            audio_path = os.path.join('uploads', filename)
            
            features = None
            if os.path.exists(audio_path):
                features = self.afe.extract_features(audio_path)
            
            if not features:
                # Se não encontrar o áudio, atribui valores médios para o gênero para não quebrar a base
                features = self._get_default_features(row['genre'])
            
            # Correção: Converter row para dict antes do update para garantir novas colunas
            row_data = row.to_dict()
            row_data.update(features)
            audio_features_list.append(row_data)
            
        final_df = pd.DataFrame(audio_features_list)

        final_df = pd.DataFrame(audio_features_list)

        # 4. Phase 5: Clusterização de Sub-gêneros (Hierarquia)
        print("\nCalculando sub-gêneros via K-Means Clustering...")
        try:
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            # Colunas numéricas para o cluster
            cluster_features = ['bpm', 'energy', 'danceability', 'valence', 'acousticness', 'loudness', 'lyric_positivity', 'slang_count']
            
            final_df['sub_genre'] = ""
            for genre in ['mpb', 'rnb', 'pop']:
                mask = final_df['genre'] == genre
                if mask.any():
                    genre_data = final_df[mask][cluster_features]
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(genre_data)
                    
                    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                    clusters = kmeans.fit_predict(scaled_data)
                    final_df.loc[mask, 'sub_genre'] = [f"{genre}_{c+1}" for c in clusters]
            print("  > Sub-gêneros calculados com sucesso.")
        except Exception as e:
            print(f"  > Aviso: Erro na clusterização: {e}. Usando gênero principal como sub-gênero.")
            final_df['sub_genre'] = final_df['genre']

        # 5. Salva a base final
        final_df.to_csv(self.output_path, index=False)
        print(f"\n" + "="*50)
        print(f"SUCESSO! Base de dados salva em: {self.output_path}")
        print(f"Total de registros: {len(final_df)}")
        print("="*50 + "\n")

    def _get_default_features(self, genre):
        """Retorna características padrão baseadas no gênero para preenchimento"""
        defaults = {
            'mpb': {
                'bpm': 100, 'energy': 0.4, 'danceability': 0.5, 'valence': 0.5, 
                'acousticness': 0.7, 'loudness': -10, 'key': 'C', 'mode': 1,
                'spectral_flatness': 0.001, 'zero_crossing_rate': 0.05, 'mfcc_mean': -10,
                'spectral_contrast': 20.0, 'poly_features': 0.1
            },
            'rnb': {
                'bpm': 90, 'energy': 0.6, 'danceability': 0.7, 'valence': 0.6, 
                'acousticness': 0.3, 'loudness': -7, 'key': 'A', 'mode': 0,
                'spectral_flatness': 0.005, 'zero_crossing_rate': 0.07, 'mfcc_mean': -5,
                'spectral_contrast': 15.0, 'poly_features': 0.2
            },
            'pop': {
                'bpm': 124, 'energy': 0.8, 'danceability': 0.8, 'valence': 0.7, 
                'acousticness': 0.1, 'loudness': -5, 'key': 'G', 'mode': 1,
                'spectral_flatness': 0.01, 'zero_crossing_rate': 0.1, 'mfcc_mean': 0,
                'spectral_contrast': 12.0, 'poly_features': 0.3
            }
        }
        feat = defaults.get(genre, defaults['pop']).copy()
        # Adiciona campos faltantes
        feat.update({'instrumentalness': 0.05, 'liveness': 0.1, 'speechiness': 0.1})
        return feat

if __name__ == "__main__":
    builder = RobustDatabaseBuilder()
    builder.run(target_count_per_genre=2000)
