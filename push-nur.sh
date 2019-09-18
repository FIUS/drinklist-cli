#!/bin/bash
echo "Applying git config"
git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis CI"
echo "Cloning nur repository"
git clone https://${GH_TOKEN}@github.com/marzipankaiser/nur-packages.git ./nur 2>&1 | sed "s|${GH_TOKEN}|TOKEN|"
ls -l ./nur
echo "Copying default.nix"
cp packages/default.nix ./nur/pkgs/drinklist-cli/default.nix

echo "cd into repository"
cd ./nur
echo "Adding default.nix"
git add ./pkgs/drinklist-cli/default.nix
if [ "$(git status --short)" = "" ]
then
    echo "Nothing to do"
else
    echo "Things to update:"
    git status
    echo "Committing"
    git commit -m "drinklist-cli: update"
    echo "Pushing"
    git push --quiet origin master
    echo "Ready"
fi
