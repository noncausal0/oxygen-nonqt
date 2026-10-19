#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Rewrite the new tab page colours in every profile the theme was installed
# into (listed by `make firefox-install`), from the current KDE scheme.
# Run by the oxygen-firefox-colors user unit whenever kdeglobals changes.
DIR=$(cd "$(dirname "$0")" && pwd)
LIST="${XDG_DATA_HOME:-$HOME/.local/share}/oxygen-nonqt/firefox-profiles"
SCHEME="${FF_SCHEME:-$HOME/.config/kdeglobals}"
[ -f "$LIST" ] || exit 0
while IFS= read -r profile; do
    [ -d "$profile/chrome/oxygen" ] || continue
    python3 -I "$DIR/firefox_colors.py" "$SCHEME" "$profile/chrome/oxygen/content-colors.css"
done < "$LIST"
