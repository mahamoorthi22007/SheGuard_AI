import requests
import numpy as np
import librosa
import joblib
import os
import warnings
import logging
from firebase import trigger_device_alarm

warnings.filterwarnings("ignore")
logging.getLogger('geocoder').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# --- CONFIGURATION METRICS ---
# ⚠️ REMEMBER: Change this IP address to match the one on your phone screen!
AUDIO_STREAM_URL = "http://10.122.188.206:8080/audio.wav" 
MODEL_FILE = "scream_detector_model.pkl"
SAMPLE_RATE = 16000  
BYTES_PER_SAMPLE = 2  
WINDOW_DURATION = 1   
CHUNK_SIZE = SAMPLE_RATE * BYTES_PER_SAMPLE * WINDOW_DURATION

# Your exact requested labels mapped for the presentation jury
audio_profiles = {
    0: {"name": "Normal Environment", "threat": 0},
    1: {"name": "Media Recorded Audio", "threat": 15},
    2: {"name": "Original Scream", "threat": 100},
    3: {"name": "Children Playing", "threat": 35}
}

if not os.path.exists(MODEL_FILE):
    print(f"❌ Error: Run your 'python main.py' script first to generate '{MODEL_FILE}'")
    exit()

model = joblib.load(MODEL_FILE)
print("=" * 75)
print("🎙️  SHEGUARD MULTIMODAL INTELLIGENCE GATEWAY RUNNING...")
print("=" * 75)

try:
    audio_response = requests.get(AUDIO_STREAM_URL, stream=True, timeout=10)
    print("[SUCCESS] Audio feed connected. Monitoring live signals...\n")
    buffer = b""

    for packet in audio_response.iter_content(chunk_size=4096):
        buffer += packet

        if len(buffer) >= CHUNK_SIZE:
            audio_chunk = buffer[:CHUNK_SIZE]
            buffer = buffer[CHUNK_SIZE:]

            raw_audio = np.frombuffer(audio_chunk, dtype=np.int16)
            normalized_audio = raw_audio.astype(np.float32) / 32768.0

            # --- EXTRACT LIVE AUDIO MATRIX ---
            mfccs = librosa.feature.mfcc(y=normalized_audio, sr=SAMPLE_RATE, n_mfcc=13)
            spectral_centroid = librosa.feature.spectral_centroid(y=normalized_audio, sr=SAMPLE_RATE)
            spectral_flatness = librosa.feature.spectral_flatness(y=normalized_audio)
            
            live_vector = np.concatenate((
                np.mean(mfccs, axis=1), np.var(mfccs, axis=1), 
                np.mean(librosa.feature.spectral_contrast(y=normalized_audio, sr=SAMPLE_RATE), axis=1), 
                np.mean(librosa.feature.chroma_stft(y=normalized_audio, sr=SAMPLE_RATE), axis=1)
            )).reshape(1, -1)

            # 1. Evaluate base threat prediction using your trained dataset model
            base_prediction = int(model.predict(live_vector)[0])
            
            # 2. Extract acoustic parameters for environmental processing
            mean_flatness = np.mean(spectral_flatness)
            mean_centroid = np.mean(spectral_centroid)
            rms_energy = np.sqrt(np.mean(normalized_audio**2))

            # --- DYNAMIC INTEL DISPATCH SEPARATOR ---
            # --- DYNAMIC INTEL DISPATCH SEPARATOR ---
            if rms_energy > 0.008: # Slightly lowered noise floor to capture quieter speakers
                if base_prediction == 2 and mean_centroid > 2100:
                    prediction_id = 2  # ORIGINAL SCREAM
                elif mean_centroid > 2500: # Tuned down from 2600 for faster capture
                    prediction_id = 3  # CHILDREN PLAYING
                # Lowered flatness threshold from 0.0035 to 0.0015 to easily catch compressed YouTube audio
                elif mean_flatness > 0.0015: 
                    prediction_id = 1  # MEDIA RECORDED AUDIO
                else:
                    prediction_id = 0  # NORMAL ENVIRONMENT fallback
            else:
                prediction_id = 0      # Quiet background room state    # Quiet background room state

            audio_name = audio_profiles[prediction_id]["name"]
            audio_threat = audio_profiles[prediction_id]["threat"]

            # --- FIXED GEOGRAPHIC LOCATION (Ottakkalmandapam) ---
            current_lat, current_lon = 10.9990, 77.0324   
            perimeter_name = "Ottakkalmandapam Sector"
            gps_threat_score = 45 

            average_threat_score = int((audio_threat + gps_threat_score) / 2)

            # --- SYSTEM ACTIONS OUTPUT ---
            if prediction_id == 2:
                print(f"\n🚨 [CRITICAL ALERT] EMERGENCY DISPATCH BREACHED!")
                print(f"📍 Location Context          : {perimeter_name.upper()} ({current_lat:.4f}, {current_lon:.4f})")
                print(f"🎙️ Acoustic Profiler Analysis : {audio_name.upper()}")
                print(f"📊 FUSED TOTAL RISK RATING    : {average_threat_score}%")
                try:
                    trigger_device_alarm(fcm_token="mock_token", zone_name=perimeter_name, threat_score=average_threat_score)
                except Exception:
                    pass
                print("-" * 75)
            else:
                print(f"[SHIELD ACTIVE] Coords: ({current_lat:.4f}, {current_lon:.4f}) | Location Info: {perimeter_name} ({gps_threat_score}%) | Audio: {audio_name} ({audio_threat}%) | FUSED RISK: {average_threat_score}%")

except KeyboardInterrupt:
    print("\n[SHUTDOWN] System terminated cleanly.")
except Exception as e:
    print(f"\n[NETWORK DISCONNECT] Feed error: {e}")