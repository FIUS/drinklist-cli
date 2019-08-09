# Maintainer: Marcial Gaißert <drinklist-cli@gaisseml.de>
pkgname=drinklist-cli
pkgver=master
pkgrel=2
pkgdesc="A CLI for the FIUS drinklist"
arch=('any')
url="https://github.com/FIUS/drinklist-cli"
license=('GPL')
depends=(python python-requests python-numpy python-appdirs)
source=("https://github.com/FIUS/drinklist-cli/archive/master.tar.gz")
sha256sums=('cb5bfac7835ea157c3ad07712fca5460075fd3ad47346d16cdbcc1856ca8aedb')

build() {
	cd "$srcdir/$pkgname-$pkgver"
    ./build.sh
}

package() {
	cd "$srcdir/$pkgname-$pkgver"
    mkdir -p $pkgdir/usr/bin
    cp ./drinklist $pkgdir/usr/bin/
    echo '#!/bin/bash' > $pkgdir/usr/bin/drink
    echo 'drinklist drink "$@"' >> $pkgdir/usr/bin/drink
    chmod +x $pkgdir/usr/bin/drink
    mkdir -p $pkgdir/usr/share/bash-completion/completions
    cp ./bash_completions.sh $pkgdir/usr/share/bash-completion/completions/drinklist
    cp ./bash_completions.sh $pkgdir/usr/share/bash-completion/completions/drink
}
