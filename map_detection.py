import time
import threading
import logging
import os
import pyautogui
from datetime import datetime

logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class MapDetectionManager:
    def __init__(self, cooldown):
        self.map_detection_running = False
        self.last_screenshot_time = 0
        self.cooldown = cooldown

    def is_map_visible(self, map_image_path):
        try:
            location = pyautogui.locateOnScreen(map_image_path, confidence=0.5)
            return location is not None
        except Exception as e:
            logging.error(f"Error detecting image: {e}")
            return False

    def validate_map_screenshot(self):
        logging.info("Validating map screenshot...")
        return True  # Implement further validation if needed

    def take_screenshot(self, screenshot_folder, region=None):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(screenshot_folder, f"{timestamp}.jpg")
        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        screenshot.save(screenshot_path)
        return screenshot_path

    def run_map_detection(self, screenshot_folder, get_hll_window):
        map_image_path = "Icon/reference.png"
        logging.info("Monitoring screen for map detection...")
        while self.map_detection_running:
            current_time = time.time()
            hll_window = get_hll_window()
            if hll_window and self.is_map_visible(map_image_path) and (
                    current_time - self.last_screenshot_time > self.cooldown):
                if self.validate_map_screenshot():
                    region = (hll_window.left, hll_window.top, hll_window.width, hll_window.height)
                    screenshot_path = self.take_screenshot(screenshot_folder, region=region)
                    logging.info(f"Screenshot saved: {screenshot_path}")
                    self.last_screenshot_time = current_time

    def toggle_detection(self, screenshot_folder, get_hll_window):
        if self.map_detection_running:
            self.map_detection_running = False
            logging.info("Map detection stopped.")
        else:
            self.map_detection_running = True
            threading.Thread(target=self.run_map_detection, args=(screenshot_folder, get_hll_window),
                             daemon=True).start()
            logging.info("Map detection started.")
