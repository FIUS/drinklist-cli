#!/usr/bin/env python3

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

import requests
import json
import getpass
import pathlib
import parameter_store
from ppformat import pp
import ppformat
import sys
import subprocess
import levenshtein as LD
import copy
import appdirs
from utils import y_or_n_pred, find_minimizing_with_rating

cfg = None
cache = None
interactive = True

def get_login_token():
    """Get the login token"""
    global cache
    refresh_token()
    return cache['token']

def refresh_token():
    """Fetch a new login token"""
    global cfg, cache
    r = requests.post(cfg['url'] + "/auth/login", json={'password': cfg['pw']})
    if r.status_code == 403:
        print("Failed to get login token: wrong password.", file=sys.stderr)
        cfg.reset_parameter('pw')
        refresh_token()
        return
    if not r.ok:
        print("Failed to get token: " + str(r.status_code) + ": " + r.text, file=sys.stderr)
        sys.exit(1)
    json_result = json.loads(r.text)
    cache['token'] = json_result[u'token']

def get(suburl, retry=True):
    """HTTP GET the given API suburl and parse the result as json"""
    global cfg, cache
    r = requests.get(cfg["url"] + suburl, headers={'X-Auth-Token': cache['token']})
    if r.status_code == 403 and retry:
        refresh_token()
        return get(suburl, False)
    if not r.ok:
        print("API returned error " + str(r.status_code) + ": " + r.text, file=sys.stderr)
    return json.loads(r.text)

def get_beverages():
    """Get available beverages"""
    return get("/beverages")

def get_users():
    """Get all users"""
    return get("/users")

def expand_alias(drink):
    """Replace alias drink names by their real names"""
    aliases = cfg["aliases"]
    if drink in aliases.keys():
        return aliases[drink]
    else:
        return drink

def add_alias(alias, drink):
    """Add alias as an alias for drink"""
    cfg["aliases"][alias] = drink
    cfg.dump()

def del_alias(alias):
    """Remove the alias alias"""
    cfg["aliases"].pop(alias)
    cfg.dump()

def get_aliases():
    """Get all aliases"""
    return cfg["aliases"]

def undo():
    """Delete the last drink ordered"""
    order = get("/orders/"+cfg["user"])[0] # assumes result is ordered by timestamp
    r = requests.delete(cfg["url"] + "/orders/" + order["id"],
                        headers={'X-Auth-Token': cache['token']})
    if r.ok:
        print("Order of {} for {} deleted. (Response: {})"
              .format(order["reason"], order["user"],
                      r.text))
    else:
        print("Error")

def order_drink(drink, retry=True):
    """Order the drink drink."""
    global cfg, cache, interactive
    drink = expand_alias(drink)
    r = requests.post(cfg["url"] + "/orders",
                      headers={'X-Auth-Token': cache['token']},
                      params={'user': cfg['user'], 'beverage': drink})
    if r.status_code == 403 and retry:
        refresh_token()
        return order_drink(drink, retry=False)

    if not r.ok:
        if not r.text == "Unknown beverage":
            print(str(r.status_code) + ": " + r.text, file=sys.stderr)
            sys.exit(1)

        def rating_fn(other):
            ld = LD.generalized_distance(drink, other["name"],
                                         5, 10,
                                         lambda x,y: 10 if x.lower()!=y.lower() else 1,
                                         1)
            return (ld, len(other))

        (correctDrink, rating) = find_minimizing_with_rating(get_beverages(), rating_fn)
        correctName = correctDrink["name"]

        if rating <= (len(correctName), len(drink)) or (interactive and y_or_n_pred("Did you mean {}".format(correctName), False)):
            print("Corrected {} to {}.".format(drink, correctName))
            order_drink(correctName)
        else:
            print("Unknown beverage")
    else:
        print(r.text)

