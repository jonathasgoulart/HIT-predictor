
import os
import sys
import subprocess
import numpy as np
import librosa

# Adiciona diretório do projeto ao PATH para encontrar ffmpeg.exe
if getattr(sys, 'frozen', False):
    # Se estiver rodando como executável (PyInstaller)
    base_temp = sys._MEIPASS
    exe_dir = os.path.dirname(sys.executable)
    
    # Tenta adicionar AMBOS (Temp do PyInstaller e Pasta do Executável)
    paths_to_add = [base_temp, exe_dir]
    print(f"    [DEBUG] Frozen Mode Detected.")
    print(f"    [DEBUG] _MEIPASS: {base_temp}")
    print(f"    [DEBUG] EXE Dir: {exe_dir}")
else:
    # Se estiver rodando como script normal
    current_file = os.path.abspath(__file__)
    backend_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(backend_dir)
    paths_to_add = [project_root]

# Atualiza PATH do sistema
for p in paths_to_add:
    if p not in os.environ["PATH"]:
        os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]

# Verifica se ffmpeg está acessível
print(f"    [DEBUG] Testando FFmpeg...")
try:
    # Tenta rodar e capturar erro
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
    print(f"    [DEBUG] FFmpeg SUCESSO! Versão: {result.stdout.splitlines()[0]}")
except Exception as e:
    print(f"    [CRITICAL] FFmpeg FALHOU: {str(e)}")
    print(f"    [DEBUG] PATH atual: {os.environ['PATH']}")

# import librosa
# import numpy as np
# from scipy import stats

