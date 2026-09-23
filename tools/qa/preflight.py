"""PFO_NewWeb — PHASE 11 上線前檢查（preflight）。只用 Python 標準函式庫，Windows 可直接執行。

用法（專案根目錄）：
    python tools/qa/preflight.py            # 檢查「正式版」：IS_PRODUCTION = True 產生的結果
    python tools/qa/preflight.py --test     # 檢查「測試版」：應該是 noindex、有測試橫幅

檢查項目：
  1. 設定：robots meta、測試橫幅、canonical／sitemap 網址一致、robots.txt、deploy 檔是否仍是測試版
  2. 資源：CSS／JS 的 ?v= 版本號與檔案內容相符、壓縮檔比原始檔新、引用的檔案都存在
  3. 圖片：沒有多餘的中繼資料（XMP、C2PA）、logo.webp 存在；暫用圖（G1 前）提出警告
  4. 內容：畫面文字不得出現彩新數據、舊資本額、英文名稱、[NEEDS CONFIRMATION] 等標記
  5. 連結：站內連結都指向存在的檔案

結果：PASS / WARN / FAIL。有 FAIL 時結束代碼為 1，請勿上傳。
"""
import hashlib, html.parser, os, re, sys, urllib.parse
import xml.etree.ElementTree as ET

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SITE = os.path.join(REPO, "PFO-v2")
DEPLOY = os.path.join(REPO, "deploy")
TEST = "--test" in sys.argv

# 暫用圖（PHASE 8 產生）的 MD5：檔案仍是這些值 = 尚未換成正式 Logo（G1）
PLACEHOLDERS = {
    "assets/img/og-default.png": "cbc2071d428d685046d26736a69abfe1",
    "assets/icons/favicon.svg": "2e03a1bbe09d359a672481d301ce3288",
    "assets/icons/favicon.ico": "db41da3614332bbead0a7fbd101ee4a5",
    "assets/icons/apple-touch-icon.png": "70e799c848603d075782c09d8f3d5d1a",
}
# 畫面上絕對不可出現的字串（H1、H2、H3 決策）
FORBIDDEN = [
    ("彩新", "H1：不使用彩新資料"), ("28家", "H1：彩新數據"), ("28 家", "H1：彩新數據"),
    ("500床", "H1：彩新數據"), ("500 床", "H1：彩新數據"), ("22,000", "H1：彩新數據"), ("22000", "H1：彩新數據"),
    ("PFL renal", "H2：不放英文名稱"), ("112,000,000", "H3：舊資本額已過時"),
    ("[NEEDS CONFIRMATION]", "待確認標記不可出現在畫面"), ("[PROPOSED", "建議標記不可出現在畫面"),
    ("PLACEHOLDER", "暫用字樣"), ("TODO", "未完成標記"), ("lorem", "假文"),
]
METADATA_MARKERS = [b"c2pa", b"C2PA", b"jumb", b"XMP DataXMP", b"<x:xmpmeta", b"<metadata"]

results = []
def rec(level, msg): results.append((level, msg))


