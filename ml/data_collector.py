"""
Coletor de dados de músicas do Spotify
Estratégia: 500 populares + 500 médias (1K-1M plays) por gênero
"""
import pandas as pd
import time
from datetime import datetime
from spotify_auth import SpotifyAuth
from playlist_finder import PlaylistFinder

class DataCollector:
    """Coleta dados de músicas do Spotify com estratégia balanceada"""
    
    def __init__(self, spotify_auth):
        """
        Inicializa coletor
        
        Args:
            spotify_auth: Instância de SpotifyAuth
        """
        self.spotify = spotify_auth.get_client()
        self.finder = PlaylistFinder(spotify_auth)
        self.collected_tracks = set()  # Evita duplicatas
    
    def get_track_features(self, track_id):
        """
        Extrai features de áudio de uma track
        
        Args:
            track_id: ID da track no Spotify
            
        Returns:
            Dicionário com features ou None se erro
        """
        try:
            # Audio features do Spotify
            features = self.spotify.audio_features(track_id)[0]
            if not features:
                return None
            
            # Informações da track
            track = self.spotify.track(track_id)
            
            return {
                'track_id': track_id,
                'track_name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'popularity': track['popularity'],
                'duration_ms': features['duration_ms'],
                'bpm': features['tempo'],
                'energy': features['energy'],
                'danceability': features['danceability'],
                'valence': features['valence'],
                'acousticness': features['acousticness'],
                'instrumentalness': features['instrumentalness'],
                'liveness': features['liveness'],
                'speechiness': features['speechiness'],
                'loudness': features['loudness'],
                'key': features['key'],
                'mode': features['mode'],
                'time_signature': features['time_signature']
            }
        except Exception as e:
            print(f"  ✗ Erro ao obter features de {track_id}: {e}")
            return None
    
    def collect_from_playlist(self, playlist_id, max_tracks=None):
        """
        Coleta tracks de uma playlist
        
        Args:
            playlist_id: ID da playlist
            max_tracks: Número máximo de tracks a coletar
            
        Returns:
            Lista de features das tracks
        """
        tracks_data = []
        offset = 0
        limit = 100
        
        while True:
            try:
                results = self.spotify.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=limit,
                    fields='items(track(id,name,popularity,artists)),total'
                )
                
                if not results['items']:
                    break
                
                for item in results['items']:
                    if not item['track'] or not item['track']['id']:
                        continue
                    
                    track_id = item['track']['id']
                    
                    # Evita duplicatas
                    if track_id in self.collected_tracks:
                        continue
                    
                    # Obtém features
                    features = self.get_track_features(track_id)
                    if features:
                        tracks_data.append(features)
                        self.collected_tracks.add(track_id)
                        print(f"  ✓ {len(tracks_data)}: {features['track_name']} - {features['artist']}")
                    
                    # Limite de tracks
                    if max_tracks and len(tracks_data) >= max_tracks:
                        return tracks_data
                    
                    # Rate limiting
                    time.sleep(0.1)
                
                offset += limit
                
                # Verifica se há mais resultados
                if offset >= results['total']:
                    break
                    
            except Exception as e:
                print(f"  ✗ Erro ao coletar playlist: {e}")
                break
        
        return tracks_data
    
    def collect_balanced_dataset(self, genre, target_popular=500, target_medium=500):
        """
        Coleta dataset balanceado para um gênero
        
        Estratégia:
        - 500 tracks populares (popularidade > 70)
        - 500 tracks médias (popularidade 30-70, estimativa 1K-1M plays)
        
        Args:
            genre: Nome do gênero
            target_popular: Número de tracks populares desejadas
            target_medium: Número de tracks médias desejadas
            
        Returns:
            DataFrame com tracks coletadas
        """
        print(f"\n=== Coletando {genre.upper()} ===")
        print(f"Meta: {target_popular} populares + {target_medium} médias\n")
        
        # Busca playlists do gênero
        playlists = self.finder.get_playlists_for_genre(genre)
        
        if not playlists:
            raise ValueError(f"Nenhuma playlist encontrada para {genre}")
        
        all_tracks = []
        popular_tracks = []
        medium_tracks = []
        
        # Coleta de todas as playlists
        for playlist in playlists:
            print(f"\nColetando de: {playlist['name']}")
            tracks = self.collect_from_playlist(playlist['id'])
            all_tracks.extend(tracks)
            print(f"  Total coletado desta playlist: {len(tracks)}")
        
        print(f"\n--- Total de tracks únicas coletadas: {len(all_tracks)} ---\n")
        
        # Separa por popularidade
        for track in all_tracks:
            if track['popularity'] > 70:
                popular_tracks.append(track)
            elif 30 <= track['popularity'] <= 70:
                medium_tracks.append(track)
        
        print(f"Tracks populares (>70): {len(popular_tracks)}")
        print(f"Tracks médias (30-70): {len(medium_tracks)}")
        
        # Seleciona amostra balanceada
        import random
        
        # Populares: pega as mais populares
        popular_tracks.sort(key=lambda x: x['popularity'], reverse=True)
        selected_popular = popular_tracks[:target_popular]
        
        # Médias: amostra aleatória
        if len(medium_tracks) > target_medium:
            selected_medium = random.sample(medium_tracks, target_medium)
        else:
            selected_medium = medium_tracks
        
        # Combina
        final_tracks = selected_popular + selected_medium
        
        # Adiciona labels
        for track in final_tracks:
            # Hit = popularidade > 70
            track['is_hit'] = 1 if track['popularity'] > 70 else 0
            track['genre'] = genre
        
        print(f"\n✓ Dataset final: {len(final_tracks)} tracks")
        print(f"  - Populares (hits): {len(selected_popular)}")
        print(f"  - Médias (não-hits): {len(selected_medium)}")
        
        return pd.DataFrame(final_tracks)
    
    def save_dataset(self, df, filename):
        """
        Salva dataset em CSV
        
        Args:
            df: DataFrame com dados
            filename: Nome do arquivo
        """
        output_path = f"datasets/{filename}"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Dataset salvo em: {output_path}")
        print(f"  Total de músicas: {len(df)}")
        print(f"  Hits: {df['is_hit'].sum()}")
        print(f"  Não-hits: {len(df) - df['is_hit'].sum()}")
        
        return output_path

if __name__ == '__main__':
    print("=== Coletor de Dados Spotify ===\n")
    
    try:
        # Autenticação
        auth = SpotifyAuth()
        collector = DataCollector(auth)
        
        # Coleta MPB
        print("\n" + "="*50)
        df_mpb = collector.collect_balanced_dataset('mpb', target_popular=500, target_medium=500)
        collector.save_dataset(df_mpb, 'mpb_dataset.csv')
        
        # Coleta R&B Brasil
        print("\n" + "="*50)
        collector.collected_tracks.clear()  # Reset para novo gênero
        df_rnb = collector.collect_balanced_dataset('rnb_brasil', target_popular=500, target_medium=500)
        collector.save_dataset(df_rnb, 'rnb_brasil_dataset.csv')
        
        print("\n" + "="*50)
        print("✓ Coleta concluída com sucesso!")
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")