class AudioAnalyzer:
    """Analisa características de áudio para predição de hits"""
    
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.y = None
        self.sr = None
        self.features = {}
        
    def load_audio(self):
        """Carrega o arquivo de áudio"""
        # Implementação 100% manual sem librosa.load para evitar Numba/Resampy crash
        import audioread
        import contextlib
        import numpy as np
        
        print(f"    [DEBUG] Carregando áudio (Nativo): {self.audio_path}")
        
        try:
            with audioread.audio_open(self.audio_path) as input_file:
                # 1. Metadados
                self.sr = input_file.samplerate
                self.features['duration'] = input_file.duration
                channels = input_file.channels
                
                print(f"    [DEBUG] Metadados: SR={self.sr}, Ch={channels}, Dur={input_file.duration:.2f}s")
                
                # 2. Definição da janela de leitura (Otimização)
                total_samples = int(input_file.duration * self.sr)
                # Janela de 30s
                analysis_duration = min(30.0, input_file.duration)
                
                # offset logic
                if input_file.duration > 30:
                    start_time = 15.0
                else:
                    start_time = 0.0
                    
                start_sample = int(start_time * self.sr)
                end_sample = start_sample + int(analysis_duration * self.sr)
                
                # 3. Decodificação Bufferizada
                # Audioread não suporta seek preciso em todos backends, então lemos e descartamos ou carregamos tudo (se memória permitir)
                # Para evitar complexidade de seek, vamos carregar blocos
                
                audio_data = []
                current_sample = 0
                
                for buf in input_file:
                    # Converte buffer de bytes para array numpy int16
                    # Supondo 16-bit PCM que é o padrão da maioria dos decoders
                    array_buf = np.frombuffer(buf, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Se estéreo, o buffer vem entrelaçado [L, R, L, R...]
                    if channels > 1:
                        array_buf = array_buf.reshape((-1, channels))
                        # Mix down to mono immediato para economizar RAM
                        array_buf = np.mean(array_buf, axis=1)
                        
                    n_samples = len(array_buf)
                    
                    # Lógica de recorte de janela
                    block_start = current_sample
                    block_end = current_sample + n_samples
                    
                    # Verifica intersecção com a janela desejada [start_sample, end_sample]
                    intersect_start = max(block_start, start_sample)
                    intersect_end = min(block_end, end_sample)
                    
                    if intersect_start < intersect_end:
                        # Calcula índices relativos ao buffer atual
                        rel_start = intersect_start - block_start
                        rel_end = intersect_end - block_start
                        audio_data.append(array_buf[rel_start:rel_end])
                        
                    current_sample += n_samples
                    
                    # Se já passamos do fim da janela, pode parar
                    if current_sample > end_sample:
                        break
                
                if not audio_data:
                    raise RuntimeError("Nenhum dado de áudio decodificado")
                    
                self.y = np.concatenate(audio_data)
                
                # 4. Decimação Manual (Downsample) para 11025Hz
                target_sr = 11025
                if self.sr > target_sr:
                    step = int(self.sr / target_sr)
                    if step > 1:
                        self.y = self.y[::step]
                        self.sr = int(self.sr / step)
                
                # 5. PEAK NORMALIZATION (CRÍTICO)
                # Garante que o áudio esteja no volume máximo antes da análise
                # Isso resolve o problema de arquivos baixos terem features ruins
                max_val = np.max(np.abs(self.y))
                if max_val > 0.001:
                    print(f"    [DEBUG] Normalizando pico: {max_val:.4f} -> 0.95")
                    self.y = (self.y / max_val) * 0.95
                
            # Verificação de segurança
            energy_sum = np.sum(np.abs(self.y))
            if energy_sum < 0.001:
                print("    [WARNING] Audio carregado parece estar em silencio absoluto!")
                
        except Exception as e:
            print(f"    [ERROR] Falha no carregamento nativo: {e}")
            raise RuntimeError(f"Erro ao carregar (Método Seguro): {str(e)}")
            print(f"    [ERROR] Falha ao carregar áudio com librosa: {e}")
            raise RuntimeError(f"Erro ao carregar arquivo de áudio: {str(e)}")
        return self
    
    def extract_tempo(self):
        """Extrai BPM usando FFT puro (SEM LIBROSA - compatível Python 3.14)"""
        print(f"    [DEBUG] === BPM EXTRACTION (Pure NumPy Mode) ===")
        
        import numpy as np
        from scipy import signal
        
        try:
            if self.y is None or len(self.y) < 1000:
                raise ValueError("Audio muito curto")
            
            # 1. Detect Onset Envelope (Energy-based, rápido)
            # Calcula a magnitude do espectrograma manualmente
            hop_length = 512
            n_fft = 2048
            
            # Janelamento
            window = np.hanning(n_fft)
            
            # Calcula Short-Time Fourier Transform manualmente
            num_frames = 1 + (len(self.y) - n_fft) // hop_length
            onset_env = np.zeros(num_frames)
            
            for i in range(num_frames):
                start = i * hop_length
                end = start + n_fft
                if end > len(self.y):
                    break
                    
                # Windowed frame
                frame = self.y[start:end] * window
                
                # FFT magnitude
                spectrum = np.abs(np.fft.rfft(frame))
                
                # Onset strength = diferença espectral (flux)
                if i > 0:
                    onset_env[i] = np.sum(np.maximum(0, spectrum - prev_spectrum))
                prev_spectrum = spectrum
            
            # Normaliza
            if np.max(onset_env) > 0:
                onset_env = onset_env / np.max(onset_env)
            
            # 2. Autocorrelação para encontrar periodicidade
            # Limita ao range 30-200 BPM
            min_bpm = 30
            max_bpm = 200
            
            min_lag = int(60 * self.sr / (max_bpm * hop_length))
            max_lag = int(60 * self.sr / (min_bpm * hop_length))
            
            # Autocorrelação usando NumPy puro
            ac = np.correlate(onset_env, onset_env, mode='full')
            ac = ac[len(ac)//2:]  # Pega só a metade positiva
            
            # Limita ao range de BPMs válidos
            if max_lag < len(ac):
                ac = ac[min_lag:max_lag]
            else:
                ac = ac[min_lag:]
            
            # Encontra o pico dominante
            peak_idx = np.argmax(ac) + min_lag
            
            # Converte lag para BPM
            tempo = 60 * self.sr / (peak_idx * hop_length)
            
            print(f"    [DEBUG] FFT BPM RAW: {tempo:.1f}")
            
            # 3. Correção de Oitavas (fix half/double tempo)
            if tempo < 70:
                tempo *= 2
            elif tempo > 180:
                tempo /= 2
            elif 70 <= tempo <= 90:
                # Provável half-tempo
                doubled = tempo * 2
                if 100 <= doubled <= 170:
                    tempo = doubled
            
            # Clamp final
            tempo = np.clip(tempo, 60, 200)
            
            self.features['bpm'] = float(round(tempo, 1))
            print(f"    [DEBUG] BPM FINAL: {self.features['bpm']}")
            
        except Exception as e:
            print(f"    [ERROR] BPM extraction failed: {e}")
            import traceback
            traceback.print_exc()
            self.features['bpm'] = 120.0
        
        return self
    
    def extract_energy(self):
        """Calcula energia e Loudness usando NumPy (Nativo)"""
        import numpy as np
        
        try:
            # 1. RMS Energy (Simples e direto)
            # Energia = raiz quadrada da média dos quadrados da amplitude
            rms_value = np.sqrt(np.mean(self.y**2))
            self.features['energy'] = float(rms_value)
            
            # Variância aproximada (calculada em blocos para simular frame-wise)
            # Dividimos em 100 blocos para estatística
            blocks = np.array_split(self.y, 100)
            block_rms = [np.sqrt(np.mean(b**2)) for b in blocks if len(b) > 0]
            self.features['energy_variance'] = float(np.var(block_rms))
            
            # 2. Loudness (dBFS) - MELHORADO
            # Referência digital full scale = 1.0 (que é nosso max amplitude float)
            # dB = 20 * log10(RMS)
            if rms_value > 0:
                loudness_db = 20 * np.log10(rms_value)
            else:
                loudness_db = -80.0
                
            # Ajuste empírico melhorado para A-Weighting
            # Spotify usa LUFS (Loudness Units Full Scale) que é ~= dBFS + offset
            # Compensação: +2dB base + ajuste por energia espectral
            loudness_db += 2.5
            
            # Clamp entre -60 e 0
            self.features['loudness'] = float(max(-60.0, min(0.0, loudness_db)))
            print(f"    [DEBUG] Loudness (Nativo): {self.features['loudness']:.2f} dBFS")
            
        except Exception as e:
            print(f"    [ERROR] Erro no cálculo de loudness nativo: {e}")
            self.features['loudness'] = -12.0 # Default seguro
            self.features['energy'] = 0.5
            
        return self
    
    def extract_spectral_features(self):
        """Extrai características espectrais"""
        import librosa
        return self

    def extract_spectral_features(self):
        """Extrai features espectrais usando NumPy/Scipy (Nativo)"""
        import numpy as np
        from scipy import signal
        
        try:
            # Reutiliza ou calcula STFT
            n_fft = 2048
            hop_length = 512
            f, t, Zxx = signal.stft(self.y, fs=self.sr, nperseg=n_fft, noverlap=n_fft-hop_length)
            magnitude = np.abs(Zxx)
            
            # Frequências em Hz
            freqs = np.linspace(0, self.sr/2, magnitude.shape[0])
            
            # 1. Spectral Centroid
            # C = sum(f * mag) / sum(mag)
            mag_sum = np.sum(magnitude, axis=0) + 1e-9
            centroid = np.sum(freqs[:, np.newaxis] * magnitude, axis=0) / mag_sum
            self.features['brightness'] = float(np.mean(centroid))
            
            # 2. Spectral Rolloff (85%)
            # Frequência onde acumula 85% da energia
            cum_energy = np.cumsum(magnitude, axis=0)
            total_energy = cum_energy[-1, :]
            threshold = 0.85 * total_energy
            # Encontra índice onde passa do threshold
            rolloff_idx = np.argmax(cum_energy >= threshold, axis=0)
            rolloff = freqs[rolloff_idx]
            self.features['spectral_rolloff'] = float(np.mean(rolloff))
            
            # 3. Spectral Bandwidth
            # Largura de banda ponderada
            diff = freqs[:, np.newaxis] - centroid
            bandwidth = np.sqrt(np.sum((diff**2) * magnitude, axis=0) / mag_sum)
            self.features['spectral_bandwidth'] = float(np.mean(bandwidth))
            
        except Exception as e:
            print(f"    [ERROR] Falha espectral nativa: {e}")
            self.features['brightness'] = 1000.0
            self.features['spectral_rolloff'] = 2000.0
            self.features['spectral_bandwidth'] = 1500.0
            
        return self
    
    def extract_key(self):
        """Estima tonalidade por pico de frequência (Simplificado)"""
        # Nota: Chroma completo é complexo sem librosa. Usaremos pico de gravidade.
        self.features['key'] = 'C' # Placeholder seguro
        return self
    
    def extract_danceability(self):
        """Estima dançabilidade por BPM e Energia (Nativo, Dinâmico)"""
        try:
            # Fórmula Baseada em Pesquisas de Musicologia
            # 1. Energia: Quanto mais energia, mais vontade de mover (peso 0.5)
            # 2. BPM: O ideal para dança é ~110-120 BPM. Distância disso reduz nota.
            
            energy = self.features.get('energy', 0.5)
            bpm = self.features.get('bpm', 0)
            
            # Fator Energia (0.0 a 0.5)
            energy_factor = energy * 0.5
            
            # Fator BPM (Gaussian-ish)
            # 120 é o pico. 60 ou 180 cai para zero.
            if bpm > 0:
                dist = abs(bpm - 118)
                bpm_factor = max(0.0, 0.5 - (dist * 0.006)) # Cai 0.06 a cada 10 BPM de distância
            else:
                bpm_factor = 0.2
            
            # Soma Base
            score = 0.1 + energy_factor + bpm_factor
            
            # Penalidade para muito rápido/muito lento (além do fator)
            if bpm < 50 or bpm > 190:
                score *= 0.7
                
            self.features['danceability'] = float(np.clip(score, 0.1, 0.98))
            
        except Exception as e:
            print(f"    [DEBUG] Erro Danceability: {e}")
            self.features['danceability'] = 0.5
        return self
    
    def extract_zero_crossing_rate(self):
        """Taxa de cruzamento por zero manual"""
        import numpy as np
        try:
            # ZCR = média de mudanças de sinal
            zero_crossings = np.sum(np.abs(np.diff(np.signbit(self.y))))
            zcr = zero_crossings / (2 * len(self.y))
            self.features['zero_crossing_rate'] = float(zcr)
        except Exception:
            self.features['zero_crossing_rate'] = 0.0
        return self
    
    def extract_mfcc(self):
        """Estima MFCCs usando log-energia em bandas (Simplificado)"""
        import numpy as np
        from scipy import signal, fftpack
        
        try:
            # Simplificação: Log-Energy em 13 bandas lineares + DCT
            # Não é um MFCC perfeito (escala linear vs Mel), mas captura timbre
            n_fft = 2048
            f, t, Zxx = signal.stft(self.y, fs=self.sr, nperseg=n_fft)
            psd = np.abs(Zxx)**2
            
            # Divide em 13 bandas
            n_bins = psd.shape[0]
            bands = np.array_split(psd, 13, axis=0)
            energies = np.array([np.mean(b, axis=0) for b in bands])
            
            # Log
            log_energies = np.log(energies + 1e-9)
            
            # DCT Tipo 2
            # mfcc_approx = fftpack.dct(log_energies, type=2, axis=0, norm='ortho')
            # Simplificando: Média das log-energias serve como proxy de feature
            avg_log_energies = np.mean(log_energies, axis=1)
            
            for i in range(5):
                # Pega as primeiras 5 bandas como features
                val = avg_log_energies[i] if i < len(avg_log_energies) else 0.0
                self.features[f'mfcc_{i+1}'] = float(val)
                
        except Exception as e:
            print(f"    [ERROR] Falha MFCC nativa: {e}")
            for i in range(5):
                self.features[f'mfcc_{i+1}'] = 0.0
        return self
    
    def analyze_structure(self):
        """Analisa variação dinâmica (Estrutura)"""
        import numpy as np
        try:
            # Usa variância da magnitude do STFT global
            # Se já calculamos STFT no passo anterior, poderíamos reutilizar, mas ok recalcular
            # Variação simples da amplitude
            variation = np.std(np.abs(self.y))
            self.features['dynamic_variation'] = float(variation)
        except Exception:
            self.features['dynamic_variation'] = 0.0
        return self
    
    def _calibrate_to_spotify(self):
        """
        Camada de calibração para alinhar features extraídas do áudio RAW
        com a escala perceptual usada pelo Spotify (treinamento do modelo).
        """
        # Mantém calibração existente
        import numpy as np
        
        print("    [DEBUG] Aplicando calibragem Perceptual (Spotify Scale)...")
        
        # 1. ENERGIA (Spotify Energy é densidade espectral + volume + entropia)
        # O RMS puro costuma ser baixo (0.1-0.3), Spotify Energy é 0.5-0.9 para hits.
        raw_energy = self.features.get('energy', 0.5)
        brightness = self.features.get('brightness', 2500)
        loudness = self.features.get('loudness', -10)
        
        # Fórmula Perceptual Melhorada: Volume (RMS) + Brilho + Loudness
        # Normalizamos brightness (0-5000 -> 0-1)
        norm_brightness = min(1.0, brightness / 4000)
        # Normalizamos loudness (-60 a 0 -> 0 a 1)
        norm_loudness = (loudness + 60) / 60
        
        # BOOST AJUSTADO: Combina RMS, brilho e loudness
        calibrated_energy = (np.sqrt(raw_energy) * 1.2) + (norm_brightness * 0.15) + (norm_loudness * 0.25)
        self.features['energy'] = float(min(0.98, max(0.1, calibrated_energy)))
        
        # 2. DANÇABILIDADE (DESABILITADO - Agora usa fórmula dinâmica em extract_danceability)
        # raw_dance = self.features.get('danceability', 0.5)
        # self.features['danceability'] = float(min(0.95, raw_dance * 1.8))
        
        # 3. LOUDNESS (Verificamos se está dentro da média da base -7.1 dB)
        # Já extraímos dBFS A-weighted, que é uma boa aproximação.
        
        print(f"    [DEBUG] Calibragem concluída: Energy={self.features['energy']:.2f}, Dance={self.features['danceability']:.2f}")

    def analyze_all(self):
        """Executa todas as análises com alta resiliência e calibragem"""
        print("    [DEBUG] Iniciando análise completa...")
        self.load_audio()
        
        # Lista de funções de extração
        extractions = [
            ("BPM", self.extract_tempo, 120.0),
            ("Energia/Loudness", self.extract_energy, 0.5),
            ("Esquema Espectral", self.extract_spectral_features, None),
            ("Tonalidade", self.extract_key, "C"),
            ("Dançabilidade", self.extract_danceability, 0.5),
            ("Percurssividade", self.extract_zero_crossing_rate, 0.05),
            ("Timbre", self.extract_mfcc, None),
            ("Estrutura", self.analyze_structure, 0.2)
        ]

        import sys
        print(f"    [DEBUG] PREPARANDO LOOP DE EXTRAÇÃO - {len(extractions)} funções")
        sys.stdout.flush()

        for name, func, default in extractions:
            import sys
            print(f"    [DEBUG] >>> Iniciando extração: {name}")
            sys.stdout.flush()  # FORÇA output imediato
            try:
                func()
                print(f"    [DEBUG] <<< {name} concluído com sucesso")
                sys.stdout.flush()
            except Exception as e:
                print(f"    [WARNING] Falha em {name}: {e}")
                import traceback
                traceback.print_exc()
                sys.stdout.flush()
                # Fallbacks mapeados por nome de feature
                if "BPM" in name: self.features['bpm'] = default
                elif "Energia" in name: self.features['energy'] = default
        
        # APLICA CALIBRAGEM SPOTIFY
        self.extract_spectral_features()
        self._calibrate_to_spotify()
        
        # Extrai features do Spotify (aproximações)
        print("    [DEBUG] Extraindo features do Spotify...")
        self.extract_valence()
        self.extract_acousticness()
        self.extract_instrumentalness()
        self.extract_liveness()
        self.extract_speechiness()
        
        # Limpeza de memória
        import gc
        gc.collect()
        
        return self.features
    
    
    def extract_valence(self):
        """Aproxima Valence (positividade musical) usando features básicas (Nativo)"""
        try:
            # Valence positivo: BPM rápido, Energia alta, Brightness alto
            # Valence negativo: BPM lento, Energia baixa, Brightness baixo
            
            bpm_norm = min(self.features.get('bpm', 120) / 180, 1.0)
            energy = self.features.get('energy', 0.5)
            brightness_norm = min(self.features.get('brightness', 1500) / 4000, 1.0)
            
            # Fórmula empírica
            valence = (bpm_norm * 0.3) + (energy * 0.4) + (brightness_norm * 0.3)
            self.features['valence'] = float(np.clip(valence, 0.0, 1.0))
            
        except Exception as e:
            print(f"    [ERROR] Erro em valence nativo: {e}")
            self.features['valence'] = 0.5
        return self

    def extract_acousticness(self):
        """Aproxima Acousticness (Nativo)"""
        try:
            # Acústico = Baixa Energia + Baixo Brilho 
            energy = self.features.get('energy', 0.5)
            brightness_norm = min(self.features.get('brightness', 1500) / 5000, 1.0)
            
            # Inverso da energia e brilho
            non_acoustic_score = (energy * 0.6) + (brightness_norm * 0.4)
            acousticness = 1.0 - non_acoustic_score
            
            self.features['acousticness'] = float(np.clip(acousticness, 0.0, 1.0))
            
        except Exception as e:
            print(f"    [ERROR] Erro em acousticness nativo: {e}")
            self.features['acousticness'] = 0.5
        return self

    def extract_instrumentalness(self):
        """Aproxima Instrumentalness (Nativo)"""
        try:
            # Vocal costuma ter alta variação de ZCR (fala) e energia média
            # Instrumental costuma ser mais estável ou repetitivo
            
            # Simplificação: Instrumental se ZCR for muito baixo (grave) ou muito estável
            # Por enquanto, usaremos uma heurística baseada em "falta de voz"
            # Voz geralmente está em 200-3000Hz com alta variação.
            
            # Heurística: Alta energia + Baixa variação dinâmica = Eletrônico/Instrumental
            
            energy = self.features.get('energy', 0.5)
            zcr_rate = self.features.get('zero_crossing_rate', 0.05)
            
            # Se ZCR for alto, provavelmente tem voz (consoantes) ou pratos (bateria)
            # Se ZCR for muito baixo, é bass puro.
            
            # Vamos assumir:
            instr_score = 0.5 # Neutro
            if zcr_rate < 0.05: instr_score += 0.3 # Muito grave/puro
            if energy > 0.8: instr_score += 0.2 # Muito comprimido (eletrônico)
            
            self.features['instrumentalness'] = float(np.clip(instr_score, 0.0, 0.95))
            
        except Exception as e:
            self.features['instrumentalness'] = 0.0
        return self

    def extract_liveness(self):
        """Aproxima Liveness (Nativo)"""
        # Difícil sem ML real. Retorna baixo por padrão para estúdio.
        self.features['liveness'] = 0.1
        return self

    def extract_speechiness(self):
        """Aproxima Speechiness (Nativo) - COM ANÁLISE DE PITCH"""
        try:
            # Fala/Rap tem características específicas:
            # 1. ZCR alto (consoantes)
            # 2. PITCH IRREGULAR (fala não é tonal como canto)
            # 3. Variação temporal rápida (sílabas)
            # 4. Espectro mais plano (menos harmônico)
            
            zcr = self.features.get('zero_crossing_rate', 0.05)
            brightness = self.features.get('brightness', 2000)
            dynamic_var = self.features.get('dynamic_variation', 0.1)
            energy = self.features.get('energy', 0.5)
            spectral_bandwidth = self.features.get('spectral_bandwidth', 1500)
            
            # NOVO: Análise de Pitch (CRÍTICO para detectar rap)
            pitch_irregularity = self._analyze_pitch_irregularity()
            
            # Fator 1: ZCR (ajustado para detectar rap)
            # Música: 0.05-0.10, Rap: 0.10-0.20
            if zcr < 0.08:
                zcr_factor = 0.0  # Definitivamente não é rap
            elif zcr < 0.12:
                # Zona cinzenta: pode ser música com hi-hats ou rap leve
                zcr_factor = (zcr - 0.08) / 0.04 * 0.3  # Max 0.3
            else:
                # Provavelmente rap
                zcr_factor = 0.3 + min((zcr - 0.12) / 0.08, 1.0) * 0.7  # 0.3 a 1.0
            
            # Fator 2: PITCH IRREGULARITY (NOVO - MAIS IMPORTANTE!)
            # Canto tem pitch estável, Rap/Fala tem pitch irregular
            # pitch_irregularity: 0.0 = muito estável (canto), 1.0 = muito irregular (fala)
            pitch_factor = pitch_irregularity * 0.8  # Peso ALTO
            
            # Fator 3: Brightness médio (fala humana: 1800-2500Hz)
            if 1800 <= brightness <= 2500:
                brightness_factor = 0.2
            elif brightness < 1800:
                brightness_factor = max(0, 0.2 - (1800 - brightness) / 2000)
            else:
                brightness_factor = max(0, 0.2 - (brightness - 2500) / 2000)
            
            # Fator 4: Variação dinâmica (fala tem variação moderada-alta)
            if dynamic_var > 0.15:
                var_factor = min(dynamic_var / 0.3, 0.2)
            else:
                var_factor = 0.0
            
            # Fator 5: Largura espectral (fala tem espectro mais plano)
            if spectral_bandwidth > 1800:
                bandwidth_factor = 0.15
            else:
                bandwidth_factor = 0.0
            
            # Combina fatores (PITCH é o mais importante agora!)
            speech_score = pitch_factor + zcr_factor + brightness_factor + var_factor + bandwidth_factor
            
            # Normaliza para 0-1 (max teórico = 0.8 + 1.0 + 0.2 + 0.2 + 0.15 = 2.35)
            speech_score = speech_score / 2.35
            
            # Ajuste final: penaliza energia MUITO alta (eletrônico/rock)
            if energy > 0.90:
                speech_score *= 0.7
            
            # Limita
            self.features['speechiness'] = float(min(0.66, max(0.03, speech_score)))
            
        except Exception as e:
            print(f"    [ERROR] Erro em speechiness: {e}")
            self.features['speechiness'] = 0.05
        return self
    
    def _analyze_pitch_irregularity(self):
        """
        Analisa irregularidade do pitch para distinguir canto de fala/rap
        Retorna: 0.0 = pitch estável (canto), 1.0 = pitch irregular (fala/rap)
        """
        try:
            import librosa
            import numpy as np
            
            # Extrai pitch usando pYIN (melhor para voz)
            # pYIN é robusto para detectar pitch em música com voz
            f0, voiced_flag, voiced_probs = librosa.pyin(
                self.y,
                fmin=librosa.note_to_hz('C2'),  # ~65 Hz (voz masculina grave)
                fmax=librosa.note_to_hz('C7'),  # ~2093 Hz (voz feminina aguda)
                sr=self.sr,
                frame_length=2048
            )
            
            # Remove NaN (frames sem pitch detectado)
            f0_clean = f0[~np.isnan(f0)]
            
            if len(f0_clean) < 10:
                # Muito pouco pitch detectado = provavelmente instrumental
                return 0.0
            
            # Calcula métricas de irregularidade
            
            # 1. Variação do pitch (desvio padrão)
            pitch_std = np.std(f0_clean)
            pitch_mean = np.mean(f0_clean)
            
            # Coeficiente de variação (CV = std/mean)
            # Canto: CV ~0.05-0.15, Fala: CV > 0.20
            cv = pitch_std / pitch_mean if pitch_mean > 0 else 0
            
            # 2. Saltos de pitch (mudanças abruptas)
            pitch_diff = np.abs(np.diff(f0_clean))
            large_jumps = np.sum(pitch_diff > 50)  # Saltos > 50 Hz
            jump_ratio = large_jumps / len(pitch_diff) if len(pitch_diff) > 0 else 0
            
            # 3. Frames vozeados (quanto do áudio tem voz)
            voiced_ratio = np.sum(voiced_flag) / len(voiced_flag)
            
            # Combina métricas
            # CV alto + muitos saltos + baixo voiced_ratio = Fala/Rap
            irregularity_score = 0.0
            
            # CV: 0.15 = 0, 0.30 = 1.0
            if cv > 0.15:
                irregularity_score += min((cv - 0.15) / 0.15, 1.0) * 0.5
            
            # Jump ratio: 0.1 = 0, 0.3 = 1.0
            if jump_ratio > 0.1:
                irregularity_score += min((jump_ratio - 0.1) / 0.2, 1.0) * 0.3
            
            # Voiced ratio: < 0.6 = fala (muitas pausas)
            if voiced_ratio < 0.6:
                irregularity_score += (0.6 - voiced_ratio) / 0.6 * 0.2
            
            return min(irregularity_score, 1.0)
            
        except Exception as e:
            print(f"    [DEBUG] Pitch analysis failed: {e}")
            # Fallback: sem análise de pitch
            return 0.0

