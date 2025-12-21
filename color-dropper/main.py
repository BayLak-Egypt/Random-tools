import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class UltraColorPickerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Dropper")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e2e")

        self.img_full = None
        self.tk_img = None
        self.current_scale = 1.0
        self.zoom_precision_size = 180
        self.edge_margin = 50
        self.mouse_x = 0
        self.mouse_y = 0

        self.setup_ui()
        self.edge_panning_loop()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#11111b", height=70)
        header.pack(side=tk.TOP, fill=tk.X)

        tk.Button(header, text="LOAD IMAGE", command=self.open_image, 
                  bg="#89b4fa", fg="#11111b", font=("Arial", 9, "bold"), 
                  padx=15, relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=20, pady=15)

        info_text = "Wheel: Zoom | Right Click: Drag | Left Click: Pick Color"
        tk.Label(header, text=info_text, bg="#11111b", fg="#a6adc8", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)

        credit_frame = tk.Frame(header, bg="#11111b")
        credit_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(credit_frame, text="Version 1.0", bg="#11111b", fg="#585b70", font=("Arial", 8)).pack()
        tk.Label(credit_frame, text="Created by Baylak", bg="#11111b", fg="#89b4fa", font=("Arial", 9, "bold")).pack()

        sidebar = tk.Frame(self.root, width=300, bg="#181825", padx=15, pady=15)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(sidebar, text="PRECISION VIEW", bg="#181825", fg="#89b4fa", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.zoom_canvas = tk.Canvas(sidebar, width=self.zoom_precision_size, height=self.zoom_precision_size, 
                                     bg="black", highlightthickness=1, highlightbackground="#313244")
        self.zoom_canvas.pack(pady=10)

        self.color_preview = tk.Frame(sidebar, height=40, bg="#313244", highlightthickness=1, highlightbackground="#cdd6f4")
        self.color_preview.pack(fill=tk.X, pady=5)

        self.hex_entry = self.create_input_row(sidebar, "HEX CODE")
        self.rgb_entry = self.create_input_row(sidebar, "RGB VALUE")

        self.canvas = tk.Canvas(self.root, bg="#1e1e2e", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<MouseWheel>", self.handle_zoom)
        self.canvas.bind("<Button-4>", self.handle_zoom)
        self.canvas.bind("<Button-5>", self.handle_zoom)
        
        self.canvas.bind("<ButtonPress-3>", self.start_drag)
        self.canvas.bind("<B3-Motion>", self.do_drag)
        
        self.canvas.bind("<Motion>", self.sync_mouse)
        self.canvas.bind("<Button-1>", self.pick_color)

    def create_input_row(self, parent, label):
        f = tk.Frame(parent, bg="#181825")
        f.pack(fill=tk.X, pady=8)
        tk.Label(f, text=label, bg="#181825", fg="#9399b2", font=("Arial", 8)).pack(anchor=tk.W)
        row = tk.Frame(f, bg="#181825")
        row.pack(fill=tk.X)
        entry = tk.Entry(row, font=("Consolas", 11), bg="#313244", fg="#cdd6f4", borderwidth=0)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(row, text="Copy", command=lambda: self.copy(entry.get()), 
                  bg="#45475a", fg="white", font=("Arial", 8), relief=tk.FLAT, padx=8).pack(side=tk.RIGHT, padx=2)
        return entry

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if path:
            raw = Image.open(path)
            if getattr(raw, "is_animated", False):
                raw.seek(0)
            self.img_full = raw.convert("RGB")
            self.current_scale = 1.0
            self.render()

    def render(self):
        if not self.img_full: return
        w, h = int(self.img_full.width * self.current_scale), int(self.img_full.height * self.current_scale)
        quality = Image.Resampling.NEAREST if self.current_scale > 2 else Image.Resampling.LANCZOS
        disp = self.img_full.resize((w, h), quality)
        self.tk_img = ImageTk.PhotoImage(disp)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.canvas.config(scrollregion=(0, 0, w, h))

    def handle_zoom(self, event):
        if not self.img_full: return
        if event.delta > 0 or event.num == 4:
            self.current_scale *= 1.2
        else:
            self.current_scale *= 0.8
        self.current_scale = max(0.1, min(self.current_scale, 10.0))
        self.render()

    def start_drag(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def do_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def sync_mouse(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        if not self.img_full: return
        ix = int(self.canvas.canvasx(event.x) / self.current_scale)
        iy = int(self.canvas.canvasy(event.y) / self.current_scale)
        if 0 <= ix < self.img_full.width and 0 <= iy < self.img_full.height:
            box = (ix-8, iy-8, ix+8, iy+8)
            crop = self.img_full.crop(box).resize((self.zoom_precision_size, self.zoom_precision_size), Image.NEAREST)
            self.zoom_tk = ImageTk.PhotoImage(crop)
            self.zoom_canvas.delete("all")
            self.zoom_canvas.create_image(0, 0, anchor=tk.NW, image=self.zoom_tk)
            mid = self.zoom_precision_size // 2
            self.zoom_canvas.create_rectangle(mid-3, mid-3, mid+3, mid+3, outline="white")
            r, g, b = self.img_full.getpixel((ix, iy))
            self.color_preview.config(bg='#{:02x}{:02x}{:02x}'.format(r, g, b))

    def edge_panning_loop(self):
        if self.img_full:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            if self.mouse_x > w - self.edge_margin: self.canvas.xview_scroll(2, "units")
            elif self.mouse_x < self.edge_margin: self.canvas.xview_scroll(-2, "units")
            if self.mouse_y > h - self.edge_margin: self.canvas.yview_scroll(2, "units")
            elif self.mouse_y < self.edge_margin: self.canvas.yview_scroll(-2, "units")
        self.root.after(30, self.edge_panning_loop)

    def pick_color(self, event):
        if not self.img_full: return
        ix, iy = int(self.canvas.canvasx(event.x)/self.current_scale), int(self.canvas.canvasy(event.y)/self.current_scale)
        if 0 <= ix < self.img_full.width and 0 <= iy < self.img_full.height:
            r, g, b = self.img_full.getpixel((ix, iy))
            hex_v = '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()
            self.hex_entry.delete(0, tk.END); self.hex_entry.insert(0, hex_v)
            self.rgb_entry.delete(0, tk.END); self.rgb_entry.insert(0, f"{r},{g},{b}")
            self.copy(hex_v)

    def copy(self, txt):
        self.root.clipboard_clear()
        self.root.clipboard_append(txt)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraColorPickerPro(root)
    root.mainloop()
