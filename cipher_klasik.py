import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# ========================== ALGORITMA CIPHER ==========================

# Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for c in text.upper():
        if c.isalpha():
            result += chr((ord(c) - 65 + shift) % 26 + 65)
        else:
            result += c
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Vigenere Cipher
def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for c in text.upper():
        if c.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(c) - 65 + shift) % 26 + 65)
            key_index += 1
        else:
            result += c
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for c in text.upper():
        if c.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(c) - 65 - shift) % 26 + 65)
            key_index += 1
        else:
            result += c
    return result

# Affine Cipher
def affine_encrypt(text, a, b):
    result = ""
    for c in text.upper():
        if c.isalpha():
            result += chr(((a * (ord(c) - 65) + b) % 26) + 65)
        else:
            result += c
    return result

def affine_decrypt(text, a, b):
    result = ""
    a_inv = pow(a, -1, 26)
    for c in text.upper():
        if c.isalpha():
            result += chr(((a_inv * ((ord(c) - 65) - b)) % 26) + 65)
        else:
            result += c
    return result

# Playfair Cipher
def generate_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I")))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = ""
    for c in key + alphabet:
        if c not in matrix:
            matrix += c
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            pairs.append(a + "X")
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    result = ""
    pos = {matrix[i][j]: (i, j) for i in range(5) for j in range(5)}
    for pair in pairs:
        a, b = pair
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            result += matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5]
        elif ca == cb:
            result += matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb]
        else:
            result += matrix[ra][cb] + matrix[rb][ca]
    return result

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pos = {matrix[i][j]: (i, j) for i in range(5) for j in range(5)}
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ra, ca = pos[a]
        rb, cb = pos[b]
        if ra == rb:
            result += matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5]
        elif ca == cb:
            result += matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb]
        else:
            result += matrix[ra][cb] + matrix[rb][ca]
    return result

# Hill Cipher
def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(key_matrix, pair) % 26
        result += ''.join([chr(int(num) + 65) for num in res])
    return result

def hill_decrypt(text, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)
    key_inv = (det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)) % 26
    text = text.upper().replace(" ", "")
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(key_inv, pair) % 26
        result += ''.join([chr(int(num) + 65) for num in res])
    return result


# ========================== GUI IMPLEMENTASI ==========================

def proses_cipher():
    algo = combo_algo.get()
    text = entry_text.get().strip()
    key = entry_key.get().strip()
    mode = combo_mode.get()
    result = ""

    try:
        if algo == "Caesar Cipher":
            shift = int(key)
            result = caesar_encrypt(text, shift) if mode == "Enkripsi" else caesar_decrypt(text, shift)

        elif algo == "Vigenere Cipher":
            result = vigenere_encrypt(text, key) if mode == "Enkripsi" else vigenere_decrypt(text, key)

        elif algo == "Affine Cipher":
            a, b = map(int, key.split(","))
            result = affine_encrypt(text, a, b) if mode == "Enkripsi" else affine_decrypt(text, a, b)

        elif algo == "Playfair Cipher":
            result = playfair_encrypt(text, key) if mode == "Enkripsi" else playfair_decrypt(text, key)

        elif algo == "Hill Cipher":
            values = list(map(int, key.split(",")))
            key_matrix = np.array(values).reshape(2, 2)
            result = hill_encrypt(text, key_matrix) if mode == "Enkripsi" else hill_decrypt(text, key_matrix)

        # Tampilkan hasil di GUI
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result)

        # Simpan otomatis ke file txt
        with open("hasil_cipher.txt", "a", encoding="utf-8") as f:
            f.write(f"Algoritma: {algo}\nMode: {mode}\nTeks: {text}\nKunci: {key}\nHasil: {result}\n{'-'*50}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")


root = tk.Tk()
root.title("Program Cipher Klasik - 5 Algoritma")
root.geometry("500x500")

tk.Label(root, text="Pilih Algoritma:").pack()
combo_algo = ttk.Combobox(root, values=[
    "Caesar Cipher", "Vigenere Cipher", "Affine Cipher", "Playfair Cipher", "Hill Cipher"
])
combo_algo.current(0)
combo_algo.pack()

tk.Label(root, text="Mode:").pack()
combo_mode = ttk.Combobox(root, values=["Enkripsi", "Dekripsi"])
combo_mode.current(0)
combo_mode.pack()

tk.Label(root, text="Teks:").pack()
entry_text = tk.Entry(root, width=50)
entry_text.pack()

tk.Label(root, text="Kunci: (contoh: 3 / ABC / 5,8 / HILL / 3,2,7,9)").pack()
entry_key = tk.Entry(root, width=50)
entry_key.pack()

tk.Button(root, text="Proses", command=proses_cipher, bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Hasil:").pack()
text_output = tk.Text(root, height=8, width=50)
text_output.pack()

root.mainloop()
