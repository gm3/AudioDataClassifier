import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import click

@click.command()
@click.argument('audio_folder', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def analyze_audio_folder(audio_folder):
    # Loop through each file in the specified folder
    for filename in os.listdir(audio_folder):
        if filename.endswith('.mp3'):
            filepath = os.path.join(audio_folder, filename)
            
            # Load the audio file
            y, sr = librosa.load(filepath)
            
            # Perform a Fourier Transform to get the spectrum
            D = librosa.stft(y)
            
            # Get amplitude and phase
            amplitude, phase = librosa.magphase(D)
            
            # Calculate BPM
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            bpm = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)[0]
            
            print(f"Calculated BPM for {filename}: {bpm}")
            
            # Optional: Plot the spectrum
            plt.figure()
            librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
            plt.title(f'Spectral analysis of {filename}')
            plt.colorbar(format='%+2.0f dB')
            plt.tight_layout()
            plt.show()

if __name__ == '__main__':
    analyze_audio_folder()


# $ pip install click librosa matplotlib
# $ python folder_audio_analyzer.py /path/to/audio/folder/
