from gtts import gTTS
from pydub import AudioSegment
from music21 import note, stream
import subprocess
import os

# Percorso del tuo SoundFont (.sf2)
soundfont_path = "path_to_your_soundfont.sf2"

# Testo da "cantare"
testo = "Ciao! Questo è un esempio di sintesi vocale che canta."

# Creazione dell'oggetto gTTS
voce = gTTS(text=testo, lang='it', slow=False)
voce.save("voce.mp3")

# Caricamento della voce sintetica
voce_audio = AudioSegment.from_file("voce.mp3")

# Creazione delle note con music21 (Do, Re, Mi, Fa, Sol)
do = note.Note('C4')  # Do centrale
re = note.Note('D4')  # Re
mi = note.Note('E4')  # Mi
fa = note.Note('F4')  # Fa
sol = note.Note('G4')  # Sol

# Creare un flusso musicale con le note
melodia = stream.Stream([do, re, mi, fa, sol])

# Salvataggio della melodia come file MIDI
midi_filename = "melodia.mid"
melodia.write('midi', fp=midi_filename)

# Conversione del MIDI in WAV usando FluidSynth
wav_filename = "melodia.wav"
subprocess.run([
    'fluidsynth',
    '-ni', soundfont_path,  # SoundFont file
    midi_filename,          # MIDI file
    '-F', wav_filename,     # Output file
    '-r', '44100'           # Sample rate
])

# Caricamento del file WAV della melodia
melodia_audio = AudioSegment.from_file(wav_filename)

# Unione della melodia strumentale con la voce
canzone_finale = melodia_audio.overlay(voce_audio)

# Salvataggio della canzone finale in formato MP3
canzone_finale.export("canzone_con_musica.mp3", format="mp3")

# Pulizia dei file intermedi (MIDI e WAV)
os.remove(midi_filename)
os.remove(wav_filename)
