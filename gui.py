import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
import json
from main import dirSort
import shutil


class FileSorterApp:
    DEAFULT_OPTION = "Downloads"

    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")

        # Load or initialize settings
        self.base_path = Path.home()
        self.settings = self.load_settings()
        self.sorting = dirSort(self.base_path, self.settings)
        self.safe_moves = tk.BooleanVar(value=True)

        # Initialize main menu
        self.main_menu()

    def load_settings(self):
        # Load settings from file
        try:
            with open("settings.json", "r") as file:
                return json.load(file)
        except:
            # Initialize settings to the user's home directory
            settings = {}
            for file in os.listdir(self.base_path):
                if not file.startswith("."):
                    settings[file] = {"Path": f"/{file}", "Format": [], "Keywords" : []}
            self.save_settings(settings)
            return settings

    def save_settings(self, data):
        with open("settings.json", "w") as file:
            json.dump(data, file, indent=4)

    def toggle_safe_moves(self):
        self.safe_moves = not self.safe_moves

    def sort_directory(self, directory):

        moves = self.sorting.sort(f'{self.base_path}{self.settings[directory]["Path"]}')
        print("# Moves: " , len(moves))

        if moves:
            if self.safe_moves:
                self.show_confirmation_window(moves)
            else:
                for move in moves:
                    try:
                        shutil.move(move[0], move[1])
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to move {move[0]}: {e}")
        else:
            messagebox.showinfo("Info", "No files to move.")


    def show_confirmation_window(self, moves):
        num_items = len(moves)
        processed_items = 0
        # Create a pop-up window
        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Confirm File Moves")

        # Table frame
        table = tk.Frame(confirmation_window)  # Define `table` here
        table.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Function to handle file acceptance
        def accept_move(index):
            move = moves[index]
            try:
                shutil.move(move[0], move[1])  # Perform the move
                for widget in table.grid_slaves(row=index):  # Remove the row
                    widget.destroy()
                nonlocal processed_items
                processed_items += 1
                if num_items <= processed_items:  # Close the window if all moves are done
                    confirmation_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move {move[0]}: {e}")

        # Function to reject a move
        def reject_move(index):
            for widget in table.grid_slaves(row=index):  # Remove the row
                widget.destroy()
            nonlocal processed_items
            processed_items += 1
            if num_items <= processed_items:  # Close the window if all moves are done
                confirmation_window.destroy()

        # Table header
        tk.Label(confirmation_window, text="Source", width=30, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(confirmation_window, text="Destination", width=30, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(confirmation_window, text="Action", width=30, anchor="w").grid(row=0, column=2, padx=5, pady=5)

        # Table rows
        for index, move in enumerate(moves):
            source_label = tk.Label(table, text=move[0], width=30, anchor="w")
            destination_label = tk.Label(table, text=move[1], width=30, anchor="w")
            accept_button = tk.Button(table, text="Accept", command=lambda idx=index: accept_move(idx))
            reject_button = tk.Button(table, text="Reject", command=lambda idx=index: reject_move(idx))

            source_label.grid(row=index, column=0, padx=5, pady=5)
            destination_label.grid(row=index, column=1, padx=5, pady=5)
            accept_button.grid(row=index, column=2, padx=5, pady=5)
            reject_button.grid(row=index, column=3, padx=5, pady=5)        

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Choose a directory to sort").pack(pady=10)
        dir_selector = ttk.Combobox(self.root, values=list(self.settings.keys()), state="readonly")
        dir_selector.set(self.DEAFULT_OPTION)
        dir_selector.pack(pady=10)

        tk.Button(self.root, text="Sort", command=lambda: self.sort_directory(dir_selector.get())).pack(pady=10)
        tk.Button(self.root, text="Settings", command=self.open_settings).pack(pady=10)

        tk.Checkbutton(self.root, text="Safe Moves", variable=self.safe_moves, command=self.toggle_safe_moves).pack(pady=10)


    def open_settings(self):
        self.clear_window()

        # Keybinding for saving settings
        self.root.bind("<Command-s>", lambda e: self.save_edits())
        self.root.bind("<Control-s>", lambda e: self.save_edits())

        def valid_path(path):
            return os.path.exists(f'{self.base_path}{path}')

        def refresh_tree():
            tree.delete(*tree.get_children())
            for category, details in self.settings.items():
                print(category, details)
                tree.insert("", "end", text=category, values=(details["Path"], ", ".join(details["Format"]), ", ".join(details["Keywords"])) )

        def on_select(event):
            selected = tree.focus()
            if not selected:
                return

            category = tree.item(selected)["text"]
            if category in self.settings:
                entry_name.delete(0, tk.END)
                entry_name.insert(0, category)

                entry_path.delete(0, tk.END)
                entry_path.insert(0, self.settings[category]["Path"])

                entry_format.delete(0, tk.END)
                entry_format.insert(0, ", ".join(self.settings[category]["Format"]))

                entry_keywords.delete(0, tk.END)
                entry_keywords.insert(0, ", ".join(self.settings[category]["Keywords"]))


        def save_edits():
            category = entry_name.get().strip()
            path = entry_path.get().strip()
            formats = [fmt.strip() for fmt in entry_format.get().split(",")]
            keywords = [kw.strip() for kw in entry_keywords.get().split(",")]

            if not category or not path:
                messagebox.showerror("Error", "Name and Path cannot be empty.")
                return

            if not valid_path(path):
                messagebox.showerror("Error", "Invalid path.")
                return
            try:
                selected = tree.focus()
                old_category = tree.item(selected)["text"]

                if old_category and old_category != category:
                    self.settings[category] = self.settings.pop(old_category)

                self.settings[category] = {"Path": path, "Format": formats, "Keywords": keywords}
                refresh_tree()
                self.save_settings(self.settings)
                status_field.config(text=f"Category {category} updated successfully.")
            except Exception as e:
                status_field.config(text=f"Error: {e}")

        def add_category():
            category = entry_name.get().strip()
            path = entry_path.get().strip()
            formats = [fmt.strip() for fmt in entry_format.get().split(",")]

            if category in self.settings:
                messagebox.showerror("Error", "Category already exists.")
                return

            self.settings[category] = {"Path": path, "Format": formats}
            refresh_tree()
            self.save_settings(self.settings)
            status_field.config(text=f"Category {category} added successfully.")

        def remove_category():
            selected = tree.focus()
            if not selected:
                return

            category = tree.item(selected)["text"]
            self.settings.pop(category, None)
            refresh_tree()
            self.save_settings(self.settings)
            status_field.config(text=f"Category {category} removed successfully.")

        tree = ttk.Treeview(self.root, columns=("Path", "Formats", "Keywords"), show="tree headings")
        tree.heading("Path", text="Path")
        tree.heading("Formats", text="Formats")
        tree.heading("Keywords", text="Keywords")
        tree.column("Path", width=200)
        tree.column("Formats", width=200)
        tree.column("Keywords", width=200)

        tree.bind("<<TreeviewSelect>>", on_select)
        tree.pack(fill="both", expand=True)

        # Editable fields
        frame = tk.Frame(self.root)
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

        tk.Label(frame, text="Keywords (comma-separated):").grid(row=3, column=0, sticky="w")
        entry_keywords = tk.Entry(frame)
        entry_keywords.grid(row=3, column=1, sticky="ew")


        frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(button_frame, text="Save Changes", command=save_edits).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add Category", command=add_category).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Category", command=remove_category).pack(side="left", padx=5)
        status_field = tk.Label(button_frame, text="")
        status_field.pack(side="left", padx=5)
        tk.Button(button_frame, text="Go Back", command=self.main_menu).pack(side="right", padx=5)

        
        # Populate Treeview
        refresh_tree()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()