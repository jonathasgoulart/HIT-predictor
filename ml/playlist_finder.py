"""
Descoberta de playlists brasileiras por gênero
"""
from spotify_auth import SpotifyAuth

class PlaylistFinder:
    """Encontra playlists brasileiras relevantes por gênero"""
    
    # Playlists curadas manualmente (IDs oficiais do Spotify)
    CURATED_PLAYLISTS = {
        'mpb': [
            '37i9dQZF1DWWvQj8b1Hx7B',  # MPB Hits
            '37i9dQZF1DX0HRj9P7NxSu',  # Nova MPB
            '37i9dQZF1DX2pNI6eOAWKP',  # MPB Clássica
        ],
        'rnb_brasil': [
            '37i9dQZF1DX6PKX5dyBKeq',  # R&B Brasil
            '37i9dQZF1DWYmmr74INQlb',  # Soul Brasil
        ],
        'funk': [
            '37i9dQZF1DX0FOF1IUWK1W',  # Funk Hits
            '37i9dQZF1DWTKessAUp8JA',  # Baile Funk
        ],
        'sertanejo': [
            '37i9dQZF1DXdSjVZQzv2tl',  # Sertanejo Hits
            '37i9dQZF1DX0lkwbJPTvNY',  # Sertanejo Universitário
        ],
        'pagode': [
            '37i9dQZF1DWWqNV5cS50j6',  # Pagode
            '37i9dQZF1DX70RN3TfWWJh',  # Pagode Romântico
        ],
        'pop_brasil': [
            '37i9dQZF1DX0FOF1IUWK1W',  # Pop Brasil
            '37i9dQZF1DWZd79rJ6a7lp',  # Top Brasil
        ]
    }
    
    def __init__(self, spotify_auth):
        """
        Inicializa finder
        
        Args:
            spotify_auth: Instância de SpotifyAuth
        """
        self.spotify = spotify_auth.get_client()
    
    def get_playlists_for_genre(self, genre):
        """
        Retorna lista de playlists para um gênero
        
        Args:
            genre: Nome do gênero ('mpb', 'rnb_brasil', etc.)
            
        Returns:
            Lista de dicionários com informações das playlists
        """
        if genre not in self.CURATED_PLAYLISTS:
            raise ValueError(f"Gênero '{genre}' não suportado. Use: {list(self.CURATED_PLAYLISTS.keys())}")
        
        playlist_ids = self.CURATED_PLAYLISTS[genre]
        playlists = []
        
        for playlist_id in playlist_ids:
            try:
                playlist = self.spotify.playlist(playlist_id)
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'total_tracks': playlist['tracks']['total'],
                    'url': playlist['external_urls']['spotify']
                })
                print(f"  ✓ {playlist['name']} ({playlist['tracks']['total']} músicas)")
            except Exception as e:
                print(f"  ✗ Erro ao buscar playlist {playlist_id}: {e}")
        
        return playlists
    
    def search_additional_playlists(self, genre_keywords, limit=10):
        """
        Busca playlists adicionais por palavras-chave
        
        Args:
            genre_keywords: Lista de palavras-chave (ex: ['mpb', 'brasil'])
            limit: Número máximo de playlists a retornar
            
        Returns:
            Lista de playlists encontradas
        """
        query = ' '.join(genre_keywords)
        results = self.spotify.search(q=query, type='playlist', market='BR', limit=limit)
        
        playlists = []
        for item in results['playlists']['items']:
            playlists.append({
                'id': item['id'],
                'name': item['name'],
                'total_tracks': item['tracks']['total'],
                'url': item['external_urls']['spotify']
            })
        
        return playlists
    
    def get_all_available_genres(self):
        """Retorna lista de gêneros disponíveis"""
        return list(self.CURATED_PLAYLISTS.keys())

if __name__ == '__main__':
    print("=== Buscador de Playlists ===\n")
    
    try:
        auth = SpotifyAuth()
        finder = PlaylistFinder(auth)
        
        print("Gêneros disponíveis:", finder.get_all_available_genres())
        print("\nBuscando playlists de MPB...")
        
        playlists = finder.get_playlists_for_genre('mpb')
        print(f"\nEncontradas {len(playlists)} playlists de MPB")
        
    except Exception as e:
        print(f"Erro: {e}")
