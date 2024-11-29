from midi2audio import FluidSynth
from pydub import AudioSegment
from gtts import gTTS
import ddsp
import tensorflow as tf
import numpy as np
import librosa
import tensorflow_hub as hub

import numpy as np


def generate_vocal_audio(lyrics, output_path):
    tts = gTTS(text=lyrics, lang='it', slow=False)
    tts.save(output_path)



# Function to convert MP3 to WAV using pydub
def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

# Function to convert WAV to MP3 using pydub
def wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

# Example: Load an audio file and extract its mel-spectrogram
def load_audio(filepath):
    audio, sr = librosa.load(filepath, sr=16000)
    return audio, sr




# Carica il soundfont di qualità
#sound_font = "Bass Guitars.sf2"  # Es: "GeneralUser.sf2"
midi_file = "5.mid"  # Il tuo file MIDI
output_audio = "output_audio.wav"  # File audio di output


#fs = FluidSynth(sound_font)
fs = FluidSynth()
fs.midi_to_audio(midi_file, output_audio)

# Inizializza il client TTS di Google Cloud
lyrics = "Dopo aver giocato, metti i giocattoli a posto, ogni cosa al suo posto, così la stanza è più bella, è facile, basta fare attenzione!"

generate_vocal_audio(lyrics, 'vocals.mp3')
audio_path = 'vocals.mp3'
audio, sr = librosa.load(audio_path, sr=16000)
mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=80)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
np.save('mel_spectrogram.npy', log_mel_spectrogram)
mel_spectrogram = tf.convert_to_tensor(mel_spectrogram, dtype=tf.float32)

#vocoder_url = '/'
#vocoder_model = hub.load(vocoder_url)
#audio = vocoder_model(mel_spectrogram)

# Save the output as a WAV file
#audio_output = audio.numpy().squeeze()
#librosa.output.write_wav("final_vocal.wav", audio_output, sr=16000)

instrumental = AudioSegment.from_wav("output_audio.wav")  # Audio strumentale (MIDI->WAV)
vocal = AudioSegment.from_mp3("vocals.mp3")  # Audio vocale (TTS)

# Allinea la lunghezza delle tracce (taglia la traccia vocale se è più lunga dell'strumentale)
min_length = min(len(instrumental), len(vocal))
instrumental = instrumental[:min_length]
vocal = vocal[:min_length]

# Regola il volume della traccia vocale se necessario
vocal = vocal - 10  # Abbassa il volume della voce di 10 dB se necessario

# Mescola le tracce
final_mix = instrumental.overlay(vocal)

# Esporta il mix finale
final_mix.export("final_song.mp3", format="mp3")
