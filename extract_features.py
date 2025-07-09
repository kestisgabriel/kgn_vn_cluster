import librosa
import numpy as np
import pandas as pd
import os

# --- Configuration ---
# Directory where your normalized audio files are.
AUDIO_DIR = "normalized_audio"
OUTPUT_CSV = "music_features_structural.csv"

# --- Parameters for Segmentation ---
# The number of segments to find in each file. This is now the main parameter to tune.
# For a 3-5 minute song, 3-5 segments might be appropriate (intro, verse, chorus, etc.).
# For a long, one-hour jam, you might want more, like 20-30.
# You will need to experiment with this value.
TARGET_SEGMENTS = 15 

# --- Feature Extraction for a single chunk ---
def extract_segment_features(y_segment, sr):
    """Extracts features from a small audio segment."""
    n_fft = 2048
    hop_length = 512

    chroma = librosa.feature.chroma_stft(y=y_segment, sr=sr, n_fft=n_fft, hop_length=hop_length)
    mfccs = librosa.feature.mfcc(y=y_segment, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

    return {
        'chroma_mean': np.mean(chroma), 'chroma_std': np.std(chroma),
        'mfccs_mean': np.mean(mfccs), 'mfccs_std': np.std(mfccs),
    }

# --- Main Script Logic ---
if __name__ == "__main__":
    all_segment_features = []
    
    for filename in os.listdir(AUDIO_DIR):
        if not filename.endswith('.wav'):
            continue
            
        file_path = os.path.join(AUDIO_DIR, filename)
        print(f"Segmenting: {filename}...")

        try:
            y, sr = librosa.load(file_path, sr=None)
            
            # --- Structural Segmentation Logic ---
            # 1. Compute features to detect change (we'll use chroma)
            chroma_for_segmentation = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # 2. Find the segment boundaries
            # We add a 0 at the start and the total number of frames at the end
            # This gives us start and end points for our segments.
            boundaries = librosa.segment.agglomerative(chroma_for_segmentation, k=TARGET_SEGMENTS)
            boundary_times = librosa.frames_to_time(boundaries, sr=sr)

            # --- Process each discovered segment ---
            for i in range(len(boundary_times) - 1):
                start_time = boundary_times[i]
                end_time = boundary_times[i+1]
                
                start_sample = librosa.time_to_samples(start_time, sr=sr)
                end_sample = librosa.time_to_samples(end_time, sr=sr)
                
                y_segment = y[start_sample:end_sample]

                # Extract the features we'll use for clustering
                segment_features = extract_segment_features(y_segment, sr)

                segment_features['filename'] = filename
                segment_features['start_time_s'] = start_time
                segment_features['end_time_s'] = end_time
                
                all_segment_features.append(segment_features)

        except Exception as e:
            print(f"Could not process {filename}: {e}")

    # --- Save Results ---
    if all_segment_features:
        df = pd.DataFrame(all_segment_features)
        cols = ['filename', 'start_time_s', 'end_time_s'] + [c for c in df.columns if c not in ['filename', 'start_time_s', 'end_time_s']]
        df = df[cols]
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n✅ Structural segmentation complete!")
        print(f"📊 Data saved to {OUTPUT_CSV}")
    else:
        print("No features were extracted.")