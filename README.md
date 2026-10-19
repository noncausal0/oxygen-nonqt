# oxygen-nonqt

The KDE Oxygen theme for non-Qt toolkits, so GTK apps and Firefox look consistent next to your Qt/KDE ones. There are no colour variants: it follows whatever KDE colour scheme and accent you use.

> **Disclosure:** This project is AI-generated. The code and documentation are written by an AI assistant (Claude) under human direction. Review accordingly.

## What's covered

| | |
|---|---|
| GTK 3 apps | yes |
| GTK 4 apps | yes |
| libadwaita apps (Nautilus, Flatseal, …) | yes, with some per-app polish still to come |
| Firefox toolbars, tabs, menus and new tab page | yes |
| Flatpak apps | yes, with one extra step |
| Qt apps | already Oxygen, nothing to do |

Early stage: expect rough edges. Screenshots are [further down](#screenshots).

## Installation

You need KDE Plasma with its GTK integration (`kde-gtk-config`, which comes with Plasma). The Oxygen icon theme is optional but recommended.

There are two packages, so you can take just the part you want. Download them from the [latest release](https://github.com/noncausal0/oxygen-nonqt/releases/latest): `oxygen-gtk` for GTK and libadwaita apps, and `oxygen-firefox` for Firefox. Each comes with its own short README. Installing from the source tree is described at the end of this section.

### 1. GTK and libadwaita apps (`oxygen-gtk`)

```
tar xzf oxygen-gtk-*.tar.gz
cd oxygen-gtk-*
./install.sh
```

Then choose **Oxygen** in System Settings → Colors & Themes → Application Style → Configure GNOME/GTK Application Style, and restart your GTK apps.

Optional: Oxygen has no overlay scrollbars, and GTK turns them on by default. To get the classic always-visible ones:

```
gsettings set org.gnome.desktop.interface overlay-scrolling false
```

### 2. Firefox (`oxygen-firefox`, optional)

Find your profile folder at `about:profiles` (look for "Root Directory"), then:

```
tar xzf oxygen-firefox-*.tar.gz
cd oxygen-firefox-*
./install.sh /path/to/your/profile
```

Restart Firefox. It needs `python3`, and the theme is made for Firefox's classic design in compact density, which the install switches to.

### 3. Flatpak apps (optional)

Flatpak apps can't see your theme unless you allow it. This changes your Flatpak permissions, so it's not part of the install. To allow it for all apps, run:

```
flatpak override --user \
  --filesystem=xdg-config/gtk-3.0:ro \
  --filesystem=xdg-config/gtk-4.0:ro \
  --filesystem=xdg-data/themes:ro
```

Then restart the apps. A few apps have their own theme setting that needs switching to the system theme, such as GIMP and Inkscape; see [Flatpak details](#flatpak-details).

### Uninstalling

From the same unpacked folders:

```
./uninstall.sh
oxygen-firefox-setup uninstall /path/to/your/profile   # before uninstalling the Firefox package
```

For Flatpak, remove the permissions with [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal) or see [Flatpak details](#flatpak-details).

### From the source tree

You also need `make`, `sassc` and `python3`:

```
make install                                    # the GTK theme
make firefox-install PROFILE=/path/to/profile   # Firefox
make dist                                       # build both release tarballs into dist/
```

### For distro packagers

Both packages are prebuilt, so building them needs nothing beyond what `make dist` uses, and installing them needs only `sh` (plus `python3` at runtime for the Firefox package). The install scripts honour `PREFIX` and `DESTDIR`:

```
DESTDIR="$pkgdir" PREFIX=/usr ./install.sh
```

- **GTK package:** installs the theme to `$PREFIX/share/themes/Oxygen` and the `oxygen-gtk-setup` command to `$PREFIX/bin`. libadwaita apps only read each user's own config, so a package can't hook them up system-wide: each user runs `oxygen-gtk-setup enable` once. With `DESTDIR` set, the scripts never touch any user's home.
- **Firefox package:** installs its files to `$PREFIX/share/oxygen-firefox` and `oxygen-firefox-setup` to `$PREFIX/bin`. Profiles are per-user, so each user runs `oxygen-firefox-setup install PROFILE`.
- Tarballs are reproducible (`SOURCE_DATE_EPOCH` is honoured) and come with a `SHA256SUMS` file. Releases are tagged `vX.Y.Z`, and the version is in `VERSION`.

## Screenshots

The comparison windows from `tools/compare/`, in KDE's stock Oxygen and Oxygen Dark schemes. Click for full size.

| | Oxygen | Oxygen Dark |
|---|---|---|
| **Qt (reference)** | <a href="docs/screenshots/qt-light.png"><img src="docs/screenshots/qt-light.png" width="380"></a> | <a href="docs/screenshots/qt-dark.png"><img src="docs/screenshots/qt-dark.png" width="380"></a> |
| **GTK 3** | <a href="docs/screenshots/gtk3-light.png"><img src="docs/screenshots/gtk3-light.png" width="380"></a> | <a href="docs/screenshots/gtk3-dark.png"><img src="docs/screenshots/gtk3-dark.png" width="380"></a> |
| **GTK 4** | <a href="docs/screenshots/gtk4-light.png"><img src="docs/screenshots/gtk4-light.png" width="380"></a> | <a href="docs/screenshots/gtk4-dark.png"><img src="docs/screenshots/gtk4-dark.png" width="380"></a> |
| **libadwaita** | <a href="docs/screenshots/libadwaita-light.png"><img src="docs/screenshots/libadwaita-light.png" width="380"></a> | <a href="docs/screenshots/libadwaita-dark.png"><img src="docs/screenshots/libadwaita-dark.png" width="380"></a> |
| **Firefox** | <a href="docs/screenshots/firefox-light.png"><img src="docs/screenshots/firefox-light.png" width="380"></a> | <a href="docs/screenshots/firefox-dark.png"><img src="docs/screenshots/firefox-dark.png" width="380"></a> |
| **Firefox, vertical tabs** | <a href="docs/screenshots/firefox-vertical-light.png"><img src="docs/screenshots/firefox-vertical-light.png" width="380"></a> | <a href="docs/screenshots/firefox-vertical-dark.png"><img src="docs/screenshots/firefox-vertical-dark.png" width="380"></a> |
| **Firefox, new tab page** | <a href="docs/screenshots/firefox-newtab-light.png"><img src="docs/screenshots/firefox-newtab-light.png" width="380"></a> | <a href="docs/screenshots/firefox-newtab-dark.png"><img src="docs/screenshots/firefox-newtab-dark.png" width="380"></a> |

The Qt and GTK 3 windows are shown without a titlebar, since KWin draws theirs. The libadwaita window is a gallery of real libadwaita widgets in a test window, not an actual app. The striped address bar in the Firefox shots is Firefox marking the window as remote-controlled by the screenshot script, and the third tab is held in its hover state.

## Details

Everything below is optional reading.

### How the colours work

KDE's GTK integration exports your colour scheme and accent to `~/.config/gtk-3.0/colors.css` and `~/.config/gtk-4.0/colors.css`. The theme is written entirely in terms of those colours and derives its shades from them, so it follows scheme and accent changes without any variants. Without KDE's export, it falls back to the stock Oxygen colours. Titlebars use the window colour, like Oxygen's window decoration.

### Layout of the repository

- `gtk3/`, `gtk4/`: the GTK 3 and GTK 4 themes, written in SCSS and built with `sassc`.
- `packaging/`: the install scripts and READMEs of the two release packages.
- `gtk4/scss/_libadwaita.scss`: the libadwaita layer. libadwaita apps ignore GTK themes and only read `~/.config/gtk-4.0/gtk.css`, so installing the GTK package adds one `@import` line there that loads Oxygen on top of libadwaita, and uninstalling removes it. This layer relies on KDE's exported colours and has no fallbacks.
- `common/`: colour handling, drawing recipes and image assets shared by GTK 3 and GTK 4.
- `firefox/`: `userChrome.css` for the toolbars, tabs, address bar and menus, `userContent.css` for the new tab page, with Oxygen icons loaded from your system icon theme.
- `tools/compare/`: windows that render the same widgets in Qt Oxygen, GTK 3, GTK 4, libadwaita and Firefox with any KDE `.colors` scheme, for side-by-side checks. `tools/screenshots.sh` regenerates the screenshots above after `make install`.

### Firefox details

The Firefox install puts the theme in the profile's `chrome/oxygen/`, adds one `@import` line each to `chrome/userChrome.css` and `chrome/userContent.css` (existing rules are kept), and adds these preferences to `user.js`:

- `toolkit.legacyUserProfileCustomizations.stylesheets`: load the stylesheets.
- `widget.gtk.libadwaita-colors.enabled = false`: otherwise Firefox replaces light GTK themes' colours with libadwaita's.
- `svg.context-properties.content.enabled`: lets the theme's own SVG glyphs take their colour from the scheme; Firefox otherwise draws them black.
- `browser.nova.enabled = false` and `browser.uidensity = 1`: the classic design in compact density.

Prefs Firefox has already applied stay set in `prefs.js` after uninstalling; change them in `about:config` if you want them back.

Firefox's own pages, like the new tab page, only get the real accent colour; the other system colours are replaced by fixed stand-ins so web pages cannot read them. So the install writes your current KDE colours for the new tab page. To keep them in step with your colour scheme automatically, install the optional watcher, a systemd user path unit on `~/.config/kdeglobals` (the new tab page picks the colours up at the next Firefox start):

```
oxygen-firefox-setup watch-enable
oxygen-firefox-setup watch-disable
```

### Flatpak details

Flatpak apps only see their own private config folder, so they use plain Adwaita until you let them read the theme. The command in the installation section applies to all Flatpak apps. To do it for one app only, add its ID to the end of the command (for example `org.gnome.Boxes`). Flatseal shows and undoes these permissions under "Filesystem"; without it, remove the three `xdg-config/…` and `xdg-data/themes` entries from `~/.local/share/flatpak/overrides/global` (or from the app's file in that folder).

Some apps need a bit more:
- Apps with their own theme preference, like GIMP and Inkscape, must be set to use the system theme in their preferences.
- GTK 4 and libadwaita apps pick up your KDE colours and the Oxygen styling this way, but only after the GTK package is installed, since the libadwaita part loads from your `gtk.css`.
- Qt Flatpaks (Kdenlive, Krita, qBittorrent and the like) use a separate Qt runtime and are not covered.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
