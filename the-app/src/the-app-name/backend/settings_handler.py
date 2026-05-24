import json
import os

SETTINGS_FILE = "settings.json"


class SettingsManager:

    def __init__(self):

        self.settings = {
            "text_speed": "Normal"
        }

        self.load_settings()

    def set_text_speed(self, speed):
        self.settings["text_speed"] = speed

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                loaded = json.load(file)
                self.settings.update(loaded)