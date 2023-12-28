import tkinter as tk
import pyqrcode
from PIL import Image, ImageTk

def generate_qr_code():
    # Ottieni l'URL dall'input dell'utente
    url = url_entry.get()
    
    # Crea un oggetto QRCode
    qr = pyqrcode.create(url)
    
    # Salva il QR code in un file immagine
    qr.png("qrcode.png", scale=6)
    
    # Carica il QR code nell'interfaccia
    qr_image = Image.open("qrcode.png")
    qr_image = ImageTk.PhotoImage(qr_image)
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

# Creazione della finestra principale
window = tk.Tk()
window.title("Generatore QR Code")

# Etichetta per l'URL
url_label = tk.Label(window, text="Incolla l'URL:")
url_label.pack()

# Campo di inserimento per l'URL
url_entry = tk.Entry(window)
url_entry.pack()

# Bottone per generare il QR code
generate_button = tk.Button(window, text="Genera QR Code", command=generate_qr_code)
generate_button.pack()

# Etichetta per il QR code generato
qr_label = tk.Label(window)
qr_label.pack()

# Esegui l'applicazione
window.mainloop()
