from gtts import gTTS
from pydub import AudioSegment
import numpy as np

# Funzione per generare un'onda sinusoidale simile a un pianoforte
def genera_nota_piano(frequenza, durata_ms):
    sample_rate = 44100
    t = np.linspace(0, durata_ms / 1000, int(sample_rate * (durata_ms / 1000)), False)
    onda = 0.5 * np.sin(2 * np.pi * frequenza * t) * (1 - t * frequenza % 1.0)  # Onda simile a un pianoforte
    return AudioSegment(onda.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)

# Frequenze delle note (Do, Re, Mi, Fa, Sol)
frequenze = [261.63, 293.66, 329.63, 349.23, 392.00]  # Frequenze delle note in Hz

# Testo da "cantare"
testo = "Ciao! Questo è un esempio di sintesi vocale che canta."

# Creazione dell'oggetto gTTS
voce = gTTS(text=testo, lang='it', slow=False)
voce.save("voce.mp3")

# Caricamento della voce sintetica
voce_audio = AudioSegment.from_file("voce.mp3")

# Variazione dell'intonazione
intonazioni = [0, 2, 4, 5, 7]
melodia_strumentale = AudioSegment.silent(duration=0)
durata_nota = 1000  # Durata di ciascuna nota in millisecondi

# Generazione della melodia strumentale
for semitono in intonazioni:
    frequenza = frequenze[semitono % len(frequenze)]
    nota = genera_nota_piano(frequenza, durata_nota)
    melodia_strumentale += nota 

# Combine the audio
voce_audio = voce_audio + 5  # Decrease the voice volume
melodia_strumentale = melodia_strumentale - 2  # Increase the melody volume
combined_audio = melodia_strumentale.overlay(voce_audio)

melodia_strumentale.export("melodia.mp3", format="mp3")

# Save the final audio
combined_audio.export("canzone.mp3", format="mp3")