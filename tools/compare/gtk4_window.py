#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""GTK 4 counterpart of qt_window.py, plus a libadwaita page.

--files shows a mock of Nautilus's window (same widget types and style
classes) instead of the widget gallery; --list makes it the list view. --adw loads the built libadwaita.css from build/Oxygen as user CSS on top of
libadwaita, so nothing has to be installed. Without it the window uses the
GTK theme, so run it with GTK_THEME=Oxygen after `make install`. --colors FILE.colors applies a KDE
colour scheme to this process only (otherwise KDE's exported colours are
used), and --snapshot FILE.png renders the window and exits.
"""
import os
import sys
import warnings

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Graphene", "1.0")
gi.require_version("Adw", "1")
from gi.repository import Gdk, Gio, GLib, Graphene, Gtk  # noqa: E402

import kdecolors  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
BUILD = os.path.join(ROOT, "build", "Oxygen", "gtk-4.0")
FILES = "--files" in sys.argv
ADW = "--adw" in sys.argv or FILES
warnings.filterwarnings("ignore", category=DeprecationWarning)


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def add_css(path=None, data=None, priority=Gtk.STYLE_PROVIDER_PRIORITY_USER):
    p = Gtk.CssProvider()
    if path:
        p.load_from_file(Gio.File.new_for_path(path))
    else:
        p.load_from_string(data)
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), p, priority)


def vbox(spacing=6):
    return Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)


def frame(title, child):
    f = Gtk.Frame(label=title)
    for side in ("start", "end", "top", "bottom"):
        getattr(child, "set_margin_" + side)(6)
    f.set_child(child)
    return f


def widgets():
    grid = Gtk.Grid(row_spacing=8, column_spacing=8, column_homogeneous=True)
    for side in ("start", "end", "top", "bottom"):
        getattr(grid, "set_margin_" + side)(8)

    b = vbox()
    b.append(Gtk.Button(label="Normal"))
    default = Gtk.Button(label="Default")
    default.add_css_class("suggested-action")
    b.append(default)
    b.append(Gtk.ToggleButton(label="Toggled", active=True))
    b.append(Gtk.Button(label="Disabled", sensitive=False))
    tools = Gtk.Box(spacing=2)
    for icon in ("document-open", "document-save", "edit-copy"):
        t = Gtk.Button(icon_name=icon)
        t.add_css_class("flat")
        tools.append(t)
    b.append(tools)
    grid.attach(frame("Buttons", b), 0, 0, 1, 1)

    i = vbox()
    i.append(Gtk.Entry(text="Text entry"))
    i.append(Gtk.Entry(text="Disabled entry", sensitive=False))
    i.append(Gtk.DropDown.new_from_strings(["Drop down", "Second"]))
    combo = Gtk.ComboBoxText.new_with_entry()
    for t in ("Editable combo", "Second"):
        combo.append_text(t)
    combo.set_active(0)
    i.append(combo)
    spin = Gtk.SpinButton.new_with_range(0, 99, 1)
    spin.set_value(42)
    i.append(spin)
    grid.attach(frame("Inputs", i), 1, 0, 1, 1)

    c = vbox()
    c.append(Gtk.CheckButton(label="Unchecked"))
    c.append(Gtk.CheckButton(label="Checked", active=True))
    c.append(Gtk.CheckButton(label="Partial", inconsistent=True))
    r1 = Gtk.CheckButton(label="Radio on", active=True)
    c.append(r1)
    c.append(Gtk.CheckButton(label="Radio off", group=r1))
    c.append(Gtk.CheckButton(label="Disabled", active=True, sensitive=False))
    grid.attach(frame("Checks", c), 2, 0, 1, 1)

    r = vbox()
    scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    scale.set_value(40)
    r.append(scale)
    r.append(Gtk.ProgressBar(fraction=0.6, show_text=True))
    r.append(Gtk.Switch(active=True, halign=Gtk.Align.START))
    grid.attach(frame("Ranges", r), 0, 1, 1, 1)

    nb = Gtk.Notebook()
    for name in ("First", "Second", "Third"):
        nb.append_page(Gtk.Box(), Gtk.Label(label=name))
    grid.attach(nb, 1, 1, 1, 1)

    model = Gtk.StringList.new(["Item %d" % n for n in range(1, 30)])
    factory = Gtk.SignalListItemFactory()
    factory.connect("setup", lambda _f, item: item.set_child(Gtk.Label(xalign=0)))
    factory.connect("bind", lambda _f, item: item.get_child().set_label(item.get_item().get_string()))
    selection = Gtk.SingleSelection(model=model)
    selection.set_selected(2)
    view = Gtk.ListView(model=selection, factory=factory)
    scroller = Gtk.ScrolledWindow(has_frame=True, vexpand=True)
    scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
    scroller.set_child(view)
    grid.attach(scroller, 2, 1, 1, 1)
    return grid


def adw_page():
    from gi.repository import Adw
    page = vbox(12)
    for side in ("start", "end", "top", "bottom"):
        getattr(page, "set_margin_" + side)(12)

    group = Adw.PreferencesGroup(title="Preferences group", description="A boxed list of rows")
    row = Adw.ActionRow(title="Action row", subtitle="With a subtitle", activatable=True)
    row.add_suffix(Gtk.Image(icon_name="go-next-symbolic"))
    group.add(row)
    group.add(Adw.SwitchRow(title="Switch row", active=True))
    group.add(Adw.EntryRow(title="Entry row"))
    group.add(Adw.ComboRow(title="Combo row", model=Gtk.StringList.new(["One", "Two"])))
    group.add(Adw.SpinRow.new_with_range(0, 10, 1))
    page.append(group)

    buttons = Gtk.Box(spacing=8, halign=Gtk.Align.CENTER)
    pill = Gtk.Button(label="Pill button")
    pill.add_css_class("pill")
    buttons.append(pill)
    sug = Gtk.Button(label="Suggested")
    sug.add_css_class("suggested-action")
    sug.add_css_class("pill")
    buttons.append(sug)
    dest = Gtk.Button(label="Destructive")
    dest.add_css_class("destructive-action")
    buttons.append(dest)
    page.append(buttons)

    card = Gtk.Label(label="A card", margin_top=16, margin_bottom=16)
    card_box = Gtk.Box()
    card_box.add_css_class("card")
    card_box.append(card)
    card.set_hexpand(True)
    page.append(card_box)
    return page


def files_window(app):
    """Nautilus's layout: a view-coloured window, a sidebar with places and a
    toolbar with a path bar over a grid of files."""
    from gi.repository import Adw
    win = Adw.ApplicationWindow(application=app, title="Home")
    win.add_css_class("view")
    split = Adw.OverlaySplitView(max_sidebar_width=240, sidebar_width_fraction=0.2)

    side = Adw.ToolbarView()
    shb = Adw.HeaderBar(title_widget=Adw.WindowTitle(title="Files"), show_end_title_buttons=False)
    shb.pack_start(Gtk.ToggleButton(icon_name="edit-find-symbolic"))
    shb.pack_end(Gtk.MenuButton(icon_name="open-menu-symbolic"))
    side.add_top_bar(shb)
    places = Gtk.ListBox()
    places.add_css_class("navigation-sidebar")
    for icon, name in (("user-home", "Home"), ("document-open-recent", "Recent"), ("starred", "Starred"),
                       ("network-workgroup", "Network"), ("user-trash", "Trash")):
        row = Gtk.Box(spacing=8)
        row.append(Gtk.Image(icon_name=icon))
        row.append(Gtk.Label(label=name, xalign=0))
        places.append(row)
    places.select_row(places.get_row_at_index(0))
    side.set_content(Gtk.ScrolledWindow(child=places, vexpand=True))
    split.set_sidebar(side)

    content = Adw.ToolbarView()
    hb = Adw.HeaderBar(show_start_title_buttons=False)
    for icon in ("go-previous-symbolic", "go-next-symbolic"):
        hb.pack_start(Gtk.Button(icon_name=icon))
    path = Gtk.Box(hexpand=True)
    path.add_css_class("nautilus-pathbar")
    for name, current in (("/", False), ("home", False), ("Home", True)):
        b = Gtk.Button(label=name)
        b.add_css_class("flat")
        b.add_css_class("nautilus-path-button")
        if current:
            b.add_css_class("current-dir")
        path.append(b)
    hb.set_title_widget(path)
    hb.pack_end(Gtk.MenuButton(icon_name="view-more-symbolic"))
    content.add_top_bar(hb)
    names = ["Applications", "Documents", "Downloads", "Music", "Pictures",
             "Public", "Templates", "Videos", "cat.jpg", "notes.txt"]
    if "--list" in sys.argv:
        names *= 3  # enough rows for a scroll bar, as in a real folder
    model = Gtk.StringList.new(names)
    factory = Gtk.SignalListItemFactory()
    def setup(_f, item):
        cell = vbox(4)
        cell.append(Gtk.Image(pixel_size=64))
        cell.append(Gtk.Label())
        item.set_child(cell)
    def bind(_f, item):
        name = item.get_item().get_string()
        cell = item.get_child()
        cell.get_first_child().set_from_icon_name("folder" if "." not in name else "image-x-generic")
        cell.get_last_child().set_label(name)
    factory.connect("setup", setup)
    factory.connect("bind", bind)
    selection = Gtk.SingleSelection(model=model)
    selection.set_selected(1)
    view = Gtk.Box()
    if "--list" in sys.argv:
        # Nautilus's own style sheet (padding, row radius), when it is installed,
        # so the list view is laid out as in the real app.
        try:
            import subprocess
            css = subprocess.run(["gresource", "extract", "/usr/bin/nautilus", "/org/gnome/nautilus/style.css"],
                                 capture_output=True, check=True).stdout
            add_css(data=css.decode(), priority=Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except (OSError, subprocess.CalledProcessError):
            pass
        # Classic scroll bars, which Oxygen uses, take space from the list.
        Gtk.Settings.get_default().set_property("gtk-overlay-scrolling", "--overlay" in sys.argv)
        columns = Gtk.ColumnView(model=selection)
        view.add_css_class("nautilus-list-view")
        sizes = ("4 items", "3 items", "11 items", "9 items", "2 items", "1 item", "0 items", "5 items", "56.8 kB", "1.2 kB")
        for title, text in (("Name", None), ("Size", sizes * 3), ("Modified", ("Last week",) * 30)):
            f = Gtk.SignalListItemFactory()
            def lsetup(_f, item):
                label = Gtk.Label(xalign=0)
                label.add_css_class("nautilus-view-cell")
                item.set_child(label)
            def lbind(_f, item, text=text):
                label = item.get_child()
                label.set_label(item.get_item().get_string() if text is None else text[item.get_position()])
            f.connect("setup", lsetup)
            f.connect("bind", lbind)
            col = Gtk.ColumnViewColumn(title=title, factory=f, expand=title == "Name", resizable=True)
            columns.append_column(col)
        view.append(Gtk.ScrolledWindow(child=columns, hexpand=True, vexpand=True))
    else:
        grid = Gtk.GridView(model=selection, factory=factory, max_columns=6)
        view.add_css_class("nautilus-grid-view")
        view.append(Gtk.ScrolledWindow(child=grid, hexpand=True, vexpand=True))
    content.set_content(view)
    split.set_content(content)

    win.set_content(split)
    win.set_default_size(1000, 640)
    return win


def build(app):
    if FILES:
        add_css(os.path.join(BUILD, "libadwaita.css"))
        win = files_window(app)
    elif ADW:
        from gi.repository import Adw
        add_css(os.path.join(BUILD, "libadwaita.css"))
        win = Adw.ApplicationWindow(application=app, title="Oxygen libadwaita")
        tv = Adw.ToolbarView()
        hb = Adw.HeaderBar()
        hb.pack_start(Gtk.Button(icon_name="list-add-symbolic"))
        hb.pack_end(Gtk.MenuButton(icon_name="open-menu-symbolic"))
        tv.add_top_bar(hb)
        tabs = Adw.TabView()
        bar = Adw.TabBar(view=tabs, autohide=False)
        tv.add_top_bar(bar)
        content = Gtk.Box()
        content.append(adw_page())
        content.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        content.append(widgets())
        tabs.append(content).set_title("First tab")
        tabs.append(Gtk.Box()).set_title("Second tab")
        tv.set_content(tabs)
        win.set_content(tv)
        win.set_default_size(1180, 560)
    else:
        win = Gtk.ApplicationWindow(application=app, title="Oxygen GTK 4")
        hb = Gtk.HeaderBar()
        hb.pack_start(Gtk.Button(icon_name="document-open"))
        win.set_titlebar(hb)
        box = vbox(0)
        menu = Gio.Menu()
        for name in ("File", "Edit", "View", "Help"):
            sub = Gio.Menu()
            sub.append("Open…", "app.open")
            menu.append_submenu(name, sub)
        box.append(Gtk.PopoverMenuBar.new_from_model(menu))
        box.append(widgets())
        win.set_child(box)
        win.set_default_size(720, 480)

    if arg("--colors"):
        add_css(data=kdecolors.gtk_css(arg("--colors")), priority=Gtk.STYLE_PROVIDER_PRIORITY_USER + 1)

    win.present()
    if arg("--snapshot"):
        GLib.timeout_add(1500, snapshot, win, arg("--snapshot"), app)


def snapshot(win, path, app):
    w, h = win.get_width(), win.get_height()
    paintable = Gtk.WidgetPaintable.new(win)
    snap = Gtk.Snapshot()
    paintable.snapshot(snap, w, h)
    node = snap.to_node()
    texture = win.get_native().get_renderer().render_texture(node, Graphene.Rect().init(0, 0, w, h))
    texture.save_to_png(path)
    app.quit()
    return False


def main():
    if ADW:
        from gi.repository import Adw
        app = Adw.Application(application_id="org.oxygen.compare.Adw")
    else:
        app = Gtk.Application(application_id="org.oxygen.compare.Gtk4")
    app.connect("activate", build)
    app.run([])


if __name__ == "__main__":
    main()
