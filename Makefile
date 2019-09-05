SRC_FILES=$(wildcard src/*.py) $(wildcard src/*.sh)
GIT_REV=$(shell git rev-parse HEAD)
TARBALL_URL=https://github.com/FIUS/drinklist-cli/archive/$(GIT_REV).tar.gz
TARBALL_SHA256SUM=$(shell curl -L "$(TARBALL_URL)" | sha256sum) # This is a hack, but tarballs sadly don't seem to be deterministic

.PHONY: clean

all: packages/PKGBUILD

packages/PKGBUILD: package_templates/PKGBUILD.template $(SRC_FILES)
	mkdir -p packages
	sed "s|%%TARBALL_URL%%|$(TARBALL_URL)|;s|%%TARBALL_SHA256SUM%%|$(TARBALL_SHA256SUM)|" $< > $@
