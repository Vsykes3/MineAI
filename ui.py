import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import os
import random

class MinecraftSlider(tk.Canvas):
    def __init__(self, master, variable, from_=0, to=1, **kwargs):
        super().__init__(master, width=200, height=24, bg= "gray24", highlightthickness=0, **kwargs)
        self.variable = variable
        self.from_ = from_
        self.to = to
        self.slider = self.create_rectangle(0, 0, 0, 0, fill="white", outline="white")
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Button-1>", self.on_click)
        self.draw_slider()

    def on_click(self, event):
        self.set_value(event.x)

    def on_drag(self, event):
        self.set_value(event.x)

    def set_value(self, x):
        width = self.winfo_width()
        val = (x / width) * (self.to - self.from_) + self.from_
        val = max(self.from_, min(self.to, val))
        self.variable.set(val)
        self.draw_slider()

    def draw_slider(self):
        width = self.winfo_width()
        value_ratio = (self.variable.get() - self.from_) / (self.to - self.from_)
        pos = int(value_ratio * width)
        self.coords(self.slider, pos - 10, 4, pos + 10, 20)

class SettingsUI:
    def __init__(self, root, on_settings_change):
        self.root = root
        self.on_settings_change = on_settings_change
        self.root.title("Mob TTS Assist")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        # Font loading
        font_path = "Minecraftia.ttf"  # Put this in the same folder
        if os.path.exists(font_path):
            self.block_font = tkfont.Font(file=font_path, size=10)
        else:
            self.block_font = ("Courier", 10, "bold")

        self.canvas = tk.Canvas(root, width=320, height=260, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_tiled_background()

        self.volume_var = tk.DoubleVar(value=1.0)
        self.voice_var = tk.StringVar(value="default")
        self.hotkey_var = tk.StringVar(value="f8")

        y = 20
        self.add_label("Volume", y)
        y += 30
        self.volume_slider = MinecraftSlider(self.canvas, self.volume_var, from_=0, to=1)
        self.canvas.create_window(160, y, window=self.volume_slider)
        y += 40

        self.add_label("Voice", y)
        y += 30
        self.voice_dropdown = ttk.Combobox(
            root, textvariable=self.voice_var,
            values=["default", "female", "male"], state="readonly",
            font=self.block_font
        )
        self.canvas.create_window(160, y, window=self.voice_dropdown, width=200)
        self.voice_dropdown.bind("<<ComboboxSelected>>", lambda _: self.update_settings())
        y += 40

        self.add_label("Set Hotkey (click then press key)", y)
        y += 30
        self.hotkey_button = tk.Label(
            root, text=self.hotkey_var.get().upper(), bg="#c6c6c6",
            font=self.block_font, bd=3, relief="raised", padx=10, pady=4
        )
        self.canvas.create_window(160, y, window=self.hotkey_button)
        self.hotkey_button.bind("<Button-1>", lambda e: self.start_hotkey_capture())
        self.hotkey_button.bind("<Enter>", lambda e: self.hotkey_button.config(bg="#d8d8d8"))
        self.hotkey_button.bind("<Leave>", lambda e: self.hotkey_button.config(bg="#c6c6c6"))

        self.listening_for_key = False
        self.update_settings()
        self.root.after(100, self.refresh_slider)

    def draw_tiled_background(self):
        tile_colors = ["#926c4d", "#ad9f8e", "#593d29", "#79553a"]
        for x in range(0, 320, 32):
            for y in range(0, 260, 32):
                color = random.choice(tile_colors)
                self.canvas.create_rectangle(x, y, x+32, y+32, fill=color, outline=color)

    def refresh_slider(self):
        self.volume_slider.draw_slider()
        self.update_settings()
        self.root.after(100, self.refresh_slider)

    def add_label(self, text, y):
        label = tk.Label(self.root, text=text, bg="gray24", fg="white", font=self.block_font)
        self.canvas.create_window(160, y, window=label)

    def start_hotkey_capture(self):
        if self.listening_for_key:
            return
        self.listening_for_key = True
        self.hotkey_button.config(text="Press any key...")
        self.root.bind("<Key>", self.capture_key)

    def capture_key(self, event):
        key_name = event.keysym.lower()
        self.hotkey_var.set(key_name)
        self.hotkey_button.config(text=key_name.upper())
        self.root.unbind("<Key>")
        self.listening_for_key = False
        self.update_settings()

    def update_settings(self):
        settings = {
            "volume": self.volume_var.get(),
            "voice": self.voice_var.get(),
            "hotkey": self.hotkey_var.get()
        }
        self.on_settings_change(settings)

# Example usage
def on_settings_change(settings):
    print(settings)

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsUI(root, on_settings_change)
    root.mainloop()
