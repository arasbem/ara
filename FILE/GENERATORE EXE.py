import tkinter as tk
from tkinter import filedialog
import os
import subprocess

def select_script():
    global script_path
    script_path = filedialog.askopenfilename(filetypes=[("File Python", "*.py")])
    update_entry(script_entry, script_path)

def select_icon():
    global icon_path
    icon_path = filedialog.askopenfilename(filetypes=[("File Icona", "*.ico")])
    update_entry(icon_entry, icon_path)

def update_entry(entry, value):
    entry.config(state="normal")
    entry.delete(0, "end")
    entry.insert(0, value)
    entry.config(state="readonly")

def run_pyinstaller():
    if script_path and icon_path:
        script_dir = os.path.dirname(script_path)
        script_name = os.path.basename(script_path)
        icon_name = os.path.basename(icon_path)

        command = f'cd "{script_dir}" && pyinstaller --onefile --noconsole --icon="{icon_name}" "{script_name}"'
        
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            status_label.config(text=f"File generato con successo!\n{result.stdout}", fg="green")
        except subprocess.CalledProcessError as e:
            status_label.config(text=f"Errore durante l'esecuzione di PyInstaller:\n{e.stderr}", fg="red")
    else:
        status_label.config(text="Seleziona il percorso dello script e l'icona prima di eseguire.", fg="red")

root = tk.Tk()
root.title("PyInstaller GUI")

script_label = tk.Label(root, text="Seleziona il file .py da convertire:")
script_label.pack()

script_entry = tk.Entry(root, state="readonly", width=40)
script_entry.pack()

script_button = tk.Button(root, text="Sfoglia", command=select_script)
script_button.pack()

icon_label = tk.Label(root, text="Seleziona l'icon .ico (opzionale):")
icon_label.pack()

icon_entry = tk.Entry(root, state="readonly", width=40)
icon_entry.pack()

icon_button = tk.Button(root, text="Sfoglia", command=select_icon)
icon_button.pack()

run_button = tk.Button(root, text="Esegui PyInstaller", command=run_pyinstaller)
run_button.pack()

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

root.mainloop()
