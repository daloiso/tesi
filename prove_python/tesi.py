from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine
import random

# Testo da cantare
testo = "Ciao! Questo è un esempio di sintesi vocale con melodia variata."

# Creazione dell'oggetto gTTS
voce = gTTS(text=testo, lang='it', slow=False)
voce.save("voce.mp3")

# Caricamento della voce sintetica
voce_audio = AudioSegment.from_file("voce.mp3")

# Creazione di una melodia variata
melodia = AudioSegment.silent(duration=0)  # Iniziamo con un segmento silenzioso

# Aggiungiamo note diverse per creare variazioni
frequenze = [440, 494, 523, 587, 659, 698, 784]  # Frequenze delle note
durazioni = [400, 600, 800]  # Durate delle note

for _ in range(len(voce_audio) // 500):  # Genera note per tutta la durata della voce
    frequenza = random.choice(frequenze)
    durata = random.choice(durazioni)
    nota = Sine(frequenza).to_audio_segment(duration=durata)
    melodia += nota

# Aggiunta della melodia alla voce
canzone = voce_audio.overlay(melodia)

# Salvataggio della canzone finale
canzone.export("canzone.mp3", format="mp3")