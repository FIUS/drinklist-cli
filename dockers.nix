{ pkgs ? import <nixpkgs> {}
, buildImage ? pkgs.dockerTools.buildImage
, ...
}:
let
  deps = import ./dependencies.nix { inherit pkgs; };
in
rec {
  build-container = let
    allDeps = deps.baseSystem ++ deps.packageDeps ++ deps.nativeBuildDeps ++ deps.buildDeps;
  in buildImage {
    name = "build-container";
    tag = "latest";
    contents = allDeps;
    config.Env = [ "PATH=${builtins.concatStringsSep ":" (map (x:"${x}/bin/") allDeps)}" ];
  };
}
