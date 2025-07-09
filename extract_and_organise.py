import pandas as pd
import os
import subprocess

# config
RESULTS_CSV = "clustered_results_sorted.csv"
SOURCE_AUDIO_DIR = "normalized_audio"
FINAL_OUTPUT_DIR = "final_clustered_audio"

if __name__ == "__main__":
    # load clustered results
    df = pd.read_csv(RESULTS_CSV)

    # create output dir
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)
    print(f"Created main directory: {FINAL_OUTPUT_DIR}")

    # process each segment from .csv
    for index, row in df.iterrows():
        cluster_label = f"Cluster_{int(row['cluster']):03d}" # e.g., Cluster_005
        original_filename = row['filename']
        start_time = row['start_time_s']
        end_time = row['end_time_s']
        duration = end_time - start_time

        # create dir for the cluster if it doesn't exist
        cluster_dir = os.path.join(FINAL_OUTPUT_DIR, cluster_label)
        os.makedirs(cluster_dir, exist_ok=True)

        # define file paths
        input_path = os.path.join(SOURCE_AUDIO_DIR, original_filename)
        output_filename = f"{cluster_label}_{original_filename.replace('.wav', '')}__{index}.wav"
        output_path = os.path.join(cluster_dir, output_filename)

        print(f"Extracting segment for {cluster_label} from {original_filename}...")

        # construct ffmpeg command to extract the segment
        command = [
            'ffmpeg',
            '-i', input_path,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c', 'copy', # copy audio without re-encoding
            '-y',         # overwrite output file if it exists
            output_path
        ]
        
        # subprocess to execute command
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\n All segments successfully extracted and organized.")