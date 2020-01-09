PY_SRC_FILES=$(wildcard src/*.py)
SH_SRC_FILES=$(wildcard src/*.sh)
SRC_FILES=$(wildcard src/*.py) $(wildcard src/*.sh)
GIT_REV=$(shell git rev-parse HEAD)
TARBALL_URL=https://github.com/FIUS/drinklist-cli/archive/$(GIT_REV).tar.gz
TARBALL_SHA256SUM=$(shell curl -L "$(TARBALL_URL)" | sha256sum | head -c 64)# This is a hack, but tarballs sadly don't seem to be deterministic
NIX_SHA256SUM=$(shell nix-prefetch-url --unpack "$(TARBALL_URL)")
VERSION=0.2
DEB_PACKAGE_NAME=packages/drinklist-cli_$(VERSION)-1
ARCH_PACKAGE_NAME=packages/drinklist-cli-$(GIT_REV)-1-any.pkg.tar.gz

.PHONY: clean all arch-package deb

all: packages/drinklist packages/PKGBUILD $(ARCH_PACKAGE_NAME) $(DEB_PACKAGE_NAME).deb packages/default.nix

clean:
	rm -rf packages

packages/drinklist: $(SRC_FILES) # Builds a single standalone executable from the python files
	mkdir -p packages
	cp src/drink.py __main__.py
	zip -j drinklist.zip __main__.py $(filter-out src/drink.py, $(PY_SRC_FILES))
	echo "#!/usr/bin/env python3" > packages/drinklist
	cat drinklist.zip >> packages/drinklist
	chmod +x packages/drinklist
	rm __main__.py
	rm drinklist.zip

install: packages/drinklist
	mkdir -p $(DESTDIR)/usr/bin
	cp ./packages/drinklist $(DESTDIR)/usr/bin/drinklist
	cp ./drink_alias.sh $(DESTDIR)/usr/bin/drink
	chmod +x $(DESTDIR)/usr/bin/drink
	mkdir -p $(DESTDIR)/usr/share/bash-completion/completions
	cp ./src/bash_completions.sh $(DESTDIR)/usr/share/bash-completion/completions/drinklist
	cp ./src/bash_completions.sh $(DESTDIR)/usr/share/bash-completion/completions/drink
	mkdir -p $(DESTDIR)/usr/share/zsh/site-functions
	cp ./src/zsh_completion_helpers.zsh $(DESTDIR)/usr/share/zsh/site-functions/_drinklist_completion_helpers
	cp ./src/zsh_completion_drinklist.zsh $(DESTDIR)/usr/share/zsh/site-functions/_drinklist
	cp ./src/zsh_completion_drink.zsh $(DESTDIR)/usr/share/zsh/site-functions/_drink
	mkdir -p $(DESTDIR)/usr/share/doc/drinklist-cli
	cp ./LICENSE $(DESTDIR)/usr/share/doc/drinklist-cli/LICENSE

packages/default.nix: package_templates/default.nix
	mkdir -p packages
	sed "s|%%TARBALL_URL%%|$(TARBALL_URL)|;s|%%NIX_SHA256SUM%%|$(NIX_SHA256SUM)|;s|%%TARBALL_SHA256SUM%%|$(TARBALL_SHA256SUM)|;s|%%GIT_REV%%|$(GIT_REV)|" $< > $@

arch-install: packages/PKGBUILD
	cd packages && makepkg -s
	cd packages && makepkg --install

packages/PKGBUILD: package_templates/PKGBUILD.template $(SRC_FILES)
	mkdir -p packages
	sed "s|%%TARBALL_URL%%|$(TARBALL_URL)|;s|%%TARBALL_SHA256SUM%%|$(TARBALL_SHA256SUM)|;s|%%GIT_REV%%|$(GIT_REV)|" $< > $@

$(ARCH_PACKAGE_NAME): packages/PKGBUILD # ugly since downloading source from github but works TODO
	curl -L "$(TARBALL_URL)" > ./packages/$(GIT_REV).tar.gz # manually download tarball since this fails on non-archlinux
	cd packages && makepkg -d
	rm -rf packages/src
	rm -rf packages/pkg
	rm packages/$(GIT_REV).tar.gz
arch-package: $(ARCH_PACKAGE_NAME)

$(DEB_PACKAGE_NAME).deb: package_templates/DEBIAN_control.template packages/drinklist
	mkdir -p $(DEB_PACKAGE_NAME)/DEBIAN
	sed "s|%%VERSION%%|$(VERSION)|" $< > $(DEB_PACKAGE_NAME)/DEBIAN/control
	$(MAKE) install DESTDIR=$(DEB_PACKAGE_NAME)
	dpkg-deb --build $(DEB_PACKAGE_NAME)
	rm -rf $(DEB_PACKAGE_NAME)
deb: $(DEB_PACKAGE_NAME).deb
