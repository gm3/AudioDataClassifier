
# Audio Analysis Tool

## Overview

This Python script is designed to analyze audio files, particularly MP3 files, in a given folder. It extracts various audio features such as BPM (Beats Per Minute), Key, Length, Spectral Centroid, Spectral Bandwidth, Zero Crossing Rate, Chroma STFT, and MFCC (Mel-frequency cepstral coefficients). The script also plots the spectral analysis of the audio files and saves the metadata both individually for each audio file and collectively for all audio files in the folder.

## Prerequisites

Python 3.x
`ffmpeg`
`aubio`
`eyed3`
`librosa`
`matplotlib`
`numpy`
You can install the required Python packages using pip:

```bash
pip install aubio eyed3 librosa matplotlib numpy
```

And you can install `ffmpeg` using the package manager for your system. For example, on Ubuntu:

```bash
sudo apt-get install ffmpeg
```

## How to Use

Place your `.mp3` audio files in the folder where the script is located (or specify the folder path in the script).

Run the script:

```bash
python <script_name>.py
```

Replace \<script_name\> with the name of this script.

The script will analyze each `.mp3` file in the folder and will create JSON files with the metadata for each audio file. It will also create a combined JSON file for all the audio files.

Spectral plots will be displayed for each audio file during the analysis.

## Output

Individual JSON files for each audio file with their metadata.
A combined JSON file that contains metadata for all audio files.
Spectral plots displayed during the analysis.
## Metadata Fields

`BPM`: Beats Per Minute
`Description`: A placeholder field, set to "N/A" by default.
`IfItLoops`: A placeholder field, set to "Unknown" by default.
`Key`: Musical key of the audio file
`Length`: Duration of the audio file in seconds
`SpectralCentroid`: Spectral Centroid of the audio file
`SpectralBandwidth`: Spectral Bandwidth of the audio file
`ZeroCrossingRate`: Zero Crossing Rate of the audio file
`ChromaSTFT`: Chroma Short-time Fourier Transform of the audio file
`MFCC`: Mel-frequency cepstral coefficients of the audio file
## Troubleshooting

If you encounter an error message saying "ffmpeg is not installed", please ensure that ffmpeg is installed and accessible from the command line.

## License

This project is open-source and available under the MIT License.
