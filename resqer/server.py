import tkinter as tk
import socket, threading, base64
import numpy as np
from PIL import Image, ImageTk
import qrcode
from crypto_utils import encrypt, decrypt, generate_key
from schat import add_message_bubble, add_typing_indicator
canvas_width = 20
canvas_height = 200
def make_qr(data_bytes, width, height=None):
    qr = qrcode.QRCode(box_size=1, border=0)
    qr.add_data(data_bytes)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("L")
    if height is None:
        height = img.height
    img = img.resize((width, height), Image.NEAREST)
    return np.array(img)
class DualQRServerGUI:
    def __init__(self, host="0.0.0.0", port=9000):
        self.host = host
        self.port = port
        self.qr_send_canvas = np.ones((canvas_height, canvas_width), dtype=np.uint8) * 255
        self.qr_recv_canvas = np.ones((canvas_height, canvas_width), dtype=np.uint8) * 255
        self.conn = None
        self.session_key = None
        self.typing_bubble = None
        self.typing_sent = False
        self.root = tk.Tk()
        self.root.title("Server Chat + QR")
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=5, pady=5, fill="both", expand=True)
        self.canvas = tk.Canvas(main_frame, bg="#e5ddd5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#e5ddd5")
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", in_=self.canvas)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        strip_frame = tk.Frame(main_frame)
        strip_frame.pack(side="left", padx=5)
        tk.Label(strip_frame, text="SEND").pack()
        self.qr_send_label = tk.Label(strip_frame)
        self.qr_send_label.pack(pady=5)
        tk.Label(strip_frame, text="RECV").pack()
        self.qr_recv_label = tk.Label(strip_frame)
        self.qr_recv_label.pack(pady=5)
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=5)
        self.entry = tk.Entry(entry_frame, width=50)
        self.entry.pack(side="left", padx=5)
        tk.Button(entry_frame, text="SEND", command=self.send_msg).pack(side="left")
        self.entry.bind("<KeyRelease>", self.on_typing)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.add_local_bubble(f"🟢 Server listening on {self.host}:{self.port}", "System")
        threading.Thread(target=self.accept_clients_loop, daemon=True).start()
        self.root.mainloop()
    def safe_send(self, data_bytes):
        if not self.conn:
            return
        self.conn.send(data_bytes)
        self.update_qr_strip(self.qr_send_canvas, self.qr_send_label, data_bytes, down=True)
    def safe_recv(self, bufsize=4096):
        if not self.conn:
            return None
        data = self.conn.recv(bufsize)
        if data:
            self.update_qr_strip(self.qr_recv_canvas, self.qr_recv_label, data, down=False)
        return data
    def add_local_bubble(self, msg, sender_name="Server"):
        add_message_bubble(self.scrollable_frame, self.canvas, msg, sender_name, client_name=sender_name)
    def on_typing(self, event):
        if not self.conn or not self.session_key:
            return
        text = self.entry.get().strip()
        try:
            if text and not self.typing_sent:
                self.safe_send(encrypt(self.session_key, b"__TYPING__"))
                self.typing_sent = True
            elif not text and self.typing_sent:
                self.safe_send(encrypt(self.session_key, b"__STOP_TYPING__"))
                self.typing_sent = False
        except:
            pass
    def send_msg(self):
        if not self.conn or not self.session_key:
            self.add_local_bubble("⚠️ No client connected", "System")
            return
        msg = self.entry.get().strip()
        if not msg:
            return
        try:
            enc = encrypt(self.session_key, msg.encode())
            self.safe_send(enc)
            self.add_local_bubble(msg, "Server")
            self.entry.delete(0, tk.END)
            if self.typing_sent:
                self.safe_send(encrypt(self.session_key, b"__STOP_TYPING__"))
                self.typing_sent = False
        except:
            self.add_local_bubble("❌ Send failed", "System")
    def accept_clients_loop(self):
        while True:
            conn, addr = self.sock.accept()
            self.conn = conn
            self.session_key = generate_key(32)
            self.safe_send(base64.b64encode(self.session_key))
            self.add_local_bubble(f"🔵 Client connected: {addr}", "System")
            threading.Thread(target=self.receive_loop, daemon=True).start()
    def receive_loop(self):
        while True:
            try:
                data = self.safe_recv(4096)
                if not data:
                    self.add_local_bubble("⚠️ Client disconnected", "System")
                    break
                msg = decrypt(self.session_key, data).decode()
                if msg == "__TYPING__":
                    if not self.typing_bubble:
                        self.typing_bubble = add_typing_indicator(
                            self.scrollable_frame, self.canvas, "Client", "Server"
                        )
                    continue
                if msg == "__STOP_TYPING__":
                    if self.typing_bubble:
                        self.typing_bubble.destroy()
                        self.typing_bubble = None
                    continue
                if self.typing_bubble:
                    self.typing_bubble.destroy()
                    self.typing_bubble = None
                self.add_local_bubble(msg, "Client")
            except:
                self.add_local_bubble("❌ Receive error", "System")
                break
    def update_qr_strip(self, canvas, label, data_bytes, down=True):
        qr = make_qr(data_bytes, canvas_width, canvas_height)
        h = qr.shape[0]
        if down:
            canvas[:] = np.roll(canvas, -h, axis=0)
            canvas[-h:, :] = qr
        else:
            canvas[:] = np.roll(canvas, h, axis=0)
            canvas[:h, :] = qr
        img = ImageTk.PhotoImage(Image.fromarray(canvas))
        label.config(image=img)
        label.image = img
if __name__ == "__main__":
    DualQRServerGUI(host="0.0.0.0", port=9000)