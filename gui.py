import tkinter as tk
from tkinter import ttk
from main import dirSort
import os
from pathlib import Path


base_path = Path.home()
print(base_path)



directories = {'Pictures' : f'{base_path}/Pictures',
               'Documents' : f'{base_path}/Documents',
                'Music' : f'{base_path}/Music',
                'Movies' : f'{base_path}/Movies',
                'Downloads' : f'{base_path}/Downloads',
                'Skola' : f'{base_path}/Skola'}


def on_button_click():
    selected_directory = dir.get()
    dirSort(directories[selected_directory]).sort()
    

def on_selection_change(event):
    if dir.get() != "Choose directory":
        button.pack(pady=10)  # Show the button


root = tk.Tk()
root.title("File sorter")

tk.Label(root, text="Choose a directory to sort").pack(pady=10)
dir = ttk.Combobox(root, values=list(directories.keys()), state='readonly')
dir.set('Choose directory')
dir.pack(pady=10)

dir.bind("<<ComboboxSelected>>", on_selection_change)
button = tk.Button(root, text="Sort", command=on_button_click)

root.mainloop()