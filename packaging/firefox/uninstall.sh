#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Remove the files installed by install.sh (same PREFIX/DESTDIR). Profiles the
# theme was added to keep it until you run `oxygen-firefox-setup uninstall
# PROFILE` for each of them, which has to be done first.
set -e

PREFIX="${PREFIX:-$HOME/.local}"
setup="$DESTDIR$PREFIX/bin/oxygen-firefox-setup"

if [ -z "$DESTDIR" ] && [ -x "$setup" ]; then "$setup" watch-disable; fi
rm -rf "$DESTDIR$PREFIX/share/oxygen-firefox" "$setup"
echo "Removed the Oxygen Firefox files."
