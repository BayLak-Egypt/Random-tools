import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr
import threading
import json
import os
CONFIG_FILE = "settings.json"
class VoiceCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Voice Cleaner Pro")
        self.root.geometry("550x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#1C1C1C")
        self.settings = self.load_settings()
        tk.Label(root, text="AI Voice Cleaner Pro", font=("Arial", 18, "bold"),
                 fg="#FFD700", bg="#1C1C1C").pack(pady=15)
        frame = tk.Frame(root, bg="#2B2B2B", bd=2, relief=tk.RIDGE)
        frame.pack(pady=10, padx=15, fill=tk.X)
        self.select_button = tk.Button(frame, text="Select Audio File", command=self.select_file,
                                       bg="#0078D7", fg="white", font=("Arial", 12, "bold"), bd=0, padx=10, pady=5)
        self.select_button.pack(pady=15, fill=tk.X, padx=40)
        tk.Label(frame, text="Voice Boost (Gain x):", fg="white", bg="#2B2B2B", font=("Arial", 11)).pack()
        self.gain = tk.DoubleVar(value=self.settings.get("gain", 1.2))
        self.gain_slider = tk.Scale(frame, from_=1.0, to=3.0, resolution=0.1,
                                    orient=tk.HORIZONTAL, variable=self.gain,
                                    bg="#2B2B2B", fg="white", highlightbackground="#2B2B2B",
                                    troughcolor="#444444", sliderlength=20, length=400)
        self.gain_slider.pack(pady=5)
        self.reset_button = tk.Button(frame, text="Reset Settings", command=self.reset_settings,
                                       bg="#444444", fg="white", font=("Arial", 9), bd=0)
        self.reset_button.pack(pady=5)
        pb_frame = tk.Frame(root, bg="#1C1C1C")
        pb_frame.pack(pady=15)
        tk.Label(pb_frame, text="Processing Progress:", fg="white", bg="#1C1C1C").pack()
        self.progress = ttk.Progressbar(pb_frame, orient="horizontal", length=450, mode="determinate")
        self.progress.pack(pady=5)
        tk.Label(root, text="Created by Baylak", font=("Arial", 10, "italic"),
                 fg="#777777", bg="#1C1C1C").pack(side=tk.BOTTOM, pady=10)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"gain": 1.2}
        return {"gain": 1.2}
    def save_settings(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"gain": self.gain.get()}, f)
    def reset_settings(self):
        self.gain.set(1.2)
        messagebox.showinfo("Reset", "Settings restored to default.")
    def on_closing(self):
        self.save_settings()
        self.root.destroy()
    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if filename:
            self.select_button.config(state=tk.DISABLED)
            threading.Thread(target=self.process_file, args=(filename,), daemon=True).start()
    def process_file(self, filepath):
        try:
            y, sr = librosa.load(filepath, sr=None, mono=True)
            self.root.after(0, lambda: self.progress.configure(value=20))
            clean = nr.reduce_noise(y=y, sr=sr, stationary=True)
            self.root.after(0, lambda: self.progress.configure(value=60))
            clean *= self.gain.get()
            if np.max(np.abs(clean)) > 1.0:
                clean = clean / np.max(np.abs(clean))
            self.root.after(0, lambda: self.progress.configure(value=90))
            save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                     filetypes=[("WAV files", "*.wav")])
            if save_path:
                sf.write(save_path, clean, sr)
                self.root.after(0, lambda: messagebox.showinfo("Success", f"File saved successfully!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.progress.configure(value=0))
            self.root.after(0, lambda: self.select_button.config(state=tk.NORMAL))
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceCleanerGUI(root)
    root.mainloop()
