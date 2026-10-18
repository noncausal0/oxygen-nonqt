# oxygen-nonqt

Ports of the KDE Oxygen theme to non-Qt toolkits (GTK and others), so the whole desktop looks consistent alongside Qt/KDE applications.

> **Disclosure:** This project is AI-generated. The code and documentation are written by an AI assistant (Claude) under human direction. Review accordingly.

## Status

Early stage. There are no colour variants: the theme follows the KDE colour scheme and accent colour that KDE's GTK integration exports to `~/.config/gtk-{3,4}.0/colors.css`. Titlebars use the window colour, like Oxygen's window decoration.

- **GTK 3** (`gtk3/`): a regular GTK theme.
- **GTK 4** (`gtk4/`): a regular GTK theme for plain GTK 4 apps.
- **libadwaita** (`gtk4/scss/_libadwaita.scss`): libadwaita apps ignore GTK themes, so `make install` adds one `@import` line to `~/.config/gtk-4.0/gtk.css` that loads Oxygen on top of libadwaita. `make uninstall` removes it again. This layer relies on the colours KDE exports and has no fallbacks of its own.

Shared colour handling and drawing recipes live in `common/`.

```
make            # needs sassc
make install    # copies to ~/.local/share/themes/Oxygen and hooks up libadwaita
```

Then pick "Oxygen" under System Settings → Colors & Themes → Application Style → Configure GNOME/GTK Application Style.

Oxygen has no overlay scrollbars. GTK decides that outside the theme, so turn them off to get the classic always-visible scrollbars:

```
gsettings set org.gnome.desktop.interface overlay-scrolling false
```

`tools/compare/` renders the same widgets in Qt Oxygen, GTK 3, GTK 4 and libadwaita, with any KDE `.colors` scheme, for side-by-side checks.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
