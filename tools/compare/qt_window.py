#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Reference window: common widgets in the native Qt Oxygen style.

Mirrors gtk3_window.py widget for widget, so screenshots can be compared.
Takes the same --snapshot FILE.png and --colors FILE.colors options.
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLineEdit, QListWidget, QMainWindow, QProgressBar, QPushButton,
    QRadioButton, QSlider, QSpinBox, QTabWidget, QToolButton, QVBoxLayout,
    QWidget,
)


def main():
    app = QApplication(sys.argv)
    app.setStyle("oxygen")
    if "--colors" in sys.argv:
        app.setPalette(palette(sys.argv[sys.argv.index("--colors") + 1]))
    win = QMainWindow()
    win.setWindowTitle("Oxygen Qt reference")
    menu = win.menuBar()
    for name in ("File", "Edit", "View", "Help"):
        m = menu.addMenu(name)
        m.addAction("Open…")
        m.addAction("Save")
        m.addSeparator()
        m.addAction("Quit")

    central = QWidget()
    grid = QGridLayout(central)

    buttons = QGroupBox("Buttons")
    b = QVBoxLayout(buttons)
    b.addWidget(QPushButton("Normal"))
    default = QPushButton("Default")
    default.setDefault(True)
    b.addWidget(default)
    toggled = QPushButton("Toggled")
    toggled.setCheckable(True)
    toggled.setChecked(True)
    b.addWidget(toggled)
    disabled = QPushButton("Disabled")
    disabled.setEnabled(False)
    b.addWidget(disabled)
    tools = QHBoxLayout()
    for icon in ("document-open", "document-save", "edit-copy"):
        t = QToolButton()
        t.setAutoRaise(True)
        from PyQt6.QtGui import QIcon
        t.setIcon(QIcon.fromTheme(icon))
        tools.addWidget(t)
    tools.addStretch()
    b.addLayout(tools)
    grid.addWidget(buttons, 0, 0)

    inputs = QGroupBox("Inputs")
    i = QVBoxLayout(inputs)
    i.addWidget(QLineEdit("Text entry"))
    off = QLineEdit("Disabled entry")
    off.setEnabled(False)
    i.addWidget(off)
    combo = QComboBox()
    combo.addItems(["Combo box", "Second"])
    i.addWidget(combo)
    ecombo = QComboBox()
    ecombo.setEditable(True)
    ecombo.addItems(["Editable combo", "Second"])
    i.addWidget(ecombo)
    spin = QSpinBox()
    spin.setValue(42)
    i.addWidget(spin)
    grid.addWidget(inputs, 0, 1)

    checks = QGroupBox("Checks")
    c = QVBoxLayout(checks)
    c.addWidget(QCheckBox("Unchecked"))
    on = QCheckBox("Checked")
    on.setChecked(True)
    c.addWidget(on)
    tri = QCheckBox("Partial")
    tri.setTristate(True)
    tri.setCheckState(Qt.CheckState.PartiallyChecked)
    c.addWidget(tri)
    r1 = QRadioButton("Radio on")
    r1.setChecked(True)
    c.addWidget(r1)
    c.addWidget(QRadioButton("Radio off"))
    dis = QCheckBox("Disabled")
    dis.setChecked(True)
    dis.setEnabled(False)
    c.addWidget(dis)
    grid.addWidget(checks, 0, 2)

    ranges = QGroupBox("Ranges")
    r = QVBoxLayout(ranges)
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setValue(40)
    r.addWidget(slider)
    bar = QProgressBar()
    bar.setValue(60)
    r.addWidget(bar)
    r.addStretch()
    grid.addWidget(ranges, 1, 0)

    tabs = QTabWidget()
    for name in ("First", "Second", "Third"):
        tabs.addTab(QWidget(), name)
    grid.addWidget(tabs, 1, 1)

    lst = QListWidget()
    lst.addItems(["Item %d" % n for n in range(1, 30)])
    lst.setCurrentRow(2)
    grid.addWidget(lst, 1, 2)

    win.setCentralWidget(central)
    win.resize(720, 480)
    if "--snapshot" in sys.argv:
        win.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
        win.show()
        app.processEvents()
        win.grab().save(sys.argv[sys.argv.index("--snapshot") + 1])
        return
    win.show()
    sys.exit(app.exec())


def palette(path):
    import kdecolors
    c = kdecolors.load(path)
    roles = {
        QPalette.ColorRole.Window: ("Window", "BackgroundNormal"),
        QPalette.ColorRole.WindowText: ("Window", "ForegroundNormal"),
        QPalette.ColorRole.Base: ("View", "BackgroundNormal"),
        QPalette.ColorRole.AlternateBase: ("View", "BackgroundAlternate"),
        QPalette.ColorRole.Text: ("View", "ForegroundNormal"),
        QPalette.ColorRole.Button: ("Button", "BackgroundNormal"),
        QPalette.ColorRole.ButtonText: ("Button", "ForegroundNormal"),
        QPalette.ColorRole.Highlight: ("Selection", "BackgroundNormal"),
        QPalette.ColorRole.HighlightedText: ("Selection", "ForegroundNormal"),
        QPalette.ColorRole.ToolTipBase: ("Tooltip", "BackgroundNormal"),
        QPalette.ColorRole.ToolTipText: ("Tooltip", "ForegroundNormal"),
        QPalette.ColorRole.Link: ("View", "ForegroundLink"),
    }
    pal = QPalette()
    for role, key in roles.items():
        pal.setColor(role, QColor(*c(*key)))
    for role in (QPalette.ColorRole.WindowText, QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText):
        pal.setColor(QPalette.ColorGroup.Disabled, role, QColor(*c("Window", "ForegroundInactive")))
    return pal


if __name__ == "__main__":
    main()
