import numpy as np
from scipy.fftpack import dctn, idctn
import numpy as np
from visualizer import visualize_dct_coefficients 

def compute_D(N):
    """
    Costruisce la matrice di trasformazione DCT-II di dimensione N x N
    Seguendo la logica matematica della funzione compute_D di MATLAB
    """
    # 1. Inizializzazione del vettore alpha (i coefficienti di normalizzazione)
    alpha_vect = np.zeros(N)
    alpha_vect[0] = N**(-0.5)               # Corrisponde a alpha_vect(1) in MATLAB
    alpha_vect[1:] = (N**(-0.5)) * np.sqrt(2) # Corrisponde a alpha_vect(2:end) in MATLAB
    
    # 2. Costruzione della matrice D usando il broadcasting di NumPy (sostituisce i due cicli for)
    # Creiamo una griglia di indici k (righe) e i (colonne) da 0 a N-1
    k = np.arange(N).reshape(N, 1) # Vettore colonna delle frequenze (0, 1, ..., N-1)
    i = np.arange(N).reshape(1, N) # Vettore riga degli spazi/pixel (0, 1, ..., N-1)
    
    # Formula della DCT-II identica a quella MATLAB
    # Nota: in Python usiamo k e i direttamente (0-indexed), che equivalgono a (k-1) e (i-1) di MATLAB (1-indexed)
    D = alpha_vect.reshape(N, 1) * np.cos(k * np.pi * (2 * i + 1) / (2 * N))
    
    return D

def my_dct1d(f_vect):
    """
    Funzione principale che calcola la DCT e mostra il grafico
    Speculare alla funzione dct_1D di MATLAB
    """
    N = len(f_vect)
    
    # Genera la matrice di trasformazione D
    D = compute_D(N)
    
    # Calcola il vettore dei coefficienti tramite prodotto matrice-vettore
    # In Python, l'operatore @ esegue il prodotto matriciale (pari al * di MATLAB)
    c_vect = D @ f_vect
    return c_vect



""" def my_dct1d(x):
    Implementazione DCT-II monodimensionale (scelta comune per compressione
    N = len(x)
    c = np.zeros(N)
    for k in range(N):
        s = 0
        for n in range(N):
            # Formula standard della DCT-II
            s += x[n] * np.cos(np.pi * (k-1) * (2 * n - 1) / (2 * N))
        
        # Scaling: attenzione a far corrispondere i dati di test del docente
        alpha = np.sqrt(1/N) if k == 0 else np.sqrt(2/N)
        c[k] = s * alpha
    return c """

def my_dct2(block):
    """Implementazione DCT2 tramite separabilità"""
    N = block.shape[0]
    res = np.zeros((N, N))
    # Passaggio 1: DCT sulle righe
    for i in range(N):
        res[i, :] = my_dct1d(block[i, :])
    # Passaggio 2: DCT sulle colonne del risultato
    for j in range(N):
        res[:, j] = my_dct1d(res[:, j])
    return res

def compress_block(block, d):
    """Applica DCT2, taglia le frequenze e applica IDCT2 [cite: 18, 19, 20]"""
    F = block.shape[0]
    # Trasformata veloce della libreria [cite: 6]
    c = dctn(block, type=2, norm='ortho')
    
    # Eliminazione frequenze k+l > d [cite: 20, 21]
    for k in range(F):
        for l in range(F):
            if k + l > d:
                c[k, l] = 0
    
    # Antitrasformata [cite: 45]
    ff = idctn(c, type=2, norm='ortho')
    
    # Normalizzazione: arrotondamento e clipping [cite: 45]
    ff = np.round(ff)
    ff = np.clip(ff, 0, 255)
    return ff.astype(np.uint8)