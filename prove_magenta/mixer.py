from midi2audio import FluidSynth
from pydub import AudioSegment
from gtts import gTTS
import tensorflow as tf
import numpy as np
import librosa

import librosa
import soundfile as sf
from pydub import AudioSegment
import ddsp
import pretty_midi
from ddsp.training import inference

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


#import torch
#import torchaudio
#from melgan import MelGAN  # Assicurati di avere il modello di MelGAN pre-addestrato

#def apply_melgan_vocoder(input_audio_path, output_audio_path, midi_path):
    # Carica l'audio della voce
#    waveform, sample_rate = torchaudio.load(input_audio_path)

    # Carica il modello MelGAN pre-addestrato (o usa un modello personalizzato)
#    melgan_model = MelGAN.load_pretrained('melgan_model.pth')

    # Converti la traccia MIDI in mel-spectrogrammi
#    mel_spectrogram = midi_to_mel_spectrogram(midi_path)

    # Usa il modello vocoder per generare la traccia audio modificata
#    modified_waveform = melgan_model(mel_spectrogram)

    # Salva l'audio risultante
#    torchaudio.save(output_audio_path, modified_waveform, sample_rate)

# Carica il soundfont di qualità
#sound_font = "Bass Guitars.sf2"  # Es: "GeneralUser.sf2"
midi_file = "3.mid"  # Il tuo file MIDI
output_audio = "output_audio.wav"  # File audio di output


#fs = FluidSynth(sound_font)
fs = FluidSynth()
fs.midi_to_audio(midi_file, output_audio)

# Inizializza il client TTS di Google Cloud
#lyrics = "Dopo aver giocato, metti i giocattoli a posto, ogni cosa al suo posto, così la stanza è più bella, è facile, basta fare attenzione!"

#generate_vocal_audio(lyrics, 'vocals.mp3')


#mp3_to_wav('vocals.mp3','path_to_vocal_audio.wav')

#wav_to_mp3('audio.wav','audio_synth.mp3')
#apply_melgan_vocoder('path_to_vocal_audio.wav', 'output_audio_path.wav', '5.mid')

#vocoder_url = '/'
#vocoder_model = hub.load(vocoder_url)
#audio = vocoder_model(mel_spectrogram)

# Save the output as a WAV file
#audio_output = audio.numpy().squeeze()
#librosa.output.write_wav("final_vocal.wav", audio_output, sr=16000)

instrumental = AudioSegment.from_wav("output_audio.wav")  # Audio strumentale (MIDI->WAV)
vocal = AudioSegment.from_wav("3.wav")  # Audio vocale (TTS)

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
