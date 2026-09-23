"""PHASE 10 — Lighthouse runner.

Runs Lighthouse (mobile + desktop presets) on the main pages and prints a
score table. Results (JSON) go to tools/perf/reports/<label>/.

Usage (from repo root, with a local server running):
    python -m http.server 8765
    python tools/perf/lighthouse_run.py --base http://localhost:8765/PFO-v2/ --label test

Requires: Node.js + `npm install lighthouse` (CLI on PATH or via npx),
and Chrome/Chromium (set CHROME_PATH if not auto-detected).
"""
import argparse, json, os, subprocess, sys

PAGES = [("home", ""), ("about", "about/"), ("services", "services/"),
         ("products", "products/"), ("trixo", "products/trixo/"),
         ("news-article", "news/2014-02-21-trixo-hand-cream/"), ("contact", "contact/")]
CATS = ["performance", "accessibility", "best-practices", "seo"]

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://localhost:8765/PFO-v2/")
ap.add_argument("--label", default="run")
ap.add_argument("--lighthouse", default=os.environ.get("LIGHTHOUSE_BIN", "npx lighthouse"))
a = ap.parse_args()

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", a.label)
os.makedirs(outdir, exist_ok=True)
rows, low = [], []
for form in ("mobile", "desktop"):
    for name, path in PAGES:
        out = os.path.join(outdir, f"{form}-{name}.json")
        cmd = a.lighthouse.split() + [a.base + path, "--quiet", "--output=json", f"--output-path={out}",
               "--chrome-flags=--headless=new --no-sandbox", f"--only-categories={','.join(CATS)}"]
        if form == "desktop":
            cmd.append("--preset=desktop")
        subprocess.run(cmd, check=True)
        r = json.load(open(out, encoding="utf-8"))
        sc = {c: round(r["categories"][c]["score"] * 100) for c in CATS}
        au = r["audits"]
        m = {k: au[k]["displayValue"] for k in ("first-contentful-paint", "largest-contentful-paint",
                                                 "total-blocking-time", "cumulative-layout-shift", "speed-index")}
        m["bytes"] = au["total-byte-weight"]["numericValue"]
        rows.append((form, name, sc, m))
        # failing audits (score < 1, scored, not informative)
        for c in CATS:
            for ref in r["categories"][c]["auditRefs"]:
                x = au[ref["id"]]
                if ref["weight"] and x.get("score") is not None and x["score"] < 1:
                    low.append((form, name, c, ref["id"], x["score"], x.get("displayValue", "")))

print(f"\n{'form':8}{'page':14}{'Perf':>5}{'A11y':>5}{'BP':>5}{'SEO':>5}  FCP / LCP / TBT / CLS / SI / bytes")
for form, name, sc, m in rows:
    print(f"{form:8}{name:14}{sc['performance']:>5}{sc['accessibility']:>5}{sc['best-practices']:>5}{sc['seo']:>5}  "
          f"{m['first-contentful-paint']} / {m['largest-contentful-paint']} / {m['total-blocking-time']} / "
          f"{m['cumulative-layout-shift']} / {m['speed-index']} / {m['bytes']/1024:.1f} KiB")
print("\nAudits below 100%:")
for l in low: print("  ", l)
json.dump([{"form": f, "page": n, "scores": s, "metrics": m} for f, n, s, m in rows],
          open(os.path.join(outdir, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fails = [r for r in rows if min(r[2].values()) < 90]
print("\nPAGES BELOW 90:", len(fails))
sys.exit(1 if fails else 0)
