from gtts import gTTS
from pydub import AudioSegment

# Frequenze delle note (Do, Re, Mi, Fa, Sol)
note_piano = {
    0: "note_do.wav",   # File per Do
    2: "note_re.wav",   # File per Re
    4: "note_mi.wav",   # File per Mi
    5: "note_fa.wav",   # File per Fa
    7: "note_sol.wav"   # File per Sol
}

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

# Generazione della melodia strumentale
for semitono in intonazioni:
    if semitono in note_piano:
        nota = AudioSegment.from_file(note_piano[semitono])
        melodia_strumentale += nota + AudioSegment.silent(duration=200)  # Pausa tra le note

# Unione delle tracce
canzone_finale = melodia_strumentale.overlay(voce_audio)

# Salvataggio della canzone finale
canzone_finale.export("canzone_con_musica.mp3", format="mp3")
