import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# === Fungsi dasar Vigenère Cipher ===
def vigenere_encrypt(plain, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plain = plain.upper().replace(" ", "")
    key = key.upper()
    result = ""
    for i in range(len(plain)):
        p = alphabet.index(plain[i])
        k = alphabet.index(key[i % len(key)])
        c = alphabet[(p + k) % 26]
        result += c
    return result


def vigenere_decrypt(cipher, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = cipher.upper().replace(" ", "")
    key = key.upper()
    result = ""
    for i in range(len(cipher)):
        c = alphabet.index(cipher[i])
        k = alphabet.index(key[i % len(key)])
        p = alphabet[(c - k) % 26]
        result += p
    return result


# === Fungsi menyimpan hasil ke satu file ===
def save_to_single_file(mode, text, key, result):
    filename = "hasil_vigenere.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(f"Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Teks asli: {text}\n")
        f.write(f"Kunci: {key}\n")
        f.write(f"Hasil: {result}\n")
        f.write("=" * 50 + "\n\n")
    return filename


# === Fungsi tombol Enkripsi dan Dekripsi ===
def encrypt_text():
    plain = entry_message.get()
    key = entry_key.get()

    if not plain or not key:
        messagebox.showwarning("Peringatan", "Masukkan teks dan kunci terlebih dahulu!")
        return

    result = vigenere_encrypt(plain, key)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

    filename = save_to_single_file("ENKRIPSI", plain, key, result)
    messagebox.showinfo("Berhasil", f"Hasil enkripsi disimpan di file:\n{filename}")


def decrypt_text():
    cipher = entry_message.get()
    key = entry_key.get()

    if not cipher or not key:
        messagebox.showwarning("Peringatan", "Masukkan ciphertext dan kunci terlebih dahulu!")
        return

    result = vigenere_decrypt(cipher, key)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

    filename = save_to_single_file("DEKRIPSI", cipher, key, result)
    messagebox.showinfo("Berhasil", f"Hasil dekripsi disimpan di file:\n{filename}")


# === GUI ===
root = tk.Tk()
root.title("Vigenère Cipher GUI")
root.geometry("500x400")
root.resizable(False, False)

tk.Label(root, text="🔐 Vigenère Cipher", font=("Arial", 16, "bold")).pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Teks (Plain/Cipher):", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
entry_message = tk.Entry(frame_input, width=40, font=("Arial", 11))
entry_message.grid(row=0, column=1)

tk.Label(frame_input, text="Kunci:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
entry_key = tk.Entry(frame_input, width=40, font=("Arial", 11))
entry_key.grid(row=1, column=1)

frame_button = tk.Frame(root)
frame_button.pack(pady=10)

btn_encrypt = tk.Button(frame_button, text="🔒 Enkripsi", width=15, bg="#4CAF50", fg="white", command=encrypt_text)
btn_encrypt.grid(row=0, column=0, padx=10)

btn_decrypt = tk.Button(frame_button, text="🔓 Dekripsi", width=15, bg="#2196F3", fg="white", command=decrypt_text)
btn_decrypt.grid(row=0, column=1, padx=10)

tk.Label(root, text="Hasil:", font=("Arial", 11)).pack(pady=5)
output_text = tk.Text(root, height=6, width=55, font=("Consolas", 11))
output_text.pack()

root.mainloop()
