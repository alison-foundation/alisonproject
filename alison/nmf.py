from sklearn.decomposition import SparseCoder, NMF
import librosa.decompose as dcp
from libnmf.pnmf import PNMF

def get_nmf(stft, n_components):
    return dcp.decompose(stft, n_components=n_components)

def get_pnmf(stft, n):
    pnmf= PNMF(stft, rank=n)
    pnmf.compute_factors(max_iter=30)
    return (pnmf.W, pnmf.H)
    
def get_activations(stft, dico, n_nonzero_coefs=None):
    coder = SparseCoder(
        dictionary=dico.T,
        transform_n_nonzero_coefs=n_nonzero_coefs,
        transform_algorithm="lasso_cd",
        positive_code=True)
    return coder.transform(stft.T).T
