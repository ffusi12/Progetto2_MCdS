import numpy as np

def compute_D(N):
    alpha_vect = np.zeros(N)
    alpha_vect[0] = N**(-0.5)              
    alpha_vect[1:] = (N**(-0.5)) * np.sqrt(2) 
    
    k = np.arange(N).reshape(N, 1) 
    i = np.arange(N).reshape(1, N) 
    
    D = alpha_vect.reshape(N, 1) * np.cos(k * np.pi * (2 * i + 1) / (2 * N))
    
    return D 

def my_dct1d(f_vect):
    
    N = len(f_vect)
    D = compute_D(N)
    c_vect = D @ f_vect

    return c_vect

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
