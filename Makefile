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

# Firefox, per profile: make firefox-install PROFILE=<dir from about:profiles>.
# The theme goes into chrome/oxygen/ and is pulled in by one @import line, so
# an existing userChrome.css keeps working; the prefs it needs go into user.js
# between markers. firefox-uninstall removes exactly those again.
FF_IMPORT := @import url("oxygen/userChrome.css");
FF_BEGIN  := // oxygen-nonqt begin
FF_END    := // oxygen-nonqt end

firefox-check:
	@test -n "$(PROFILE)" || { echo "Usage: make $(MAKECMDGOALS) PROFILE=<profile directory, see about:profiles>"; exit 1; }
	@test -f "$(PROFILE)/prefs.js" || { echo "$(PROFILE) does not look like a Firefox profile (no prefs.js)"; exit 1; }

firefox-install: firefox-check
	rm -rf "$(PROFILE)/chrome/oxygen"
	mkdir -p "$(PROFILE)/chrome"
	cp -r firefox/chrome "$(PROFILE)/chrome/oxygen"
	@touch "$(PROFILE)/chrome/userChrome.css"
	@grep -qF '$(FF_IMPORT)' "$(PROFILE)/chrome/userChrome.css" || { \
		{ echo '$(FF_IMPORT)'; cat "$(PROFILE)/chrome/userChrome.css"; } > "$(PROFILE)/chrome/userChrome.css.tmp"; \
		mv "$(PROFILE)/chrome/userChrome.css.tmp" "$(PROFILE)/chrome/userChrome.css"; }
	@touch "$(PROFILE)/user.js"
	@grep -qF '$(FF_BEGIN)' "$(PROFILE)/user.js" || { \
		if [ -n "$$(tail -c1 "$(PROFILE)/user.js")" ]; then echo >> "$(PROFILE)/user.js"; fi; \
		{ echo '$(FF_BEGIN)'; cat firefox/user.js; echo '$(FF_END)'; } >> "$(PROFILE)/user.js"; }
	@echo "Installed into $(PROFILE). Restart Firefox."

firefox-uninstall: firefox-check
	rm -rf "$(PROFILE)/chrome/oxygen"
	@if [ -f "$(PROFILE)/chrome/userChrome.css" ]; then \
		grep -vF '$(FF_IMPORT)' "$(PROFILE)/chrome/userChrome.css" > "$(PROFILE)/chrome/userChrome.css.tmp"; \
		mv "$(PROFILE)/chrome/userChrome.css.tmp" "$(PROFILE)/chrome/userChrome.css"; fi
	@if [ -f "$(PROFILE)/user.js" ]; then \
		sed '\|^$(FF_BEGIN)$$|,\|^$(FF_END)$$|d' "$(PROFILE)/user.js" > "$(PROFILE)/user.js.tmp"; \
		mv "$(PROFILE)/user.js.tmp" "$(PROFILE)/user.js"; fi
	@echo "Removed from $(PROFILE). Prefs already applied stay set in prefs.js until changed in about:config."

.PHONY: all gtk3 gtk4 install uninstall clean firefox-check firefox-install firefox-uninstall
