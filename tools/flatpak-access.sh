#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Let Flatpak apps see the theme: a user-wide override giving every Flatpak
# read-only access to the GTK config (where the colours and the libadwaita
# import live) and to ~/.local/share/themes (where the theme is installed).
# Flatpak apps otherwise only see their own private config directory.
#
#   flatpak-access.sh install | uninstall | status
set -e

PERMS="xdg-config/gtk-3.0:ro xdg-config/gtk-4.0:ro xdg-data/themes:ro"
OVERRIDES="${FLATPAK_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/flatpak}/overrides/global"

case "$1" in
install)
    for p in $PERMS; do flatpak override --user --filesystem="$p"; done
    echo "Flatpak apps can now read the GTK config and themes (restart them)."
    ;;
uninstall)
    [ -f "$OVERRIDES" ] || exit 0
    # `flatpak override --nofilesystem` adds a deny entry instead of removing
    # the grant, so the entries are removed from the file directly.
    python3 - "$OVERRIDES" $PERMS <<'PY'
import sys
path, drop = sys.argv[1], set(sys.argv[2:])
out = []
for line in open(path).read().splitlines():
    if line.startswith("filesystems="):
        kept = [e for e in line[len("filesystems="):].split(";") if e and e not in drop]
        if not kept:
            continue
        line = "filesystems=" + ";".join(kept) + ";"
    out.append(line)
open(path, "w").write("\n".join(out) + "\n")
PY
    echo "Removed the theme's Flatpak permissions."
    ;;
status)
    grep -E '^filesystems=' "$OVERRIDES" 2>/dev/null || echo "no global filesystem overrides"
    ;;
*)
    echo "Usage: $0 install|uninstall|status" >&2
    exit 1
    ;;
esac
