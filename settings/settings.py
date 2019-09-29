# Settings file for the library

import yaml

class Settings():
    def __init__(self):
        self.token = None
        self.load_settings()


    def load_settings(self):
        with open("settings.yml", "r") as settings_file:
            config = yaml.safe_load(settings_file)
            for k,v in config.items():
                setattr(self, k, v)
