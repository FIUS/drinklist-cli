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

class ParameterStore(object):
    def __init__(self, file_paths, path_parameter=None, path_parameter_help=""):
        """Creates a new parameter store object.

        Parameters:
        file_paths -- a list of paths to be checked in order
        path_parameter -- cmdline parameter name for specifying the store file
        path_parameter_help -- help for the cmdline parameter for the store file
        """
        self.params = {}
        self.paths = file_paths
        self.values = {}
        self.tmp_values = {}
        self.did_read = False
        self.path_parameter = path_parameter
        self.path_parameter_help = path_parameter_help

    def load(self):
        """Read the parameters from the first existing file"""
        for path in self.paths:
            if path.exists():
                with path.open() as f:
                    self.values = json.load(f)
                break
        self.did_read = True

    def dump(self):
        """Write the parameters to the first existing file or the first file.

        Goes throgh list of files and is one of them exists, overwrites that.
        Else creates and writes to the first existing file.
        """
        res_path = None
        for path in self.paths:
            if path.exists():
                res_path = path
                break
        if res_path is None:
            res_path = self.paths[0]
        res_path.parent.mkdir(0o700,True,True)
        with res_path.open(mode='w+') as f:
            json.dump(self.values, f, indent=4)

    def reset_parameter(self, name):
        """Removes the value for the given parameter.

        Parameters:
        name -- the name of the parameter
        """
        if name in self.values:
            self.values.pop(name)
        if name in self.tmp_values:
            self.tmp_values.pop(name)

    def add_parameter(self, name, initializer, type=str, parameter=None,
                      help="", non_cmd=False):
        """Adds the given parameter.

        Parameters:
        name -- the name of the parameter
        initializer -- a nullary function to initialize this parameter on demand
        type -- the type of this parameter, default str
        parameter -- the cmdline parameter for this parameter
        help -- help text for this parameter
        non_cmd -- if True, do not add a cmdline parameter
        """
        if parameter is None:
            parameter = '-{}'.format(name)
        self.params[name] = {'name': name, 'type': type, 'parameter': parameter, 'help':help,
                             'initializer': initializer, 'non_cmd': non_cmd}

    def init_argparse_parser(self, parser):
        """Add cmdline parameters to argparse parser

        Parameters:
        parser -- an argparse parser. This function will call add_argument on this parser
        """
        if not (self.path_parameter is None):
            parser.add_argument('-{}'.format(self.path_parameter),
                                dest=self.path_parameter,
                                type=str,
                                help=self.path_parameter_help)
        for cp in self.params.values():
            if not cp['non_cmd']:
                parser.add_argument(cp['parameter'], dest=cp['name'], type=cp['type'], help=cp['help'])

    def parse_argparse_results(self, args):
        """Read parameters from argparse results

        Parameters:
        args -- the result of argparse
        """
        if self.path_parameter in args.__dict__ and args.__dict__[self.path_parameter] is not None:
            self.set_files([pathlib.Path(args.__dict__[self.path_parameter]).expanduser()])
            self.load()
        for cp in self.params.values():
            if cp['name'] in args.__dict__ and args.__dict__[cp['name']] is not None:
                self.tmp_values[cp['name']] = args.__dict__[cp['name']]

    def set_files(self, paths):
        """Set the files to be used. This calls load internally.

        Parameters:
        paths -- a list of paths to be checked in order
        """
        self.paths = paths
        self.load()

    def __getitem__(self, key):
        if not self.did_read:
            self.load()
        if key in self.tmp_values and self.tmp_values[key] is not None:
            return self.tmp_values[key]
        elif key in self.values and self.values[key] is not None:
            return self.values[key]
        else:
            self.values[key] = self.params[key]['initializer']()
            self.dump()
            return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value
        self.dump()
