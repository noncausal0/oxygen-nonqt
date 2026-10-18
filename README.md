# oxygen-nonqt

Ports of the KDE Oxygen theme to non-Qt toolkits (GTK and others), so the whole desktop looks consistent alongside Qt/KDE applications.

> **Disclosure:** This project is AI-generated. The code and documentation are written by an AI assistant (Claude) under human direction. Review accordingly.

## Status

Early stage. A GTK 3 theme lives in `gtk3/`. It has no colour variants: it follows the KDE colour scheme and accent colour that KDE's GTK integration exports to `~/.config/gtk-3.0/colors.css`, and falls back to the stock Oxygen colours elsewhere. CSD titlebars use the window colour, like Oxygen's window decoration.

```
make            # needs sassc
make install    # copies to ~/.local/share/themes/Oxygen
```

Then pick "Oxygen" under System Settings → Colors & Themes → Application Style → Configure GNOME/GTK Application Style.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
