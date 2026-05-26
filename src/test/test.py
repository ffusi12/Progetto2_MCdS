import time
from matplotlib import pyplot as plt
import numpy as np
from scipy.fftpack import dctn
from logic.dct import my_dct1d, my_dct2


def run_benchmarks():
    test_block_dct2 = np.array([
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]
    ])

    print("Verifica Scaling DCT2...")
    risultato_mio = my_dct2(test_block_dct2)
    print("\n\t\t--- MATRICE DCT2 RISULTANTE (Attesa come da Tabella PDF) ---\n")    
    for riga in risultato_mio:
        stringa_riga = " ".join(f"{valore:10.2e}" for valore in riga)
        print(stringa_riga)

    # Test DCT1 monodimensionale
    test_block_dct1 = np.array([231, 32, 233, 161, 24, 71, 140, 245])

    print("\nVerifica Scaling DCT1...")
    risultato_mio_dct1 = my_dct1d(test_block_dct1)
    print("\n\t\t--- VETTORE DCT1 RISULTANTE (Attesa come da Tabella PDF) ---\n")
    stringa_riga = " ".join(f"{valore:10.2e}" for valore in risultato_mio_dct1)
    print(stringa_riga)


    # --- BENCHMARK TEMPI ---
    sizes = [8, 16, 32, 64, 128, 256]
    t_manuale = []
    t_fast = []

    for N in sizes:
        A = np.random.rand(N, N)
        
        # Tempo Manuale O(N^3)
        start = time.time()
        my_dct2(A)
        t_manuale.append(time.time() - start)
        
        # Tempo Libreria O(N^2 log N)
        start = time.time()
        dctn(A, type=2, norm='ortho')
        t_fast.append(time.time() - start)


    # --- GRAFICO SEMILOGARITMICO ---
    plt.figure()
    plt.semilogy(sizes, t_manuale, 'r-o', label='Manuale $N^3$')
    plt.semilogy(sizes, t_fast, 'b-s', label='Libreria $N^2 \log N$') 
    plt.title("Confronto Tempi DCT2 (Scala Semilog)")
    plt.xlabel("N (dimensione matrice)")
    plt.ylabel("Tempo (secondi)")
    plt.legend()
    plt.grid(True)
    plt.savefig("../docs/grafico_tempi.png")
    plt.show()


if __name__ == "__main__":
    run_benchmarks()