# PFO_NewWeb — tools/a11y/textzoom.py (PHASE 9)
# Requires: pip install playwright && python -m playwright install chromium
#           npm install axe-core   (axe_run.py only; or set AXE_PATH)
# Serve the repo root first:  python -m http.server 8765
# Base URL override: PFO_BASE=http://host/path/
import os
"""WCAG 1.4.4 resize text: root font-size 200% at 1280 (text-only zoom) + a11y tree spot check."""
from playwright.sync_api import sync_playwright
BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/", "news/", "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 800})
    for u in PAGES:
        pg.goto(BASE + u); pg.add_style_tag(content="html { font-size: 200% !important; }")
        r = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth,
           overlap: (() => { const n = document.querySelector('.pfo-nav'); if (!n || n.offsetParent === null) return 0;
                             const items = [...n.querySelectorAll('a')].map(a => a.getBoundingClientRect()); return new Set(items.map(r => Math.round(r.top))).size; })(),
           clipped: [...document.querySelectorAll('h1,h2,h3,p,a,li,dd')].filter(e => e.offsetParent && !e.closest('.visually-hidden') && !e.classList.contains('pfo-clamp-2') && getComputedStyle(e).overflow !== 'visible' && e.scrollWidth > e.clientWidth + 1).length})""")
        if r["sw"] > 1280 or r["clipped"]: bad.append((u or "index", r))
        print("200% text", u or "index", r)
        pg.goto(BASE); pg.add_style_tag(content="html { font-size: 200% !important; }"); pg.screenshot(path="textzoom-home.png")
    # accessibility tree of the header + first section (what a screen reader hears)
    pg.set_viewport_size({"width": 375, "height": 800}); pg.goto(BASE + "products/trixo/")
    snap = pg.accessibility.snapshot()
    def walk(n, d=0, out=[]):
        if d < 4 and n.get("role") not in ("generic", "none", "StaticText", "InlineTextBox"):
            out.append("  " * d + f"{n.get('role')}: {n.get('name','')[:40]}")
        for c in n.get("children", [])[:12]: walk(c, d + 1, out)
        return out
    print("\n".join(walk(snap)[:45]))
    b.close()
print("TEXT-ZOOM PROBLEMS", bad)
