import threading
import time
import pyautogui
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw

# Settings
CLICK_INTERVAL = 0.5
MOUSE_BUTTON = 'left'
START_STOP_KEY = keyboard.Key.f6

class AutoClicker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.program_running = True
        self.daemon = True # Ends thread when main program exits

    def run(self):
        while self.program_running:
            while self.running:
                pyautogui.click(button=MOUSE_BUTTON)
                time.sleep(CLICK_INTERVAL)
            time.sleep(0.1)

click_thread = AutoClicker()
click_thread.start()

def on_press(key):
    if key == START_STOP_KEY:
        click_thread.running = not click_thread.running
    elif key == keyboard.Key.esc:
        stop_program()

def stop_program(icon=None):
    click_thread.program_running = False
    if icon:
        icon.stop()
    listener.stop()

# Create a simple 64x64 icon image (a blue square)
def create_image():
    image = Image.new('RGB', (64, 64), color='blue')
    d = ImageDraw.Draw(image)
    d.rectangle((16, 16, 48, 48), fill='white')
    return image

# Define Tray Menu
menu = pystray.Menu(
    pystray.MenuItem("Quit", stop_program)
)

icon = pystray.Icon("AutoClicker", create_image(), "AutoClicker (F6 to toggle)", menu)

# Start keyboard listener in its own thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run the system tray icon (this loop blocks the main thread)
icon.run()
