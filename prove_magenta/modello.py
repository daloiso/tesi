import magenta
from magenta.models import melody_rnn
from magenta.music import midi_io, note_seq

# Inizializza il modello
bundle = melody_rnn.prepare_bundle('path/to/melody_rnn.mag')  # Specifica il percorso al tuo modello
melody_rnn_model = melody_rnn.MelodyRnnModel(bundle)

# Configura i parametri per la generazione
num_steps = 128  # Numero di note da generare
temperature = 1.0  # Controlla la varietà della generazione

# Genera la sequenza musicale
melody_sequence = melody_rnn_model.generate(num_steps, temperature)

# Salva la sequenza in un file MIDI
midi_io.note_sequence_to_midi_file(melody_sequence, 'melody.mid')
