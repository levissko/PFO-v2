# PFO_NewWeb — tools/a11y/sr_zoom.py (PHASE 9)
# Requires: pip install playwright && python -m playwright install chromium
#           npm install axe-core   (axe_run.py only; or set AXE_PATH)
# Serve the repo root first:  python -m http.server 8765
# Base URL override: PFO_BASE=http://host/path/
import os
"""Screen-reader structure, focus-ring contrast, reduced motion, reflow (200%/400%), text spacing."""
from playwright.sync_api import sync_playwright
BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/", "news/", "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]
problems = []

STRUCT = r"""() => {
  const out = {};
  // landmarks
  const lm = [...document.querySelectorAll('header, nav, main, footer, aside, section[aria-label], section[aria-labelledby], [role=region], [role=note]')]
     .filter(e => { const s = getComputedStyle(e); return s.display !== 'none' && !e.closest('[hidden]'); })
     .map(e => { const role = e.getAttribute('role') || {HEADER:'banner',NAV:'navigation',MAIN:'main',FOOTER:'contentinfo',ASIDE:'complementary',SECTION:'region'}[e.tagName];
                 let name = e.getAttribute('aria-label') || (e.getAttribute('aria-labelledby') && document.getElementById(e.getAttribute('aria-labelledby'))?.textContent.trim()) || '';
                 // header/footer only count as landmarks when not inside main/section
                 return role + (name ? `「${name}」` : ''); });
  out.landmarks = lm;
  // duplicate navigation labels
  const navs = lm.filter(x => x.startsWith('navigation'));
  out.dupNav = navs.filter((x, i) => navs.indexOf(x) !== i);
  // unlabeled navs
  out.unlabeledNav = navs.filter(x => x === 'navigation');
  // links/buttons accessible name
  out.noName = [...document.querySelectorAll('a[href], button')].filter(e => e.offsetParent !== null || e.closest('.pfo-skip'))
     .filter(e => !(e.getAttribute('aria-label') || e.textContent.trim() || e.querySelector('img[alt]:not([alt=""])'))).map(e => e.outerHTML.slice(0, 80));
  // aria-hidden with focusable descendants
  out.hiddenFocusable = [...document.querySelectorAll('[aria-hidden="true"]')].filter(e => e.querySelector('a[href],button,input,[tabindex]:not([tabindex="-1"])')).length;
  // svg icons not hidden
  out.svgNotHidden = [...document.querySelectorAll('svg')].filter(s => !s.closest('[aria-hidden="true"]') && s.getAttribute('aria-hidden') !== 'true' && !s.getAttribute('role')).length;
  // role=img must have name
  out.imgNoName = [...document.querySelectorAll('[role=img]')].filter(e => !e.getAttribute('aria-label')).length;
  // same link text pointing to different URLs (2.4.4 ambiguity)
  const map = {};
  [...document.querySelectorAll('a[href]')].filter(e => e.offsetParent !== null).forEach(a => {
     const n = (a.getAttribute('aria-label') || a.textContent).trim().replace(/\s+/g, ' ');
     (map[n] = map[n] || new Set()).add(new URL(a.getAttribute('href'), location.href).pathname); });
  out.ambiguous = Object.entries(map).filter(([k, v]) => v.size > 1).map(([k, v]) => k + ' → ' + [...v].join(', '));
  // headings outline
  out.headings = [...document.querySelectorAll('h1,h2,h3,h4')].map(h => h.tagName[1] + ':' + h.textContent.trim().slice(0, 14)).join(' | ');
  // lang attributes on English-only text blocks
  out.lang = document.documentElement.lang;
  // new-window links announce it
  out.newWindowUnannounced = [...document.querySelectorAll('a[target=_blank]')].filter(a => !/新視窗/.test(a.textContent)).length;
  return out;
}"""

