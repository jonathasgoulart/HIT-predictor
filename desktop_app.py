import os
import sys
import tempfile

# CONFIGURAÇÃO CRÍTICA PARA NUMBA/LIBROSA NO EXECUTÁVEL
# Deve ser feita ANTES de qualquer outro import que possa carregar o Numba
os.environ['NUMBA_DISABLE_JIT'] = '1'
os.environ['NUMBA_DISABLE_CUDA'] = '1'
# Define diretório de cache em local gravável (Temp) para evitar erros de permissão
os.environ['NUMBA_CACHE_DIR'] = os.path.join(tempfile.gettempdir(), 'numba_cache')

import threading
import time
import subprocess
import webbrowser
from backend.api import app

# Configurações
PORT = 5002
HOST = '127.0.0.1'
URL = f'http://{HOST}:{PORT}'

def start_server():
    """Inicia o servidor Flask em background"""
    app.run(host=HOST, port=PORT, use_reloader=False)

def open_browser():
    """Abre a interface em modo App (sem barra de navegação)"""
    print(f"Abrindo interface em: {URL}")
    try:
        # Tenta abrir Edge em modo App (Padrão Windows)
        # O comando 'start' do Windows cuida do path
        subprocess.run(f'start msedge --app={URL}', shell=True, check=True)
        return
    except Exception:
        pass
    
    try:
        # Tenta Chrome
        subprocess.run(f'start chrome --app={URL}', shell=True, check=True)
        return
    except Exception:
        pass

    # Fallback: Abre navegador padrão
    print("Navegador em modo App não encontrado, abrindo padrão...")
    webbrowser.open(URL)

def start_app():
    """Inicia a aplicação Desktop"""
    # 1. Inicia o Backend
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # 2. Aguarda servidor
    time.sleep(2)
    
    # 3. Abre Interface
    open_browser()
    
    # 4. Mantém vivo até o usuário fechar a janela do console (se existir)
    # ou matar o processo.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    start_app()
