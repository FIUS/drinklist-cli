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

def get_beverages():
    global cfg
    r = requests.get(cfg["url"] + "/beverages", headers={'X-Auth-Token' : cfg['token']})
    return json.loads(r.text)

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
    parser.add_argument('-d', dest='drink', type=str)
    args = parser.parse_args()

    if args.drink is None:
        list_beverages()
    else:
        order_drink(args.drink)
