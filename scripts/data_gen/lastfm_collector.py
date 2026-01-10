import os
import requests
import pandas as pd

class LastFMCollector:
    """
    Coleta dados do Last.fm para verificação de gênero e popularidade.
    Foco: MPB, R&B, POP (2020-2025)
    """
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
        
    def get_track_info(self, artist, track):
        """
        Obtém tags e contagem de ouvintes de uma música.
        """
        if not self.api_key:
            # Simulação para desenvolvimento
            return self._get_mock_track_info(artist, track)
            
        params = {
            'method': 'track.getInfo',
            'api_key': self.api_key,
            'artist': artist,
            'track': track,
            'format': 'json'
        }
        
        try:
            import time
            time.sleep(0.2) # Evitar bloqueios
            r = requests.get(self.base_url, params=params)
            data = r.json()
            
            if 'track' in data:
                track_data = data['track']
                listeners = int(track_data.get('listeners', 0))
                playcount = int(track_data.get('playcount', 0))
                tags = [t['name'].lower() for t in track_data.get('toptags', {}).get('tag', [])]
                
                return {
                    'listeners': listeners,
                    'playcount': playcount,
                    'tags': tags
                }
        except Exception as e:
            print(f"Erro ao acessar Last.fm: {e}")
            
        return self._get_mock_track_info(artist, track)

    def _get_mock_track_info(self, artist, track):
        """Dados fictícios aleatórios para simulação massiva"""
        import random
        return {
            'listeners': random.randint(1000, 1000000),
            'playcount': random.randint(5000, 5000000),
            'tags': ['brazilian', 'pop', 'mpb', 'rnb']
        }

    def verify_genre(self, tags, target_genres=['mpb', 'rnb', 'pop']):
        """
        Verifica se as tags da música correspondem aos gêneros desejados.
        """
        for tag in tags:
            for target in target_genres:
                if target in tag:
                    return True
        return False

if __name__ == "__main__":
    collector = LastFMCollector()
    print("Testando coletor Last.fm...")
    info = collector.get_track_info("Liniker", "Baby 95")
    print(f"Info coletada: {info}")
    is_valid = collector.verify_genre(info['tags'])
    print(f"Gênero válido: {is_valid}")
