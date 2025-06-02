import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MinecraftSlider(tk.Canvas):
    def __init__(self, master, variable, from_=0, to=1, **kwargs):
        super().__init__(master, width=200, height=24, bg="#8b5a2b", highlightthickness=0, **kwargs)
        self.variable = variable
        self.from_ = from_
        self.to = to
        self.slider_pos = 0
        self.slider = self.create_rectangle(0, 0, 0, 0, fill="#d7c297", outline="#3a2c1e")
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
        self.slider_pos = pos
        self.coords(self.slider, pos - 10, 4, pos + 10, 20)

class SettingsUI:
    def __init__(self, root, on_settings_change):
        self.on_settings_change = on_settings_change
        self.root = root
        self.root.title("Mob TTS Assist")
        self.root.geometry("320x260")
        self.root.resizable(False, False)

        try:
            self.block_font = ("Minecraftia", 10)
        except:
            self.block_font = ("Courier", 10, "bold")

        # Background tiling
        self.bg_tile = ImageTk.PhotoImage(Image.open("C:/Users/vaibh/Downloads/brown_tile.png").resize((32, 32)))
        self.canvas = tk.Canvas(root, width=320, height=260)
        self.canvas.pack(fill="both", expand=True)
        for x in range(0, 320, 32):
            for y in range(0, 260, 32):
                self.canvas.create_image(x, y, anchor="nw", image=self.bg_tile)

        self.ui_frame = tk.Frame(root, bg="#a07e4d")
        self.canvas.create_window(0, 0, anchor="nw", window=self.ui_frame, width=320, height=260)

        self.volume_var = tk.DoubleVar(value=1.0)
        self.voice_var = tk.StringVar(value="default")
        self.hotkey_var = tk.StringVar(value="f8")

        self.add_label("Volume")
        self.volume_slider = MinecraftSlider(self.ui_frame, self.volume_var, from_=0, to=1)
        self.volume_slider.pack(pady=5)

        self.add_label("Voice")
        self.voice_dropdown = ttk.Combobox(self.ui_frame, textvariable=self.voice_var,
                                           values=["default", "female", "male"], state="readonly", font=self.block_font)
        self.voice_dropdown.pack(fill='x', padx=20)
        self.voice_dropdown.bind("<<ComboboxSelected>>", lambda _: self.update_settings())

        self.add_label("Set Hotkey (click then press key)")
        self.hotkey_button = tk.Label(self.ui_frame, text=self.hotkey_var.get().upper(),
                                      bg="#c6a664", font=self.block_font, bd=3,
                                      relief="raised", padx=10, pady=4)
        self.hotkey_button.pack(pady=5)
        self.hotkey_button.bind("<Button-1>", lambda e: self.start_hotkey_capture())
        self.hotkey_button.bind("<Enter>", lambda e: self.hotkey_button.config(bg="#e7d08c"))
        self.hotkey_button.bind("<Leave>", lambda e: self.hotkey_button.config(bg="#c6a664"))

        self.listening_for_key = False
        self.update_settings()
        self.root.after(100, self.refresh_slider)

    def refresh_slider(self):
        self.volume_slider.draw_slider()
        self.update_settings()
        self.root.after(100, self.refresh_slider)

    def add_label(self, text):
        label = tk.Label(self.ui_frame, text=text, bg="#a07e4d", fg="white", font=self.block_font)
        label.pack(pady=4)

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
