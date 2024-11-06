import torch
import numpy as np
import librosa
import scipy.io.wavfile as wav
from torchaudio.models.tacotron2 import Tacotron2
from waveglow.glow import WaveGlow
from tacotron2.text import text_to_sequence  # Tacotron text preprocessing

# Carica il modello Tacotron 2 pre-addestrato
tacotron2 = Tacotron2()
tacotron2.load_state_dict(torch.load('tacotron2_statedict.pt'))
tacotron2 = tacotron2.cuda().eval()

# Carica il vocoder WaveGlow pre-addestrato
waveglow = WaveGlow()
waveglow.load_state_dict(torch.load('waveglow_256channels_ljs_v2.pt'))
waveglow = waveglow.cuda().eval()

# Funzione per generare la voce cantata a partire da testo e melodia
def generate_singing_voice(text, melody_pitches):
    # Step 1: Preprocessa il testo
    sequence = np.array(text_to_sequence(text, ['english_cleaners']))[None, :]
    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

    # Step 2: Genera lo spettrogramma mel con Tacotron 2
    mel_outputs, mel_lengths, alignment = tacotron2(sequence)

    # Step 3: Usa WaveGlow per trasformare lo spettrogramma in audio
    with torch.no_grad():
        audio = waveglow.infer(mel_outputs)

    # Step 4: Normalizza e restituisce il risultato come array numpy
    audio = audio[0].data.cpu().numpy()
    audio = audio / np.max(np.abs(audio))

    return audio

# Testo e melodia
text = "Hello, this is a test of singing voice synthesis!"
melody_pitches = [60, 62, 64, 65, 67, 69, 71, 72]  # Una sequenza di note in MIDI

# Genera la voce cantata
audio_output = generate_singing_voice(text, melody_pitches)

# Salva l'output come file WAV
wav.write('output_sung_voice.wav', 22050, audio_output)
