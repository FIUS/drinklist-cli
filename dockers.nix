{ pkgs ? import <nixpkgs> {}
, buildLayeredImage ? pkgs.dockerTools.buildLayeredImage
, ...
}:
let
  deps = import ./dependencies.nix { inherit pkgs; };
in
rec {
  build-container = let
    allDeps = deps.baseSystem ++ deps.packagingDeps ++ deps.nativeBuildInputs ++ deps.buildInputs;
  in buildLayeredImage {
    name = "build-container";
    tag = "latest";
    contents = allDeps;
    config.Env = [ "PATH=${builtins.concatStringsSep ":" (map (x:"${x}/bin/") allDeps)}" ];
  };
}
