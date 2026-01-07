# Imports pesados movidos para escopo local para economizar memória no boot
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
        
        import librosa
        self.y, self.sr = librosa.load(self.audio_path, duration=60)  # Primeiros 60 segundos para poupar RAM
        return self
    
    def extract_tempo(self):
        """Extrai BPM (batidas por minuto)"""
        import librosa
        tempo, _ = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.features['bpm'] = float(tempo)
        return self
    
    def extract_energy(self):
        """Calcula energia e loudness"""
        import librosa
        import numpy as np
        # RMS Energy
        rms = librosa.feature.rms(y=self.y)[0]
        self.features['energy'] = float(np.mean(rms))
        self.features['energy_variance'] = float(np.var(rms))
        
        # Loudness
        self.features['loudness'] = float(np.mean(librosa.amplitude_to_db(rms)))
        return self
    
    def extract_spectral_features(self):
        """Extrai características espectrais"""
        import librosa
        import numpy as np
        # Spectral Centroid (brightness)
        spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
        self.features['brightness'] = float(np.mean(spectral_centroids))
        
        # Spectral Rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
        self.features['spectral_rolloff'] = float(np.mean(spectral_rolloff))
        
        # Spectral Bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)[0]
        self.features['spectral_bandwidth'] = float(np.mean(spectral_bandwidth))
        
        return self
    
    def extract_key(self):
        """Detecta a tonalidade da música"""
        import librosa
        import numpy as np
        chroma = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
        key_index = np.argmax(np.sum(chroma, axis=1))
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.features['key'] = keys[key_index]
        return self
    
    def extract_danceability(self):
        """Calcula dançabilidade baseada em regularidade rítmica"""
        import librosa
        import numpy as np
        # Onset strength
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        
        # Tempogram para análise de ritmo
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=self.sr)
        
        # Regularidade do ritmo (quanto mais regular, mais dançante)
        rhythm_regularity = float(1 - np.std(tempogram) / (np.mean(tempogram) + 1e-6))
        
        self.features['danceability'] = max(0, min(1, rhythm_regularity))
        return self
    
    def extract_zero_crossing_rate(self):
        """Taxa de cruzamento por zero (indica percussividade)"""
        import librosa
        import numpy as np
        zcr = librosa.feature.zero_crossing_rate(self.y)[0]
        self.features['zero_crossing_rate'] = float(np.mean(zcr))
        return self
    
    def extract_mfcc(self):
        """Extrai MFCCs (características timbrais)"""
        import librosa
        import numpy as np
        mfccs = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
        
        # Média dos primeiros 5 MFCCs (mais relevantes para timbre)
        for i in range(5):
            self.features[f'mfcc_{i+1}'] = float(np.mean(mfccs[i]))
        
        return self
    
    def calculate_duration(self):
        """Calcula duração da música"""
        import librosa
        duration = librosa.get_duration(y=self.y, sr=self.sr)
        self.features['duration'] = float(duration)
        return self
    
    def analyze_structure(self):
        """Analisa estrutura da música (variação dinâmica)"""
        import librosa
        import numpy as np
        # Segmentação baseada em mudanças espectrais
        chroma = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
        
        # Calcula variação ao longo do tempo
        variation = np.std(chroma, axis=1)
        self.features['dynamic_variation'] = float(np.mean(variation))
        
        return self
    
    def analyze_all(self):
        """Executa todas as análises"""
        self.load_audio()
        self.extract_tempo()
        self.extract_energy()
        self.extract_spectral_features()
        self.extract_key()
        self.extract_danceability()
        self.extract_zero_crossing_rate()
        self.extract_mfcc()
        self.calculate_duration()
        self.analyze_structure()
        
        return self.features
