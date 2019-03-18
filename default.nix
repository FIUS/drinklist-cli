{ pkgs ? import <nixpkgs> {}
}:
with pkgs;
let
python-requirements = ps : with ps; [
    numpy
    requests
  ];
  python-package = (python3.withPackages python-requirements);
  python-binary = "${python-package}/bin/python";
in
stdenv.mkDerivation rec {
   name = "drinklist-cli";

   meta = {
     homepage = https://github.com/FIUS/drinklist-cli;
     description = "A CLI for the FIUS drinklsit";
     license = stdenv.lib.licenses.gpl3;
   };

   src = fetchGit {
     url = https://github.com/FIUS/drinklist-cli;
   };

   buildInputs = [ python-package ];
   installPhase = ''
     mkdir -p $out/bin
     mkdir -p $out/opt
     cp ./*.py $out/opt/
     echo '#!/bin/sh' > $out/bin/drinklist
     echo "${python-binary} $out/opt/drink.py \"\$@\"" > $out/bin/drinklist
     chmod +x $out/bin/drinklist

     # Link bash completion
     mkdir -p $out/etc/bash_completion.d
     ln -s $out/opt/bash_completions.sh $out/etc/bash_completion.d/drinklist.sh
   '';
}
