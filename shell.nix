{ pkgs ? import <nixpkgs> {}
, ...
}:
with pkgs;
let
  python-requirements = ps : with ps; [
    numpy
    requests
    appdirs
  ];
  python-package = (python3.withPackages python-requirements);
in
stdenvNoCC.mkDerivation rec {
   name = "drinklist-cli";

   meta = {
     homepage = https://github.com/FIUS/drinklist-cli;
     description = "A CLI for the FIUS drinklsit";
     license = stdenv.lib.licenses.gpl3;
   };

   dontBuild = true;
   nativeBuildInputs = [ makeWrapper ];
   buildInputs = [
     python-package
     # for deb packaging
     dpkg
     # for arch packaging
     pacman libarchive fakeroot
   ];
}
