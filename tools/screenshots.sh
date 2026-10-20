#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Render the comparison windows in Oxygen and OxygenDark for the README.
# Run from the repository root after `make install`.
set -e

OUT=docs/screenshots
SCHEMES=/usr/share/color-schemes
mkdir -p "$OUT"

for scheme in Oxygen OxygenDark; do
    colors="$SCHEMES/$scheme.colors"
    tag=$(echo "$scheme" | sed 's/Oxygen/light/; s/lightDark/dark/')
    python3 tools/compare/qt_window.py --colors "$colors" --snapshot "$OUT/qt-$tag.png"
    GTK_THEME=Oxygen python3 tools/compare/gtk3_window.py --colors "$colors" --snapshot "$OUT/gtk3-$tag.png"
    GTK_THEME=Oxygen python3 tools/compare/gtk4_window.py --colors "$colors" --snapshot "$OUT/gtk4-$tag.png"
    python3 tools/compare/gtk4_window.py --adw --colors "$colors" --snapshot "$OUT/libadwaita-$tag.png"
    # Firefox runs in a throwaway profile under build/.
    python3 tools/compare/firefox_window.py build/firefox-profile "$OUT/firefox-$tag.png" --colors "$colors" --height 360 --hover-tab
    python3 tools/compare/firefox_window.py build/firefox-profile "$OUT/firefox-vertical-$tag.png" --vertical --colors "$colors" --height 360
    python3 tools/compare/firefox_window.py build/firefox-profile "$OUT/firefox-newtab-$tag.png" --newtab --colors "$colors" --height 680
done
rm -rf build/firefox-profile
