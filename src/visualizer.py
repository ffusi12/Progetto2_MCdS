import numpy as np
import matplotlib.pyplot as plt

def visualize_dct_coefficients(c_vect):
    N = len(c_vect)
    plt.figure()
    plt.bar(range(1, N + 1), c_vect, color='blue', edgecolor='black')
    plt.title("Coefficienti DCT (Energy Compaction)")
    plt.xlabel("Indice del coefficiente")
    plt.ylabel("Ampiezza")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show() 
    