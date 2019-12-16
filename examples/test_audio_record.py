import pyaudio
import wave
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

import alison.spectrum as spectrum
from alison.nmf import *

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio_Record.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

def record ():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    return frames

files = [
    "../samples/Sonnette/sonnette", "../samples/Fire_Alarm/fire_alarm",
    "../samples/Phone_Ring/phone"
]

dico = np.zeros([513, 0])
print(dico.shape)

for file in files:
    stft = np.zeros([513, 0])

    for i in range(1, 4):
        rate, signal = wav.read(file + str(i) + ".wav")
        stft = np.concatenate((stft, spectrum.get_stft(signal / 1.0)),
                              axis=1)

    dico_plus, _ = get_nmf(stft, 3)
    dico = np.concatenate((dico, dico_plus), axis=1)

for file in files:
    rate2, signal2 = wav.read("audio_Record.wav")
    stft2 = spectrum.get_stft(signal2 * 1.0)
    activations = get_activations(stft2, dico, 3)

    plt.clf()

    for i in range(0, 9):
        plt.subplot(3, 3, i + 1)
        plt.title("Ligne " + str(i))
        plt.stem(activations[i, :])

    plt.suptitle(file)
    plt.show()