if __name__ == '__main__':
    import argparse
    parent_parser = argparse.ArgumentParser(add_help = False)
    parent_parser.add_argument('-format', choices=['text', 'json'], help='Output format')
    parent_parser.add_argument('-sort-by', type=str, default=None, help='Sort the output by the given column (if possible)')
    parent_parser.add_argument('-columns', type=str, nargs='+', default=None, help='The columns to show (if applicable)')
    parent_parser.add_argument('-sort-descending', action='store_true', help='Sort items descending')
    parent_parser.add_argument('-sort-ascending', action='store_true', help='Sort items ascending')
    parent_parser.add_argument('-b', dest='noninteractive', action='store_true', help="Noninteractive mode. Will not ask the user anything.")

    cfg = parameter_store.ParameterStore(
        [pathlib.Path(appdirs.user_config_dir("drinklist_cli", "FIUS")).joinpath("config.json"),
         pathlib.Path("~/.drinklist").expanduser()],
        "config_file",
        "The config file to use")
    cache = parameter_store.ParameterStore(
        [pathlib.Path(appdirs.user_cache_dir("drinklist_cli", "FIUS")).joinpath("cache.json")],
        "cache_file",
        "The cache file to use")
    def get_pw():
        if cfg['password_command'] is not None:
            return subprocess.check_output(cfg['password_command'], shell=True).decode("utf-8").splitlines()[0]
        else:
            return getpass.getpass()
    def store_pw_pred():
        return (cfg['password_command'] is None) and y_or_n_pred("Store the password in plaintext in the config file")
    cfg.add_parameter('url', lambda: "https://fius.informatik.uni-stuttgart.de/drinklist/api",
                      help='The API url of the drinklist', parameter='--url')
    cfg.add_parameter('pw', get_pw,
                      store_if=store_pw_pred,
                      help='The drinklist password')
    cfg.add_parameter('user', lambda: (input("Username: ") if interactive else sys.exit(1)),
                      help='Your drinklist username')
    cfg.add_parameter('aliases', lambda: {},
                      help='The aliases defined for drinks',
                      non_cmd=True)
    cfg.add_parameter('password_command', lambda: None,
                      help='The command to run to get the drinklist password')
    cache.add_parameter('token', lambda: get_login_token(),
                        help='The login token to use.')
    cfg.init_argparse_parser(parent_parser)
    cache.init_argparse_parser(parent_parser)

    parser = argparse.ArgumentParser(parents = [copy.deepcopy(parent_parser)])

    for action in parent_parser._actions:
      action.dest = "sub_" + action.dest

    commands = parser.add_subparsers(title='commands',
                                     metavar='command',
                                     dest='command',
                                     description='The command to run')
    list_parser = commands.add_parser('list', help='List all available beverages.', parents = [parent_parser])
    list_parser.add_argument('-regex', help='Filter drinks by regex.', type=str, default=None)

    drink_parser = commands.add_parser('drink', help='Order a drink.', parents = [parent_parser])
    order_parser = commands.add_parser('order', help='Alias for drink.', parents = [parent_parser])

    def init_drink_parser(drink_parser):
        drink_parser.add_argument('drink', type=str, help='The drink to order. If multiple arguments are given, they are joined together with spaces',
nargs='+')
    init_drink_parser(drink_parser)
    init_drink_parser(order_parser)

    commands.add_parser('users', help='List all registered users.')
    balance_parser = commands.add_parser('balance', help='Get the balance.', parents = [parent_parser])
    balance_parser.add_argument('-all', action='store_true',
                                help='show balance for all users')

    history_parser = commands.add_parser('history', help='Get the history.', parents = [parent_parser])
    history_parser.add_argument('-all', action='store_true',
                                help='Show history for all users')

    commands.add_parser('refresh_token',
                        help='Get a new authentication token for the drinklist.', parents = [parent_parser])

    alias_parser = commands.add_parser('alias', help='Manage aliases for drinks')
    alias_cmds = alias_parser.add_subparsers(title='alias commands',
                                             metavar='aliascmd',
                                             dest='aliascmd',
                                             description='The alias command')
    alias_list_parser = alias_cmds.add_parser('list', help='List all defined aliases', parents = [parent_parser])
    alias_delete_parser = alias_cmds.add_parser('delete', help='Remove all aliases')
    alias_delete_parser.add_argument('alias', type=str, help='The alias to delete')
    alias_define_parser = alias_cmds.add_parser('set', help='Add a new alias')
    alias_define_parser.add_argument('alias', type=str, help='The alias to add')
    alias_define_parser.add_argument('drink', type=str, help='The drink the alias should point to')

    commands.add_parser('undo', help="Undo the last drink ordered for user")

    commands.add_parser('license', help='Show the license for this program')

    help_parser = commands.add_parser('help', help='Show this help.')
    help_parser.add_argument('subject', type=str, nargs='*', help='The command to show help for')
    args = parser.parse_args()
    interactive = not args.noninteractive

    for arg in args.__dict__:
        if(arg.startswith("sub_")):
            orig = arg[4:]
            default = [action.default for action in parser._actions if action.dest == orig][0]
            if args.__dict__[arg] != default:
              args.__dict__[orig] = args.__dict__[arg]

    cfg.parse_argparse_results(args)
    cache.parse_argparse_results(args)

    formatter = None
    if args.format == 'json':
        def formatter(x): return print(json.dumps(x))
    else:
        if args.columns is not None:
            def formatter(x): return print(
                ppformat.format_obj_table(x, args.columns))
        else:
            def formatter(x): return print(pp(x))

    sort_descending = False
    sort_by = args.sort_by
    if args.command == 'history' and sort_by is None:
            sort_by = 'timestamp'
    if args.sort_descending and args.sort_ascending:
        print("Can't sort ascending and descending")
        exit(1)
    elif args.sort_ascending:
        sort_descending = False
    elif args.sort_descending:
        sort_descending = True
    if sort_by is not None:
        inner_formatter = formatter

        def real_formatter(x):
            x.sort(key=lambda y: y[sort_by], reverse=sort_descending)
            return inner_formatter(x)
        formatter = real_formatter

    if args.command in [None, 'help']:
        if args.command is None or args.subject == []:
          parser.print_help()
        else:
          args.subject = " ".join(args.subject)
          if args.subject == 'list':
              list_parser.print_help()
          elif args.subject == 'help':
              help_parser.print_help()
          elif args.subject in ['drink', 'order']:
              drink_parser.print_help()
          elif args.subject == 'balance':
              balance_parser.print_help()
          elif args.subject == 'history':
              history_parser.print_help()
          elif args.subject == 'alias':
            alias_parser.print_help()
          elif args.subject.startswith('alias '):
              if args.subject.startswith('delete', 6):
                  alias_delete_parser.print_help()
              elif args.subject.startswith('set', 6):
                  alias_define_parser.print_help()
              elif args.subject.startswith('', 6):
                  alias_list_parser.print_help()
          else:
              print("There is no help page for {}".format(args.subject))
    elif args.command == 'list':
        beverages = get_beverages()
        if args.regex is not None:
            import re
            p = re.compile(args.regex, re.IGNORECASE if args.regex == args.regex.lower() else re.ASCII)
            beverages = [b for b in beverages if p.search(b['name']) is not None]
        formatter(beverages)
    elif args.command in ['order', 'drink']:
        order_drink(' '.join(args.drink))
    elif args.command == 'balance':
        if args.all:
            res = []
            for user in get_users():
                res += [get("/users/" + user)]
            formatter(res)
        else:
            formatter([get("/users/" + cfg['user'])])
    elif args.command == 'history':
        if args.all:
            formatter(get("/orders"))
        else:
            formatter(get("/orders/" + cfg['user']))
    elif args.command == 'users':
        formatter(get_users())
    elif args.command == 'refresh_token':
        refresh_token()
    elif args.command == 'undo':
        undo()
    elif args.command == 'alias':
        if args.aliascmd == 'list':
            formatter(get_aliases())
        elif args.aliascmd == 'delete':
            del_alias(args.alias)
        elif args.aliascmd == 'set':
            add_alias(args.alias, args.drink)
        else:
            alias_parser.print_help()
    elif args.command == 'license':
        root = pathlib.Path(__file__).absolute().parent;
        for filename in [
                pathlib.Path("/usr/share/doc/drinklist-cli/LICENSE"),
                root.joinpath("LICENSE"),
                root.joinpath("COPYING")
                ]:
            if filename.exists():
                with open(filename) as file:
                    for line in file.readlines():
                        print(line, end='')
                sys.exit(0)
        print("License file missing. Downloading from gnu.org...")
        r = requests.get("https://www.gnu.org/licenses/gpl-3.0.txt")
        if r.ok:
            print(r.text)
        else:
            print("Failed. This Program is licensed under GPLv3, see https://www.gnu.org/licenses/gpl-3.0.txt.")
