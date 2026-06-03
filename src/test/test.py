import time
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy.fftpack import dctn
from decimal import Decimal, ROUND_HALF_DOWN
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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

    # --- BENCHMARK TEMPI (CON MEDIA SU 100 ESECUZIONI) ---
    sizes = [128, 256, 512]
    num_runs = 100
    t_manuale = []
    t_fast = []

    print("\n--- AVVIO BENCHMARK TEMPI (Media su 100 esecuzioni) ---")
    
    for N in sizes:
        print(f"Calcolo in corso per N = {N:3d}...", end="", flush=True)
        
        run_times_manuale = []
        run_times_fast = []
        A = np.random.rand(N, N)

        for _ in range(num_runs):            
            # Tempo Manuale O(N^3) usando perf_counter()
            start = time.perf_counter()
            my_dct2(A)
            run_times_manuale.append(time.perf_counter() - start)
            
            # Tempo Libreria O(N^2 log N)
            start = time.perf_counter()
            dctn(A, type=2, norm='ortho')
            run_times_fast.append(time.perf_counter() - start)
            
        # Calcolo della media
        t_manuale.append(np.mean(run_times_manuale))
        t_fast.append(np.mean(run_times_fast))
        print(" Completato.")

    #  CALCOLO DEI RAPPORTI 
    rapporti_manuale = ["-"]  
    rapporti_fast = ["-"]

    for i in range(1, len(sizes)):
        ratio_manuale = t_manuale[i] / t_manuale[i-1]
        rapporti_manuale.append(f"{ratio_manuale:.2f}")
        
        ratio_fast = t_fast[i] / t_fast[i-1]
        rapporti_fast.append(f"{ratio_fast:.2f}")

    # STAMPA TABELLA COMPLETA IN CONSOLE 
    print("\n" + "="*95)
    print("--- TEMPI MEDI DI ESECUZIONE E VERIFICA SCALING ---")
    print("="*95)
    # Intestazione colonne ben spaziata
    print(f"{'N':>5} | {'Manuale (N³)':>15} | {'Rapp. Manuale':>14} | {'Libreria (N²logN)':>18} | {'Rapp. Libreria':>15}")
    print("-" * 95)
    
    # Ciclo di stampa dei dati riga per riga
    for i, N in enumerate(sizes):
        print(f"{N:>5} | {t_manuale[i]:>15.6e} | {rapporti_manuale[i]:>14} | {t_fast[i]:>18.6e} | {rapporti_fast[i]:>15}")
    print("="*95 + "\n")

    # --- GRAFICO ---
    plt.figure()
    plt.semilogy(sizes, t_manuale, 'r-o', label='Manuale $N^3$')
    plt.semilogy(sizes, t_fast, 'b-s', label='Libreria $N^2 \\log N$') 
    
    # Aggiunge i valori dei rapporti sul grafico sopra i punti del manuale
    for i in range(1, len(sizes)):
        plt.text(sizes[i], t_manuale[i] * 1.5, f"ratio: {rapporti_manuale[i]}", 
                 color='red', fontsize=9, fontweight='bold', ha='center')

    plt.title("Confronto Tempi Medi DCT2 e Verifica Costante Scaling (~8)")
    plt.xlabel("N (dimensione matrice)")
    plt.ylabel("Tempo Medio (secondi)")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    
    # Crea la cartella se non esiste, evitando errori di salvataggio
    os.makedirs("../../relazione/immagini", exist_ok=True)
    plt.savefig("../../relazione/immagini/grafico_tempi.png")
    plt.show()


if __name__ == "__main__":
    run_benchmarks()