RING = r"""() => {
  // focus ring colour vs. the background right behind the element
  const lum = c => { const m = c.match(/\d+(\.\d+)?/g).map(Number); const f = v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
                     return .2126 * f(m[0]) + .7152 * f(m[1]) + .0722 * f(m[2]); };
  const bgOf = el => { for (let n = el.parentElement; n; n = n.parentElement) { const b = getComputedStyle(n).backgroundColor; if (b && !/rgba\(0, 0, 0, 0\)|transparent/.test(b)) return b; } return 'rgb(255, 255, 255)'; };
  const res = [];
  for (const el of document.querySelectorAll('a[href], button')) {
    if (el.offsetParent === null) continue;
    el.focus({preventScroll: true});
    if (document.activeElement !== el) continue;
    const s = getComputedStyle(el); const oc = s.outlineColor; const bg = bgOf(el);
    const a = lum(oc), b = lum(bg); const cr = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    if (cr < 3) res.push([(el.getAttribute('aria-label') || el.textContent).trim().slice(0, 16), oc, bg, cr.toFixed(2)]);
  }
  document.activeElement.blur();
  return res;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------- structure + focus ring contrast ----------
    for w in (1440, 375):
        pg = b.new_page(viewport={"width": w, "height": 900})
        for u in PAGES:
            pg.goto(BASE + u)
            s = pg.evaluate(STRUCT)
            tag = f"{w}|{u or 'index'}"
            if w == 1440: print(tag, "landmarks:", s["landmarks"]); print("   headings:", s["headings"])
            for k in ("dupNav", "unlabeledNav", "noName", "ambiguous"):
                if s[k]: problems.append((tag, k, s[k]))
            for k in ("hiddenFocusable", "svgNotHidden", "imgNoName", "newWindowUnannounced"):
                if s[k]: problems.append((tag, k, s[k]))
            if s["lang"] != "zh-Hant-TW": problems.append((tag, "lang", s["lang"]))
            r = pg.evaluate(RING)
            if r: problems.append((tag, "focus ring contrast < 3:1", r))
        pg.close()

    # ---------- reduced motion ----------
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page(); pg.goto(BASE)
    rm = pg.evaluate("""() => ({scroll: getComputedStyle(document.documentElement).scrollBehavior,
        dur: getComputedStyle(document.querySelector('.pfo-card')).transitionDuration,
        btn: getComputedStyle(document.querySelector('.pfo-btn')).transitionDuration,
        lift: getComputedStyle(document.documentElement).getPropertyValue('--card-lift-hover').trim(),
        animations: document.getAnimations().length})""")
    print("reduced-motion:", rm)
    if rm["scroll"] != "auto" or any(x not in ("0s",) for x in rm["dur"].split(", ")) or rm["lift"] not in ("0",):
        problems.append(("reduced-motion", rm))
    ctx.close()

    # ---------- reflow: 200% zoom of 1280 = 640 CSS px; 400% = 320 CSS px (WCAG 1.4.10) ----------
    for w in (640, 320):
        pg = b.new_page(viewport={"width": w, "height": 512})
        for u in PAGES:
            pg.goto(BASE + u)
            r = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth,
                clipped: [...document.querySelectorAll('h1,h2,h3,p,a,li,dd,span')].filter(e => e.offsetParent && !e.closest('.visually-hidden') && getComputedStyle(e).overflow !== 'visible' && !e.classList.contains('pfo-clamp-2') && e.scrollWidth > e.clientWidth + 1).length})""")
            if r["sw"] > w or r["clipped"]: problems.append((f"reflow {w}|{u or 'index'}", r))
        pg.close()
    print("reflow 640/320 checked")

    # ---------- text spacing (WCAG 1.4.12) ----------
    pg = b.new_page(viewport={"width": 375, "height": 800})
    for u in PAGES:
        pg.goto(BASE + u)
        pg.add_style_tag(content="* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; } p { margin-bottom: 2em !important; }")
        r = pg.evaluate("""() => ({sw: document.documentElement.scrollWidth,
            clipped: [...document.querySelectorAll('h1,h2,h3,p,a,li,dd,dt,span,time')].filter(e => e.offsetParent && !e.closest('.visually-hidden') && !e.classList.contains('pfo-clamp-2') && (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 2) && getComputedStyle(e).overflow !== 'visible').map(e => e.textContent.trim().slice(0, 12))})""")
        if r["sw"] > 375 or r["clipped"]: problems.append((f"text-spacing|{u or 'index'}", r))
    pg.close()
    print("text spacing checked")
    b.close()

for pr in problems: print("PROBLEM", pr)
print("PROBLEMS", len(problems))
