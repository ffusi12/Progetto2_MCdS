import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.fftpack import dctn
from logic.dct import my_dct2, my_dct1d
from logic.compressor import compress, plot_images
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image


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
    compressed_img, h_new, w_new = compress(img_array, F, d)
    
    plot_images(img_array, compressed_img, h_new, w_new, F, d)


if __name__ == "__main__":
    main()