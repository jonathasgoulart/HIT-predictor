"""
Coletor de Playlists Editoriais do Spotify
Coleta musicas de playlists curadas = HITS VERIFICADOS
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pathlib import Path
import time

def setup_spotify():
    """Configura autenticacao do Spotify"""
    print("="*70)
    print("CONFIGURACAO SPOTIFY API")
    print("="*70 + "\n")
    
    # Tenta carregar credenciais
    try:
        from spotify_auth import get_spotify_client
        sp = get_spotify_client()
        print("OK Autenticacao configurada!\n")
        return sp
    except Exception as e:
        print(f"Erro ao configurar: {e}\n")
        print("SOLUCAO:")
        print("1. Acesse: https://developer.spotify.com/dashboard")
        print("2. Crie um app")
        print("3. Copie Client ID e Client Secret")
        print("4. Configure em ml/spotify_auth.py")
        return None

def collect_playlist_tracks(sp, playlist_id, playlist_name):
    """Coleta todas as musicas de uma playlist"""
    print(f"\nColetando: {playlist_name}")
    print(f"Playlist ID: {playlist_id}")
    
    try:
        # Pega informacoes da playlist
        playlist = sp.playlist(playlist_id)
        print(f"  Seguidores: {playlist['followers']['total']:,}")
        
        # Coleta todas as tracks
        tracks = []
        results = sp.playlist_tracks(playlist_id)
        
        while results:
            for item in results['items']:
                if item['track'] is None:
                    continue
                
                track = item['track']
                
                # Pega audio features
                try:
                    features = sp.audio_features(track['id'])[0]
                    if features is None:
                        continue
                    
                    track_data = {
                        'track_id': track['id'],
                        'track_name': track['name'],
                        'artist': ', '.join([a['name'] for a in track['artists']]),
                        'popularity': track['popularity'],
                        'bpm': features['tempo'],
                        'energy': features['energy'],
                        'danceability': features['danceability'],
                        'valence': features['valence'],
                        'acousticness': features['acousticness'],
                        'instrumentalness': features['instrumentalness'],
                        'liveness': features['liveness'],
                        'speechiness': features['speechiness'],
                        'loudness': features['loudness'],
                        'is_hit': 1,  # Playlist editorial = HIT
                        'source_playlist': playlist_name
                    }
                    
                    tracks.append(track_data)
                    
                except Exception as e:
                    continue
            
            # Proxima pagina
            if results['next']:
                results = sp.next(results)
            else:
                break
            
            time.sleep(0.1)  # Rate limiting
        
        print(f"  Coletadas: {len(tracks)} musicas")
        return tracks
        
    except Exception as e:
        print(f"  ERRO: {e}")
        return []

def collect_editorial_playlists():
    """Coleta musicas de playlists editoriais do Spotify"""
    
    # Configura Spotify
    sp = setup_spotify()
    
    if sp is None:
        print("\nNao foi possivel conectar ao Spotify API")
        return None
    
    print("="*70)
    print("COLETA DE PLAYLISTS EDITORIAIS")
    print("="*70 + "\n")
    
    # Playlists editoriais verificadas
    playlists = {
        'mpb': [
            ('37i9dQZF1DX0FOF1IUWK1W', 'MPB Hits'),
            ('37i9dQZF1DWZVdPqvgJJZW', 'Nova MPB'),
        ],
        'rnb_brasil': [
            ('37i9dQZF1DX6VdMW310YC7', 'R&B Brasil'),
            ('37i9dQZF1DWYmmr74INQlb', 'Soul Brasil'),
        ]
    }
    
    all_tracks = {'mpb': [], 'rnb_brasil': []}
    
    for genre, playlist_list in playlists.items():
        print(f"\n{'='*70}")
        print(f"GENERO: {genre.upper()}")
        print(f"{'='*70}")
        
        for playlist_id, playlist_name in playlist_list:
            tracks = collect_playlist_tracks(sp, playlist_id, playlist_name)
            all_tracks[genre].extend(tracks)
            time.sleep(1)  # Rate limiting
    
    return all_tracks

def save_playlist_data(all_tracks):
    """Salva dados coletados"""
    output_dir = Path(__file__).parent / 'datasets' / 'spotify_playlists'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"\n\n{'='*70}")
    print("SALVANDO DADOS")
    print(f"{'='*70}\n")
    
    for genre, tracks in all_tracks.items():
        if not tracks:
            print(f"{genre}: Nenhuma musica coletada")
            continue
        
        df = pd.DataFrame(tracks)
        
        # Remove duplicatas
        df = df.drop_duplicates(subset=['track_id'])
        
        output_file = output_dir / f'{genre}_editorial_hits.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"[OK] {genre.upper()}: {len(df)} musicas -> {output_file.name}")
    
    print(f"\n{'='*70}")
    print("COLETA CONCLUIDA!")
    print(f"{'='*70}")
    print(f"\nArquivos salvos em: {output_dir}")
    print("\nProximo passo:")
    print("  python ml/retrain_with_spotify_playlists.py")

def main():
    all_tracks = collect_editorial_playlists()
    
    if all_tracks:
        save_playlist_data(all_tracks)
    else:
        print("\nNenhum dado coletado. Verifique configuracao do Spotify API.")

if __name__ == "__main__":
    main()
