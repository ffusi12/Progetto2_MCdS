import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

from PIL import Image
import numpy as np


def block_division(img_array, F):

    h, w = img_array.shape

    # F multiple dimensions
    h_new = (h // F) * F
    w_new = (w // F) * F

    # Cut off any leftovers
    img_crop = img_array[:h_new, :w_new]

    blocks = []

    # Blocks Extraction 
    for y in range(0, h_new, F):
        for x in range(0, w_new, F):

            block = img_crop[y:y+F, x:x+F]

            blocks.append(block)

    return  blocks


# -----------------------------
# Main provvisorio

root = tk.Tk()
root.withdraw()

filepath = filedialog.askopenfilename(
    title="Seleziona immagine BMP",
    filetypes=[("Bitmap", "*.bmp")]
)

if not filepath:
    messagebox.showinfo("Info", "Nessun file selezionato")
    exit()

img = Image.open(filepath).convert('L')

img_array = np.array(img)

F = simpledialog.askinteger(
    "Input",
    "Inserisci dimensione   blocks F:",
    minvalue=1
)

d = simpledialog.askinteger(
    "Input",
    f"Inserisci d (0 <= d <= {2*F - 2}):",
    minvalue=0,
    maxvalue=2*F - 2
)

blocks = block_division(img_array, F)