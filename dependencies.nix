{ pkgs, ... }:
rec {
  pythonDeps = ps: with ps; [
    numpy
    requests
    appdirs
  ];
  pythonPackage = pkgs.python3.withPackages pythonDeps;
  buildInputs = with pkgs; [
    pythonPackage
  ];
  nativeBuildInputs = with pkgs; [
    makeWrapper
  ];
  baseSystem = with pkgs; [
    # basics
    bash coreutils findutils
    binutils
    openssl cacert curl
    gnumake
    gnused
    gzip
    gnugrep
    binutils-unwrapped
    file
    gawk
    gnutar
  ];
  packagingDeps = with pkgs; [
    # general packaging
    binutils git zip
    # nix packaging
    nix
    # for deb packaging
    dpkg
    # for arch packaging
    pacman libarchive fakeroot
  ];
}
