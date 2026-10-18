#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""GTK 3 counterpart of qt_window.py, for side-by-side comparison.

Run with GTK_THEME=Oxygen. Pass --csd for a headerbar instead of a menu bar,
or --snapshot FILE.png to render offscreen and exit, which avoids depending on
window focus. --colors FILE.colors applies a KDE colour scheme to this
process only.
"""
import sys

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk  # noqa: E402

import kdecolors  # noqa: E402


def frame(title, child):
    f = Gtk.Frame(label=title)
    child.set_border_width(6)
    f.add(child)
    return f


def vbox():
    return Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)


def main():
    csd = "--csd" in sys.argv
    snapshot = sys.argv[sys.argv.index("--snapshot") + 1] if "--snapshot" in sys.argv else None
    if "--colors" in sys.argv:
        css = Gtk.CssProvider()
        css.load_from_data(kdecolors.gtk_css(sys.argv[sys.argv.index("--colors") + 1]).encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)
    win = Gtk.OffscreenWindow() if snapshot else Gtk.Window(title="Oxygen GTK 3")
    win.connect("destroy", Gtk.main_quit)
    outer = vbox()
    outer.set_spacing(0)

    if csd and not snapshot:
        hb = Gtk.HeaderBar(title="Oxygen GTK 3", show_close_button=True)
        hb.pack_start(Gtk.Button.new_from_icon_name("document-open", Gtk.IconSize.BUTTON))
        hb.pack_end(Gtk.MenuButton())
        win.set_titlebar(hb)
    else:
        bar = Gtk.MenuBar()
        for name in ("File", "Edit", "View", "Help"):
            item = Gtk.MenuItem(label=name)
            menu = Gtk.Menu()
            for label in ("Open…", "Save", None, "Quit"):
                menu.append(Gtk.SeparatorMenuItem() if label is None else Gtk.MenuItem(label=label))
            item.set_submenu(menu)
            bar.append(item)
        outer.pack_start(bar, False, False, 0)

    grid = Gtk.Grid(row_spacing=8, column_spacing=8, column_homogeneous=True)
    grid.set_border_width(8)

    b = vbox()
    b.add(Gtk.Button(label="Normal"))
    default = Gtk.Button(label="Default")
    default.get_style_context().add_class("suggested-action")
    b.add(default)
    toggled = Gtk.ToggleButton(label="Toggled", active=True)
    b.add(toggled)
    b.add(Gtk.Button(label="Disabled", sensitive=False))
    tools = Gtk.Box(spacing=2)
    for icon in ("document-open", "document-save", "edit-copy"):
        t = Gtk.Button.new_from_icon_name(icon, Gtk.IconSize.LARGE_TOOLBAR)
        t.set_relief(Gtk.ReliefStyle.NONE)
        tools.add(t)
    b.add(tools)
    grid.attach(frame("Buttons", b), 0, 0, 1, 1)

    i = vbox()
    i.add(Gtk.Entry(text="Text entry"))
    i.add(Gtk.Entry(text="Disabled entry", sensitive=False))
    combo = Gtk.ComboBoxText()
    for t in ("Combo box", "Second"):
        combo.append_text(t)
    combo.set_active(0)
    i.add(combo)
    ecombo = Gtk.ComboBoxText.new_with_entry()
    for t in ("Editable combo", "Second"):
        ecombo.append_text(t)
    ecombo.set_active(0)
    i.add(ecombo)
    spin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spin.set_value(42)
    i.add(spin)
    grid.attach(frame("Inputs", i), 1, 0, 1, 1)

    c = vbox()
    c.add(Gtk.CheckButton(label="Unchecked"))
    c.add(Gtk.CheckButton(label="Checked", active=True))
    c.add(Gtk.CheckButton(label="Partial", inconsistent=True))
    r1 = Gtk.RadioButton(label="Radio on")
    c.add(r1)
    c.add(Gtk.RadioButton.new_with_label_from_widget(r1, "Radio off"))
    c.add(Gtk.CheckButton(label="Disabled", active=True, sensitive=False))
    grid.attach(frame("Checks", c), 2, 0, 1, 1)

    r = vbox()
    scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    scale.set_draw_value(False)
    scale.set_value(40)
    r.add(scale)
    bar = Gtk.ProgressBar(fraction=0.6, show_text=True)
    r.add(bar)
    sw = Gtk.Switch(active=True)
    sw.set_halign(Gtk.Align.START)
    r.add(sw)
    grid.attach(frame("Ranges", r), 0, 1, 1, 1)

    nb = Gtk.Notebook()
    for name in ("First", "Second", "Third"):
        nb.append_page(Gtk.Box(), Gtk.Label(label=name))
    grid.attach(nb, 1, 1, 1, 1)

    store = Gtk.ListStore(str)
    for n in range(1, 30):
        store.append(["Item %d" % n])
    view = Gtk.TreeView(model=store, headers_visible=False)
    view.append_column(Gtk.TreeViewColumn("Item", Gtk.CellRendererText(), text=0))
    view.get_selection().select_path(Gtk.TreePath(2))
    scroller = Gtk.ScrolledWindow(shadow_type=Gtk.ShadowType.IN)
    scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
    scroller.set_overlay_scrolling(False)
    scroller.add(view)
    grid.attach(scroller, 2, 1, 1, 1)

    outer.pack_start(grid, True, True, 0)
    win.add(outer)
    win.set_default_size(720, 480)
    win.show_all()
    if snapshot:
        win.set_size_request(720, 480)
        while Gtk.events_pending():
            Gtk.main_iteration()
        win.get_pixbuf().savev(snapshot, "png", [], [])
        return
    Gtk.main()


if __name__ == "__main__":
    main()
