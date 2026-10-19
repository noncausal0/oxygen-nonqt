# Oxygen for Firefox

An Oxygen look for Firefox's toolbars, tabs (horizontal or vertical), address
bar, menus and new tab page, with Oxygen icons from your system icon theme.
Firefox takes its colours from the GTK theme, so install the Oxygen GTK theme
too (the `oxygen-gtk` package) for it to follow your KDE colour scheme.

Needs `python3`. Made for Firefox's classic design (the Nova redesign off) in
compact density, which the install switches to.

## Install

Find your profile folder at `about:profiles` ("Root Directory"), then:

```
./install.sh /path/to/your/profile
```

and restart Firefox. This copies the files to `~/.local/share/oxygen-firefox`,
adds `oxygen-firefox-setup` to `~/.local/bin`, and installs the theme into that
profile. For more profiles run `oxygen-firefox-setup install PROFILE`.

For a system-wide install, run `PREFIX=/usr ./install.sh` as root (no profile),
then each user runs `oxygen-firefox-setup install PROFILE`.

## New tab page colours

Firefox's own pages only get the real accent colour, so the install writes your
current KDE colours for the new tab page. To keep them in step when you change
colour scheme (picked up at the next Firefox start):

```
oxygen-firefox-setup watch-enable     # watch-disable turns it off
```

## Uninstall

```
oxygen-firefox-setup uninstall /path/to/your/profile    # for each profile
./uninstall.sh
```

The install adds `@import` lines to the profile's `chrome/userChrome.css` and
`userContent.css`, and a marked block of preferences to `user.js`; uninstalling
removes exactly those. Preferences Firefox has already applied stay set until
you change them in `about:config`.

Project, screenshots and source: https://github.com/noncausal0/oxygen-nonqt
