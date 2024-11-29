from mido import MidiFile, MidiTrack, Message
from gtts import gTTS
from pydub import AudioSegment
import subprocess
import re
import nltk
import pretty_midi
import matplotlib.pyplot as plt

# Scarica i dati necessari da NLTK (solo la prima volta)
nltk.download('punkt')


# Funzione per dividere una parola in sillabe in italiano
def syllabify_italian(word):
    word = word.lower()  # Converti la parola in minuscolo
    vowels = "aeiouàèéìòóù"  # Vocale italiana
    syllables = []  # Lista per contenere le sillabe
    syllable = ""  # Variabile temporanea per la sillaba corrente

    # Scorrere ogni lettera della parola
    i = 0
    while i < len(word):
        if word[i] in vowels:
            syllable += word[i]  # Aggiungi la vocale alla sillaba
            # Verifica se la vocale è seguita da una consonante
            if i + 1 < len(word) and word[i + 1] not in vowels:
                syllables.append(syllable)  # Aggiungi la sillaba alla lista
                syllable = ""  # Resetta la sillaba corrente
        else:
            syllable += word[i]  # Aggiungi la consonante alla sillaba

        i += 1

    if syllable:
        syllables.append(syllable)  # Aggiungi l'ultima sillaba

    return syllables


def split_into_syllables(text):
    # Split the lyrics into syllables
    syllables = [syllabify_italian(word) for word in text.split()]
    return syllables


import mido
from mido import MidiFile, MidiTrack, Message


def adjust_midi_for_syllables(midi_file_path, syllables, output_file='modified_midi.mid'):
    midi = MidiFile(midi_file_path)
    adjusted_midi = MidiFile()

    # Durata base delle note per le tracce musicali (in ticks)
    note_duration = 960  # Durata base per le note musicali in ticks

    syllable_index = 0
    syllable_group_index = 0  # Indice per gestire i gruppi di sillabe

    # Estrai il BPM e i ticks per beat dal file MIDI
    ticks_per_beat = midi.ticks_per_beat
    bpm = 120  # Imposta un valore di default di BPM, se non c'è il cambio tempo (tempo in battiti per minuto)

    # Estrazione del BPM dal messaggio 'set_tempo' se presente
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                microseconds_per_beat = msg.time  # Microsecondi per battuta
                if microseconds_per_beat==0 :
                    bpm=60
                else:
                    bpm = 60000000 // microseconds_per_beat  # Formula per calcolare il BPM
                print(f"BPM estratto: {bpm}")  # Stampa il BPM per la verifica
                break

    # Calcolare la durata di un beat in secondi
    seconds_per_beat = 60.0 / bpm  # 60 secondi diviso il BPM
    ticks_per_second = ticks_per_beat / seconds_per_beat  # Calcola quanti ticks per secondo

    print(f"BPM finale in uso: {bpm}")  # Stampa il BPM finale per la verifica

    # Processa ogni traccia nel file MIDI
    for track in midi.tracks:
        new_track = MidiTrack()
        adjusted_midi.tracks.append(new_track)

        # Flag per identificare la traccia della batteria (canale 10 in MIDI)
        is_drum_track = False

        # Verifica se la traccia contiene note della batteria (canale 10, ovvero canale 9 in Python)
        for msg in track:
            if msg.type == 'program_change' and msg.channel == 9:  # Channel 10 (index 9) per la batteria
                is_drum_track = True
                break

        # Elabora i messaggi nella traccia
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                if is_drum_track:
                    # Se è una traccia della batteria, mantieni la durata originale
                    new_track.append(msg)
                else:
                    # Se è una traccia musicale, modifica la durata delle note in base alla lunghezza della sillaba
                    syllable_group = syllables[syllable_group_index]  # Ottieni il gruppo di sillabe per questa "parola"
                    syllable = syllable_group[syllable_index]  # Seleziona la sillaba corrente

                    syllable_length = len(syllable)  # La lunghezza della sillaba definisce la durata

                    # Calcola la durata della nota in ticks in base alla sillaba
                    note_length = syllable_length * note_duration

                    # Ricalcola la durata della nota in ticks, tenendo conto del BPM
                    note_length_in_ticks = note_length * ticks_per_beat / 480  # scala rispetto alla durata base (480)

                    # Assicurati che la durata delle note non sia troppo piccola o troppo grande
                    note_length_in_ticks = max(ticks_per_beat, note_length_in_ticks)  # Imposta un minimo per la durata

                    # Aggiungi il messaggio 'note_on' e 'note_off' con la durata modificata
                    if msg.type == 'note_on':
                        new_track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=msg.time))
                    elif msg.type == 'note_off':
                        # Regola il tempo della nota in base alla durata calcolata
                        new_track.append(Message('note_off', note=msg.note, time=int(note_length_in_ticks)))

                    # Passa alla prossima sillaba nel gruppo
                    syllable_index = (syllable_index + 1) % len(syllable_group)

                    # Se abbiamo finito le sillabe per il gruppo, passa al gruppo successivo
                    if syllable_index == 0:
                        syllable_group_index = (syllable_group_index + 1) % len(syllables)
            else:
                # Copia altri messaggi (ad esempio 'control_change', 'program_change', ecc.)
                new_track.append(msg)

    # Salva il MIDI modificato
    adjusted_midi.save(output_file)


