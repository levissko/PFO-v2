# PFO_NewWeb — tools/a11y/kbd.py (PHASE 9)
# Requires: pip install playwright && python -m playwright install chromium
#           npm install axe-core   (axe_run.py only; or set AXE_PATH)
# Serve the repo root first:  python -m http.server 8765
# Base URL override: PFO_BASE=http://host/path/
import os
"""Keyboard / focus audit."""
import json
from playwright.sync_api import sync_playwright
BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/", "news/", "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]

INFO = r"""() => {
  const el = document.activeElement;
  if (!el || el === document.body) return {body: true};
  const r = el.getBoundingClientRect();
  const s = getComputedStyle(el);
  const hdr = document.querySelector('.pfo-header');
  const hb = hdr ? hdr.getBoundingClientRect().bottom : 0;
  const inHeader = !!el.closest('.pfo-header');
  return {
    tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '',
    text: (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g,' ').slice(0, 24),
    w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top), bottom: Math.round(r.bottom),
    vh: innerHeight,
    outline: s.outlineStyle + ' ' + s.outlineWidth + ' ' + s.outlineColor,
    ring: (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2) || (s.boxShadow && s.boxShadow !== 'none'),
    ariaHiddenAncestor: !!el.closest('[aria-hidden="true"]'),
    obscured: (() => { const cx = Math.min(Math.max(r.left + r.width/2, 1), innerWidth-1), cy = Math.min(Math.max(r.top + Math.min(r.height/2, 10), 1), innerHeight-1);
                       const hit = document.elementFromPoint(cx, cy); return !(hit && (hit === el || el.contains(hit))); })(),
    offscreen: r.bottom < 0 || r.top > innerHeight,
  };
}"""

report = {}
problems = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 375):
        ctx = b.new_context(viewport={"width": w, "height": 800}, reduced_motion="reduce")
        pg = ctx.new_page()
        for u in PAGES:
            pg.goto(BASE + u); pg.wait_for_timeout(60)
            seq = []
            for i in range(80):
                pg.keyboard.press("Tab")
                info = pg.evaluate(INFO)
                if info.get("body"):
                    break
                key = (info["tag"], info["text"], info["top"] + int(pg.evaluate("scrollY")))
                if seq and key == seq[0]["key"]:
                    break
                info["key"] = key
                seq.append(info)
                where = f"{w}|{u or 'index'}|#{i+1} {info['tag']} '{info['text']}'"
                if not info["ring"]: problems.append((where, "no visible focus ring", info["outline"]))
                if info["ariaHiddenAncestor"]: problems.append((where, "focusable inside aria-hidden"))
                if info["obscured"]: problems.append((where, "obscured by sticky header", info["top"]))
                if info["offscreen"]: problems.append((where, "focused element off-screen"))
                if info["w"] == 0 or info["h"] == 0: problems.append((where, "zero-size focus target"))
            else:
                problems.append((f"{w}|{u}", "no end of tab sequence within 80 presses (trap?)"))
            report[f"{w}|{u or 'index'}"] = [f"{s['tag']}:{s['text']}" for s in seq]
            # first stop must be skip link, and Enter must move focus into main
            if not seq or "跳至主要內容" not in seq[0]["text"]:
                problems.append((f"{w}|{u}", "first tab stop is not the skip link"))
            pg.goto(BASE + u); pg.keyboard.press("Tab"); pg.keyboard.press("Enter"); pg.wait_for_timeout(50)
            if pg.evaluate("document.activeElement.id") != "main":
                problems.append((f"{w}|{u}", "skip link does not move focus to main"))
        # mobile menu keyboard flow
        if w == 375:
            pg.goto(BASE)
            for _ in range(10):
                pg.keyboard.press("Tab")
                if pg.evaluate("document.activeElement.hasAttribute('data-menu-toggle')"): break
            pg.keyboard.press("Enter"); pg.wait_for_timeout(50)
            first = pg.evaluate("document.activeElement.textContent.trim()")
            inside = []
            for _ in range(20):
                pg.keyboard.press("Tab")
                inside.append(pg.evaluate("!!document.activeElement.closest('.pfo-header')"))
            pg.keyboard.press("Shift+Tab")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(50)
            back = pg.evaluate("document.activeElement.hasAttribute('data-menu-toggle')")
            hidden = pg.evaluate("document.getElementById('mobile-menu').hidden")
            report["menu"] = {"first": first, "all_inside": all(inside), "esc_returns": back, "closed": hidden}
            if first != "關於我們" or not all(inside) or not back or not hidden:
                problems.append(("menu", report["menu"]))
            # background reachable by screen reader while open?
            pg.click("[data-menu-toggle]")
            report["menu"]["main_inert"] = pg.evaluate("document.getElementById('main').inert")
        ctx.close()
    b.close()

for k, v in report.items():
    if k != "menu": print(k, len(v), "stops")
print("menu", report.get("menu"))
print("sample 1440|index:", report["1440|index"])
for pr in problems: print("PROBLEM", pr)
print("PROBLEMS", len(problems))
