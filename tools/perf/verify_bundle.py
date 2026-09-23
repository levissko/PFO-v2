"""PHASE 10 — prove that site.min.css renders identically to the source CSS.

Loads every page twice (1440 and 375 wide, plus the open mobile menu):
  A) as built (site.min.css)
  B) same HTML, but the request for site.min.css is answered with the plain
     concatenation of tokens.css + components.css + site.css
and compares getComputedStyle() of every element (all properties) and
::before/::after. Custom properties (--*) keep their source text, so they are
compared with whitespace removed; all other properties are compared exactly. Any difference is printed. Needs a local server on 8765.
"""
import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/PFO-v2/"
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/", "news/",
         "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]
CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "PFO-v2", "assets", "css")
SRC = "".join(open(os.path.join(CSS, n), encoding="utf-8").read() + "\n" for n in ("tokens.css", "components.css", "site.css"))

SNAP = """() => [...document.querySelectorAll('*')].map((el, i) => {
  const out = {};
  for (const pseudo of [null, '::before', '::after']) {
    const cs = getComputedStyle(el, pseudo);
    for (let k = 0; k < cs.length; k++) { const n = cs[k]; out[(pseudo || '') + n] = cs.getPropertyValue(n); }
  }
  return [el.tagName + '.' + el.className, out];
})"""

diffs = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 375):
        for mode in ("min", "src"):
            ctx = b.new_context(viewport={"width": w, "height": 900}, reduced_motion="reduce")  # no transitions mid-snapshot
            if mode == "src":
                ctx.route("**/site.min.css*", lambda r: r.fulfill(status=200, content_type="text/css", body=SRC))
            pg = ctx.new_page()
            snaps = {}
            for u in PAGES:
                pg.goto(BASE + u)
                snaps[u] = pg.evaluate(SNAP)
                if w == 375:
                    pg.click("[data-menu-toggle]")
                    snaps[u + "#menu"] = pg.evaluate(SNAP)
                    pg.mouse.move(0, 0)
            if mode == "min": A = snaps
            else: B = snaps
            ctx.close()
        for u in A:
            for (ta, sa), (tb, sb) in zip(A[u], B[u]):
                for k in sa:
                    va, vb = sa[k], sb.get(k) or ""
                    if "--" in k:   # custom properties keep their raw text: compare without whitespace
                        va, vb = "".join(va.split()), "".join(vb.split())
                    if va != vb:
                        diffs += 1
                        if diffs <= 20: print("DIFF", w, u, ta, k, sa[k], "!=", sb.get(k))
        print(f"{w}px: {len(A)} page states, {sum(len(v) for v in A.values())} elements compared")
    b.close()
print("DIFFERENCES", diffs)
