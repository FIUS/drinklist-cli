import requests
import json
import getpass
import os.path
import pathlib

config = {}
config_file = pathlib.Path("~/.drinklist").expanduser()

def read_config(config_file):
    global config
    if config_file.exists():
        with config_file.open() as f:
            config = json.load(f)
def write_config(config_file):
    global config
    with config_file.open(mode='w') as f:
        json.dump(config, f)

api_url = "https://fius.informatik.uni-stuttgart.de/drinklist/api"

def get_login_token(api_url, password):
    r = requests.post(api_url + "/login", data = {'password' : password})
    j = json.loads(r.text)
    return j[u'token']

read_config(config_file)

def init_config_value(key, initializer):
    global config
    if not key in config:
        config[key] = initializer()
        write_config(config_file)

init_config_value('url', lambda: "https://fius.informatik.uni-stuttgart.de/drinklist/api")
init_config_value('pw', lambda: getpass.getpass())
init_config_value('token', lambda: get_login_token(api_url,config['pw']))
init_config_value('user', lambda: raw_input("Username: "))

def list_beverages():
    r = requests.get(api_url + "/beverages", headers={'X-Auth-Token' : config['token']})
    j = json.loads(r.text)
    for drink in j:
        print(u"{}\t{}".format(drink["name"], drink["price"]))
def order_drink(drink):
    r = requests.post(api_url + "/orders",
                      headers={'X-Auth-Token': config['token']},
                      params={'user': config['user'], 'beverage': drink})
    print(r.text)
    print(config['user'])
    print(drink)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d', dest='drink', type=str)
args = parser.parse_args()

if args.drink is None:
    list_beverages()
else:
    order_drink(args.drink)
