from pynput import keyboard

class HotkeyManager:
    def __init__(self, callback, toggle_key='f8'):
        self.toggle_key = toggle_key.lower()
        self.callback = callback
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            # For letter/number keys
            if hasattr(key, 'char') and key.char and key.char.lower() == self.toggle_key:
                self.callback()
        except AttributeError:
            # For special keys like f8, etc.
            if hasattr(key, 'name') and key.name == self.toggle_key:
                self.callback()

    def stop(self):
        self.listener.stop()
