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

import tensorflow as tf
import librosa
import pretty_midi
import numpy as np
import soundfile as sf
from melgan import MelGANGenerator  # Assicurati di avere il modello MelGAN configurato

def load_melgan_model():
    # Carica il modello MelGAN pre-addestrato
    # Assicurati che il modello MelGAN sia stato addestrato e disponibile come un file .h5 o checkpoint
    model = MelGANGenerator()
    model.load_weights('melgan_model.h5')  # Sostituisci con il percorso del tuo modello MelGAN
    return model

def apply_vocoder(input_audio_path, output_audio_path, midi_path):
    # Carica il file vocale
    y, sr = librosa.load(input_audio_path, sr=None)

    # Carica la melodia generata dal MIDI
    midi_data = pretty_midi.PrettyMIDI(midi_path)

    # Estrai il pitch (f0_hz) e la durata delle note MIDI
    f0_hz = []
    time_stamps = []  # Timestamps per ogni nota
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            f0_hz.append(note.pitch)  # La nota MIDI viene convertita in frequenza (Hz)
            time_stamps.append(note.start)  # Aggiungi il timestamp di inizio della nota

    # Ora 'f0_hz' e 'time_stamps' sono liste che rappresentano il pitch e il tempo delle note
    f0_hz = np.array(f0_hz)
    time_stamps = np.array(time_stamps)

    # Creare una sequenza di pitch per l'audio: interpolazione tra i punti temporali
    f0_interpolated = np.interp(np.linspace(0, len(y) / sr, len(y)), time_stamps, f0_hz)

    # Pre-processa l'audio per generare il mel-spectrogramma
    mel_spec = librosa.feature.melspectrogram(y, sr=sr, n_mels=80, fmax=8000)
    mel_spec = np.expand_dims(mel_spec, axis=0)  # Aggiungi dimensione batch per MelGAN

    # Carica il modello MelGAN
    model = load_melgan_model()

    # Usa MelGAN per generare l'audio
    generated_audio = model.predict(mel_spec)  # Il vocoder MelGAN restituisce audio sintetizzato

    # Converti l'audio generato in un array numpy
    generated_audio = generated_audio.squeeze()  # Rimuovi le dimensioni extra

    # Salva l'output vocoder come file WAV
    sf.write(output_audio_path, generated_audio, sr)


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
apply_vocoder('vocals.mp3', 'vocal1.mp3', midi_file)

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
