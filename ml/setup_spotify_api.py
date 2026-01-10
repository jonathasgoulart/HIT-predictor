"""
Helper para configurar Spotify API
Execute este script para configurar suas credenciais
"""
from spotify_auth import SpotifyAuth

def main():
    print("="*70)
    print("CONFIGURACAO SPOTIFY API - PASSO A PASSO")
    print("="*70 + "\n")
    
    print("PASSO 1: Obter Credenciais")
    print("-" * 70)
    print("1. Acesse: https://developer.spotify.com/dashboard")
    print("2. Faca login com sua conta Spotify")
    print("3. Clique em 'Create app'")
    print("4. Preencha:")
    print("   - App name: Hit Predictor")
    print("   - App description: ML model for hit prediction")
    print("   - Redirect URI: http://localhost:8888/callback")
    print("5. Aceite os termos")
    print("6. Clique em 'Settings'")
    print("7. Copie Client ID e Client Secret\n")
    
    print("PASSO 2: Configurar Credenciais")
    print("-" * 70)
    
    client_id = input("Cole seu Client ID: ").strip()
    client_secret = input("Cole seu Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("\nERRO: Credenciais nao fornecidas!")
        return
    
    # Salva credenciais
    SpotifyAuth.setup_credentials(client_id, client_secret)
    
    # Testa
    try:
        auth = SpotifyAuth(client_id, client_secret)
        print("\nOK Autenticacao testada com sucesso!")
        print("\nPROXIMO PASSO:")
        print("  python ml/collect_spotify_playlists.py")
    except Exception as e:
        print(f"\nERRO ao testar: {e}")
        print("\nVerifique se as credenciais estao corretas")

if __name__ == "__main__":
    main()
