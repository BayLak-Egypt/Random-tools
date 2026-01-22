import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageTk
try:
    from circle import round_image_tk
except ImportError:
    def round_image_tk(img):
        return ImageTk.PhotoImage(img)
def add_message_bubble(scrollable_frame, canvas, msg, sender_name, client_name):
    chat_font = tkfont.Font(family="Segoe UI", size=10)
    max_bubble_width = 280
    text_w = chat_font.measure(msg)
    if text_w > max_bubble_width - 30:
        width = max_bubble_width
        lines = (text_w // (max_bubble_width - 30)) + 1
        height = (lines * 20) + 45
    else:
        width = text_w + 40
        height = 60
    row_container = tk.Frame(scrollable_frame, bg=scrollable_frame["bg"])
    row_container.pack(fill="x", expand=True, pady=3)
    if sender_name == client_name:
        bg_color = (220, 248, 198, 255)
        side_direction = "right"
        name_color = "#075e54"
        padx_val = (60, 15)
    else:
        bg_color = (255, 255, 255, 255)
        side_direction = "left"
        name_color = "#128c7e"
        padx_val = (15, 60)
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width, height], radius=15, fill=bg_color)
    tk_img = round_image_tk(img)
    bubble_canvas = tk.Canvas(row_container, width=width, height=height,
                              bg=scrollable_frame["bg"], highlightthickness=0)
    bubble_canvas.create_image(0, 0, anchor="nw", image=tk_img)
    bubble_canvas.image = tk_img
    bubble_canvas.create_text(15, 8, text=sender_name, anchor="nw",
                              fill=name_color, font=("Segoe UI", 8, "bold"))
    bubble_canvas.create_text(15, 25, text=msg, anchor="nw",
                              width=max_bubble_width-30,
                              fill="#303030", font=chat_font)
    bubble_canvas.pack(side=side_direction, padx=padx_val)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)
def add_typing_indicator(scrollable_frame, canvas, sender_name, client_name):
    width, height = 60, 35
    row_container = tk.Frame(scrollable_frame, bg=scrollable_frame["bg"])
    row_container.pack(fill="x", expand=True, pady=3)
    is_client = (sender_name == client_name)
    side = "right" if is_client else "left"
    bg_color = (220, 248, 198, 255) if is_client else (255, 255, 255, 255)
    padx_val = (60, 15) if is_client else (15, 60)
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width, height], radius=15, fill=bg_color)
    tk_img = round_image_tk(img)
    bubble_canvas = tk.Canvas(row_container, width=width, height=height,
                              bg=scrollable_frame["bg"], highlightthickness=0)
    bubble_canvas.create_image(0, 0, anchor="nw", image=tk_img)
    bubble_canvas.image = tk_img
    bubble_canvas.pack(side=side, padx=padx_val)
    def animate_dots():
        dots = [".", "..", "..."]
        idx = 0
        def loop():
            nonlocal idx
            if bubble_canvas.winfo_exists():
                bubble_canvas.delete("dot")
                bubble_canvas.create_text(width//2, height//2, text=dots[idx],
                                          fill="#303030", font=("Segoe UI", 16, "bold"),
                                          tags="dot", anchor="center")
                idx = (idx + 1) % len(dots)
                bubble_canvas.after(500, loop)
        loop()
    animate_dots()
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)
    return row_container