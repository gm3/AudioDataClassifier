import os
import json
import aubio
import eyed3
import subprocess
import librosa
import matplotlib.pyplot as plt
import numpy as np

def convert_mp3_to_wav(mp3_path, wav_path):
    cmd = ["ffmpeg", "-i", mp3_path, wav_path]
    subprocess.call(cmd)

    

def get_bpm_aubio(file_path):
    temp_wav = None
    if file_path.lower().endswith('.mp3'):
        temp_wav = "/tmp/temp_bpm_extraction.wav"
        convert_mp3_to_wav(file_path, temp_wav)
        file_path = temp_wav

    src = aubio.source(file_path, 0, 512)
    hop_size = src.hop_size
    tempo = aubio.tempo("default", 1024, hop_size, src.samplerate)
    
    beats = 0
    while True:
        samples, read = src()
        is_beat = tempo(samples)
        if is_beat:
            beats += 1
        if read < hop_size:
            break

    if temp_wav:
        os.remove(temp_wav)

    return tempo.get_bpm()

def get_key(y, sr):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
    
    # Get the key based on the maximum mean value of chroma feature
    key_idx = np.argmax(np.mean(chroma, axis=1))
    key_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = key_notes[key_idx]
    
    # Determine Major or Minor key based on tonnetz
    fifth = tonnetz[4]
    minor_third = tonnetz[2]
    if np.mean(minor_third) > np.mean(fifth):
        key += "m"  # Minor
        
    return key


def get_audio_metadata(file_path):
    try:
        y, sr = librosa.load(file_path)
        length = float(librosa.get_duration(y=y, sr=sr))
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        spectral_bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
        zero_crossing_rate = float(np.mean(librosa.feature.zero_crossing_rate(y)))
        chroma_stft = float(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr)).tolist()  # Assuming this is a list of float32

        return {
            "Length": length,
            "SpectralCentroid": spectral_centroid,
            "SpectralBandwidth": spectral_bandwidth,
            "ZeroCrossingRate": zero_crossing_rate,
            "ChromaSTFT": chroma_stft,
            "MFCC": mfcc  # This should already be a list of native Python floats
        }
    except Exception as e:
        print(f"Exception in get_audio_metadata: {e}")
        return {}





def write_metadata_to_file(file_path, metadata):
    audio_file = eyed3.load(file_path)
    if audio_file is not None:
        audio_file.tag.bpm = int(metadata.get("BPM", 0))
        audio_file.tag.comments.set(metadata.get("Description", "N/A"))
        audio_file.tag.save()

def plot_spectrum(D, filename):
    plt.figure()
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
    plt.title(f'Spectral analysis of {filename}')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()

def analyze_audio_folder(audio_folder):
    combined_audio_metadata = {}
    
    for filename in os.listdir(audio_folder):
        if filename.endswith('.mp3'):
            filepath = os.path.join(audio_folder, filename)
            single_audio_metadata = {}
            
            try:
                bpm = get_bpm_aubio(filepath)
                y, sr = librosa.load(filepath)
                key = get_key(y, sr)
                extracted_metadata = get_audio_metadata(filepath)
    
                
                # Combine the extracted metadata with additional fields
                metadata = {
                    "BPM": bpm,
                    "Description": "N/A",
                    "IfItLoops": "Unknown",
                    "Key": key,
                    **extracted_metadata  # Merge in the extracted metadata
                }

                single_audio_metadata[filename] = metadata
                
                # Save individual JSON
                individual_json_filename = f"{filename}_metadata.json"
                individual_json_filepath = os.path.join(audio_folder, individual_json_filename)
                
                with open(individual_json_filepath, "w") as f:
                    json.dump(single_audio_metadata, f, indent=4)
                
                print(f"Metadata for {filename} saved at {individual_json_filepath}")
                
                # Extract spectral data and plot
                y, sr = librosa.load(filepath)
                D = librosa.stft(y)
                plot_spectrum(D, filename)
                
                write_metadata_to_file(filepath, metadata)
                
                # Update combined metadata
                combined_audio_metadata[filename] = metadata
                
            except Exception as e:
                print(f"Could not process {filename}. Error: {e}")
                
    # Save combined JSON
    combined_json_filename = "combined_audio_metadata.json"
    combined_json_filepath = os.path.join(audio_folder, combined_json_filename)
    
    with open(combined_json_filepath, "w") as f:
        json.dump(combined_audio_metadata, f, indent=4)
        
    print(f"Combined metadata JSON saved at {combined_json_filepath}")

if __name__ == '__main__':
    if not os.system("which ffmpeg"):
        analyze_audio_folder('.')  # Replace with your actual folder path
    else:
        print("ffmpeg is not installed. Please install ffmpeg first.")
