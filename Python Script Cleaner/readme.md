![ScreenShot](https://raw.githubusercontent.com/BayLak-ONE/Random-tools/refs/heads/main/Python%20Script%20Cleaner/Screenshot%20from%202026-01-12%2021-08-50.png?token=GHSAT0AAAAAADQIYFFD5IHKCOU4KQ6XF5TM2LFJDIQ)
# Python Script Cleaner 

A robust desktop utility built with Python to streamline your source code. This tool automatically removes comments and redundant blank lines while ensuring your functional code (like Hex color codes) remains intact.

## ✨ Key Features

- **Drag & Drop Support**: Simply drag files or folders directly into the app (powered by `tkinterdnd2`).
- **Smart Cleaning**: 
    - Removes full-line and trailing comments (`#`).
    - **Safe-Hex Technology**: Intelligently ignores `#` inside strings and Hex color codes (e.g., `bg="#ffffff"` stays safe).
- **In-place Updates**: Directly overwrites the original files to keep your workspace clean.
- **Asynchronous Processing**: Multi-threaded scanning and cleaning to prevent UI freezing, even with thousands of files.
- **Context Menu**: Right-click anywhere in the list to add files, add folders, or remove specific items.
- **Progress Tracking**: Real-time progress bar for batch operations.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x
- Tkinter (standard with Python)

### Optional (For Drag & Drop)
To enable the Drag & Drop feature, install the following:
```bash
pip install tkinterdnd2
