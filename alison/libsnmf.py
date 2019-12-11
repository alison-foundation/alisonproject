import numpy as np
import argparse
import matplotlib.pyplot as plt
from libnmf.gnmf import GNMF
from libnmf.pnmf import PNMF
from libnmf.fpdnmf import FPDNMF
import nimfa
import librosa.decompose as dcp

def get_dcpnmf(stft, n):
    return dcp.decompose(stft, n_components=n)


def get_pnmf(stft, n):
    pnmf= PNMF(stft, rank=n)
    pnmf.compute_factors(max_iter=30)
    return (pnmf.W, pnmf.H)

def get_gnmf(stft, n):
    gnmf= GNMF(stft, rank=n)
    gnmf.compute_factors(max_iter=30)
    return (gnmf.W, gnmf.H)

def get_fpdnmf(stft, n):
    fpdnmf= FPDNMF(stft, rank=n)
    fpdnmf.compute_factors(max_iter=30)
    return (fpdnmf.W, fpdnmf.H)

def get_nimfa(stft, n):
    lsnmf = nimfa.Lsnmf(stft, seed='random_vcol', rank=n, max_iter=30)
    return (lsnmf.V, lsnmf.H)