import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import threading

def clean_python_code(code: str) -> str:
    cleaned_lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "#" in line:
            parts = re.split(r'(?:"[^"]*"|\'[^\']*\')', line)
            if "#" in parts[-1] or "#" in line:
                 line = line.split("#", 1)[0].rstrip()
        if line.strip():
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
    current_list = listbox_files.get(0, tk.END)
    for f in files:
        abs_path = os.path.abspath(f)
        if abs_path not in current_list:
            listbox_files.insert(tk.END, abs_path)

def select_folder():
    folder = filedialog.askdirectory(mustexist=True)
    if folder:
        folder = os.path.abspath(folder)
        threading.Thread(target=scan_folder_task, args=(folder,), daemon=True).start()

def scan_folder_task(folder):
    current_list = listbox_files.get(0, tk.END)
    new_files = []
    for root_dir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.abspath(os.path.join(root_dir, file))
                if full_path not in current_list and full_path not in new_files:
                    new_files.append(full_path)
    for path in new_files:
        root.after(0, lambda p=path: listbox_files.insert(tk.END, p))

def delete_selected():
    selected_indices = listbox_files.curselection()
    for i in reversed(selected_indices):
        listbox_files.delete(i)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def process_files_task(files):
    progress_bar["maximum"] = len(files)
    for idx, file_path in enumerate(files, start=1):
        try:
            if not os.path.exists(file_path): continue
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            cleaned_code = clean_python_code(code)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_code)
        except Exception:
            pass
        root.after(0, lambda v=idx: progress_bar.configure(value=v))
    root.after(0, lambda: messagebox.showinfo("Success", "Files updated successfully!"))
    root.after(0, lambda: listbox_files.delete(0, tk.END))
    root.after(0, lambda: progress_bar.configure(value=0))

def start_cleaning():
    files = listbox_files.get(0, tk.END)
    if not files:
        messagebox.showwarning("Warning", "The list is empty!")
        return
    if messagebox.askyesno("Confirm", "Overwrite original files?"):
        threading.Thread(target=process_files_task, args=(files,), daemon=True).start()

root = tk.Tk()
root.title("Python Script Cleaner")
root.geometry("700x550")
root.configure(bg="#f0f2f5")

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Add File(s)", command=select_files)
context_menu.add_command(label="Add Folder", command=select_folder)
context_menu.add_separator()
context_menu.add_command(label="Remove Selected", command=delete_selected, foreground="red")

tk.Label(root, text="Files to Process:", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(pady=(15, 5), padx=25, anchor="w")

list_frame = tk.Frame(root, bg="#f0f2f5")
list_frame.pack(fill="both", expand=True, padx=25)

scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")

listbox_files = tk.Listbox(
    list_frame, font=("Consolas", 10), selectmode=tk.EXTENDED,
    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set,
    borderwidth=1, relief="solid"
)

scroll_y.config(command=listbox_files.yview)
scroll_x.config(command=listbox_files.xview)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
listbox_files.pack(side="left", fill="both", expand=True)

listbox_files.bind("<Button-3>", show_context_menu)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
progress_bar.pack(fill="x", padx=25, pady=15)

btn_run = tk.Button(
    root, text="START CLEANING", command=start_cleaning,
    bg="#1a73e8", fg="white", font=("Arial", 11, "bold"),
    relief="flat", pady=12, cursor="hand2"
)
btn_run.pack(fill="x", padx=25, pady=(0, 10))

footer_label = tk.Label(root, text="2026 made by baylak", bg="#f0f2f5", fg="#888", font=("Arial", 9, "italic"))
footer_label.pack(pady=(0, 15))

root.mainloop()
