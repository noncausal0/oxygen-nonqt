#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Remove the Oxygen GTK theme installed by install.sh (same PREFIX/DESTDIR).
set -e

PREFIX="${PREFIX:-$HOME/.local}"
setup="$DESTDIR$PREFIX/bin/oxygen-gtk-setup"

if [ -z "$DESTDIR" ] && [ -x "$setup" ]; then "$setup" disable; fi
rm -rf "$DESTDIR$PREFIX/share/themes/Oxygen" "$setup"
echo "Removed the Oxygen GTK theme."
