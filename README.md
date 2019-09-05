# Drinklist CLI

CLI for the [Drinklist](http://github.com/FIUS/drinklist)

For help, run `src/drink.py help` (or, install a packaged version and run `drinklist help`)

## Bash Completions
The bash completions are in `src/bash_completions.sh`.
To enable them first edit the two first constants to match the commands 
you use to run the drinklist and then soft link them to the bash completions directory:
`ln -s <path/to/drinklist-cli>/bash_completions.sh /usr/share/bash-completion/completions/<name of used command>`
Don't forget to do this also for your alias.
