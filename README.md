# FileSorter

**FileSorter** is a personal, non-profit Python application designed to help organize and sort files on your macOS system. This tool simplifies file management by categorizing and sorting files based on predefined formats, paths, and custom keywords.

---

## Features

- **File Sorting**: Automatically organizes files into specified directories based on their formats and keywords.
- **Customizable Settings**: Define your own categories, paths, and formats in a user-friendly interface.
- **Keyword Filtering**: Sort files based on associated keywords for better customization.
- **GUI with Tkinter**:
  - Main menu for directory selection and sorting.
  - Settings menu for adding, editing, and deleting categories.

---

## Installation

1. **Install Python and Tkinter**:
   - Make sure you have Python 3 installed on your system.
   - Install Tkinter if not already included:
     ```bash
     brew install python-tk
     ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/filesorter.git
   cd filesorter
   ```

3. **Install Dependencies**:
   The project relies on built-in Python libraries, so no additional dependencies are required.

4. **Run the Application**:
   ```bash
   python3 gui.py
   ```

---

## Configuration

The application uses a `settings.json` file to define sorting categories, paths, and file formats. You can modify this file directly or through the GUI in the settings menu.

### Example `settings.json` File:

```json
{
  "Pictures": {
    "Path": "/Pictures",
    "Format": ["jpg", "png"],
    "Keywords": ["vacation", "family"]
  },
  "Documents": {
    "Path": "/Documents",
    "Format": ["pdf", "docx"],
    "Keywords": ["work", "school"]
  }
}
```

---

## Usage

### Main Menu
- Select a directory to sort from the dropdown menu.
- Click **Sort** to organize the files in the selected directory.
- Access the **Settings** menu for more customization.

### Settings Menu
- View, add, edit, or delete sorting categories.
- Modify file formats and paths for each category.
- Save your changes and return to the main menu.

### Keyboard Shortcuts
- **Cmd + S** (macOS) / **Ctrl + S** (Windows/Linux): Save changes in the settings menu.

---

## Project Structure

```
filesorter/
│
├── gui.py              # Main GUI application code
├── main.py             # Core file sorting logic
├── settings.json       # Configuration file for categories, paths, and formats
└── README.md           # Project documentation
```

---

## Contributions

This is a personal, non-profit project. Contributions and suggestions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgements

- Built with ❤️ by a passionate developer to simplify file management on macOS.
