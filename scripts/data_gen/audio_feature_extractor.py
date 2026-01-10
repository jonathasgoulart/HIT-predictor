import librosa
import numpy as np
import pandas as pd
import os
import soundfile as sf

class AudioFeatureExtractor:
    """
    Extrai características de áudio locais usando librosa.
    Substitui as métricas da API do Spotify (BPM, Energia, Danceability, etc).
    """
    def __init__(self):
        self.feature_columns = [
            'bpm', 'energy', 'danceability', 'valence', 
            'acousticness', 'instrumentalness', 'liveness', 'loudness'
        ]

    def extract_features(self, audio_path):
        """
        Analisa um arquivo de áudio e retorna um dicionário de características.
        Inclui métricas avançadas para mimetizar a análise profunda do Spotify.
        """
        print(f"Analisando: {os.path.basename(audio_path)}...")
        
        try:
            # Carrega o áudio
            y, sr = librosa.load(audio_path, duration=60)
            
            # Separa componente harmônico e percussivo
            y_harm, y_perc = librosa.effects.hpss(y)
            
            # 1. BPM (Tempo)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            bpm = float(tempo)
            
            # 2. Loudness (DB RMS)
            rms = librosa.feature.rms(y=y)
            loudness = float(librosa.amplitude_to_db([np.mean(rms)]))
            
            # 3. Energy (Intensidade e atividade)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            energy = np.mean(rms) * 8 + np.mean(spectral_centroid) / 4000
            energy = np.clip(energy, 0, 1)
            
            # 4. Danceability (Rítmica e estabilidade)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
            danceability = np.mean(tempogram) * 10 
            danceability = np.clip(danceability, 0, 1)
            
            # 5. Acousticness (Presença de instrumentos acústicos vs sintéticos)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
            acousticness = 1.0 - (np.mean(rolloff) / (sr/2))
            acousticness = np.clip(acousticness, 0, 1)
            
            # 6. Valence (Positividade musical)
            chroma = librosa.feature.chroma_cqt(y=y_harm, sr=sr)
            valence = np.mean(chroma) * 1.5
            valence = np.clip(valence, 0, 1)

            # 7. Key e Mode (Tom e Escala)
            chroma_mean = np.mean(chroma, axis=1)
            key_index = np.argmax(chroma_mean)
            keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            key_name = keys[key_index]
            
            # Mode (Simplificado: Major se a terça maior é mais forte que a menor)
            # Para C (index 0), terça menor é D# (index 3), terça maior é E (index 4)
            third_minor = chroma_mean[(key_index + 3) % 12]
            third_major = chroma_mean[(key_index + 4) % 12]
            mode = 1 if third_major > third_minor else 0 # 1 = Major, 0 = Minor

            # 8. Spectral Flatness (Ruído vs Tom)
            flatness = librosa.feature.spectral_flatness(y=y)
            spectral_flatness = float(np.mean(flatness))

            # 9. Zero Crossing Rate (Percussividade/Brilho)
            zcr = librosa.feature.zero_crossing_rate(y)
            zero_crossing_rate = float(np.mean(zcr))

            # 10. MFCCs (Timbre - Médias dos 13 primeiros coeficientes)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs)

            # 11. Spectral Contrast (Textura espectral)
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            spectral_contrast = np.mean(contrast)

            # 12. Poly Features (Complexidade harmônica)
            poly = librosa.feature.poly_features(y=y_harm, sr=sr, order=1)
            poly_features = np.mean(poly)

            return {
                'bpm': round(bpm, 2),
                'loudness': round(loudness, 2),
                'energy': round(energy, 3),
                'danceability': round(danceability, 3),
                'acousticness': round(acousticness, 3),
                'valence': round(valence, 3),
                'key': key_name,
                'mode': mode,
                'spectral_flatness': round(spectral_flatness, 4),
                'zero_crossing_rate': round(zero_crossing_rate, 4),
                'mfcc_mean': round(float(mfcc_mean), 3),
                'spectral_contrast': round(float(spectral_contrast), 3),
                'poly_features': round(float(poly_features), 3),
                'instrumentalness': 0.05,
                'liveness': 0.1,
                'speechiness': 0.05
            }
            
        except Exception as e:
            print(f"Erro ao processar {audio_path}: {e}")
            return None

if __name__ == "__main__":
    extractor = AudioFeatureExtractor()
    # Exemplo de teste (se houver um arquivo na pasta uploads)
    test_dir = 'uploads'
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith(('.mp3', '.wav'))]
        if files:
            features = extractor.extract_features(os.path.join(test_dir, files[0]))
            print("\nCaracterísticas extraídas:")
            for k, v in features.items():
                print(f"  {k}: {v}")
        else:
            print("Nenhum arquivo de áudio encontrado em 'uploads' para teste.")
    else:
        print("Pasta 'uploads' não encontrada.")
