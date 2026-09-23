"""PFO_NewWeb — tools/seo_audit.py (PHASE 8)
Static SEO checks on the generated site. Python 3 standard library only.
Usage: python tools/seo_audit.py
"""
import glob, html.parser, json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PFO-v2"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Head(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = {}; self.links = {}; self.title = ""; self._t = False
        self._ld = False; self.ld = []; self.base = None; self.h1 = 0
    def handle_starttag(self, tag, a):
        d = dict(a)
        if tag == "title": self._t = True
        if tag == "h1": self.h1 += 1
        if tag == "base": self.base = d.get("href")
        if tag == "meta":
            k = d.get("name") or d.get("property")
            if k: self.meta[k] = d.get("content", "")
        if tag == "link": self.links.setdefault(d.get("rel"), []).append(d.get("href"))
        if tag == "script" and d.get("type") == "application/ld+json": self._ld = True; self.ld.append("")
    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag == "script": self._ld = False
    def handle_data(self, data):
        if self._t: self.title += data
        if self._ld: self.ld[-1] += data

sm = ET.parse(os.path.join(ROOT, "sitemap.xml")).getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
sitemap_urls = [u.find("s:loc", ns).text for u in sm.findall("s:url", ns)]
problems = []
REQ_OG = ["og:type", "og:site_name", "og:locale", "og:title", "og:description", "og:image",
          "og:image:width", "og:image:height", "og:image:alt", "twitter:card"]
titles, descs, canons = {}, {}, {}
for f in sorted(glob.glob(ROOT + "/**/*.html", recursive=True)):
    rel = os.path.relpath(f, ROOT)
    h = Head(); h.feed(open(f, encoding="utf-8").read())
    is404 = rel == "404.html"
    t, d = h.title.strip(), h.meta.get("description", "")
    titles[rel], descs[rel] = t, d
    if not t: problems.append((rel, "missing title"))
    if len(t) > 40: problems.append((rel, f"title long ({len(t)} chars)"))
    if not (20 <= len(d) <= 160) and not is404: problems.append((rel, f"description length {len(d)}"))
    for k in REQ_OG:
        if k not in h.meta: problems.append((rel, f"missing {k}"))
    for rel_ in ("icon", "apple-touch-icon"):
        for href in h.links.get(rel_, []):
            target = os.path.normpath(os.path.join(ROOT if is404 else os.path.dirname(f), href))
            if not os.path.exists(target): problems.append((rel, f"{rel_} file missing: {href}"))
    if h.h1 != 1: problems.append((rel, f"h1 count {h.h1}"))
    if is404:
        if "noindex" not in h.meta.get("robots", ""): problems.append((rel, "404 must be noindex"))
        if h.links.get("canonical"): problems.append((rel, "404 must not have canonical"))
        continue
    c = (h.links.get("canonical") or [None])[0]
    canons[rel] = c
    if not c: problems.append((rel, "missing canonical")); continue
    if c not in sitemap_urls: problems.append((rel, "canonical not in sitemap"))
    if h.meta.get("og:url") != c: problems.append((rel, "og:url != canonical"))
    types = []
    for block in h.ld:
        try:
            obj = json.loads(block.replace("<\\/", "</"))
        except Exception as e:
            problems.append((rel, f"JSON-LD parse error {e}")); continue
        types.append(obj.get("@type"))
        if obj.get("@context") != "https://schema.org": problems.append((rel, "bad @context"))
        if obj.get("@type") == "BreadcrumbList":
            items = obj["itemListElement"]
            if [i["position"] for i in items] != list(range(1, len(items) + 1)): problems.append((rel, "breadcrumb positions"))
            if items[-1]["item"] != c: problems.append((rel, "breadcrumb last item != canonical"))
            if any(not i["item"].startswith("https://") for i in items): problems.append((rel, "breadcrumb url not absolute"))
        if obj.get("@type") == "Organization":
            for k in ("name", "url", "logo", "address", "telephone", "email"):
                if k not in obj: problems.append((rel, f"Organization missing {k}"))
    if rel != "index.html" and "BreadcrumbList" not in types: problems.append((rel, "missing BreadcrumbList"))
    print(f"{rel:48s} title={len(t):2d} desc={len(d):3d} ld={types}")

for name, dct in (("title", titles), ("description", descs)):
    vals = list(dct.values())
    dup = {v for v in vals if vals.count(v) > 1}
    if dup: problems.append(("*", f"duplicate {name}: {dup}"))
if len(set(sitemap_urls)) != len(sitemap_urls): problems.append(("sitemap", "duplicate urls"))
if set(sitemap_urls) != set(canons.values()): problems.append(("sitemap", "sitemap != canonical set"))
print(f"sitemap urls: {len(sitemap_urls)}")
for p in problems: print("PROBLEM", p)
print("PROBLEMS", len(problems))
sys.exit(1 if problems else 0)
