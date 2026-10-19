#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Install the Oxygen Firefox files.
#
#   ./install.sh [PROFILE]
#
# PREFIX (default ~/.local) and DESTDIR work as usual, so a distro package can
# run `DESTDIR=$pkgdir PREFIX=/usr ./install.sh`. The files go to
# $PREFIX/share/oxygen-firefox and the `oxygen-firefox-setup` command to
# $PREFIX/bin. Giving a PROFILE (and no DESTDIR) also installs the theme into
# that Firefox profile; otherwise run `oxygen-firefox-setup install PROFILE`
# afterwards, once per profile and user.
set -e

here=$(cd "$(dirname "$0")" && pwd)
PREFIX="${PREFIX:-$HOME/.local}"
dest="$DESTDIR$PREFIX/share/oxygen-firefox"

rm -rf "$dest"
mkdir -p "$DESTDIR$PREFIX/share" "$DESTDIR$PREFIX/bin"
cp -r "${DATA_SRC:-$here/data}" "$dest"
cp "$here/oxygen-firefox-setup" "$DESTDIR$PREFIX/bin/oxygen-firefox-setup"
chmod 755 "$DESTDIR$PREFIX/bin/oxygen-firefox-setup" "$dest/refresh-colors.sh"
echo "Installed the Firefox files to $dest"

if [ -z "$DESTDIR" ] && [ -n "$1" ]; then
    "$PREFIX/bin/oxygen-firefox-setup" install "$1"
fi
