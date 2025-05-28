import tkinter as tk
from tkinter import ttk

class SettingsUI:
    def __init__(self, root, on_settings_change):
        self.on_settings_change = on_settings_change
        self.root = root

        root.title("Mob TTS Assist")
        root.geometry("320x260")

        self.volume_var = tk.DoubleVar(value=1.0)
        self.voice_var = tk.StringVar(value="default")
        self.hotkey_var = tk.StringVar(value="f8")

        # Volume slider
        ttk.Label(root, text="Volume").pack(pady=5)
        ttk.Scale(root, from_=0, to=1, variable=self.volume_var,
                  orient="horizontal", command=lambda _: self.update_settings()).pack(fill='x', padx=10)

        # Voice dropdown only
        ttk.Label(root, text="Voice").pack(pady=5)
        self.voice_dropdown = ttk.Combobox(root, textvariable=self.voice_var,
                                           values=["default", "female", "male"], state="readonly")
        self.voice_dropdown.pack(fill='x', padx=10)
        self.voice_dropdown.bind("<<ComboboxSelected>>", lambda _: self.update_settings())

        # Hotkey binding button
        ttk.Label(root, text="Set Hotkey (click button, press a key)").pack(pady=10)
        self.hotkey_button = ttk.Button(root, text=self.hotkey_var.get().upper(), command=self.start_hotkey_capture)
        self.hotkey_button.pack(pady=5)

        self.listening_for_key = False

        self.update_settings()

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
