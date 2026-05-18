import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.fftpack import dctn
from dct_logic import my_dct2, compress_block, dctn, idctn, my_dct1d
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image


def run_benchmarks():
    # --- TEST DI VALIDAZIONE (Dati dal PDF) ---
    # Inserisci qui la matrice 8x8 fornita nel testo del progetto
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

    # Test DCT1 monodimensionale (dati dal PDF)
    test_block_dct1 = np.array([231, 32, 233, 161, 24, 71, 140, 245])

    print("\nVerifica Scaling DCT1...")
    risultato_mio_dct1 = my_dct1d(test_block_dct1)
    print("\n\t\t--- VETTORE DCT1 RISULTANTE (Attesa come da Tabella PDF) ---\n")
    stringa_riga = " ".join(f"{valore:10.2e}" for valore in risultato_mio_dct1)
    print(stringa_riga)

    # --- BENCHMARK TEMPI ---
    sizes = [8, 16, 32, 64, 128, 256] # N crescenti
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
    plt.savefig("../docs/grafico_tempi.png") # Salva per la relazione
    plt.show()

""" if __name__ == "__main__":
    run_benchmarks() """

def main():
    # Setup interfaccia file 
    root = tk.Tk()
    root.withdraw()
    
    # Scelta immagine
    file_path = filedialog.askopenfilename(title="Seleziona immagine BMP", filetypes=[("BMP files", "*.bmp")])
    if not file_path: return

    # Scelta parametri F e d [cite: 14, 15, 16]
    F = simpledialog.askinteger("Input", "Inserisci ampiezza finestra (F):", initialvalue=8)
    d = simpledialog.askinteger("Input", f"Inserisci soglia taglio d (0-{2*F-2}):", initialvalue=5)

    # Caricamento e conversione
    img = Image.open(file_path).convert('L')
    img_array = np.array(img)
    h, w = img_array.shape
    
    # Calcolo dimensioni (scartando avanzi) [cite: 17]
    h_new, w_new = (h // F) * F, (w // F) * F
    compressed_img = np.zeros((h_new, w_new), dtype=np.uint8)

    # Elaborazione a blocchi [cite: 17, 18]
    for i in range(0, h_new, F):
        for j in range(0, w_new, F):
            block = img_array[i:i+F, j:j+F]
            compressed_img[i:i+F, j:j+F] = compress_block(block, d)

    # Visualizzazione affiancata 
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img_array[:h_new, :w_new], cmap='gray')
    plt.title("Originale (ritagliata)")
    plt.subplot(1, 2, 2)
    plt.imshow(compressed_img, cmap='gray')
    plt.title(f"Compressione (F={F}, d={d})")
    plt.show()

    run_benchmarks()



if __name__ == "__main__":
    main()