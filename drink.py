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

def list_beverages():
    global cfg
    r = requests.get(cfg["url"] + "/beverages", headers={'X-Auth-Token' : cfg['token']})
    j = json.loads(r.text)
    for drink in j:
        print(u"{}\t{}".format(drink["name"], drink["price"]))

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
