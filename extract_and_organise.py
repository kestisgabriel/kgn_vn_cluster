import pandas as pd
import os
import subprocess

# --- Configuration ---
RESULTS_CSV = "clustered_results_sorted.csv"
SOURCE_AUDIO_DIR = "normalized_audio"
FINAL_OUTPUT_DIR = "final_clustered_audio"

# --- Main Logic ---
if __name__ == "__main__":
    # Load the clustered results
    df = pd.read_csv(RESULTS_CSV)

    # Create the main output directory
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)
    print(f"Created main directory: {FINAL_OUTPUT_DIR}")

    # Process each segment from the CSV
    for index, row in df.iterrows():
        cluster_label = f"Cluster_{int(row['cluster']):03d}" # e.g., Cluster_005
        original_filename = row['filename']
        start_time = row['start_time_s']
        end_time = row['end_time_s']
        duration = end_time - start_time

        # Create a directory for the cluster if it doesn't exist
        cluster_dir = os.path.join(FINAL_OUTPUT_DIR, cluster_label)
        os.makedirs(cluster_dir, exist_ok=True)

        # Define file paths
        input_path = os.path.join(SOURCE_AUDIO_DIR, original_filename)
        output_filename = f"{cluster_label}_{original_filename.replace('.wav', '')}__{index}.wav"
        output_path = os.path.join(cluster_dir, output_filename)

        print(f"Extracting segment for {cluster_label} from {original_filename}...")

        # Construct and run the FFmpeg command to extract the segment
        command = [
            'ffmpeg',
            '-i', input_path,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c', 'copy', # Copies the audio without re-encoding for speed
            '-y',         # Overwrite output file if it exists
            output_path
        ]
        
        # Use subprocess.run to execute the command
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\n✅ All segments have been extracted and organized!")