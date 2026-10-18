# SPDX-License-Identifier: GPL-3.0-or-later
"""Read a KDE .colors scheme, so the comparison windows can use any scheme
without changing the desktop's own settings."""
import configparser


def load(path):
    cp = configparser.RawConfigParser(strict=False)
    cp.optionxform = str
    cp.read(path, encoding="utf-8")

    def get(section, key):
        return tuple(int(v) for v in cp.get("Colors:" + section, key).split(",")[:3])

    return get


def gtk_css(path):
    """The subset of KDE's exported GTK colours that the theme reads."""
    c = load(path)
    hexa = lambda rgb: "#%02x%02x%02x" % rgb
    names = {
        "theme_bg_color_breeze": c("Window", "BackgroundNormal"),
        "theme_fg_color_breeze": c("Window", "ForegroundNormal"),
        "theme_base_color_breeze": c("View", "BackgroundNormal"),
        "theme_text_color_breeze": c("View", "ForegroundNormal"),
        "theme_selected_bg_color_breeze": c("Selection", "BackgroundNormal"),
        "theme_selected_fg_color_breeze": c("Selection", "ForegroundNormal"),
        "theme_unfocused_selected_bg_color_breeze": c("Selection", "BackgroundNormal"),
        "theme_unfocused_selected_fg_color_breeze": c("Selection", "ForegroundNormal"),
        "theme_button_background_normal_breeze": c("Button", "BackgroundNormal"),
        "theme_button_foreground_normal_breeze": c("Button", "ForegroundNormal"),
        "theme_button_decoration_focus_breeze": c("Button", "DecorationFocus"),
        "theme_button_decoration_hover_breeze": c("Button", "DecorationHover"),
        "theme_unfocused_fg_color_breeze": c("Window", "ForegroundInactive"),
        "insensitive_fg_color_breeze": c("Window", "ForegroundInactive"),
        "insensitive_base_color_breeze": c("View", "BackgroundAlternate"),
        "tooltip_background_breeze": c("Tooltip", "BackgroundNormal"),
        "tooltip_text_breeze": c("Tooltip", "ForegroundNormal"),
        "link_color_breeze": c("View", "ForegroundLink"),
        "link_visited_color_breeze": c("View", "ForegroundVisited"),
    }
    return "".join("@define-color %s %s;\n" % (k, hexa(v)) for k, v in names.items())
