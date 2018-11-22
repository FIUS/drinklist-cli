import pathlib
import json

class Config(object):

    def __init__(self, path):
        """
        Initializes the Configuration 
        """
        self.config_path = path
        self.config = {}
        self.read_config()

    def read_config(self):
        if self.config_path.exists():
            with self.config_path.open() as f:
                self.config = json.load(f)

    def write_config(self):
        with self.config_path.open(mode='w') as f:
            json.dump(self.config, f)

    def init_value(self, key, initializer):
        if not key in self.config:
            self.config[key] = initializer()
            self.write_config()

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value