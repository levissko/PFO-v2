# PFO_NewWeb — tools/a11y/axe_run.py (PHASE 9)
# Requires: pip install playwright && python -m playwright install chromium
#           npm install axe-core   (axe_run.py only; or set AXE_PATH)
# Serve the repo root first:  python -m http.server 8765
# Base URL override: PFO_BASE=http://host/path/
import os
import json, sys
from playwright.sync_api import sync_playwright
AXE = open(os.environ.get('AXE_PATH', 'node_modules/axe-core/axe.min.js')).read()
BASE = os.environ.get("PFO_BASE", "http://localhost:8765/PFO-v2/")
PAGES = ["", "about/", "services/", "products/", "products/trixo/", "products/idpn/", "news/", "news/2014-02-21-trixo-hand-cream/", "contact/", "404.html"]
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]
agg = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 375):
        pg = b.new_page(viewport={"width": w, "height": 900})
        for u in PAGES:
            states = ["default"] + (["menu-open"] if w == 375 and u in ("", "products/trixo/") else [])
            for st in states:
                pg.goto(BASE + u); pg.wait_for_timeout(80)
                if st == "menu-open": pg.click("[data-menu-toggle]"); pg.wait_for_timeout(80)
                pg.add_script_tag(content=AXE)
                r = pg.evaluate("""async (tags) => { const r = await axe.run(document, {runOnly:{type:'tag', values: tags}, resultTypes:['violations','incomplete']}); 
                   return {v: r.violations.map(x=>({id:x.id, impact:x.impact, tags:x.tags.filter(t=>t.startsWith('wcag')), help:x.help, nodes:x.nodes.map(n=>({t:n.target.join(' '), s:n.failureSummary}))})),
                           i: r.incomplete.map(x=>({id:x.id, n:x.nodes.length, nodes:x.nodes.slice(0,3).map(n=>n.target.join(' '))}))}; }""", TAGS)
                key = f"{w}|{u or 'index'}|{st}"
                agg[key] = r
                print(key, "violations:", [(v['id'], v['impact'], len(v['nodes'])) for v in r['v']], "incomplete:", [(i['id'], i['n']) for i in r['i']])
    b.close()
json.dump(agg, open('axe-report.json', 'w'), ensure_ascii=False, indent=1)
