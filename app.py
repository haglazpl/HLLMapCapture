from gui import App
from config import ConfigManager
from hll_detection import HLLDetectionManager
from map_detection import MapDetectionManager
import pygetwindow as gw


class AppController:
    def __init__(self):
        """Initialize the application logic, configuration, and detection managers."""
        self.config_manager = ConfigManager()
        self.screenshot_folder = self.config_manager.get("screenshot_folder", ".")  # Default to exe location
        self.cooldown = self.config_manager.get("cooldown", 10)  # Default to 10 sec
        self.detection_key = self.config_manager.get("detection_key", "m").lower()  # Default to "m"

        self.map_detection_manager = MapDetectionManager(cooldown=self.cooldown)
        self.hll_detection_manager = HLLDetectionManager(
            on_map_key_callback=self.toggle_map_detection,
            detection_key=self.detection_key
        )

    def get_screenshot_folder(self):
        """Return the screenshot folder path from config."""
        return self.screenshot_folder

    def set_screenshot_folder(self, folder_path):
        """Update the screenshot folder in config."""
        self.screenshot_folder = folder_path
        self.config_manager.set("screenshot_folder", folder_path)

    def get_hll_window(self):
        """Find and return the HLL window."""
        try:
            for window in gw.getWindowsWithTitle("Hell Let Loose"):
                if window.isActive or window.isMaximized:
                    return window
        except Exception:
            return None

    def toggle_map_detection(self):
        """Toggle the map detection feature."""
        self.map_detection_manager.toggle_detection(self.screenshot_folder, self.get_hll_window)

    def toggle_hll_detection(self, start_button):
        """Toggle HLL detection (passed to GUI)."""
        self.hll_detection_manager.toggle_detection(start_button)


def main():
    """Main entry point of the application."""
    app_controller = AppController()
    app = App(app_controller)
    app.create_gui()


if __name__ == "__main__":
    main()
