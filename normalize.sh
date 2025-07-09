#!/bin/bash

# The folder containing your original audio files
SOURCE_DIR="kgn_vn_dataset"

# The folder where processed files will be saved
DEST_DIR="normalized_audio"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Loop through all specified file types in the source directory
for f in "$SOURCE_DIR"/*.m4a "$SOURCE_DIR"/*.amr "$SOURCE_DIR"/*.wav; do
  
  # Check if a file actually exists to avoid errors
  [ -f "$f" ] || continue

  # Get the base filename without the path (e.g., "my_song.m4a")
  bname=$(basename "$f")
  
  # Get the filename without the extension (e.g., "my_song")
  fname="${bname%.*}"

  echo "Processing $bname -> ${fname}.wav"

  # Run FFmpeg to convert, normalize loudness, and set sample rate
  # -i: input file
  # -af loudnorm: applies the loudness normalization filter
  # -ar 44100: sets the sample rate to a standard 44.1kHz
  # -y: overwrite output file if it exists
  ffmpeg -i "$f" -af loudnorm -ar 44100 -y "$DEST_DIR/${fname}.wav"

done

echo "✅ Normalization complete! Files are in the '$DEST_DIR' folder."