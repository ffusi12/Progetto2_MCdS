import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from scipy.fftpack import dctn, idctn


def compress(img_array, F, d): 
    h, w = img_array.shape
    
    # Calcolo dimensioni con divisione intera (floor)
    h_new, w_new = (h // F) * F, (w // F) * F
    compressed_img = np.zeros((h_new, w_new), dtype=np.uint8)

    # Elaborazione a blocchi
    for i in range(0, h_new, F):
        for j in range(0, w_new, F):
            block = img_array[i:i+F, j:j+F]
            compressed_img[i:i+F, j:j+F] = compress_block(block, d)

    return compressed_img, h_new, w_new


def compress_block(block, d):
    F = block.shape[0]
    # Fft di scipy
    fft_coefficient = dctn(block, type=2, norm='ortho')
    
    # Eliminazione frequenze k+l > d
    for k in range(F):
        for l in range(F):
            if k + l > d:
                fft_coefficient[k, l] = 0
    
    # Dct inversa
    ff = idctn(fft_coefficient, type=2, norm='ortho')
    
    # Normalizzazione, arrotondamento e clipping
    ff = np.round(ff)
    ff = np.clip(ff, 0, 255)
    return ff.astype(np.uint8)
