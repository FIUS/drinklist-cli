{ pkgs ? import <nixpkgs> {}
, ...
}:
let
  deps = import ./dependencies.nix { inherit pkgs; };
in
with pkgs;
stdenvNoCC.mkDerivation rec {
   name = "drinklist-cli";

   meta = {
     homepage = https://github.com/FIUS/drinklist-cli;
     description = "A CLI for the FIUS drinklsit";
     license = stdenv.lib.licenses.gpl3;
   };

   dontBuild = true;
   nativeBuildInputs = deps.nativeBuildInputs;
   buildInputs = deps.packagingDeps ++ deps.buildInputs;
}
