# Drinklist CLI

CLI for the http://github.com/FIUS/drinklist

```
usage: drink.py [-h] [-format {text,json}] [-config CONFIG_PATH] [-url URL]
                [-token TOKEN] [-pw PW] [-user USER]
                command ...

optional arguments:
  -h, --help           show this help message and exit
  -format {text,json}  Output format
  -config CONFIG_PATH  The config file
  -url URL             The API url of the drinklist
  -token TOKEN         The login token to use.
  -pw PW               The drinklist password
  -user USER           Your drinklist username

commands:
  The command to run

  command
    list               List all available beverages.
    drink              Order a drink.
    order              Alias for drink.
    users              List all registered users.
    balance            Get the balance.
    history            Get the history.
    help               Show this help.
```
