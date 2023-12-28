import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def copia_o_sposta_file(cartella_sorgente, cartella_destinazione, tipi_file, azione):
    estensioni_file = {
        'audio': ['.mp3', '.wav', '.wave', '.aiff'],
        'video': ['.mp4', '.mkv', '.avi'],
        'documenti': ['.txt', '.doc', '.xls', '.xlsx', '.pdf'],
        'immagini': ['.jpeg', '.jpg']
    }

    estensioni_selezionate = []
    for tipo_file, var in zip(tipi_file, variabili_tipi_file):
        if var.get():
            estensioni_selezionate.extend(estensioni_file.get(tipo_file, []))

    for radice, cartelle, files in os.walk(cartella_sorgente):
        for file in files:
            estensione_file = os.path.splitext(file)[1].lower()
            if estensione_file in estensioni_selezionate:
                percorso_file_sorgente = os.path.join(radice, file)
                if azione == 'copia':
                    shutil.copy(percorso_file_sorgente, cartella_destinazione)
                elif azione == 'sposta':
                    shutil.move(percorso_file_sorgente, cartella_destinazione)

def seleziona_cartella(entry_widget):
    cartella = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, cartella)

def esegui_azione():
    cartella_sorgente = cartella_sorgente_entry.get()
    cartella_destinazione = cartella_destinazione_entry.get()
    tipi_file = ['audio', 'video', 'documenti', 'immagini']
    azione = azione_var.get()

    if cartella_sorgente and cartella_destinazione:
        copia_o_sposta_file(cartella_sorgente, cartella_destinazione, tipi_file, azione)
        risultato_label.config(text=f"File {azione}ti con successo.")
    else:
        risultato_label.config(text="Seleziona entrambe le cartelle prima di procedere.")

# GUI
app = tk.Tk()
app.title("Gestore File")

stile = ttk.Style()
stile.configure('TButton', padding=5, font=('Helvetica', 12))

padding_frame = {'padx': 10, 'pady': 5}

# Cartella Sorgente
frame_cartella_sorgente = ttk.Frame(app)
frame_cartella_sorgente.pack(**padding_frame)

etichetta_cartella_sorgente = ttk.Label(frame_cartella_sorgente, text="Cartella Sorgente:")
etichetta_cartella_sorgente.grid(row=0, column=0, sticky='w')

cartella_sorgente_entry = ttk.Entry(frame_cartella_sorgente, width=40)
cartella_sorgente_entry.grid(row=0, column=1, sticky='w')

bottone_cartella_sorgente = ttk.Button(frame_cartella_sorgente, text="Sfoglia", command=lambda: seleziona_cartella(cartella_sorgente_entry))
bottone_cartella_sorgente.grid(row=0, column=2, **padding_frame)

# Cartella Destinazione
frame_cartella_destinazione = ttk.Frame(app)
frame_cartella_destinazione.pack(**padding_frame)

etichetta_cartella_destinazione = ttk.Label(frame_cartella_destinazione, text="Cartella Destinazione:")
etichetta_cartella_destinazione.grid(row=0, column=0, sticky='w')

cartella_destinazione_entry = ttk.Entry(frame_cartella_destinazione, width=40)
cartella_destinazione_entry.grid(row=0, column=1, sticky='w')

bottone_cartella_destinazione = ttk.Button(frame_cartella_destinazione, text="Sfoglia", command=lambda: seleziona_cartella(cartella_destinazione_entry))
bottone_cartella_destinazione.grid(row=0, column=2, **padding_frame)

# Tipi File
frame_tipi_file = ttk.Frame(app)
frame_tipi_file.pack(**padding_frame)

etichetta_tipi_file = ttk.Label(frame_tipi_file, text="Seleziona Tipi di File:")
etichetta_tipi_file.grid(row=0, column=0, sticky='w')

variabili_tipi_file = [tk.BooleanVar(value=True) for _ in range(4)]

tipi_file = ['audio', 'video', 'documenti', 'immagini']
for i, tipo_file in enumerate(tipi_file):
    checkbox_tipo_file = ttk.Checkbutton(frame_tipi_file, text=tipo_file.capitalize(), variable=variabili_tipi_file[i])
    checkbox_tipo_file.grid(row=0, column=i + 1, **padding_frame)

# Azione
frame_azione = ttk.Frame(app)
frame_azione.pack(**padding_frame)

etichetta_azione = ttk.Label(frame_azione, text="Seleziona Azione:")
etichetta_azione.grid(row=0, column=0, sticky='w')

azione_var = tk.StringVar(value='copia')
menu_azione = ttk.Combobox(frame_azione, textvariable=azione_var, values=('copia', 'sposta'))
menu_azione.grid(row=0, column=1, **padding_frame)

# Bottone Esegui
bottone_esegui = ttk.Button(app, text="Esegui", command=esegui_azione)
bottone_esegui.pack(pady=10)

# Etichetta Risultato
risultato_label = ttk.Label(app, text="")
risultato_label.pack(pady=10)

app.mainloop()
