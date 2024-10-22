from gtts import gTTS
from pydub import AudioSegment
import numpy as np

# Funzione per variare l'intonazione
def modifica_intonazione(audio_segment, semitoni):
    # Cambia la velocità (intonazione) dell'audio
    return audio_segment._spawn(audio_segment.raw_data, overrides={
        "frame_rate": int(audio_segment.frame_rate * (2 ** (semitoni / 12.0)))
    }).set_frame_rate(audio_segment.frame_rate)

# Testo da "cantare"
testo = "Ciao! Questo è un esempio di sintesi vocale che canta."

# Creazione dell'oggetto gTTS
voce = gTTS(text=testo, lang='it', slow=False)
voce.save("voce.mp3")

# Caricamento della voce sintetica
voce_audio = AudioSegment.from_file("voce.mp3")

# Variazione dell'intonazione
intonazioni = [0, 2, 4, 5, 7]  # Semitoni da variare
melodia = AudioSegment.silent(duration=0)

for semitono in intonazioni:
    melodia += modifica_intonazione(voce_audio, semitono)

# Salvataggio della canzone finale
melodia.export("canzone.mp3", format="mp3")

# Facoltativo: riproduzione della canzone
#import os
#os.system("start canzone.mp3")  # Su Windows
