"""PHASE 11 — Hero text contrast over the background photo (WCAG 1.4.3, 4.5:1).

For every RWD width: hide the hero text (color: transparent), screenshot, then
for each text element take the BRIGHTEST background pixel inside its box and
compute the contrast with the text colour. Worst case, not average.
Needs a local server on 8765 and Playwright + Pillow.
"""
import io, os
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
WIDTHS = [1920, 1440, 1280, 1024, 768, 430, 390, 375]
# text elements drawn directly on the photo (the solid white button is excluded: it has its own background)
TARGETS = ".pfo-hero h1, .pfo-hero__lead, .pfo-hero .pfo-btn--ghost-inverse, .pfo-hero__caption"


def lum(rgb):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


worst, fails = 99, 0
with sync_playwright() as p:
    br = p.chromium.launch()
    for w in WIDTHS:
        ctx = br.new_context(viewport={"width": w, "height": 1000}, reduced_motion="reduce", device_scale_factor=1)
        pg = ctx.new_page(); pg.goto(BASE); pg.wait_for_load_state("networkidle")
        items = pg.evaluate(f"""() => [...document.querySelectorAll('{TARGETS}')].map(e => {{
            const r = e.getBoundingClientRect(), c = getComputedStyle(e).color.match(/\\d+/g).map(Number);
            return {{name: e.tagName + '.' + e.className.split(' ')[0], x: r.x, y: r.y, w: r.width, h: r.height, color: c}}; }})""")
        pg.add_style_tag(content=f"{TARGETS}, {TARGETS} * {{ color: transparent !important; }} .pfo-hero .pfo-btn--ghost-inverse {{ border-color: transparent !important; }}")
        shot = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
        for it in items:
            # the caption pill has rounded corners: skip the 4px corner/edge band outside the pill
            k = 4 if "caption" in it["name"] else 0
            box = (int(it["x"]) + k, int(it["y"]) + k, int(it["x"] + it["w"]) - k, int(it["y"] + it["h"]) - k)
            raw = shot.crop(box).tobytes()
            px = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
            brightest = max(px, key=lum)
            cr = ratio(it["color"], brightest)
            worst = min(worst, cr)
            ok = cr >= 4.5
            fails += not ok
            print(f"{w:>5}  {it['name']:<28} text rgb{tuple(it['color'][:3])}  brightest bg rgb{brightest}  {cr:5.2f}:1  {'ok' if ok else 'FAIL'}")
        ctx.close()
    br.close()
print(f"\nWORST {worst:.2f}:1   FAILS {fails}")
