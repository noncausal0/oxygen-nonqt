#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Screenshot Firefox's toolbars and tabs in a throwaway profile.

Creates a fresh profile in the given directory (never touches the user's
own), installs the theme into it with `make firefox-install` unless --stock is
given, opens a few tabs and saves a screenshot of the whole browser window,
taken through Marionette so it does not depend on window focus.

  firefox_window.py PROFILE_DIR OUT.png [--vertical] [--stock] [--wait]
                    [--colors FILE.colors] [--height PX] [--newtab] [--hover-tab] [--hover ID] [--url URL]
                    [--click SELECTOR]... [--theme NAME]

--vertical switches to vertical tabs. --wait leaves the window open for
interactive testing instead of quitting. --colors runs Firefox with its own
GTK config holding that KDE colour scheme (Firefox takes its colours from
GTK); the user's config is not touched. --newtab shows Firefox's new tab page
in the selected tab, --url loads the given page there instead, and
--hover-tab holds an inactive tab in its hover state, and --hover ID holds
the element with that id in its hover state. --click clicks the element the
CSS selector matches in the page (repeatable, in order; for opening the reader
view's menus) and --theme NAME picks the reader view's colour theme.
"""
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PORT = 2829

PREFS = {
    "toolkit.legacyUserProfileCustomizations.stylesheets": True,
    # As in firefox/user.js: without it, light GTK themes get libadwaita's colours.
    "widget.gtk.libadwaita-colors.enabled": False,
    "svg.context-properties.content.enabled": True,
    "marionette.port": PORT,
    # Marionette otherwise applies its own defaults, which blank the new tab page.
    "remote.prefs.recommended": False,
    "browser.shell.checkDefaultBrowser": False,
    "browser.startup.homepage_override.mstone": "ignore",
    "browser.aboutwelcome.enabled": False,
    "browser.startup.page": 0,
    "datareporting.policy.dataSubmissionEnabled": False,
    "toolkit.telemetry.reportingpolicy.firstRun": False,
    "browser.tabs.firefox-view": False,
    "sidebar.revamp": True,
    "sidebar.verticalTabs": False,
    "sidebar.verticalTabs.dragToPinPromo.dismissed": True,
    "browser.toolbars.bookmarks.visibility": "always",
    # Keep the new tab page static, so its screenshots look the same on every
    # machine: no weather, clocks, stories or sponsored content.
    "browser.newtabpage.activity-stream.showWeather": False,
    "browser.newtabpage.activity-stream.widgets.enabled": False,
    "browser.newtabpage.activity-stream.widgets.system.enabled": False,
    "browser.newtabpage.activity-stream.widgets.system.clocks.enabled": False,
    "browser.newtabpage.activity-stream.widgets.clocks.enabled": False,
    "browser.newtabpage.activity-stream.widgets.lists.enabled": False,
    "browser.newtabpage.activity-stream.widgets.crossword.enabled": False,
    "browser.newtabpage.activity-stream.widgets.sportsWidget.enabled": False,
    "browser.newtabpage.activity-stream.widgets.stocks.enabled": False,
    "browser.newtabpage.activity-stream.widgets.pictureOfTheDay.enabled": False,
    "browser.newtabpage.activity-stream.feeds.system.topstories": False,
    "browser.newtabpage.activity-stream.feeds.section.topstories": False,
    "browser.newtabpage.activity-stream.feeds.section.highlights": False,
    "browser.newtabpage.activity-stream.showSponsored": False,
    "browser.newtabpage.activity-stream.showSponsoredTopSites": False,
    "browser.newtabpage.activity-stream.showSponsoredStories": False,
    # As in firefox/user.js: the classic design in compact density.
    "browser.nova.enabled": False,
    "browser.uidensity": 1,
}

PAGE = "data:text/html,<title>{0}</title><body style='font:20px sans-serif;padding:2em'>{0}"


class Marionette:
    def __init__(self, port):
        for _ in range(100):
            try:
                self.sock = socket.create_connection(("127.0.0.1", port))
                break
            except OSError:
                time.sleep(0.2)
        else:
            raise SystemExit("Marionette did not start")
        self.id = 0
        self._read()  # greeting

    def _read(self):
        size = b""
        while not size.endswith(b":"):
            size += self.sock.recv(1)
        size = int(size[:-1])
        data = b""
        while len(data) < size:
            data += self.sock.recv(size - len(data))
        return json.loads(data)

    def __call__(self, name, params=None):
        self.id += 1
        msg = json.dumps([0, self.id, name, params or {}]).encode()
        self.sock.sendall(b"%d:%s" % (len(msg), msg))
        _, _, error, result = self._read()
        if error:
            raise RuntimeError("%s: %s" % (name, error))
        return result

    def js(self, script, *args):
        return self("WebDriver:ExecuteScript", {"script": script, "args": list(args)})["value"]


def make_profile(path, stock, scheme=None):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    with open(os.path.join(path, "user.js"), "w") as f:
        for key, value in PREFS.items():
            f.write("user_pref(%s, %s);\n" % (json.dumps(key), json.dumps(value)))
    if not stock:
        # The same install the user runs, so the test covers it.
        open(os.path.join(path, "prefs.js"), "a").close()
        cmd = ["make", "-s", "-C", ROOT, "firefox-install", "PROFILE=" + os.path.abspath(path)]
        if scheme:
            cmd.append("FF_SCHEME=" + os.path.abspath(scheme))
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)


def gtk_config(profile, scheme):
    """A GTK config directory whose user CSS holds the given KDE scheme."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import kdecolors
    config = os.path.join(profile, "xdg-config")
    os.makedirs(os.path.join(config, "gtk-3.0"))
    # GTK reads the icon theme and title button layout from dconf, which also
    # lives under XDG_CONFIG_HOME. A copy, so nothing writes back to the user's.
    dconf = os.path.expanduser("~/.config/dconf")
    if os.path.isdir(dconf):
        shutil.copytree(dconf, os.path.join(config, "dconf"))
    with open(os.path.join(config, "gtk-3.0", "gtk.css"), "w") as f:
        f.write(kdecolors.gtk_css(scheme))
    # Firefox picks light or dark from the desktop's preference, not from the
    # GTK colours, and uses its own colours when the two disagree, so both
    # have to match the scheme.
    r, g, b = kdecolors.load(scheme)("Window", "BackgroundNormal")
    dark = (0.299 * r + 0.587 * g + 0.114 * b) < 128
    # Keep the user's fonts, icons and title button layout.
    settings = os.path.expanduser("~/.config/gtk-3.0/settings.ini")
    lines = open(settings).read().splitlines() if os.path.exists(settings) else ["[Settings]"]
    lines = [l for l in lines if not l.startswith(("gtk-application-prefer-dark-theme", "gtk-theme-name"))]
    lines.append("gtk-application-prefer-dark-theme=%s" % ("true" if dark else "false"))
    # Firefox swaps in libadwaita's colours when the theme is Adwaita.
    lines.append("gtk-theme-name=Oxygen")
    with open(os.path.join(config, "gtk-3.0", "settings.ini"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(profile, "user.js"), "a") as f:
        f.write("user_pref(\"ui.systemUsesDarkTheme\", %d);\n" % dark)
    return config


def main():
    profile, out = sys.argv[1], sys.argv[2]
    scheme = sys.argv[sys.argv.index("--colors") + 1] if "--colors" in sys.argv else None
    make_profile(profile, "--stock" in sys.argv, scheme)
    # --pref NAME=JSON adds a preference, for experiments.
    for i, a in enumerate(sys.argv):
        if a == "--pref":
            name, value = sys.argv[i + 1].split("=", 1)
            with open(os.path.join(profile, "user.js"), "a") as f:
                f.write("user_pref(%s, %s);\n" % (json.dumps(name), value))
    env = dict(os.environ, GTK_THEME="Oxygen", TZ="UTC")  # the same time zone everywhere
    if "--colors" in sys.argv:
        env["XDG_CONFIG_HOME"] = gtk_config(profile, sys.argv[sys.argv.index("--colors") + 1])
    ff = subprocess.Popen(
        ["firefox", "--marionette", "-remote-allow-system-access", "--no-remote", "--new-instance", "--profile", profile],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    try:
        m = Marionette(PORT)
        m("WebDriver:NewSession", {"capabilities": {}})
        m("Marionette:SetContext", {"value": "chrome"})
        m.js("Services.prefs.setBoolPref('sidebar.verticalTabs', arguments[0]);", "--vertical" in sys.argv)
        height = int(sys.argv[sys.argv.index("--height") + 1]) if "--height" in sys.argv else 600
        m("WebDriver:SetWindowRect", {"width": 1100, "height": height})
        m.js("""
            const win = Services.wm.getMostRecentWindow('navigator:browser');
            const gb = win.gBrowser;
            const pages = arguments[0];
            gb.loadURI(Services.io.newURI(pages[0]), {triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()});
            for (const url of pages.slice(1))
                gb.addTab(url, {triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()});
            gb.selectedTab = gb.tabs[1];
            if (arguments[1]) {
                gb.loadURI(Services.io.newURI(arguments[1]), {triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()});
            }
            if (arguments[2])
                InspectorUtils.addPseudoClassLock(gb.tabs[2], ":hover");
            if (arguments[3])
                InspectorUtils.addPseudoClassLock(win.document.getElementById(arguments[3]), ":hover");
        """, [PAGE.format(t) for t in ("Oxygen", "Selected tab", "Another tab", "Fourth tab")],
            "about:newtab" if "--newtab" in sys.argv else (sys.argv[sys.argv.index("--url") + 1] if "--url" in sys.argv else None),
            "--hover-tab" in sys.argv,
            sys.argv[sys.argv.index("--hover") + 1] if "--hover" in sys.argv else None)
        time.sleep(6 if "--newtab" in sys.argv or "--url" in sys.argv else 2.5)
        # Firefox marks a remote-controlled window with a striped address bar and a
        # robot icon, which only exist to warn the user; a real window has neither.
        m.js("Services.wm.getMostRecentWindow('navigator:browser').document.documentElement.removeAttribute('remotecontrol');")
        time.sleep(0.5)
        selectors = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--click"]
        theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else None
        if selectors or theme:
            m("Marionette:SetContext", {"value": "content"})
            m("WebDriver:SwitchToWindow", {"handle": m("WebDriver:GetWindowHandles")[1]})
            if theme:
                m.js(""
                     "document.body.className = document.body.className.replace(/\\b(light|dark|sepia|gray|contrast)\\b/, arguments[0]);", theme)
            for sel in selectors:
                el = m("WebDriver:FindElement", {"using": "css selector", "value": sel})["value"]
                m("WebDriver:ElementClick", {"id": list(el.values())[0]})
                time.sleep(0.6)
            m("Marionette:SetContext", {"value": "chrome"})
            time.sleep(0.5)
        shot = m("WebDriver:TakeScreenshot", {"full": False})["value"]
        with open(out, "wb") as f:
            f.write(base64.b64decode(shot))
        if "--wait" in sys.argv:
            ff.wait()
        else:
            m("Marionette:Quit", {"flags": ["eForceQuit"]})
    finally:
        try:
            ff.wait(timeout=10)
        except subprocess.TimeoutExpired:
            ff.kill()


if __name__ == "__main__":
    main()
