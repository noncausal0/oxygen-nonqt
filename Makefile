# SPDX-License-Identifier: GPL-3.0-or-later
PREFIX ?= $(HOME)/.local/share/themes
SASS   ?= sassc
BUILD  := build/Oxygen

ASSETS := $(patsubst gtk3/assets/%,$(BUILD)/gtk-3.0/assets/%,$(wildcard gtk3/assets/*.svg))

all: $(BUILD)/gtk-3.0/gtk.css $(ASSETS) $(BUILD)/index.theme

$(BUILD)/gtk-3.0/assets/%.svg: gtk3/assets/%.svg
	@mkdir -p $(@D)
	cp $< $@

$(BUILD)/gtk-3.0/gtk.css: $(wildcard gtk3/scss/*.scss)
	@mkdir -p $(@D)
	$(SASS) -t expanded gtk3/scss/gtk.scss $@

$(BUILD)/index.theme: gtk3/index.theme
	@mkdir -p $(@D)
	cp $< $@

install: all
	rm -rf $(PREFIX)/Oxygen
	mkdir -p $(PREFIX)
	cp -r $(BUILD) $(PREFIX)/Oxygen

uninstall:
	rm -rf $(PREFIX)/Oxygen

clean:
	rm -rf build

.PHONY: all install uninstall clean
