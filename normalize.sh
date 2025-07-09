#!/bin/bash

SOURCE_DIR="kgn_vn_dataset"
DEST_DIR="normalized_audio"

# create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# loop through all files in SOURCE_DIR (specifically .m4a, .amr, and .wav files)
for f in "$SOURCE_DIR"/*.m4a "$SOURCE_DIR"/*.amr "$SOURCE_DIR"/*.wav; do
  
  # check that file actually exists
  [ -f "$f" ] || continue

  # exclude path from filename
  bname=$(basename "$f")
  
  # exclude extension from filename
  fname="${bname%.*}"

  echo "Processing $bname -> ${fname}.wav"

  # ffmpeg command
  # -i: input file
  # -af loudnorm: applies loudness normalization filter
  # -ar 44100: sets sample rate
  # -y: overwrite output file if it exists
  ffmpeg -i "$f" -af loudnorm -ar 44100 -y "$DEST_DIR/${fname}.wav"

done

echo "Normalization complete. Files are in the '$DEST_DIR' folder."