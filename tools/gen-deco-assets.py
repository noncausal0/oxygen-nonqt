#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write the title button images to common/assets/.

Each image is a whole Oxygen title button: rim, face, a soft white highlight
and the glyph. GTK recolours the classed shapes from CSS (success = face,
warning = rim, error = glyph). The highlight is two translucent ellipses. GTK 3
leaves ellipses alone, while GTK 4 paints every unclassed shape in the CSS
`color`, so the stylesheet sets that to white. Gradients do not survive GTK 4's
recolouring, hence stacked ellipses rather than one gradient.
"""
import os

GLYPHS = {
    "minimize": '<path class="error" d="M5.6 8.3 6.8 7.1 10 10.3 13.2 7.1 14.4 8.3 10 12.7Z"/>',
    "maximize": '<path class="error" d="M5.6 11.7 6.8 12.9 10 9.7 13.2 12.9 14.4 11.7 10 7.3Z"/>',
    "restore": '<path class="error" fill-rule="evenodd" d="M10 5.3 14.7 10 10 14.7 5.3 10Z M10 7.8 7.8 10 10 12.2 12.2 10Z"/>',
    "close": '<rect class="error" x="9.1" y="4.9" width="1.8" height="10.2" rx="0.9" transform="rotate(45 10 10)"/>'
             '<rect class="error" x="9.1" y="4.9" width="1.8" height="10.2" rx="0.9" transform="rotate(-45 10 10)"/>',
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <circle class="warning" cx="10" cy="10" r="9"/>
  <circle class="success" cx="10" cy="10" r="8"/>
  <ellipse cx="10" cy="7.6" rx="6.6" ry="5" fill="#fff" fill-opacity="0.1"/>
  <ellipse cx="10" cy="6.4" rx="5" ry="3.4" fill="#fff" fill-opacity="0.12"/>
  {glyph}
</svg>
"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common", "assets")
for name, glyph in GLYPHS.items():
    with open(os.path.join(out, "deco-%s-symbolic.svg" % name), "w") as f:
        f.write(TEMPLATE.replace("{glyph}", glyph))
