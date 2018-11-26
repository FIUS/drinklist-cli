#!/usr/bin/env python3
import requests
import json
import getpass
import pathlib
import config
from ppformat import pp

def get_login_token(api_url, password):
    global cfg
    response = requests.post(api_url + "/login", data = {'password' : password})
    json_result = json.loads(response.text)
    return json_result[u'token']

cfg = config.Config(pathlib.Path("~/.drinklist").expanduser())

cfg.init_value('url', lambda: "https://fius.informatik.uni-stuttgart.de/drinklist/api")
cfg.init_value('pw', lambda: getpass.getpass())
cfg.init_value('token', lambda: get_login_token(cfg["url"], cfg['pw']))
cfg.init_value('user', lambda: input("Username: "))

def get(suburl):
    global cfg
    r = requests.get(cfg["url"] + suburl, headers={'X-Auth-Token' : cfg['token']})
    return json.loads(r.text)

def get_beverages():
    return get("/beverages")
def get_users():
    return get("/users")

def order_drink(drink):
    global cfg
    r = requests.post(cfg["url"] + "/orders",
                      headers={'X-Auth-Token': cfg['token']},
                      params={'user': cfg['user'], 'beverage': drink})
    print(r.text)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', choices=['text', 'json'], help='Output format')
    commands = parser.add_subparsers(title='commands',
                                     metavar='command',
                                     dest='command',
                                     description='The command to run')
    list_parser = commands.add_parser('list', help='List all available beverages.')
    list_parser.add_argument('-regex', help='Filter drinks by regex.', type=str, default=None)

    drink_parser = commands.add_parser('drink', help='Order a drink.')
    order_parser = commands.add_parser('order', help='Alias for drink.')
    def init_drink_parser(drink_parser):
        drink_parser.add_argument('drink', type=str, help='The drink to order')
    init_drink_parser(drink_parser)
    init_drink_parser(order_parser)

    commands.add_parser('users', help='List all registered users.')

    commands.add_parser('help', help='Show this help.')
    args = parser.parse_args()

    formatter = None
    if args.format == 'json':
        formatter = lambda x: print(json.dumps(x))
    else:
        formatter = lambda x: print(pp(x))

    if args.command in [None, 'help']:
        parser.print_help()
    elif args.command == 'list':
        beverages = get_beverages()
        if args.regex is not None:
            import re
            p = re.compile(args.regex, re.IGNORECASE if args.regex==args.regex.lower() else re.ASCII)
            beverages = [b for b in beverages if p.search(b['name']) is not None]
        formatter(beverages)
    elif args.command in ['order', 'drink']:
        order_drink(args.drink)
    elif args.command == 'users':
        formatter(get_users())