class Page(html.parser.HTMLParser):
    """Collect head info, visible text (no comments/script/style) and all href/src/srcset."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots = None; self.canonical = None; self.base = None; self.html_cls = ""
        self.banner = False; self.refs = []; self.text = []; self._skip = 0
    def handle_starttag(self, tag, a):
        d = dict(a)
        if tag == "html": self.html_cls = d.get("class") or ""
        if tag in ("script", "style"): self._skip += 1
        if tag == "meta" and d.get("name") == "robots": self.robots = d.get("content")
        if tag == "link" and d.get("rel") == "canonical": self.canonical = d.get("href")
        if tag == "base": self.base = d.get("href")
        if "pfo-review-banner" in (d.get("class") or ""): self.banner = True
        for k in ("href", "src"):
            if d.get(k): self.refs.append((tag, d.get("rel"), d[k]))
        if d.get("srcset"):
            for part in d["srcset"].split(","):
                self.refs.append((tag, None, part.strip().split(" ")[0]))
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self._skip -= 1
    def handle_data(self, data):
        if not self._skip: self.text.append(data)


def md5(p): return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    if not os.path.isdir(SITE):
        print("找不到 PFO-v2/ 資料夾"); return 1
    pages = sorted(os.path.relpath(os.path.join(dp, f), SITE).replace(os.sep, "/")
                   for dp, _, fs in os.walk(SITE) for f in fs if f.endswith(".html"))

    # ---------- sitemap ----------
    try:
        locs = [e.text for e in ET.parse(os.path.join(SITE, "sitemap.xml")).getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    except Exception as e:
        locs = []; rec("FAIL", f"sitemap.xml 無法解析：{e}")
    site_url = min(locs, key=len) if locs else ""          # 首頁網址 = 最短的 loc
    parsed = urllib.parse.urlsplit(site_url)
    base_path = parsed.path or "/"
    rec("PASS" if len(locs) == len(pages) - 1 else "FAIL", f"sitemap.xml：{len(locs)} 個網址（頁面 {len(pages)}，扣除 404）")
    if locs and not all(l.startswith(site_url) for l in locs):
        rec("FAIL", "sitemap 網址不在同一個網站路徑下")
    print(f"網站網址（取自 sitemap）：{site_url}\n檢查模式：{'測試版' if TEST else '正式版'}\n")

    # ---------- pages ----------
    visible_hits, missing, bad_robots, bad_banner, bad_canon = [], set(), [], [], []
    for rel in pages:
        p = Page(); p.feed(open(os.path.join(SITE, rel), encoding="utf-8").read())
        is404 = rel == "404.html"
        r = p.robots or ""
        ok = r.startswith("noindex") if (TEST or is404) else r == "index, follow"
        if not ok:
            bad_robots.append(f"{rel}: {r or '（沒有 robots meta）'}")
        if TEST != (p.banner and "is-review" in p.html_cls):
            bad_banner.append(rel)
        if not is404:
            want = site_url + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
            if p.canonical != want or want not in locs:
                bad_canon.append(f"{rel}: {p.canonical}")
        else:
            if p.base != base_path: rec("FAIL", f"404.html 的 <base href> = {p.base}，應為 {base_path}")
        # visible text
        text = " ".join(p.text)
        for s, why in FORBIDDEN:
            hit = (s.lower() in text.lower()) if s == "lorem" else (s in text)
            if hit:
                visible_hits.append(f"{rel}：「{s}」（{why}）")
        # internal refs
        page_dir = os.path.dirname(rel)
        for tag, rel_attr, ref in p.refs:
            u = urllib.parse.urlsplit(ref)
            if u.scheme or ref.startswith(("#", "mailto:", "tel:", "//")): continue
            if u.path.startswith("/"):     # root-relative: must live under the site path
                target = u.path[len(base_path):] if u.path.startswith(base_path) else "__outside__" + u.path
            elif is404 and p.base:         # 404 resolves against <base href>
                target = u.path
            else:
                target = os.path.normpath(os.path.join(page_dir, u.path)).replace(os.sep, "/")
            if target in (".", ""): target = ""
            fs = os.path.join(SITE, target)
            if os.path.isdir(fs) or target.endswith("/") or target == "": fs = os.path.join(fs, "index.html")
            if not os.path.exists(fs): missing.add(f"{rel} → {ref}")
    rec("FAIL" if bad_robots else "PASS", "robots meta " + ("錯誤：" + "; ".join(bad_robots) if bad_robots else ("全部 noindex（測試版）" if TEST else "內頁 index, follow；404 noindex")))
    rec("FAIL" if bad_banner else "PASS", ("測試橫幅狀態錯誤：" + ", ".join(bad_banner)) if bad_banner else ("測試橫幅：每頁都有" if TEST else "測試橫幅與 is-review：已全部移除"))
    rec("FAIL" if bad_canon else "PASS", ("canonical 與 sitemap 不一致：" + "; ".join(bad_canon)) if bad_canon else "canonical：每頁都等於 sitemap 網址")
    rec("FAIL" if visible_hits else "PASS", ("畫面文字含禁止字串：" + "; ".join(visible_hits)) if visible_hits else "畫面文字：沒有彩新數據、英文名稱、舊資本額或待確認標記")
    rec("FAIL" if missing else "PASS", ("站內連結或資源不存在：" + "; ".join(sorted(missing))) if missing else "站內連結與資源：全部存在")

    # ---------- robots.txt ----------
    robots = open(os.path.join(SITE, "robots.txt"), encoding="utf-8").read()
    if TEST:
        rec("PASS" if f"Disallow: {base_path}" in robots else "FAIL", "robots.txt：測試版全擋")
    else:
        ok = "Disallow" not in robots and f"Sitemap: {site_url}sitemap.xml" in robots
        rec("PASS" if ok else "FAIL", "robots.txt：開放並附 Sitemap" if ok else "robots.txt 仍是測試版或缺 Sitemap 行")

    # ---------- deploy files ----------
    for name in ("htaccess-301.txt", "htaccess-performance.txt", "DEPLOY_MANIFEST.md"):
        fp = os.path.join(DEPLOY, name)
        if not os.path.exists(fp): rec("FAIL", f"deploy/{name} 不存在（請重跑 gen_pages.py）"); continue
        t = open(fp, encoding="utf-8").read()
        if not TEST and ("測試設定" in t):
            rec("FAIL", f"deploy/{name} 是用測試設定產生的，請設 IS_PRODUCTION = True 後重跑 gen_pages.py")
        if name == "htaccess-performance.txt":
            m = re.search(r"ErrorDocument 404 (\S+)", t)
            rec("PASS" if m and m.group(1) == base_path + "404.html" else "FAIL", f".htaccess 404 路徑：{m.group(1) if m else '無'}")
        if name == "htaccess-301.txt" and site_url and "RewriteRule" in t:
            targets = set(re.findall(r"RewriteRule \S+ (\S+) \[R=301", t))
            rec("PASS" if all(x.startswith(site_url) for x in targets) else "FAIL", f"301 轉址目標都指向 {site_url}")
    if not TEST and not any(l == "FAIL" and "測試設定" in m for l, m in results):
        rec("PASS", "deploy 檔：已用正式設定產生")

    # ---------- assets: version hash & freshness ----------
    css_dir, js_dir = os.path.join(SITE, "assets", "css"), os.path.join(SITE, "assets", "js")
    home = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    for fname, d, srcs in (("site.min.css", css_dir, ("tokens.css", "components.css", "site.css")), ("main.min.js", js_dir, ("main.js",))):
        fp = os.path.join(d, fname)
        if not os.path.exists(fp): rec("FAIL", f"{fname} 不存在"); continue
        body = open(fp, encoding="utf-8").read().split("\n", 1)[1]      # drop generated banner line
        want = hashlib.sha256(body.encode()).hexdigest()[:10]
        m = re.search(re.escape(fname) + r"\?v=([0-9a-f]+)", home)
        rec("PASS" if m and m.group(1) == want else "FAIL", f"{fname}：版本號 {'相符' if m and m.group(1) == want else '不符（請重跑 gen_pages.py）'}")
        stale = [s for s in srcs if os.path.getmtime(os.path.join(d, s)) > os.path.getmtime(fp) + 1]
        if stale: rec("FAIL", f"{fname} 比原始檔舊（{', '.join(stale)} 修改過）→ 重跑 gen_pages.py")

    # ---------- images ----------
    dirty = []
    for sub in ("img", "icons"):
        for f in sorted(os.listdir(os.path.join(SITE, "assets", sub))):
            if not os.path.isfile(os.path.join(SITE, "assets", sub, f)): continue   # skip img/src/
            data = open(os.path.join(SITE, "assets", sub, f), "rb").read()
            if any(mk in data for mk in METADATA_MARKERS): dirty.append(f"{sub}/{f}")
    rec("FAIL" if dirty else "PASS", ("圖片含中繼資料，請執行 python tools/perf/optimize_images.py：" + ", ".join(dirty)) if dirty else "圖片：沒有多餘中繼資料")
    rec("PASS" if os.path.exists(os.path.join(SITE, "assets", "img", "logo.webp")) else "FAIL", "logo.webp 存在")
    if os.path.isdir(os.path.join(SITE, "assets", "img", "src")):
        rec("WARN", "assets/img/src/ 是照片原始檔，上傳時請排除（網頁只用 assets/img/ 內的 WebP／JPG）")
    ph = [k for k, v in PLACEHOLDERS.items() if os.path.exists(os.path.join(SITE, k)) and md5(os.path.join(SITE, k)) == v]
    if ph:
        note = "。og-default.png 上印有「PLACEHOLDER」字樣，分享到 LINE／Facebook 時會看到" if "assets/img/og-default.png" in ph else ""
        rec("WARN", "仍是暫用圖（G1 正式 Logo 未替換）：" + ", ".join(ph) + note)

    # ---------- report ----------
    for level, msg in results:
        print(f"[{level}] {msg}")
    n = {k: sum(1 for l, _ in results if l == k) for k in ("PASS", "WARN", "FAIL")}
    print(f"\nPASS {n['PASS']}　WARN {n['WARN']}　FAIL {n['FAIL']}")
    print("→ 可以上傳" if not n["FAIL"] else "→ 有 FAIL，請先修正，不要上傳")
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
