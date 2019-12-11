import scipy.io.wavfile as wav
import numpy as np
import argparse
import matplotlib.pyplot as plt
import spectrum
import logging
import libsnmf

nb = 3

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser()
parser.add_argument(
        "--file",
        help="Recognize sound from an audio file instead of the ReSpeaker",
        type=str)
parser.add_argument(
        "--dict", help="Use a precomputed dictionary.", type=str)
args = parser.parse_args()

if args.file == None:
    logging.info("Please input a file")
else:
    print(args.file)

stft = np.zeros([513, 0])

rate, signal = wav.read(args.file)
stft = np.concatenate((stft, spectrum.get_stft(signal / 1.0)),
                            axis=1)
print(stft.shape)
dico, activ = libsnmf.get_pnmf(stft, nb)

print("dict: ") 
print(dico.shape)
print("activ: ")  
print(activ.shape)
plt.clf()

for i in range(0, nb):
    plt.subplot(nb, 2, 2*(i+1) - 1)
    plt.title("Dict " + str(i+1))
    plt.stem(dico[:, i])

    plt.subplot(nb, 2, 2*(i+1))
    plt.title("Activ " + str(i+1))
    plt.stem(activ[i, :])

plt.show()