with import <nixpkgs> {};
let
python-requirements = ps : with ps; [
    numpy
    requests
];
in buildEnv {
   name = "drinkcli-env";
   paths = [
   (python3.withPackages (ps: python-requirements ps))
   ];
}
