import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct


def DCT2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def IDCT2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


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


def filter_blocks_dct(blocks, d):

    filtered_blocks = []

    for f in blocks:

        c = DCT2(f)

        F = c.shape[0]

        # Delete frequencies
        for k in range(F):
            for l in range(F):

                if k + l >= d:
                    c[k, l] = 0

        filtered_blocks.append(c)

    return filtered_blocks


def reconstruct_image(blocks, img_shape, F):

    h, w = img_shape

    # Dimensioni multiple di F
    h_new = (h // F) * F
    w_new = (w // F) * F

    reconstructed = np.zeros((h_new, w_new), dtype=np.uint8)

    idx = 0

    for y in range(0, h_new, F):
        for x in range(0, w_new, F):

            reconstructed[y:y+F, x:x+F] = blocks[idx]

            idx += 1

    return reconstructed


# ----------- MAIN -----------

root = tk.Tk()
root.withdraw()

filename = simpledialog.askstring(
    "Input",
    "Insert the file name:"
)

if not filename:
    messagebox.showinfo("Info", "Any name inserted")
    exit()

filepath = f"data/{filename}"

try:
    img = Image.open(filepath).convert('L')

except FileNotFoundError:
    messagebox.showerror(
        "Error",
        f"File not found:\n{filepath}"
    )
    exit()

img_array = np.array(img)

F = simpledialog.askinteger(
    "Input",
    "Insert blocks F dimension:",
    minvalue=1
)

d = simpledialog.askinteger(
    "Input",
    f"Insert d (0 <= d <= {2*F - 2}):",
    minvalue=0,
    maxvalue=2*F - 2
)

blocks = block_division(img_array, F)

filtered_blocks = filter_blocks_dct(blocks, d)

reconstructed_img = reconstruct_image(
    filtered_blocks,
    img_array.shape,
    F
)

img_out = Image.fromarray(reconstructed_img)

img_out.show()

img_out.save(filename.split(".")[0] + "compressed" + ".bmp")