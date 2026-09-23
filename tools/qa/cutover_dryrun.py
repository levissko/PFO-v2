"""PFO_NewWeb — PHASE 11 Cutover 演練（在測試機的 Apache 2.4 上實際部署三種情境並逐項驗證）。

這支腳本是 QA 紀錄用，需要 Linux + Apache（a2enmod rewrite headers expires deflate brotli filter）。
業主上線時不需要執行它；上線前檢查請用 tools/qa/preflight.py。

情境：
  A  獨立網域：SITE_ORIGIN=新網域、SITE_BASE_PATH="/"；舊網域 /PFO/.htaccess 轉址到新網域
  B  同網域取代舊路徑：SITE_BASE_PATH="/PFO/"；301 規則併在新站 .htaccess
  C  同網域子路徑：SITE_BASE_PATH="/PFO-v2/"；舊站 /PFO/.htaccess 轉址過來（舊網頁檔刪除後也要有效）
"""
import csv, http.client, os, re, shutil, subprocess, sys, urllib.parse

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WORK = "/tmp/pfo_dryrun"
OLD_ORIGIN = "https://www.newimage2023.com.tw"
NEW_DOMAIN = "https://www.pfo-example.com.tw"      # 假設的獨立網域，只用於演練
OLD_FILES = ["index.html", "intro.html", "service.html", "product_b.html", "product_idpn.html",
             "news/news_list.html", "news/2014/news_140221.html", "images/main.jpg"]
fails = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)


def build(tag, origin, base):
    """Copy repo, edit config the way the owner would, run the documented script order."""
    d = os.path.join(WORK, tag, "repo")
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(REPO, d, ignore=shutil.ignore_patterns("reports", "node_modules", "textzoom-home.png", "axe-report.json"))
    g = os.path.join(d, "tools", "gen_pages.py")
    s = open(g, encoding="utf-8").read()
    s = re.sub(r'^SITE_ORIGIN = .*$', f'SITE_ORIGIN = "{origin}"', s, count=1, flags=re.M)
    s = re.sub(r'^SITE_BASE_PATH = .*$', f'SITE_BASE_PATH = "{base}"', s, count=1, flags=re.M)
    s = re.sub(r'^IS_PRODUCTION = False$', 'IS_PRODUCTION = True', s, count=1, flags=re.M)
    open(g, "w", encoding="utf-8").write(s)
    for step in (["tools/perf/optimize_images.py"], ["tools/gen_pages.py"], ["tools/qa/preflight.py"]):
        r = subprocess.run([sys.executable] + step, cwd=d, capture_output=True, text=True)
        if step[0].endswith("preflight.py"):
            last = [l for l in r.stdout.splitlines() if l.startswith(("PASS", "[FAIL]", "[WARN]"))]
            check(r.returncode == 0, f"[{tag}] preflight：{last[-1] if last else r.stdout[-200:]}")
        elif r.returncode:
            check(False, f"[{tag}] {step[0]} failed: {r.stderr[-300:]}")
    return d


def put_old_site(folder, keep_files=True):
    os.makedirs(folder, exist_ok=True)
    if keep_files:
        for f in OLD_FILES:
            p = os.path.join(folder, f); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write("<html><body>OLD SITE</body></html>")


def copy_site(repo, dest):
    shutil.copytree(os.path.join(repo, "PFO-v2"), dest, dirs_exist_ok=True)
    shutil.copy(os.path.join(repo, "deploy", "htaccess-performance.txt"), os.path.join(dest, ".htaccess"))


def req(port, path, enc="identity"):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    c.request("GET", path, headers={"Accept-Encoding": enc})
    r = c.getresponse(); body = r.read()
    return r.status, {k.lower(): v for k, v in r.getheaders()}, body


def vhost_conf(ports_roots):
    conf = ""
    for port, root in ports_roots:
        conf += f"Listen {port}\n<VirtualHost *:{port}>\n  DocumentRoot {root}\n  <Directory {root}>\n" \
                "    AllowOverride FileInfo Indexes Options\n    Require all granted\n  </Directory>\n</VirtualHost>\n"
    open("/etc/apache2/sites-available/pfo-dryrun.conf", "w").write(conf)
    subprocess.run(["a2ensite", "-q", "pfo-dryrun"], check=True)
    subprocess.run(["apache2ctl", "-k", "restart"], check=True, capture_output=True)
    import time; time.sleep(1)


