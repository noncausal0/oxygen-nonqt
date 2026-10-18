# SPDX-License-Identifier: GPL-3.0-or-later
PREFIX  ?= $(HOME)/.local/share/themes
GTK4CFG ?= $(HOME)/.config/gtk-4.0
SASS    ?= sassc
BUILD   := build/Oxygen
SASSFLAGS := -t expanded -I common/scss

COMMON := $(wildcard common/scss/*.scss)
ASSETS := $(notdir $(wildcard common/assets/*.svg))

# libadwaita only reads user CSS, so install hooks the theme's libadwaita
# stylesheet into the user's gtk.css with this line.
IMPORT := @import url("file://$(PREFIX)/Oxygen/gtk-4.0/libadwaita.css");

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

install: all
	rm -rf $(PREFIX)/Oxygen
	mkdir -p $(PREFIX)
	cp -r $(BUILD) $(PREFIX)/Oxygen
	@mkdir -p $(GTK4CFG)
	@touch $(GTK4CFG)/gtk.css
	@grep -qF '$(IMPORT)' $(GTK4CFG)/gtk.css || { \
		if [ -n "$$(tail -c1 $(GTK4CFG)/gtk.css)" ]; then echo >> $(GTK4CFG)/gtk.css; fi; \
		echo '$(IMPORT)' >> $(GTK4CFG)/gtk.css; \
		echo "Added libadwaita import to $(GTK4CFG)/gtk.css"; }

uninstall:
	rm -rf $(PREFIX)/Oxygen
	@if [ -f $(GTK4CFG)/gtk.css ]; then grep -vF '$(IMPORT)' $(GTK4CFG)/gtk.css > $(GTK4CFG)/gtk.css.tmp; mv $(GTK4CFG)/gtk.css.tmp $(GTK4CFG)/gtk.css; fi

clean:
	rm -rf build

.PHONY: all gtk3 gtk4 install uninstall clean
