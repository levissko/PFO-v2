"""PFO_NewWeb — tools/rwd_audit.py (PHASE 7 RWD audit: 8 widths x 10 pages)

Requires: pip install playwright && python -m playwright install chromium
Usage:    (1) serve the repo root:  python -m http.server 8765
          (2) python tools/rwd_audit.py            # checks only
              python tools/rwd_audit.py 768 375    # also save full-page screenshots for these widths
Checks:   horizontal overflow, clipped text, touch targets < 44px (< 1024 wide),
          font size < 13px, desktop/mobile nav mode, header rows, grid columns.
"""
import os
import json, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/",
         "news/", "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]
WIDTHS = [1920, 1440, 1280, 1024, 768, 430, 390, 375]
SHOT = set(sys.argv[1:])  # widths to screenshot, e.g. 1024 768

JS = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const out = {vw, scrollW: document.documentElement.scrollWidth, issues: []};
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0 && !el.closest('[hidden]') && !el.closest('.visually-hidden'); };
  // 1. elements poking out of the viewport (ignore decorative hero mark, which is clipped by overflow:hidden)
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el) || el.closest('.pfo-hero__mark') || el.closest('.pfo-skip')) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) { out.issues.push(['overflow', el.tagName + '.' + (el.className.baseVal ?? el.className), Math.round(r.left), Math.round(r.right)]); }
  }
  // 2. text clipped inside its own box
  for (const el of document.querySelectorAll('h1,h2,h3,h4,p,a,li,dd,dt,span,time,button')) {
    if (!vis(el)) continue;
    const s = getComputedStyle(el);
    if (el.classList.contains('pfo-clamp-2')) continue;
    if (s.overflow !== 'visible' && el.scrollWidth > el.clientWidth + 1)
      out.issues.push(['clipped-x', el.tagName + '.' + el.className, el.textContent.trim().slice(0, 20)]);
  }
  // 3. touch targets (links/buttons) < 44px tall on touch widths; inline links inside running text are exempt (WCAG 2.5.5 inline exception)
  if (vw < 1024) {
    for (const el of document.querySelectorAll('a[href], button')) {
      if (!vis(el)) continue;
      const r = el.getBoundingClientRect();
      const inline = getComputedStyle(el).display === 'inline' && el.parentElement.closest('p,dd,li') && !el.parentElement.closest('.pfo-footer__links, .pfo-mobile-menu, nav');
      if (!inline && (r.height < 43.5 || r.width < 24))
        out.issues.push(['touch<44', el.tagName + '.' + el.className, el.textContent.trim().slice(0, 16), Math.round(r.width) + 'x' + Math.round(r.height)]);
    }
  }
  // 4. font-size floor 13px
  for (const el of document.querySelectorAll('p,li,dd,dt,a,span,time,h1,h2,h3,h4,button')) {
    if (!vis(el) || !el.textContent.trim()) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 13) out.issues.push(['font<13', el.tagName + '.' + el.className, fs]);
  }
  // 5. navigation mode
  const nav = document.querySelector('.pfo-nav'), burger = document.querySelector('[data-menu-toggle]');
  out.nav = vis(nav) ? 'desktop' : 'mobile';
  out.burger = vis(burger);
  // 6. header geometry: single row?
  const hi = document.querySelector('.pfo-header__inner').getBoundingClientRect();
  out.headerH = Math.round(hi.height);
  const items = [...document.querySelectorAll('.pfo-nav__link')].filter(vis).map(e => Math.round(e.getBoundingClientRect().top));
  out.navRows = new Set(items).size;
  const logo = document.querySelector('.pfo-header__logo').getBoundingClientRect();
  const navR = nav && vis(nav) ? nav.getBoundingClientRect() : null;
  out.logoNavGap = navR ? Math.round(navR.left - logo.right) : null;
  // 7. heading wraps: count lines of H1
  const h1 = document.querySelector('h1'); const lh = parseFloat(getComputedStyle(h1).lineHeight);
  out.h1Lines = Math.round(h1.getBoundingClientRect().height / lh);
  // 8. grid columns in use
  out.grids = [...document.querySelectorAll('.pfo-grid')].map(g => getComputedStyle(g).gridTemplateColumns.split(' ').length);
  out.contentW = Math.round((document.querySelector('main .pfo-container') || document.body).getBoundingClientRect().width);
  return out;
}
"""

def dedupe(issues):
    seen, res = set(), []
    for i in issues:
        k = tuple(i[:3])
        if k not in seen:
            seen.add(k); res.append(i)
    return res

results = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in WIDTHS:
        ctx = b.new_context(viewport={"width": w, "height": 900}, is_mobile=w < 768, has_touch=w < 1024, device_scale_factor=1)
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        for i, u in enumerate(PAGES):
            pg.goto(BASE + u); pg.wait_for_timeout(80)
            r = pg.evaluate(JS)
            r["issues"] = dedupe(r["issues"])
            results[f"{w}|{u or 'index'}"] = r
            if str(w) in SHOT:
                os.makedirs("rwd-shots", exist_ok=True); pg.screenshot(path=f"rwd-shots/{w}_{i}.png", full_page=True)
        results[f"{w}|errors"] = errs
        ctx.close()
    b.close()

json.dump(results, open("rwd-report.json", "w"), ensure_ascii=False, indent=1)
tot = 0
for k, r in results.items():
    if k.endswith("errors"):
        if r: print(k, r)
        continue
    n = len(r["issues"]); tot += n
    flag = "" if (r["scrollW"] <= r["vw"] and n == 0) else "  <-- "
    print(f'{k:48s} sw={r["scrollW"]:5d} nav={r["nav"]:7s} hdrH={r["headerH"]:3d} rows={r["navRows"]} gap={r["logoNavGap"]} h1L={r["h1Lines"]} grids={r["grids"]} cw={r["contentW"]} issues={n}{flag}')
    for i in r["issues"][:6]:
        print("      ", i)
print("TOTAL ISSUES", tot)
