import time
import threading
import logging
import psutil
from tkinter import messagebox
from pynput import keyboard

logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class HLLDetectionManager:
    def __init__(self, on_map_key_callback=None, detection_key="m"):
        """Initialize HLL detection manager with configurable keybinding."""
        self.running = False
        self.listener = None
        self.on_map_key_callback = on_map_key_callback
        self.detection_key = detection_key.lower()

    def is_hll_running(self):
        """Check if Hell Let Loose is running."""
        for process in psutil.process_iter(['name']):
            if process.info['name'] == "HLL-Win64-Shipping.exe":
                return True
        return False

    def run_detection(self, start_button):
        """Check if HLL is running and monitor the process."""
        logging.info("Monitoring HLL process...")
        if not self.is_hll_running():
            messagebox.showwarning("Warning", "HLL process not detected! Please start the game.")
            logging.warning("HLL process not detected!")
            self.running = False
            start_button.config(text="Start", bootstyle="danger")
            return

        while self.running:
            if not self.is_hll_running():
                self.running = False
                logging.info("HLL process stopped.")
                messagebox.showinfo("Info", "HLL process stopped. Detection halted.")
                start_button.config(text="Start", bootstyle="danger")
                self.stop_key_listener()
                break
            time.sleep(2)

    def toggle_detection(self, start_button):
        """Start or stop detection."""
        if self.running:
            self.running = False
            logging.info("HLL detection stopped.")
            start_button.config(text="Start", bootstyle="danger")
            self.stop_key_listener()
        else:
            self.running = True
            logging.info("HLL detection started.")
            threading.Thread(target=self.run_detection, args=(start_button,), daemon=True).start()
            start_button.config(text="Active", bootstyle="success")
            self.start_key_listener()

    def on_key_press(self, key):
        """Handle key press events and trigger map detection if the correct key is pressed."""
        try:
            if key.char.lower() == self.detection_key and self.running:
                logging.info(f"'{self.detection_key.upper()}' key pressed. Delegating to map detection.")
                if self.on_map_key_callback:
                    self.on_map_key_callback()
        except AttributeError:
            pass  # Ignore non-character keys

    def start_key_listener(self):
        """Start listening for the configured key."""
        if self.listener is None or not self.listener.running:
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            logging.info(f"Key listener started (Listening for '{self.detection_key.upper()}').")

    def stop_key_listener(self):
        """Stop key listening."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
            logging.info("Key listener stopped.")
