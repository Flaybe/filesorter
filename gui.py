import tkinter as tk
from tkinter import ttk, messagebox
from main import dirSort
import os
from pathlib import Path
import json 

DEAFULT_OPTION = "Downloads"

# Save the JSON file
def save_json(data):
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=4)



try:
    settings = json.load(open('settings.json'))
except:
    # Create a default settings file
    settings = {
    "Pictures" : {
        "Path" : "/Pictures",
        "Format" : ["jpg", "png", "jpeg"]
    },
    "Music" : {
        "Path" : "/Music",
        "Format" : ["mp3", "wav"]
    },
    "Movies" : {
        "Path" : "/Movies",
        "Format" : ["mp4", "avi"]
    },
    "Documents" : {
        "Path" : "/Documents",
        "Format" : ["pdf", "docx"]
    },
    "Skola" : {
        "Path" : "/Skola",
        "Format" : []
    },
    "Downloads" : {
        "Path" : "/Downloads",
        "Format" : []
    },
    "All" : {
        "Path" : "/",
        "Format" : []
    }

}

    save_json(settings)

deafult_options = settings[DEAFULT_OPTION]

base_path = Path.home()

sorting = dirSort(base_path, settings)



def sort(directory : str):
    if directory == "All":
        for directory, details in settings.items():
            if directory == "All":
                continue
            if directory == "Skola":
                continue
            print(details)
            sorting.sort(f'{base_path}{details["Path"]}')
    else:
        print("Sorting: ", f'{base_path}{settings[directory]["Path"]}')
        sorting.sort(f'{base_path}{settings[directory]["Path"]}')
    

root = tk.Tk()
root.title("File sorter")


def open_settings():
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

        # Keybinding for Cmd + S or Ctrl + S
    def save_json_key(event=None):
        save_edits(settings)
        status_field.config(text="Settings saved successfully!")

    root.bind("<Command-s>", save_json_key)  # For macOS
    root.bind("<Control-s>", save_json_key)  # For Windows/Linux

    # Refresh the Treeview
    def refresh_tree():
        tree.delete(*tree.get_children())  # Clear all items
        for category, details in settings.items():
            tree.insert("", "end", text=category, values=(details["Path"], ", ".join(details["Format"])))

    # Update the form fields based on selected item
    def on_select(event):
        selected = tree.focus()  # Get the selected item's ID
        if not selected:
            return

        category = tree.item(selected)["text"]
        if category in settings:
            entry_name.delete(0, tk.END)
            entry_name.insert(0, category)

            entry_path.delete(0, tk.END)
            entry_path.insert(0, settings[category]["Path"])

            entry_format.delete(0, tk.END)
            entry_format.insert(0, ", ".join(settings[category]["Format"]))

    # Save edits to the JSON data
    def save_edits():

        category = entry_name.get().strip()
        path = entry_path.get().strip()
        formats = [fmt.strip() for fmt in entry_format.get().split(",")]


        if not category or not path:
            messagebox.showerror("Error", "Name and Path cannot be empty.")
            return
        
        if valid_path(path):
            messagebox.showerror("Error", "Invalid path.")
            return
        
        if category not in settings:
            add_category(category, path, formats)
            return

        # Update the JSON data
        selected = tree.focus()
        old_category = tree.item(selected)["text"]


        if old_category != category and old_category:
            print("Old category: ", old_category)
            settings[category] = settings.pop(old_category)

        settings[category]["Path"] = path
        settings[category]["Format"] = formats

        # Update the tree
        refresh_tree()
        save_json(settings)
        status_field.config(text=f"Category {category} updated successfully.")
    
    def add_category(category, path, formats):
        if category in settings:
            messagebox.showerror("Error", "Category already exists.")
            return

        settings[category] = {"Path": path, "Format": formats}
        refresh_tree()
        save_json(settings)

        status_field.config(text=f"Category {category} added successfully.")
    
    def remove_category():
        selected = tree.focus()
        if not selected:
            return

        category = tree.item(selected)["text"]
        settings.pop(category, None)

        
        refresh_tree()
        save_json(settings)
        status_field.config(text=f"Category {category} removed successfully.")

    # Treeview
    tree = ttk.Treeview(root, columns=("Path", "Formats"), show="tree headings")
    tree.heading("#0", text="Name")
    tree.heading("Path", text="Path")
    tree.heading("Formats", text="Formats")
    tree.column("Path", width=200)
    tree.column("Formats", width=200)
    tree.bind("<<TreeviewSelect>>", on_select)
    tree.pack(fill="both", expand=True)

    # Editable fields
    frame = tk.Frame(root)
    frame.pack(fill="x", padx=10, pady=5)
    

    tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
    entry_name = tk.Entry(frame)
    entry_name.grid(row=0, column=1, sticky="ew")

    tk.Label(frame, text="Path:").grid(row=1, column=0, sticky="w")
    entry_path = tk.Entry(frame)
    entry_path.grid(row=1, column=1, sticky="ew")

    tk.Label(frame, text="Formats (comma-separated):").grid(row=2, column=0, sticky="w")
    entry_format = tk.Entry(frame)
    entry_format.grid(row=2, column=1, sticky="ew")

    frame.columnconfigure(1, weight=1)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", padx=10, pady=5)

    tk.Button(button_frame, text="Save Changes", command=save_edits).pack(side="left", padx=5)
    tk.Button(button_frame, text="Add Category", command=lambda: add_category(entry_name.get(), entry_path.get(), entry_format.get().split(","))).pack(side="left", padx=5)
    tk.Button(button_frame, text="Delete Category", command=remove_category).pack(side="left", padx=5)
    status_field = tk.Label(button_frame, text="")
    status_field.pack(side="left", padx=5)
    tk.Button(button_frame, text="Go Back", command=main_menu).pack(side="right", padx=5)

    # Populate Treeview
    refresh_tree()


def main_menu():
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Choose a directory to sort").pack(pady=10)
    dir = ttk.Combobox(root, values=list(settings.keys()), state='readonly')
    dir.set(DEAFULT_OPTION)
    dir.pack(pady=10)
    tk.Button(root, text="Sort", command=lambda: sort(dir.get())).pack(pady=10)
    tk.Button(root, text="Settings", command=open_settings).pack(pady=10)


# Initialize the main menu on startup
main_menu()




root.mainloop()


