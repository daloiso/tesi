import numpy as np
import librosa
import matplotlib.pyplot as plt

# Load the carrier (synthesized sound) and modulator (voice) signals
carrier, sr = librosa.load('carrier.wav', sr=None)
modulator, sr = librosa.load('modulator.wav', sr=None)

# Ensure both signals are the same length
min_len = min(len(carrier), len(modulator))
carrier = carrier[:min_len]
modulator = modulator[:min_len]

# Frame the signals
def frame_signal(signal, frame_size, hop_size):
    num_frames = 1 + (len(signal) - frame_size) // hop_size
    frames = np.lib.stride_tricks.as_strided(
        signal, shape=(num_frames, frame_size),
        strides=(signal.strides[0] * hop_size, signal.strides[0])
    )
    return frames

frame_size = 1024
hop_size = 512

carrier_frames = frame_signal(carrier, frame_size, hop_size)
modulator_frames = frame_signal(modulator, frame_size, hop_size)
#Apply the Short-Time Fourier Transform
def stft(frames, n_fft):
    return np.fft.rfft(frames, n=n_fft)

n_fft = 1024

carrier_stft = stft(carrier_frames, n_fft)
modulator_stft = stft(modulator_frames, n_fft)
#Compute the Amplitude Envelopes
modulator_amplitude = np.abs(modulator_stft)
#Modulate the Carrier Signal
epsilon = 1e-10  # Small constant
modulated_stft = carrier_stft * (modulator_amplitude / (np.abs(carrier_stft) + epsilon))

#Inverse STFT and Reconstruct the Signal

def istft(stft_matrix, hop_size):
    num_frames, n_fft = stft_matrix.shape
    frame_size = (n_fft - 1) * 2
    signal = np.zeros(num_frames * hop_size + frame_size - hop_size)
    for n, i in enumerate(range(0, len(signal) - frame_size, hop_size)):
        signal[i:i + frame_size] += np.fft.irfft(stft_matrix[n])
    return signal

output_signal = istft(modulated_stft, hop_size)
#Normalize and Save the Output
output_signal = output_signal / np.max(np.abs(output_signal))
if len(output_signal) < len(carrier):
    output_signal = np.pad(output_signal, (0, len(carrier) - len(output_signal)), 'constant')
else:
    carrier = np.pad(carrier, (0, len(output_signal) - len(carrier)), 'constant')

overlayed_audio = output_signal + carrier
librosa.output.write_wav('vocoder_output.wav', overlayed_audio, sr)
