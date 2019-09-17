{ pkgs, ... }:
rec {
  pythonPackage = pkgs.python3.withPackages (ps: with ps; [
    numpy
    requests
    appdirs
  ]);
  buildDeps = with pkgs; [
    pythonPackage
  ];
  nativeBuildDeps = with pkgs; [
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
  packageDeps = with pkgs; [
    # general packaging
    binutils git zip
    # for deb packaging
    dpkg
    # for arch packaging
    pacman libarchive fakeroot
  ];
}
