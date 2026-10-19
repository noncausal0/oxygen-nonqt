# SPDX-License-Identifier: GPL-3.0-or-later
# PREFIX and DESTDIR follow the usual conventions: `make install` puts the
# theme in $(PREFIX)/share/themes/Oxygen.
PREFIX  ?= $(HOME)/.local
VERSION := $(shell cat VERSION)
SASS    ?= sassc
BUILD   := build/Oxygen
SASSFLAGS := -t expanded -I common/scss

COMMON := $(wildcard common/scss/*.scss)
ASSETS := $(notdir $(wildcard common/assets/*.svg))

all: gtk3 gtk4 $(BUILD)/index.theme

gtk3: $(BUILD)/gtk-3.0/gtk.css $(addprefix $(BUILD)/gtk-3.0/assets/,$(ASSETS))
gtk4: $(BUILD)/gtk-4.0/gtk.css $(BUILD)/gtk-4.0/libadwaita.css $(addprefix $(BUILD)/gtk-4.0/assets/,$(ASSETS))

$(BUILD)/gtk-3.0/gtk.css: gtk3/scss/gtk.scss $(wildcard gtk3/scss/*.scss) $(COMMON)
	@mkdir -p $(@D)
	$(SASS) $(SASSFLAGS) $< $@

$(BUILD)/gtk-4.0/gtk.css: gtk4/scss/gtk.scss $(wildcard gtk4/scss/*.scss) $(COMMON)
	@mkdir -p $(@D)
	$(SASS) $(SASSFLAGS) $< $@

$(BUILD)/gtk-4.0/libadwaita.css: gtk4/scss/libadwaita-user.scss $(wildcard gtk4/scss/*.scss) $(COMMON)
	@mkdir -p $(@D)
	$(SASS) $(SASSFLAGS) $< $@

$(BUILD)/gtk-3.0/assets/%.svg: common/assets/%.svg
	@mkdir -p $(@D)
	cp $< $@

$(BUILD)/gtk-4.0/assets/%.svg: common/assets/%.svg
	@mkdir -p $(@D)
	cp $< $@

$(BUILD)/index.theme: gtk3/index.theme
	@mkdir -p $(@D)
	cp $< $@

# --- Packages -----------------------------------------------------------------
#
# The GTK theme and the Firefox theme are two separate packages, each a tarball
# holding the finished files and small install scripts (no sassc or make
# needed to install them). `make dist` builds both into dist/.

PKG      := build/pkg
GTK_PKG  := $(PKG)/oxygen-gtk-$(VERSION)
FF_PKG   := $(PKG)/oxygen-firefox-$(VERSION)
# Fixed timestamps and ordering keep the tarballs reproducible.
EPOCH    := $(or $(SOURCE_DATE_EPOCH),$(shell git log -1 --format=%ct 2>/dev/null || echo 0))
TAR      := tar --sort=name --owner=0 --group=0 --numeric-owner --mtime=@$(EPOCH)

stage-gtk: all
	rm -rf $(GTK_PKG)
	mkdir -p $(GTK_PKG)
	cp -r $(BUILD) $(GTK_PKG)/Oxygen
	cp packaging/gtk/install.sh packaging/gtk/uninstall.sh packaging/gtk/oxygen-gtk-setup $(GTK_PKG)/
	cp packaging/gtk/README.md LICENSE $(GTK_PKG)/
	echo $(VERSION) > $(GTK_PKG)/VERSION

stage-firefox:
	rm -rf $(FF_PKG)
	mkdir -p $(FF_PKG)/data/tools
	cp -r firefox/chrome firefox/user.js $(FF_PKG)/data/
	cp -r packaging/firefox/systemd packaging/firefox/refresh-colors.sh $(FF_PKG)/data/
	cp tools/firefox_colors.py tools/compare/kdecolors.py $(FF_PKG)/data/tools/
	cp packaging/firefox/install.sh packaging/firefox/uninstall.sh packaging/firefox/oxygen-firefox-setup $(FF_PKG)/
	cp packaging/firefox/README.md LICENSE $(FF_PKG)/
	echo $(VERSION) > $(FF_PKG)/VERSION

dist: stage-gtk stage-firefox
	mkdir -p dist
	cd $(PKG) && $(TAR) -czf ../../dist/oxygen-gtk-$(VERSION).tar.gz oxygen-gtk-$(VERSION)
	cd $(PKG) && $(TAR) -czf ../../dist/oxygen-firefox-$(VERSION).tar.gz oxygen-firefox-$(VERSION)
	cd dist && sha256sum oxygen-*-$(VERSION).tar.gz > SHA256SUMS
	@cat dist/SHA256SUMS

# --- Installing from the source tree --------------------------------------------
#
# These run the packages' own scripts from the staged trees, so what is tested
# here is what users get.

install: stage-gtk
	PREFIX="$(PREFIX)" DESTDIR="$(DESTDIR)" $(GTK_PKG)/install.sh

uninstall: stage-gtk
	PREFIX="$(PREFIX)" DESTDIR="$(DESTDIR)" $(GTK_PKG)/uninstall.sh

# Firefox, per profile: make firefox-install PROFILE=<dir from about:profiles>
# (FF_SCHEME=<file>.colors picks a colour scheme other than the current one).
firefox-install: stage-firefox
	@test -n "$(PROFILE)" || { echo "Usage: make firefox-install PROFILE=<profile directory, see about:profiles>"; exit 1; }
	$(FF_PKG)/oxygen-firefox-setup install "$(PROFILE)" $(FF_SCHEME)

firefox-uninstall: stage-firefox
	@test -n "$(PROFILE)" || { echo "Usage: make firefox-uninstall PROFILE=<profile directory>"; exit 1; }
	$(FF_PKG)/oxygen-firefox-setup uninstall "$(PROFILE)"

# Refresh the new tab colours automatically when the KDE scheme changes. The
# unit needs the files installed, so this installs them into $(PREFIX) first.
firefox-watch-install: stage-firefox
	PREFIX="$(PREFIX)" $(FF_PKG)/install.sh
	"$(PREFIX)/bin/oxygen-firefox-setup" watch-enable

firefox-watch-uninstall: stage-firefox
	$(FF_PKG)/oxygen-firefox-setup watch-disable

clean:
	rm -rf build dist

.PHONY: all gtk3 gtk4 stage-gtk stage-firefox dist install uninstall clean \
	firefox-install firefox-uninstall firefox-watch-install firefox-watch-uninstall
