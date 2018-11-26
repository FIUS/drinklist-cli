#!/usr/bin/env python3
import requests
import json
import getpass
import pathlib
import config

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

def list_beverages():
    j = get_beverages()
    column_width = max(len(drink["name"]) for drink in j) + 2
    for drink in j:
        print(u"{} {}".format(drink["name"].ljust(column_width), "{0:.2f} €".format(drink["price"]/100.0)))

def order_drink(drink):
    global cfg
    r = requests.post(cfg["url"] + "/orders",
                      headers={'X-Auth-Token': cfg['token']},
                      params={'user': cfg['user'], 'beverage': drink})
    print(r.text)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(title='commands',
                                     metavar='command',
                                     dest='command',
                                     description='The command to run')
    commands.add_parser('list', help='List all available beverages.')

    drink_parser = commands.add_parser('drink', help='Order a drink.')
    drink_parser.add_argument('drink', type=str, help='The drink to order')



    commands.add_parser('help', help='Show this help.')
    args = parser.parse_args()

    if args.command in [None, 'help']:
        parser.print_help()
    elif args.command == 'list':
        list_beverages()
    elif args.command == 'drink':
        order_drink(args.drink)
