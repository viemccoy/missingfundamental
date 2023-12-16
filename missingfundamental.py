import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play

# Constants
SAMPLE_RATE = 44100  # Sample rate in Hz
DURATION = 5  # Duration in seconds

def generate_tone(frequency, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(frequency * t * 2 * np.pi)
    return tone

def remove_fundamental(tone, fundamental_freq, sample_rate):
    fft = np.fft.rfft(tone)
    fft[int(fundamental_freq * len(tone) / sample_rate)] = 0
    return np.fft.irfft(fft)

def play_and_plot_tone(tone, sample_rate):
    write('temp.wav', sample_rate, (tone * 32767).astype(np.int16))
    sound = AudioSegment.from_file('temp.wav', format="wav")
    play(sound)

    plt.figure(figsize=(10, 4))
    plt.plot(tone[:sample_rate])
    plt.show()

st.title('Missing Fundamental Visualizer')

fundamental_freq = st.slider('Set the pitch of the fundamental (Hz)', 20, 20000)

tone = generate_tone(fundamental_freq, SAMPLE_RATE, DURATION)

if st.button('Play and Show Waveform'):
    play_and_plot_tone(tone, SAMPLE_RATE)

if st.button('Remove Fundamental and Play'):
    tone_without_fundamental = remove_fundamental(tone, fundamental_freq, SAMPLE_RATE)
    play_and_plot_tone(tone_without_fundamental, SAMPLE_RATE)