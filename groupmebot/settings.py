import json
import sys
import json
from .const import CONFIG_FILE, EXCEPTIONS


class SettingsException(Exception):
    """Custom exception SettingsException"""


class Settings(object):
    """Settings to encapsulate connection values"""

    def __init__(self, file=None, **data):
        # Values needed to operate
        self.essential = {
            "accessToken": None
        }

        # Non essentials. TODO: Fill these in
        self.properties = {}

        # Load data from config
        if file:
            self.load_config(file=file)

        # Overwrite from file what's passed in
        self._load_essentials(data)
        self._load_properties(data)

    @property
    def valid(self):
        return len([0 for x in self.essential.values() if x is None]) == 0

    @property
    def accessToken(self):
        return self.essential["accessToken"]

    def _generate_json(self):
        merged = self.essential.copy()
        merged.update(self.properties)
        return json.dumps(merged)

    def _load_essentials(self, data):
        for key, value in data.items():
            if key in self.essential:
                self.essential[key] = value

        if not self.valid:
            print("Essentials not fully set")
            # Set up some logger in long run
            # logger.warning or some shit

    def _load_properties(self, data):
        for key, value in data.items():
            if key in self.properties:
                self.properties[key] = value

    def load_config(self, file=CONFIG_FILE):
        try:
            json_data = open(file).read()
            data = json.loads(json_data)

            # Load from JSON
            self._load_essentials(data)
            self._load_properties(data)

        except IOError as e:
            raise SettingsException(EXCEPTIONS.BAD_CONFIG)

    def save_config(self, file=CONFIG_FILE):
        try:
            with open(file, 'w+') as f:
                f.write(self._generate_json())
        except IOError as e:
            raise SettingsException(EXCEPTIONS.BAD_CONFIG_SAVE)
