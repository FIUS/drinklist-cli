{ pkgs ? import <nixpkgs> {}
, lib ? import <nixpkgs/lib>
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
     license = lib.licenses.gpl3;
   };

   dontBuild = true;
   nativeBuildInputs = deps.nativeBuildInputs;
   buildInputs = deps.packagingDeps ++ deps.buildInputs;
}
