import threading
import time
import pyautogui
from pynput import keyboard

# Adjustable Settings
CLICK_INTERVAL = 0.5  # Seconds between clicks
MOUSE_BUTTON = 'left' # 'left' or 'right'
START_STOP_KEY = keyboard.Key.f6

class AutoClicker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                pyautogui.click(button=MOUSE_BUTTON)
                time.sleep(CLICK_INTERVAL)
            time.sleep(0.1)

# Initialize the clicker thread
click_thread = AutoClicker()
click_thread.start()

def on_press(key):
    if key == START_STOP_KEY:
        if click_thread.running:
            click_thread.stop_clicking()
            print("Status: Stopped")
        else:
            click_thread.start_clicking()
            print("Status: Running...")
    elif key == keyboard.Key.esc:
        click_thread.exit()
        listener.stop()

# Listen for the hotkey globally
with keyboard.Listener(on_press=on_press) as listener:
    print(f"Press {START_STOP_KEY} to Start/Stop. Press ESC to quit.")
    listener.join()
