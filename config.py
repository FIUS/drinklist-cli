import pathlib
import json
import argparse

class Config(object):
    def __init__(self, config_file_path):
        self.config_params = {}
        self.config_path = config_file_path
        self.config = {}
        self.tmp_config = {}
        self.did_read_config = False

    def read_config(self):
        if self.config_path.exists():
            with self.config_path.open() as f:
                self.config = json.load(f)
        self.did_read_config = True

    def write_config(self):
        with self.config_path.open(mode='w') as f:
            json.dump(self.config, f)

    def add_config_parameter(self, name, initializer, type=str, parameter=None,
                             help=""):
        if parameter is None:
            parameter = '-{}'.format(name)
        self.config_params[name] = {'name': name, 'type': type, 'parameter': parameter, 'help':help,
                                    'initializer': initializer}

    def add_args(self, parser):
        for cp in self.config_params.values():
            parser.add_argument(cp['parameter'], dest=cp['name'], type=cp['type'], help=cp['help'])

    def parse_args(self, args):
        for cp in self.config_params.values():
            if cp['name'] in args.__dict__ and args.__dict__[cp['name']] is not None:
                self.tmp_config[cp['name']] = args.__dict__[cp['name']]

    def set_config_file(self, path):
        self.config_path = path
        self.read_config()

    def __getitem__(self, key):
        if not self.did_read_config:
            self.read_config()
        if key in self.tmp_config and self.tmp_config[key] is not None:
            return self.tmp_config[key]
        elif key in self.config and self.config[key] is not None:
            return self.config[key]
        else:
            self.config[key] = self.config_params[key]['initializer']()
            self.write_config()
            return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        self.write_config()