def generate_vocal_audio(lyrics, output_path):
    tts = gTTS(text=lyrics, lang='it', slow=False)
    tts.save(output_path)



#sudo apt-get install timidity
def midi_to_wav_timidity(midi_file, wav_output_file):
    command = ["timidity", midi_file, "-Ow", "-o", wav_output_file]
    subprocess.run(command)
    print(f"Conversion completed: {wav_output_file}")


def unisci_wav(file1, file2, output_file):
    # Carica i file WAV
    audio_wav = AudioSegment.from_wav(file1)
    audio_mp3= AudioSegment.from_mp3(file2)

    if len(audio_wav) > len(audio_mp3):
        audio_mp3 = audio_mp3 + AudioSegment.silent(duration=len(audio_wav) - len(audio_mp3))  # Aggiungi silenzio
    elif len(audio_mp3) > len(audio_wav):
        audio_wav = audio_wav + AudioSegment.silent(duration=len(audio_mp3) - len(audio_wav))  # Aggiungi silenzio

        # Sovrapponi (overlay) i due file
    combined = audio_wav.overlay(audio_mp3)  # Sovrappone le due tracce

    # Esporta il risultato in un nuovo file (può essere WAV o MP3, a seconda delle tue esigenze)
    combined.export(output_file, format="mp3")

lyrics = "Amore è sorridere, ascoltarsi e aiutarsi, prendersi per mano, è importante dire ti voglio bene, ci rende forti, sempre insieme, sempre felici."
text_without_commas = lyrics.replace(",", "")

syllables = split_into_syllables(text_without_commas)
print(syllables)
midi_data = pretty_midi.PrettyMIDI('1.mid')

notes = midi_data.instruments[0].notes  # Prende la prima traccia strumentale

# Estrai i tempi di inizio e fine e le note
starts = [note.start for note in notes]
ends = [note.end for note in notes]
pitches = [note.pitch for note in notes]

# Crea la visualizzazione
plt.figure(figsize=(10, 6))
plt.scatter(starts, pitches, c='blue', label='Start')
plt.scatter(ends, pitches, c='red', label='End')
plt.xlabel('Tempo (s)')
plt.ylabel('Nota MIDI')
plt.title('Visualizzazione delle note MIDI')
plt.legend()
plt.show()
adjust_midi_for_syllables('1.mid', syllables, 'modified_midi.mid')
midi_data = pretty_midi.PrettyMIDI('modified_midi.mid')

notes = midi_data.instruments[0].notes  # Prende la prima traccia strumentale

# Estrai i tempi di inizio e fine e le note
starts = [note.start for note in notes]
ends = [note.end for note in notes]
pitches = [note.pitch for note in notes]

# Crea la visualizzazione
plt.figure(figsize=(10, 6))
plt.scatter(starts, pitches, c='blue', label='Start')
plt.scatter(ends, pitches, c='red', label='End')
plt.xlabel('Tempo (s)')
plt.ylabel('Nota MIDI')
plt.title('Visualizzazione delle note MIDI')
plt.legend()
plt.show()
generate_vocal_audio(lyrics, 'vocals.mp3')
midi_to_wav_timidity("modified_midi.mid", "instrumental.wav")

unisci_wav('instrumental.wav','vocals.mp3',  'output_file.mp3')
