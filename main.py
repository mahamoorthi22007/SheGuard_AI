import os
import numpy as np
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# --- CONFIGURATION ---
DATASET_DIR = "dataset"
SAMPLE_RATE = 16000
MODEL_OUTPUT_FILE = "scream_detector_model.pkl"

# Mapping your exact folder names to target logic states
# 0 = Safe Environment (Normal/Media/Children), 2 = TRUE DISTRESS SCREAM
# Change this block to match your exact folder names:
CATEGORIES = {
    "NotScream": 0,   # 🌟 Removed the "-ing" to match your folder
    "Scream": 2
}

def extract_features(file_path):
    """Extracts structural acoustic arrays matching the live gateway filter."""
    try:
        # Load 1 second window duration slice
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=1.0)
        
        # Standardize sample bounds via zero padding
        if len(y) < SAMPLE_RATE:
            y = np.pad(y, (0, SAMPLE_RATE - len(y)), 'constant')
            
        # Extract identical multi-sensor matrix parameters
        mfccs = librosa.feature.mfcc(y=y, sr=SAMPLE_RATE, n_mfcc=13)
        contrast = librosa.feature.spectral_contrast(y=y, sr=SAMPLE_RATE)
        chroma = librosa.feature.chroma_stft(y=y, sr=SAMPLE_RATE)
        
        return np.concatenate((
            np.mean(mfccs, axis=1), 
            np.var(mfccs, axis=1), 
            np.mean(contrast, axis=1), 
            np.mean(chroma, axis=1)
        ))
    except Exception as e:
        print(f"⚠️ Skipping broken sample {file_path}: {e}")
        return None

def main():
    X, y = [], []
    
    print("=" * 60)
    print("   SHEGUARD AI - DATASET TRAINING ENGINE")
    print("=" * 60)
    
    for folder_name, label in CATEGORIES.items():
        folder_path = os.path.join(DATASET_DIR, folder_name)
        if not os.path.exists(folder_path):
            print(f"❌ Cannot find directory path: {folder_path}")
            continue
            
        print(f"[EXTRACTING] Processing files from: '{folder_name}'...")
        files = [f for f in os.listdir(folder_path) if f.endswith('.wav') or f.endswith('.mp3')]
        
        for file in files:
            file_path = os.path.join(folder_path, file)
            features = extract_features(file_path)
            if features is not None:
                X.append(features)
                y.append(label)

    X, y = np.array(X), np.array(y)
    if len(X) == 0:
        print("❌ Dataset is empty! Please drop your audio clips into the folders first.")
        return

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[TRAINING] Building intelligent acoustic decision trees...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Performance Validation
    y_pred = model.predict(X_test)
    print(f"\n📈 INTELLIGENCE RATING ACCURACY: {accuracy_score(y_test, y_pred) * 100:.2f}%")

    # Export compiled intelligence model asset
    joblib.dump(model, MODEL_OUTPUT_FILE)
    print(f"🎉 Saved successfully as: '{MODEL_OUTPUT_FILE}'")

if __name__ == "__main__":
    main()