// SPDX-License-Identifier: GPL-3.0-or-later
// Preferences the Oxygen userChrome.css needs.

// Load chrome/userChrome.css from the profile.
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// With light GTK themes Firefox swaps in libadwaita's colours by default
// instead of the theme's, so the chrome would not follow the KDE scheme.
user_pref("widget.gtk.libadwaita-colors.enabled", false);
