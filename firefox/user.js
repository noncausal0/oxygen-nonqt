// SPDX-License-Identifier: GPL-3.0-or-later
// Preferences the Oxygen userChrome.css needs.

// Load chrome/userChrome.css from the profile.
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// With light GTK themes Firefox swaps in libadwaita's colours by default
// instead of the theme's, so the chrome would not follow the KDE scheme.
user_pref("widget.gtk.libadwaita-colors.enabled", false);

// Let the theme's own SVG glyphs (title buttons, tab close) take their colour
// from CSS. Firefox only allows that for its built-in icons by default and
// draws the others black, which is invisible on dark schemes.
user_pref("svg.context-properties.content.enabled", true);

// The theme is made for Firefox's classic design (Nova off) in compact
// density, which also matches Oxygen's tighter metrics.
user_pref("browser.nova.enabled", false);
user_pref("browser.uidensity", 1);
