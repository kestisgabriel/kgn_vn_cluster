# Audio Categorization Pipeline

This set of scripts is a pipeline for batch-processing and categorising audio files from voice memos. This is done by normalizing source material, extracting features, and creating clusters of related audio segments.

## Requirements

-   Python
-   FFmpeg
-   Librosa
-   Pandas
-   Numpy
-   Scikit-Learn

## Usage

### 1. Preprocess Audio

Normalize the audio files in the root dir (set to `kgn_vn_dataset`) by running `./normalize.sh`. This will batch-process all the source audio files and place them in a dir called `normalized_audio`.

### 2. Extract Features

Run `python extract_features.py` to extract features from the normalized audio files. This will create `music_features_structural.csv` containing the extracted features.

### 3. Cluster Segments

Run `python cluster_segments.py` to cluster the extracted features using K-Means clustering. This will create `clustered_results.csv` containing the cluster assignments.

### 4. Sort By Cluster

Open `clustered_results.csv` in a .csv editor of choice (e.g. Excel) and sort the table by the 'cluster' column (alphabetically A-Z). Export this sorted table and save it as `clustered_results_sorted.csv`
_N.B. Make sure that the row containing the column names is still on top when exporting after sorting, or else the next script will fail._

### 5. Extract and Organize

Run `python extract_and_organise.py` to extract segments from the audio files based on the cluster assignments and organize them into corresponding folders according to their cluster labels.

## Output

The final output will be a dir called `final_clustered_audio` containing subdirectories for each cluster label, with the corresponding audio segments extracted and saved as separate files.

## Notes

-   This program works best with low-variance data sets. High variation in tempo, mic placement, instrument, etc will hamper the program's ability to deduce coherence between different audio files.
-   The pipeline is currently set up to extract features from the chroma and mel-frequency cepstral coefficients (MFCCs) of the audio segments.
-   The K-Means clustering algorithm is used to cluster the extracted features.
-   The number of clusters is set to 50, but this can be adjusted by changing the `N_CLUSTERS` variable in `cluster_segments.py`.
-   The `extract_and_organise.py` script is currently set up to extract segments of approximately 10-15 seconds in length, but this can be adjusted by changing the `TARGET_SEGMENTS` variable.
