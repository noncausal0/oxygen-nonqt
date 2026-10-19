# Oxygen for GTK

The KDE Oxygen theme for GTK 3, GTK 4 and libadwaita apps. It follows your KDE
colour scheme and accent through KDE's GTK integration (`kde-gtk-config`).

## Install

```
./install.sh
```

This copies the theme to `~/.local/share/themes/Oxygen` and hooks it into
libadwaita apps for your user. Then choose **Oxygen** in System Settings →
Colors & Themes → Application Style → Configure GNOME/GTK Application Style, and
restart your GTK apps.

For a system-wide install, run `PREFIX=/usr ./install.sh` as root. Each user
then runs `oxygen-gtk-setup enable` once for libadwaita apps, which only read
the user's own config.

## Uninstall

```
./uninstall.sh
```

(with the same `PREFIX`). It also takes the libadwaita hook out of your config.

## Notes

- libadwaita apps ignore GTK themes, so `oxygen-gtk-setup enable` adds one
  `@import` line to `~/.config/gtk-4.0/gtk.css`; `oxygen-gtk-setup disable`
  removes it.
- Flatpak apps need permission to read the theme and your GTK config. See the
  project README for the command.
- For Oxygen's always-visible scrollbars:
  `gsettings set org.gnome.desktop.interface overlay-scrolling false`

Project, screenshots and source: https://github.com/noncausal0/oxygen-nonqt
