[ScreenShot]([https://github.com/BayLak-ONE/Random-tools/blob/main/color-dropper/Screenshot%20from%202025-12-21%2022-33-23.png](https://github.com/BayLak-ONE/Random-tools/blob/dfa8af02662301b4472b5801084b0447d691e4c7/Python%20Script%20Cleaner/Screenshot%20from%202026-01-12%2021-08-50.png))
# Python Script Cleaner 

A lightweight and efficient desktop application built with Python and Tkinter to clean your Python source code. It automatically removes comments and empty lines to make your scripts concise and production-ready.

## ✨ Features

- **Batch Processing**: Clean multiple files or entire directories at once.
- **In-place Updates**: Directly updates the original files (Overwrites) to save time.
- **Intelligent Cleaning**: 
    - Removes full-line comments (`#`).
    - Removes trailing (side) comments.
    - Preserves hashes `#` inside string literals (e.g., `print("Hello # world")`).
    - Removes unnecessary blank lines.
- **Async Processing**: Uses multi-threading to prevent the UI from freezing when scanning large folders.
- **Modern UI**: 
    - Clean and intuitive interface.
    - Right-click context menu for easy file management.
    - Real-time progress bar.

## 🛠️ How to Use

1. **Run the Script**: Execute the Python file.
2. **Add Files/Folders**: 
   - Right-click inside the list area.
   - Choose **Add File(s)** to pick specific scripts.
   - Choose **Add Folder** to scan a directory recursively for `.py` files.
3. **Manage List**: If you added something by mistake, select it and right-click to **Remove Selected**.
4. **Start Cleaning**: Click the **START CLEANING** button. 
   - *Note: You will be asked for confirmation before overwriting.*

## 📋 Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## 📸 Preview

- **File List**: Shows absolute paths for accuracy.
- **Context Menu**: Add or remove items easily with a right-click.
- **Progress Tracking**: Visual feedback during the cleaning process.


