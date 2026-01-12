
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import threading

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False

def clean_python_code(code: str) -> str:
    cleaned_lines = []
    comment_re = re.compile(r'((?:(?:"(?:\\.|[^"])*")|(?:\'(?:\\.|[^\'])*\')|[^#])*)(#.*)?')
    for line in code.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        match = comment_re.match(line)
        if match:
            clean_line = match.group(1).rstrip()
            if clean_line:
                cleaned_lines.append(clean_line)
    return "\n".join(cleaned_lines)

def add_path_to_list(path):
    path = path.strip('{}').strip('"').strip("'")
    abs_path = os.path.abspath(path)
    if os.path.isfile(abs_path) and abs_path.endswith(".py"):
        if abs_path not in listbox_files.get(0, tk.END):
            listbox_files.insert(tk.END, abs_path)
    elif os.path.isdir(abs_path):
        threading.Thread(target=scan_folder_task, args=(abs_path,), daemon=True).start()

def handle_drop(event):
    data = event.data
    paths = re.findall(r'\{(.*?)\}|(\S+)', data)
    for p in paths:
        path = p[0] if p[0] else p[1]
        add_path_to_list(path)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
    for f in files:
        add_path_to_list(f)

def select_folder():
    folder = filedialog.askdirectory(mustexist=True)
    if folder:
        add_path_to_list(folder)

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
    
    root.after(0, lambda: messagebox.showinfo("Success", "Process Completed!"))
    root.after(0, lambda: listbox_files.delete(0, tk.END))
    root.after(0, lambda: progress_bar.configure(value=0))

def start_cleaning():
    files = listbox_files.get(0, tk.END)
    if not files:
        messagebox.showwarning("Warning", "The list is empty!")
        return
    if messagebox.askyesno("Confirm", "Overwrite original files?"):
        threading.Thread(target=process_files_task, args=(files,), daemon=True).start()

root = TkinterDnD.Tk() if HAS_DND else tk.Tk()
root.title("Python Script Cleaner")
root.geometry("700x600")
root.configure(bg="#f0f2f5")

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Add File(s)", command=select_files)
context_menu.add_command(label="Add Folder", command=select_folder)
context_menu.add_separator()
context_menu.add_command(label="Remove Selected", command=delete_selected, foreground="red")

status_text = "Drag & Drop enabled" if HAS_DND else "Drag & Drop disabled (Right-click to add)"
tk.Label(root, text=status_text, bg="#f0f2f5", font=("Arial", 9, "bold"), fg="#555").pack(pady=(10, 0), padx=25, anchor="w")
tk.Label(root, text="Files to Process:", bg="#f0f2f5", font=("Arial", 11, "bold")).pack(pady=(5, 5), padx=25, anchor="w")

list_frame = tk.Frame(root, bg="#f0f2f5")
list_frame.pack(fill="both", expand=True, padx=25)

scroll_y = ttk.Scrollbar(list_frame, orient="vertical")
scroll_x = ttk.Scrollbar(list_frame, orient="horizontal")

listbox_files = tk.Listbox(
    list_frame, font=("Consolas", 10), selectmode=tk.EXTENDED,
    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set,
    borderwidth=1, relief="solid"
)

if HAS_DND:
    listbox_files.drop_target_register(DND_FILES)
    listbox_files.dnd_bind('<<Drop>>', handle_drop)

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

tk.Label(root, text="2026 made by baylak", bg="#f0f2f5", fg="#888", font=("Arial", 9, "italic")).pack(pady=(0, 15))

root.mainloop()
