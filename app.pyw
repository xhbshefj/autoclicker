import threading
import time
import pyautogui
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw
import tkinter as tk

# Settings
CLICK_INTERVAL = 0.5
MOUSE_BUTTON = 'left'
START_STOP_KEY = keyboard.Key.f6

class AutoClicker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.program_running = True
        self.daemon = True 

    def run(self):
        while self.program_running:
            if self.running:
                pyautogui.click(button=MOUSE_BUTTON)
                time.sleep(CLICK_INTERVAL)
            else:
                time.sleep(0.1)

click_thread = AutoClicker()
click_thread.start()

# --- GUI Logic ---
def show_window(icon=None, item=None):
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw() # Hides window but keeps process alive

def quit_program(icon=None, item=None):
    click_thread.program_running = False
    if icon:
        icon.stop()
    root.destroy()

# Keyboard listener logic
def on_press(key):
    if key == START_STOP_KEY:
        click_thread.running = not click_thread.running
    elif key == keyboard.Key.esc:
        quit_program(icon)

# --- Tray Icon Setup ---
def create_image():
    image = Image.new('RGB', (64, 64), color='blue')
    d = ImageDraw.Draw(image)
    d.rectangle((16, 16, 48, 48), fill='white')
    return image

menu = pystray.Menu(
    pystray.MenuItem("Show Window", show_window),
    pystray.MenuItem("Quit", quit_program)
)
icon = pystray.Icon("AutoClicker", create_image(), "AutoClicker (F6 to toggle)", menu)

# --- Main Window (Tkinter) ---
root = tk.Tk()
root.title("AutoClicker Control")
root.geometry("300x150")

# Handle the "X" button to minimize to tray instead of closing
root.protocol('WM_DELETE_WINDOW', hide_window)

label = tk.Label(root, text="AutoClicker is Active\nPress F6 to Start/Stop", pady=20)
label.pack()

btn_hide = tk.Button(root, text="Minimize to Tray", command=hide_window)
btn_hide.pack()

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run Tray Icon in background thread
icon.run_detached()

# Start GUI loop
root.mainloop()
