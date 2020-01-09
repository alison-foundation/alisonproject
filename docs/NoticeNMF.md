# Non-Negative Matrix Factorization
## Process

In order to recognize a known sound from the audio input we use the Non-Negative Matrix Factorization (NMF) algorithm. This algorithm decomposes the matrix given by the Short-Term Fourier Transform (STFT) in two matrices: the dictionary and the activation matrix.

During the learning phase we make a reference dictionary nd activation matrix for each sound we want to recognize. We create those matrices by computing NMF on the STFT of the concatenation of multiple samples of one sound. In order to do this we implement a specific version of NMF : Probabilistic NMF, that give us cleaner dictionaries (see more about PNMF : https://pdfs.semanticscholar.org/18c2/302cbf1fe01a8338a186999b69abc5701c2e.pdf).

After , when there is an audio input, we run an algorithm based on the previously computed dictionary and activation matrices. For each sound we want to test, the algorithm works in two times : 

First we compute NMF with the input data by setting the dictionary equal to the reference dictionary. Then , if the activation matrix contains coefficients above a certain threshold during a certain amount of time, we consider that the sound associated to this dictionary may be present.

Secondly, we check that the activation line (the line of the activation matrix where the coefficients validate the first test) have the same pattern as one of the reference activation lines (from the corresponding activation matrix). We do so by calculating the possible shift between the line to test and the reference one. And then calculate the Pearson correlation between those two lines. If the correlation is superior to an arbitrary threshold then we consider that the sound associated to this reference dictionary (and activation matrix) is present.

Then a signal is sent to the Philips Hue to light it up in the pre-defined color.

## Diagram of the NMF method in the system process

![System Diagram](https://i.ibb.co/8NXwR6P/system.png)

## Properties

At the moment our algorithms manage to recognize superposed sounds and work in a noisy environment. We can also recognize cut-up sounds (when there is only a part of the sound we want to recognize).

 Each time a sound is picked up by the microphone, our recognition algorithm try for each reference couple dictionary-activation matrix (each couple represent a different sound) to find a match. Those tests are not exclusive, meaning that we can find matches for different sounds on the same sound record. This is how we are able to recognize superposed sounds.

To reduce our previous problem with false positives (when we recognized some sounds too often) we added the condition on the likeliness between the activation line to test and the reference one.