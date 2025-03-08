import json
import os

CONFIG_FILE = "config.json"


class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        """Load config from a JSON file, providing defaults if keys are missing."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_config(self):
        """Save current config to file."""
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.config, file, indent=4)

    def get(self, key, default=None):
        """Retrieve a value from config, return default if key is missing."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Update a value in config and save it."""
        self.config[key] = value
        self.save_config()
