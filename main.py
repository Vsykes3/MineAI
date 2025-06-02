import tkinter as tk
from threading import Thread, Event
import time

from ui import SettingsUI
from utils.screen_capture import capture_screen
from utils.detect import detect_mob
from utils.tts import speak, update_voice_settings
from hotkeys import HotkeyManager


settings = {
    "volume": 1.0,
    "voice": "default",
    "hotkey": "f8"
}


last_spoken = ""
immediate_detection = False
detection_event = Event()
hotkey_listener = None


def on_hotkey_pressed():
    global immediate_detection
    immediate_detection = True
    detection_event.set()  # interrupt wait to detect immediately

def apply_settings(new_settings):
    global settings, hotkey_listener
    settings.update(new_settings)
    update_voice_settings(settings["volume"], settings["voice"])

    # Re-register hotkey if changed
    if hotkey_listener:
        hotkey_listener.stop()
    hotkey_listener = HotkeyManager(on_hotkey_pressed, toggle_key=settings["hotkey"])

def run_detection_loop():
    global immediate_detection
    while True:
        if immediate_detection:
            print("[HOTKEY] Triggered manual detection")
            img = capture_screen()
            mob = detect_mob(img)
            if mob:
                speak(mob)
                last_spoken = mob
            immediate_detection = False
            detection_event.clear()
        else:
            if detection_event.wait(timeout=5):
                detection_event.clear()
                continue
            img = capture_screen()
            mob = detect_mob(img)
            print(f"[AUTO] Detected dangerous mob: {mob}")
            speak(mob)

if __name__ == "__main__":
    root = tk.Tk()
    ui = SettingsUI(root, apply_settings)

    hotkey_listener = HotkeyManager(on_hotkey_pressed, toggle_key=settings["hotkey"])
    Thread(target=run_detection_loop, daemon=True).start()

    root.mainloop()