def verify(tag, repo, old_port, new_port, new_origin_base, old_path="/PFO/"):
    """new_origin_base: absolute URL of new site home; local path = its path part."""
    base_path = urllib.parse.urlsplit(new_origin_base).path
    # 1) 301 map
    rows = list(csv.DictReader(open(os.path.join(repo, "deploy", "redirect-map.csv"), encoding="utf-8")))
    for row in rows:
        path = urllib.parse.urlsplit(row["old_url"]).path
        st, h, _ = req(old_port, path)
        if row["status"] == "301":
            ok = st == 301 and h.get("location") == row["new_url"]
            check(ok, f"[{tag}] {path} → 301 {row['new_url'] if ok else (st, h.get('location'))}")
            tpath = urllib.parse.urlsplit(row["new_url"]).path
            st2, h2, _ = req(new_port, tpath)
            check(st2 == 200, f"[{tag}]   目標 {tpath} → {st2}（一次轉址即到達）")
        else:
            check(st == 200, f"[{tag}] {path} 同網址，不轉址 → {st}（無迴圈）")
    # 2) new pages + headers
    locs = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(repo, "PFO-v2", "sitemap.xml"), encoding="utf-8").read())
    for u in locs:
        p = urllib.parse.urlsplit(u).path
        st, h, body = req(new_port, p)                 # uncompressed body
        h = req(new_port, p, "br, gzip")[1]             # headers as a real browser gets them
        good = (st == 200 and h.get("cache-control") == "no-cache" and h.get("content-encoding") in ("br", "gzip")
                and h.get("x-content-type-options") == "nosniff" and h.get("x-frame-options") == "SAMEORIGIN"
                and b'content="index, follow"' in body and b"pfo-review-banner" not in body)
        check(good, f"[{tag}] {p} 200／no-cache／{h.get('content-encoding')}／安全標頭／index,follow／無測試橫幅")
    # 3) assets
    home = req(new_port, base_path)[2].decode()
    for ref in re.findall(r'(?:href|src)="(assets/[^"]+\.min\.(?:css|js)\?v=[0-9a-f]+)"', home):
        st, h, _ = req(new_port, base_path + ref)
        check(st == 200 and "immutable" in h.get("cache-control", ""), f"[{tag}] {ref.split('?')[0]} 一年快取 immutable")
    st, h, _ = req(new_port, base_path + "assets/img/logo.webp")
    check(st == 200 and h.get("content-type") == "image/webp" and "max-age=2592000" in h.get("cache-control", ""), f"[{tag}] logo.webp image/webp 30 天")
    # 4) 404 + directory listing
    st, h, body = req(new_port, base_path + "no-such-page/")
    check(st == 404 and "找不到頁面".encode() in body and f'<base href="{base_path}">'.encode() in body, f"[{tag}] 不存在的網址 → 404 並顯示新站 404 頁")
    st, _, _ = req(new_port, base_path + "assets/")
    check(st == 403, f"[{tag}] 資料夾清單已關閉（assets/ → {st}）")
    # 5) robots.txt / sitemap
    st, h, body = req(new_port, base_path + "robots.txt")
    check(st == 200 and b"Sitemap: " + new_origin_base.encode() + b"sitemap.xml" in body, f"[{tag}] robots.txt 開放＋Sitemap")


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    # ---------- C ----------
    print("\n=== 情境 C：同網域子路徑 /PFO-v2/，舊站檔案保留 ===")
    rc = build("C", OLD_ORIGIN, "/PFO-v2/")
    www = os.path.join(WORK, "C", "www"); put_old_site(os.path.join(www, "PFO"))
    shutil.copy(os.path.join(rc, "deploy", "htaccess-301.txt"), os.path.join(www, "PFO", ".htaccess"))
    copy_site(rc, os.path.join(www, "PFO-v2"))
    # C2: same, but old files deleted (only /PFO/.htaccess kept)
    www2 = os.path.join(WORK, "C2", "www"); os.makedirs(os.path.join(www2, "PFO"))
    shutil.copy(os.path.join(rc, "deploy", "htaccess-301.txt"), os.path.join(www2, "PFO", ".htaccess"))
    copy_site(rc, os.path.join(www2, "PFO-v2"))
    # ---------- B ----------
    rb = build("B", OLD_ORIGIN, "/PFO/")
    wwwb = os.path.join(WORK, "B", "www"); put_old_site(os.path.join(wwwb, "PFO"))   # leftovers from old site
    copy_site(rb, os.path.join(wwwb, "PFO"))                                           # new site on top
    # ---------- A ----------
    ra = build("A", NEW_DOMAIN, "/")
    old_a = os.path.join(WORK, "A", "old"); put_old_site(os.path.join(old_a, "PFO"))
    shutil.copy(os.path.join(ra, "deploy", "htaccess-301.txt"), os.path.join(old_a, "PFO", ".htaccess"))
    new_a = os.path.join(WORK, "A", "new"); copy_site(ra, new_a)

    subprocess.run(["chmod", "-R", "a+rX", WORK])
    vhost_conf([(8791, www), (8792, www2), (8793, wwwb), (8794, old_a), (8795, new_a)])
    verify("C", rc, 8791, 8791, OLD_ORIGIN + "/PFO-v2/")
    print("\n=== 情境 C2：同上，但舊網頁檔已刪除，只留 /PFO/.htaccess ===")
    verify("C2", rc, 8792, 8792, OLD_ORIGIN + "/PFO-v2/")
    print("\n=== 情境 B：新站直接取代 /PFO/（舊檔殘留） ===")
    verify("B", rb, 8793, 8793, OLD_ORIGIN + "/PFO/")
    print("\n=== 情境 A：獨立網域（舊網域轉址到新網域） ===")
    verify("A", ra, 8794, 8795, NEW_DOMAIN + "/")
    print(f"\nFAILS {len(fails)}")
    for f in fails: print("  -", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
