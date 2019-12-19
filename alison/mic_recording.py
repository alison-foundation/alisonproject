import pyaudio
import wave
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

import alison.spectrum as spectrum
from alison.nmf import *

audio = pyaudio.PyAudio()

def record (length):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = length
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