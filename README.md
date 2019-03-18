# Drinklist CLI

CLI for the [Drinklist](http://github.com/FIUS/drinklist)

For help, run `./drink.py help`

## Bash Completions
The bash completions are in `bash_completions.sh`.
To enable them first edit the two first constants to match the commands 
you use to run the drinklist and then soft link them to the bash completions directory:
`ln -s <path/to/this/git>/bash_completions.sh /usr/share/bash-completion/completions/drinklist`