{ pkgs ? import <nixpkgs> {}
, ...
}:
with pkgs;
let
  deps = import ./dependencies.nix { inherit pkgs; };
in
stdenvNoCC.mkDerivation rec {
   name = "drinklist-cli";

   meta = {
     homepage = https://github.com/FIUS/drinklist-cli;
     description = "A CLI for the FIUS drinklsit";
     license = stdenv.lib.licenses.gpl3;
   };

   src = ./.;

   dontBuild = true;
   nativeBuildInputs = deps.nativeBuildInputs;
   buildInputs = deps.buildInputs;
   installPhase = ''
     mkdir -p $out/bin
     mkdir -p $out/opt
     for file in ./src/*
     do
       cp -r $file $out/opt/
     done
     cp LICENSE $out/opt/LICENSE
     cp COPYING $out/opt/COPYING
     makeWrapper $out/opt/drink.py $out/bin/drinklist
     makeWrapper $out/opt/drink.py $out/bin/drink --add-flags drink

     # Link bash completion
     mkdir -p $out/etc/bash_completion.d
     ln -s $out/opt/bash_completions.sh $out/etc/bash_completion.d/drinklist.bash-completion
     mkdir -p $out/share/bash-completion/completions
     ln -s $out/opt/bash_completions.sh $out/share/bash-completion/completions/drinklist
     ln -s $out/opt/bash_completions.sh $out/share/bash-completion/completions/drinklist.bash-completion

     # Link zsh completion
     mkdir -p $out/share/zsh/site-functions
     ln -s $out/opt/zsh_completions.zsh $out/share/zsh/site-functions/_drinklist
     ln -s $out/opt/zsh_completions.zsh $out/share/zsh/site-functions/_drink
     mkdir -p $out/share/zsh/vendor-completions
     ln -s $out/opt/zsh_completions.zsh $out/share/zsh/vendor-completions/_drinklist
     ln -s $out/opt/zsh_completions.zsh $out/share/zsh/vendor-completions/_drink
   '';
}
