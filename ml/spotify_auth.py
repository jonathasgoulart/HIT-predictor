"""
Autenticação com Spotify API
"""
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAuth:
    """Gerencia autenticação com Spotify API"""
    
    def __init__(self, client_id=None, client_secret=None):
        """
        Inicializa autenticação
        
        Args:
            client_id: Client ID do Spotify (ou usa variável de ambiente)
            client_secret: Client Secret do Spotify (ou usa variável de ambiente)
        """
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Credenciais do Spotify não encontradas!\n"
                "Configure SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET como variáveis de ambiente\n"
                "ou passe como parâmetros ao criar SpotifyAuth(client_id='...', client_secret='...')"
            )
        
        self.spotify = None
        self._authenticate()
    
    def _authenticate(self):
        """Realiza autenticação com Spotify"""
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.spotify = Spotify(auth_manager=auth_manager)
            
            # Testa conexão
            self.spotify.search(q='test', limit=1)
            print("✓ Autenticado com sucesso no Spotify!")
            
        except Exception as e:
            raise Exception(f"Erro ao autenticar com Spotify: {str(e)}")
    
    def get_client(self):
        """Retorna cliente Spotify autenticado"""
        return self.spotify
    
    @staticmethod
    def setup_credentials(client_id, client_secret):
        """
        Salva credenciais em arquivo .env
        
        Args:
            client_id: Client ID do Spotify
            client_secret: Client Secret do Spotify
        """
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(f"SPOTIFY_CLIENT_ID={client_id}\n")
            f.write(f"SPOTIFY_CLIENT_SECRET={client_secret}\n")
        
        print(f"✓ Credenciais salvas em {env_path}")
        print("  Use: python -m pip install python-dotenv")
        print("  E adicione no início do script: from dotenv import load_dotenv; load_dotenv()")

if __name__ == '__main__':
    print("=== Configuração de Credenciais Spotify ===\n")
    print("Para obter suas credenciais:")
    print("1. Acesse: https://developer.spotify.com/dashboard")
    print("2. Faça login")
    print("3. Crie um novo App")
    print("4. Copie Client ID e Client Secret\n")
    
    client_id = input("Cole seu Client ID: ").strip()
    client_secret = input("Cole seu Client Secret: ").strip()
    
    if client_id and client_secret:
        SpotifyAuth.setup_credentials(client_id, client_secret)
        
        # Testa autenticação
        try:
            auth = SpotifyAuth(client_id, client_secret)
            print("\n✓ Autenticação testada com sucesso!")
        except Exception as e:
            print(f"\n✗ Erro ao testar autenticação: {e}")
    else:
        print("\n✗ Credenciais não fornecidas")
