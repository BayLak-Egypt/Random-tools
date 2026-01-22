import tkinter as tk
from tkinter import ttk
import socket, threading, base64
from crypto_utils import encrypt, decrypt
from schat import add_message_bubble, add_typing_indicator
from circle import rounded_button
class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Chat Client")
        self.master.geometry("400x600")
        self.master.configure(bg="#e5ddd5")
        self.sock = None
        self.session_key = None
        self.name = "UNKNOWN"
        self.typing_bubble = None
        self._typing_sent = False
        self.show_login()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    def show_login(self):
        self.clear_window()
        main_frame = tk.Frame(self.master, bg="#e5ddd5")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(main_frame, text="Enter Your Name:", font=("Arial", 11), bg="#e5ddd5").pack(pady=5)
        self.name_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Client")
        tk.Label(main_frame, text="Server IP:", font=("Arial", 11), bg="#e5ddd5").pack(pady=5)
        self.ip_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.ip_entry.pack(pady=5)
        self.ip_entry.insert(0, "127.0.0.1")
        tk.Button(main_frame, text="Connect", bg="#25D366", fg="white",
                  font=("Arial", 12, "bold"), command=self.start_connection).pack(pady=20)
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', mode='indeterminate', length=200)
        self.progress.pack(pady=10)
        self.error_label = tk.Label(main_frame, text="", fg="red", bg="#e5ddd5")
        self.error_label.pack()
    def start_connection(self):
        self.name = self.name_entry.get().strip() or "UNKNOWN"
        self.host = self.ip_entry.get().strip()
        self.port = 9000
        threading.Thread(target=self.connect_to_server, daemon=True).start()
    def connect_to_server(self):
        self.progress.start(10)
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.show_error(f"Connecting...")
                self.sock.connect((self.host, self.port))
                self.session_key = base64.b64decode(self.sock.recv(1024))
                self.progress.stop()
                self.master.after(0, self.show_chat)
                break
            except Exception as e:
                self.show_error(f"Retrying...")
    def show_chat(self):
        self.clear_window()
        self.canvas = tk.Canvas(self.master, bg="#e5ddd5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#e5ddd5")
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.sync_width)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", in_=self.canvas)
        entry_container = tk.Frame(self.master, bg="#f0f0f0", height=60)
        entry_container.pack(fill="x", side="bottom", padx=5, pady=5)
        self.msg_entry = tk.Entry(entry_container, font=("Arial", 12))
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        self.msg_entry.bind("<KeyRelease>", lambda e: self.check_typing())
        send_btn = rounded_button(entry_container, text="Send", bg="#25D366", fg="white", radius=15,
                                  width=60, height=35, command=self.send_message)
        send_btn.pack(side="right", padx=5)
        threading.Thread(target=self.receive_messages, daemon=True).start()
    def sync_width(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)
    def check_typing(self):
        if not self.sock or not self.session_key:
            return
        msg_text = self.msg_entry.get().strip()
        try:
            if msg_text and not self._typing_sent:
                self.sock.send(encrypt(self.session_key, b"__TYPING__"))
                self._typing_sent = True
            elif not msg_text and self._typing_sent:
                self.sock.send(encrypt(self.session_key, b"__STOP_TYPING__"))
                self._typing_sent = False
        except:
            pass
    def send_message(self):
        msg = self.msg_entry.get().strip()
        if not msg:
            try:
                if self._typing_sent:
                    self.sock.send(encrypt(self.session_key, b"__STOP_TYPING__"))
                    self._typing_sent = False
            except: pass
            return
        try:
            self.sock.send(encrypt(self.session_key, msg.encode()))
            add_message_bubble(self.scrollable_frame, self.canvas, msg, self.name, self.name)
            self.msg_entry.delete(0, tk.END)
            try:
                if self._typing_sent:
                    self.sock.send(encrypt(self.session_key, b"__STOP_TYPING__"))
                    self._typing_sent = False
            except: pass
        except: pass
    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data: break
                msg = decrypt(self.session_key, data).decode()
                if msg == "__TYPING__":
                    self.master.after(0, lambda: self.start_typing_indicator("Server"))
                elif msg == "__STOP_TYPING__":
                    self.master.after(0, self.stop_typing_indicator)
                else:
                    self.master.after(0, lambda m=msg: self.stop_typing_and_add(m))
            except: break
    def start_typing_indicator(self, sender_name):
        if not self.typing_bubble:
            self.typing_bubble = add_typing_indicator(self.scrollable_frame, self.canvas, sender_name, self.name)
    def stop_typing_indicator(self):
        if self.typing_bubble:
            self.typing_bubble.destroy()
            self.typing_bubble = None
    def stop_typing_and_add(self, msg):
        self.stop_typing_indicator()
        add_message_bubble(self.scrollable_frame, self.canvas, msg, "Server", self.name)
    def show_error(self, msg):
        self.master.after(0, lambda: self.error_label.config(text=msg))
    def clear_window(self):
        for w in self.master.winfo_children():
            w.destroy()
    def on_close(self):
        if self.sock: self.sock.close()
        self.master.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()