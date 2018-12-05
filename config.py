# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
        parser.add_argument('-config', dest='config_path', type=str, help='The config file')
        for cp in self.config_params.values():
            parser.add_argument(cp['parameter'], dest=cp['name'], type=cp['type'], help=cp['help'])

    def parse_args(self, args):
        if 'config_path' in args.__dict__ and args.__dict__['config_path'] is not None:
            self.config_path = pathlib.Path(args.__dict__['config_path']).expanduser()
            self.read_config()
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
