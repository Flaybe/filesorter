import tkinter as tk
from tkinter import ttk
from main import dirSort
import os
from pathlib import Path
import json 

settings = json.load(open('settings.json'))
deafult_options = settings["Deafult_path"]
settings = settings["Settings"]


base_path = Path.home()

sorting = dirSort(base_path, settings)



def open_settings():
    os.system("open settings.json")



def sort():
    selected_directory = dir.get()
    if selected_directory == "All":
        for directory, details in settings.items():
            if directory == "All":
                continue
            if directory == "Skola":
                continue
            print(details)
            sorting.sort(f'{base_path}{details["Path"]}')
    else:
        print("Sorting: ", f'{base_path}{settings[selected_directory]["Path"]}')
        sorting.sort(f'{base_path}{settings[selected_directory]["Path"]}')
    

root = tk.Tk()
root.title("File sorter")

tk.Label(root, text="Choose a directory to sort").pack(pady=10)
dir = ttk.Combobox(root, values=list(settings.keys()), state='readonly')
dir.set(deafult_options["Name"])
dir.pack(pady=10)

# Not used have deafult value instead
# dir.bind("<<ComboboxSelected>>", on_selection_change)
sort_button = tk.Button(root, text="Sort", command=sort)
sort_button.pack(pady=10)

settings_button = tk.Button(root, text="Settings", command=open_settings)
settings_button.pack(pady=10)

root.mainloop()