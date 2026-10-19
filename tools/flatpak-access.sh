#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Let Flatpak apps see the theme: a user-wide override giving every Flatpak
# read-only access to the GTK config (where the colours and the libadwaita
# import live) and to ~/.local/share/themes (where the theme is installed).
# Flatpak apps otherwise only see their own private config directory.
#
# Some apps (GIMP) also pin their own GTK theme through an environment
# variable in their metadata, which wins over the user's choice; those get a
# per-app override setting it to Oxygen.
#
#   flatpak-access.sh install | uninstall | status
set -e

APPS_DIR="${FLATPAK_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/flatpak}/overrides"

# Installed apps whose metadata sets GTK_THEME.
pinned_apps() {
    for app in $(flatpak list --app --columns=application); do
        flatpak info --show-permissions "$app" 2>/dev/null |
            sed -n '/^\[Environment\]/,/^$/p' | grep -q '^GTK_THEME=' && echo "$app"
    done
}

PERMS="xdg-config/gtk-3.0:ro xdg-config/gtk-4.0:ro xdg-data/themes:ro"
OVERRIDES="${FLATPAK_USER_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/flatpak}/overrides/global"

case "$1" in
install)
    for p in $PERMS; do flatpak override --user --filesystem="$p"; done
    for app in $(pinned_apps); do
        flatpak override --user --env=GTK_THEME=Oxygen "$app"
        echo "$app pins its own GTK theme; set to Oxygen."
    done
    echo "Flatpak apps can now read the GTK config and themes (restart them)."
    ;;
uninstall)
    for f in "$APPS_DIR"/*; do
        [ -f "$f" ] && [ "$f" != "$OVERRIDES" ] && grep -qx 'GTK_THEME=Oxygen' "$f" || continue
        sed -i '/^GTK_THEME=Oxygen$/d' "$f"
        # Nothing left but empty section headers: remove the file.
        grep -qvE '^(\[.*\])?$' "$f" || rm "$f"
    done
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
