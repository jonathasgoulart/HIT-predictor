"""
Script completo de setup e execução do pipeline ML
"""
import os
import sys

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_dependencies():
    """Verifica se dependências estão instaladas"""
    print_header("Verificando Dependências")
    
    required = ['spotipy', 'pandas', 'sklearn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - FALTANDO")
            missing.append(package)
    
    if missing:
        print("\n⚠ Dependências faltando!")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("\n✓ Todas as dependências instaladas")
    return True

def setup_credentials():
    """Configura credenciais do Spotify"""
    print_header("Configuração do Spotify")
    
    if os.path.exists('.env'):
        print("✓ Arquivo .env encontrado")
        response = input("Deseja reconfigurar credenciais? (s/N): ").strip().lower()
        if response != 's':
            return True
    
    print("\nPara obter credenciais:")
    print("1. Acesse: https://developer.spotify.com/dashboard")
    print("2. Faça login")
    print("3. Crie um App")
    print("4. Copie Client ID e Client Secret\n")
    
    from spotify_auth import SpotifyAuth
    
    client_id = input("Cole seu Client ID: ").strip()
    client_secret = input("Cole seu Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("\n✗ Credenciais não fornecidas")
        return False
    
    try:
        SpotifyAuth.setup_credentials(client_id, client_secret)
        auth = SpotifyAuth(client_id, client_secret)
        print("\n✓ Credenciais configuradas e testadas com sucesso!")
        return True
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        return False

def collect_data():
    """Executa coleta de dados"""
    print_header("Coleta de Dados")
    
    print("Gêneros disponíveis:")
    print("1. MPB/Nova MPB")
    print("2. R&B Brasil")
    print("3. Ambos")
    
    choice = input("\nEscolha (1/2/3): ").strip()
    
    from spotify_auth import SpotifyAuth
    from data_collector import DataCollector
    
    try:
        auth = SpotifyAuth()
        collector = DataCollector(auth)
        
        if choice in ['1', '3']:
            print("\n--- Coletando MPB/Nova MPB ---")
            df_mpb = collector.collect_balanced_dataset('mpb')
            collector.save_dataset(df_mpb, 'mpb_dataset.csv')
        
        if choice in ['2', '3']:
            print("\n--- Coletando R&B Brasil ---")
            collector.collected_tracks.clear()
            df_rnb = collector.collect_balanced_dataset('rnb_brasil')
            collector.save_dataset(df_rnb, 'rnb_brasil_dataset.csv')
        
        print("\n✓ Coleta concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n✗ Erro na coleta: {e}")
        return False

def train_models():
    """Treina modelos ML"""
    print_header("Treinamento de Modelos")
    
    from train_model import ModelTrainer
    
    datasets = []
    if os.path.exists('datasets/mpb_dataset.csv'):
        datasets.append(('MPB', 'datasets/mpb_dataset.csv'))
    if os.path.exists('datasets/rnb_brasil_dataset.csv'):
        datasets.append(('R&B Brasil', 'datasets/rnb_brasil_dataset.csv'))
    
    if not datasets:
        print("✗ Nenhum dataset encontrado!")
        print("Execute a coleta de dados primeiro.")
        return False
    
    for genre_name, dataset_path in datasets:
        print(f"\n--- Treinando {genre_name} ---")
        
        try:
            trainer = ModelTrainer(dataset_path)
            trainer.load_dataset()
            trainer.prepare_data()
            trainer.train_random_forest(n_estimators=100, max_depth=10)
            metrics = trainer.evaluate()
            
            if metrics['accuracy'] > 0.70:
                trainer.save_model()
                print(f"✓ Modelo {genre_name} salvo com sucesso!")
            else:
                print(f"⚠ Performance de {genre_name} abaixo do esperado")
                
        except Exception as e:
            print(f"✗ Erro ao treinar {genre_name}: {e}")
    
    print("\n✓ Treinamento concluído!")
    return True

def main():
    """Executa pipeline completo"""
    print_header("Pipeline ML - Música Brasileira")
    
    print("Este script irá:")
    print("1. Verificar dependências")
    print("2. Configurar credenciais Spotify")
    print("3. Coletar dados de músicas brasileiras")
    print("4. Treinar modelos ML")
    
    input("\nPressione Enter para continuar...")
    
    # 1. Dependências
    if not check_dependencies():
        return
    
    # 2. Credenciais
    if not setup_credentials():
        return
    
    # 3. Coleta
    response = input("\nDeseja coletar dados agora? (S/n): ").strip().lower()
    if response != 'n':
        if not collect_data():
            return
    
    # 4. Treinamento
    response = input("\nDeseja treinar modelos agora? (S/n): ").strip().lower()
    if response != 'n':
        train_models()
    
    print_header("Concluído!")
    print("Próximos passos:")
    print("- Modelos salvos em: ml/models/")
    print("- Datasets salvos em: ml/datasets/")
    print("- Integre os modelos com o backend da aplicação")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n✗ Erro: {e}")
