#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Install the Oxygen GTK theme.
#
#   ./install.sh [--no-setup]
#
# PREFIX (default ~/.local) and DESTDIR work as usual, so a distro package can
# run `DESTDIR=$pkgdir PREFIX=/usr ./install.sh`. The theme goes to
# $PREFIX/share/themes/Oxygen. Unless --no-setup is given or DESTDIR is set,
# it then runs `oxygen-gtk-setup enable` for the current user, which hooks the
# theme into libadwaita apps; with a distro package each user runs that
# themselves.
set -e

here=$(cd "$(dirname "$0")" && pwd)
PREFIX="${PREFIX:-$HOME/.local}"
src="${THEME_SRC:-$here/Oxygen}"
dest="$DESTDIR$PREFIX/share/themes/Oxygen"

[ -d "$src" ] || { echo "No built theme at $src" >&2; exit 1; }
rm -rf "$dest"
mkdir -p "$DESTDIR$PREFIX/share/themes" "$DESTDIR$PREFIX/bin"
cp -r "$src" "$dest"
cp "$here/oxygen-gtk-setup" "$DESTDIR$PREFIX/bin/oxygen-gtk-setup"
chmod 755 "$DESTDIR$PREFIX/bin/oxygen-gtk-setup"
echo "Installed the theme to $dest"

if [ -z "$DESTDIR" ] && [ "$1" != "--no-setup" ]; then
    "$PREFIX/bin/oxygen-gtk-setup" enable
fi
