import librosa
import numpy as np
import pandas as pd
import os

# --- Configuration ---
# Directory where your normalized audio files are.
AUDIO_DIR = "normalized_audio"

# File where the final feature dataset will be saved.
OUTPUT_CSV = "music_features.csv"

# --- Feature Extraction ---
def extract_features(file_path):
    """Extracts a set of features from an audio file."""
    try:
        # Load the audio file
        y, sr = librosa.load(file_path, sr=None) # sr=None to use native sample rate

        # 1. Extract Chroma Features (for harmony)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma)
        chroma_std = np.std(chroma)

        # 2. Extract MFCCs (for timbre)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs)
        mfccs_std = np.std(mfccs)
        
        # 3. Extract Tempo (for rhythm)
        # We use beat_track which is often more robust
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return {
            "filename": os.path.basename(file_path),
            "tempo": tempo,
            "chroma_mean": chroma_mean,
            "chroma_std": chroma_std,
            "mfccs_mean": mfccs_mean,
            "mfccs_std": mfccs_std,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# --- Main Script Logic ---
if __name__ == "__main__":
    all_features = []
    
    # Walk through the directory of normalized audio files
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith('.wav'):
            file_path = os.path.join(AUDIO_DIR, filename)
            print(f"Processing: {filename}...")
            
            features = extract_features(file_path)
            
            if features:
                all_features.append(features)

    # Convert the list of features into a pandas DataFrame
    df = pd.DataFrame(all_features)
    
    # Save the DataFrame to a CSV file
    df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n✅ Feature extraction complete!")
    print(f"📊 Data saved to {OUTPUT_CSV}")