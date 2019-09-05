# Drinklist CLI

A CLI for [the FIUS Drinklist](https://github.com/FIUS/drinklist).

## Installation
Note: A GitHub Releases page serving the current builds is planned but not yet there.

### NixOS
#### NUR (recommended)
The drinklist-cli is packaged in @marzipankaiser's [NUR](https://github.com/nix-community/NUR/) repository (i.e. as `nur.repos.marzipankaiser.drinklist-cli`).

To install globally, add the following to your `configuration.nix`:
```nix
# Set up NUR
nixpkgs.config.packageOverrides = pkgs: {
    nur = import (builtins.fetchTarball "https://github.com/nix-community/NUR/archive/master.tar.gz") {
      inherit pkgs;
    };
};
```
and then install `nur.repos.marzipankaiser.drinklist-cli`.

### ArchLinux
#### Using pre-built package
There is a pre-built ArchLinux package [here](https://github.com/FIUS/drinklist-cli/releases/download/v0.1-alpha/drinklist-cli-c6a57961530af57e124f77d9d755572821fdcaaf-1-any.pkg.tar.gz)
#### Using `PKGBUILD`
There is a `PKGBUILD` [here](https://github.com/FIUS/drinklist-cli/releases/download/v0.1-alpha/PKGBUILD).
#### Generating `PKGBUILD`
Run `make packages/PKGBUILD` to generate a `PKGBUILD` for the current git commit.
This can be used to build an archlinux package.
#### Generating a package
Run `make packages/drinklist-cli-<GIT_REV>-1-any.pkg.tar.gz` 
(Replacing `<GIT_REV>` with the current git commit rev)
and then install the resulting package.

### Debian (experimental, untested)
There is a Debian package [here](https://github.com/FIUS/drinklist-cli/releases/download/v0.1-alpha/drinklist-cli_0.1-1.deb)
#### Building the Debian package from source
Run `make packages/drinklist-cli_0.1-1.deb`. This generates a Debian package that can be installed using e.g. `apt`.

### Other Linux distributions
#### Without using a package manager
Run `make install`.

## Help

CLI for the [Drinklist](http://github.com/FIUS/drinklist)

For help, run `src/drink.py help` or install a packaged version and run `drinklist help`

## Bash Completions
The bash completions are in `src/bash_completions.sh`.
To enable them first edit the two first constants to match the commands 
you use to run the drinklist and then soft link them to the bash completions directory:
`ln -s <path/to/drinklist-cli>/bash_completions.sh /usr/share/bash-completion/completions/<name of used command>`
Don't forget to do this also for your alias.
