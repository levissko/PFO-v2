# -*- coding: utf-8 -*-
"""
PFO_NewWeb page generator — tools/gen_pages.py  (Python 3, standard library only)
Usage:  python tools/gen_pages.py
Emits plain static HTML into PFO-v2/. The generated .html files are the
deliverable; this script only guarantees header/footer stay identical.
All copy below is either old-site original text, the MOEA registry, or
marked [PROPOSED COPY] in an HTML comment.
"""
import os
import re
import json
from html import escape
from urllib.parse import quote

# Output folder: <repo>/PFO-v2 (this script lives in <repo>/tools/). Override with PFO_OUT.
OUT = os.environ.get("PFO_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PFO-v2")
COMPANY = "保富齡健康事業股份有限公司"
SHORT_NAME = "保富齡健康事業"          # title suffix (= Logo 字標)

# =====================================================================
#  SITE CONFIG — 網域／環境全域設定（PHASE 8）
#  Change these, run `python tools/gen_pages.py`, deploy. Nothing else.
# =====================================================================
# H6 [NEEDS CONFIRMATION] 最終網域。預設沿用現有網域。
#   獨立新網域範例：SITE_ORIGIN = "https://www.example.com.tw"; SITE_BASE_PATH = "/"
SITE_ORIGIN = "https://www.newimage2023.com.tw"   # scheme + host, no trailing slash
SITE_BASE_PATH = "/PFO-v2/"                       # where this site lives; Cutover → "/PFO/" or "/"
# False = 測試版：noindex、測試橫幅、robots.txt 全擋。True = 正式上線。
IS_PRODUCTION = False
# 只供量測用（例如 Lighthouse 驗證正式版設定）：環境變數 PFO_PRODUCTION=1 暫時覆寫，不改本檔
if os.environ.get("PFO_PRODUCTION") == "1":
    IS_PRODUCTION = True
# 舊網站路徑（產生 301 轉址對照表用）
OLD_BASE_PATH = "/PFO/"
# 舊網站所在網域（舊網址永遠在這個網域；改用新網域時 SITE_ORIGIN 會不同）
OLD_ORIGIN = "https://www.newimage2023.com.tw"
# sitemap <lastmod>：內容最後修改日
SITE_LASTMOD = "2026-09-23"
# 暫用圖檔路徑（G1 取得正式 Logo 後，直接覆蓋同名檔案即可）
OG_IMAGE = "assets/img/og-default.png"   # 1200×630
OG_IMAGE_W, OG_IMAGE_H = 1200, 630
FAVICON_ICO = "assets/icons/favicon.ico"
FAVICON_SVG = "assets/icons/favicon.svg"
APPLE_TOUCH_ICON = "assets/icons/apple-touch-icon.png"  # 180×180
LOGO_FOR_SCHEMA = "assets/img/logo.gif"


def abs_url(path=""):
    """Absolute URL for a site-relative path ('' = home)."""
    base = SITE_BASE_PATH if SITE_BASE_PATH.endswith("/") else SITE_BASE_PATH + "/"
    return SITE_ORIGIN + base + path


SITEMAP = []   # filled by page(): (path, url)

# ---------------- Confirmed content (old site / registry) ----------------
VISION = "以創新的理念提供專業的產品服務,專注的態度提供全方位的通路規劃,讓公司創造一個全新領域的健康照護產業,成為讓大眾幸福樂活的優質企業。"
CARE = ["提供糖尿病患及安養長照相關耗材儀器及專業傷口照護之有效產品。", "腸道健康照護系統設備合作規劃。"]
IDPN_FACT = "本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。"
IDPN_NOTICE = "產品資訊請洽專業醫療團隊。"   # old product_idpn.html sentence
BRAND_DESC = "柏朗集團為全球性跨國企業,總部設於德國,成立至今已逾百年,為歐洲市場醫療器材領域之領導品牌。"
EMAIL = "pfl@pfl.tw"
OFFICES = [  # (name [PROPOSED COPY], address, tel display, tel href, fax)
    ("北部據點（總公司）", "新北市中和區中正路928號3樓", "(02)8221-5123", "+886282215123", "(02)8221-5122"),
    ("中部據點", "台中市西區五權路2-107號15樓", "(04)2376-2333", "+886423762333", "(04)2376-1177"),
    ("南部據點", "高雄市苓雅區三多二路171號9F-1", "(07)716-8518", "+88677168518", "(07)716-8730"),
]
PRODUCTS = [  # (anchor, English name, Chinese name, features, spec) — old product_b.html
    ("trixo-bottle-west", 'Trixo Bottle "WEST"', "萃詩正常肌膚用護手霜",
     ["加強皮膚照護,與皮膚親和性佳(ph 5.5),降低皮膚的敏感性", "表皮擦過乳液後仍保有自然的握持(摩擦)力,保濕並舒緩皮膚敏感", "含維他命B5及尿囊素,不油不粘快速吸收配方"], "20ml/100ml/500ml"),
    ("trixolind-bottle-west", "TRIXOLIND Bottle WEST", "萃詩抗乾敏護膚護手乳液",
     ["加強皮膚照護,與皮膚親和性佳(ph 5.5),降低皮膚的敏感性", "表皮擦過乳液後仍保有自然的握持(摩擦)力,保濕並舒緩皮膚敏感", "含維他命B5及尿囊素,不油不粘快速吸收配方"], "20ml/100ml/500ml"),
    ("trixolind-pure-tube-west", "TRIXOLIND PURE TUBE WEST", "萃詩純淨抗乾敏護膚護手乳液(無香)",
     ["無香料成份,降低皮膚過敏,防止皮膚發炎", "含維他命B5及尿囊素,不油不粘快速吸收配方"], "20ml/100ml/500ml"),
]
NEWS14_SLUG = "news/2014-02-21-trixo-hand-cream/"
NEWS14_TITLE = "對於羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜"
NEWS14_SUM = "羊毛脂能預防皮膚過於乾燥，但有些皮膚專家則認為羊毛脂易導致敏感，引起皮膚過敏，並不是每一個人都適合。為解決皮膚易過敏的問題特別研發的新產品:專為對羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜。"

# ---------------- Icons ----------------
def svg(body, sw="1.8", size=None):
    wh = f' width="{size}" height="{size}"' if size else ""
    return f'<svg viewBox="0 0 24 24"{wh} fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
I_PHONE = svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>')
I_MENU = '<svg data-icon="open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
I_CLOSE = '<svg data-icon="close" hidden viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>'
I_ARROW = svg('<path d="M5 12h14M13 6l6 6-6 6"/>', sw="2", size=18)
I_CARE = svg('<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1z"/><path d="M12 10v5M9.5 12.5h5"/>')
I_DROP = svg('<path d="M12 2.7s-6.5 7.1-6.5 11.8a6.5 6.5 0 0 0 13 0C18.5 9.8 12 2.7 12 2.7z"/><path d="M9 15a3 3 0 0 0 3 3"/>')
I_PIN = svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>')
I_MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>')
I_INFO = svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>', sw="2")
I_EXT = svg('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>', sw="2", size=16)
HERO_MARK = '''<svg class="pfo-hero__mark" viewBox="0 0 200 200" aria-hidden="true" focusable="false">
        <circle cx="100" cy="100" r="88" fill="none" stroke="currentColor" stroke-width="10"/>
        <circle cx="100" cy="100" r="62" fill="none" stroke="currentColor" stroke-width="4"/>
        <path class="accent" fill="currentColor" d="M86 58h28v28h28v28h-28v28H86v-28H58V86h28z"/>
      </svg>'''

NAV = [("about", "關於我們", "about/"), ("services", "服務項目", "services/"),
       ("products", "代理產品", "products/"), ("news", "最新消息", "news/")]


# ---------------- Photos（PHASE 11：業主提供的情境圖，tools/perf/optimize_images.py 產生） ----------------
# photos.json 由 optimize_images.py 寫入：每張圖可用的 WebP 寬度、原始比例、JPEG 備援寬度。
# 找不到某張圖時 photo() 回傳 None，頁面自動改回原本的無照片版本。
PHOTOS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perf", "photos.json")
try:
    with open(PHOTOS_JSON, encoding="utf-8") as _fh:
        PHOTOS = json.load(_fh)
except FileNotFoundError:
    PHOTOS = {}

SIZES_HALF = "(min-width: 1280px) 600px, (min-width: 768px) 50vw, 100vw"   # 2 欄卡片


def photo(p, stem, sizes, cls="", alt="", priority=False):
    """<picture>：WebP srcset（依寬度）＋ JPEG 備援 <img>，含 width/height（避免版面跳動）。
    priority=True 用在首屏（Hero）：不延遲載入、fetchpriority=high。其餘一律 loading=lazy。
    情境圖只作裝飾，文字標題已說明內容，因此 alt 預設為空字串（報讀器略過）。"""
    info = PHOTOS.get(stem)
    if not info:
        return None
    w0, h0 = info["ratio"]
    srcset = ", ".join(f"{p}assets/img/{stem}-{w}.webp {w}w" for w in info["widths"])
    fw = info["fallback"]
    fh = round(h0 * fw / w0)
    load = 'fetchpriority="high"' if priority else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}>'
            f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="{p}assets/img/{stem}-{fw}.jpg" width="{fw}" height="{fh}" alt="{alt}" {load}>'
            f'</picture>')


def arrow_link(p, href, text, sr=""):
    srs = f'<span class="visually-hidden">：{sr}</span>' if sr else ""
    return f'<a class="pfo-link-arrow" href="{p}{href}">{text}{srs}\n                {I_ARROW}\n              </a>'


def addr_html(addr):
    """PHASE 7: keep house-number runs (e.g. 171號9F-1) on one line so an
    address never breaks mid-number on narrow screens. Text is unchanged."""
    return re.sub(r"([0-9][0-9A-Za-z\-號樓]*)", r'<span class="nowrap">\1</span>', addr)


def maps_url(addr):
    # [PROPOSED] Google Maps search link (no iframe embed — performance & privacy)
    return "https://www.google.com/maps/search/?api=1&query=" + quote(addr)


# ---------------- Layout ----------------
def header(p, current):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'<li><a class="pfo-nav__link" href="{p}{href}"{cur}>{label}</a></li>')
    mitems = []
    for key, label, href in NAV + [("contact", "聯絡我們", "contact/")]:
        cur = ' aria-current="page"' if key == current else ""
        mitems.append(f'<li><a class="pfo-mobile-menu__link" href="{p}{href}"{cur}>{label}</a></li>')
    cta_cur = ' aria-current="page"' if current == "contact" else ""
    phones = "\n".join(f'          <li><a href="tel:{h}"><span>{n}</span><span>{t}</span></a></li>' for n, a, t, h, f in OFFICES)
    home = p if p else "./"
    return f'''  <!-- ================= Header ================= -->
  <header class="pfo-header">
    <div class="pfo-header__inner">
      <a class="pfo-header__logo" href="{home}" aria-label="{COMPANY} 首頁">
        <!-- 暫用舊站 Logo（273×68）：WebP（無損，tools/perf/optimize_images.py 產生）＋ GIF 備援。
             首屏圖片：不設 lazy。取得向量檔（G1）後改為 SVG，中文字標改用 gray-900 -->
        <picture>
          <source srcset="{p}assets/img/logo.webp" type="image/webp">
          <img src="{p}assets/img/logo.gif" width="273" height="68" alt="{COMPANY}">
        </picture>
      </a>

      <nav class="pfo-nav" aria-label="主選單">
        <ul class="pfo-nav__list">
          {chr(10).join('          ' + i if n else i for n, i in enumerate(items)).strip()}
        </ul>
        <a class="pfo-btn pfo-btn--primary pfo-btn--sm" href="{p}contact/"{cta_cur}>聯絡我們</a>
      </nav>

      <div class="pfo-header__actions">
        <a class="pfo-icon-btn" href="tel:+886282215123" aria-label="撥打總公司電話 (02)8221-5123">
          {I_PHONE}
        </a>
        <button class="pfo-icon-btn" type="button" data-menu-toggle aria-controls="mobile-menu" aria-expanded="false" aria-label="開啟選單">
          {I_MENU}
          {I_CLOSE}
        </button>
      </div>
    </div>

    <!-- Mobile menu（< 1024px），由 main.js 控制 -->
    <nav class="pfo-mobile-menu" id="mobile-menu" aria-label="行動版選單" hidden>
      <ul class="pfo-mobile-menu__list">
        {chr(10).join('        ' + i if n else i for n, i in enumerate(mitems)).strip()}
      </ul>
      <div class="pfo-mobile-menu__phones">
        <p class="pfo-mobile-menu__phones-title">撥打電話</p>
        <ul>
{phones}
        </ul>
      </div>
    </nav>
  </header>'''


def footer(p):
    # PHASE 9: <div> not <section aria-label> — avoids 3 extra "region" landmarks per page
    offices = "\n".join(f'''        <div class="pfo-footer__office">
          <h3>{n}</h3>
          <p>{addr_html(a)}</p>
          <p>TEL <a href="tel:{h}">{t}</a></p>
          <p>FAX {f}</p>
        </div>''' for n, a, t, h, f in OFFICES)
    links = "\n".join(f'          <li><a href="{p}{href}">{label}</a></li>' for k, label, href in NAV + [("contact", "聯絡我們", "contact/")])
    return f'''  <!-- ================= Footer（不放：彩新連結、統編、代表人、資本額） ================= -->
  <footer class="pfo-footer on-inverse">
    <h2 class="visually-hidden">公司資訊</h2>
    <div class="pfo-footer__inner">
      <div class="pfo-footer__brand">
        <p>{COMPANY}</p>
        <p>Email：<a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>

      <div class="pfo-footer__offices">
{offices}
      </div>

      <nav class="pfo-footer__links" aria-label="頁尾連結">
        <ul>
{links}
        </ul>
      </nav>
    </div>

    <!-- 版權格式沿用舊站；年份規則 [PROPOSED]：以上線年份為準 -->
    <p class="pfo-footer__bottom">© 2026 {COMPANY} All rights reserved.</p>
  </footer>'''


def intl_phone(t):
    """'(02)8221-5123' -> '+886-2-8221-5123' (schema.org recommends the country code)."""
    m = re.fullmatch(r"\(0(\d+)\)(.+)", t)
    return f"+886-{m.group(1)}-{m.group(2)}" if m else t


def org_schema():
    """Organization JSON-LD — only confirmed facts (old site + MOEA registry)."""
    def place(n, a, t, f):
        return {"@type": "Place", "name": n, "telephone": intl_phone(t), "faxNumber": intl_phone(f),
                "address": {"@type": "PostalAddress", "streetAddress": a, "addressCountry": "TW"}}
    hq = OFFICES[0]
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": abs_url() + "#organization",
        "name": COMPANY,
        "legalName": COMPANY,
        "url": abs_url(),
        "logo": abs_url(LOGO_FOR_SCHEMA),
        "email": EMAIL,
        "telephone": intl_phone(hq[2]),
        "faxNumber": intl_phone(hq[4]),
        "foundingDate": "2011-09-05",
        "address": {"@type": "PostalAddress", "streetAddress": "中正路928號3樓",
                    "addressLocality": "中和區", "addressRegion": "新北市", "addressCountry": "TW"},
        "location": [place(n, a, t, f) for n, a, t, h, f in OFFICES],
    }


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(path)}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def jsonld(obj):
    return ('  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")
            + "\n  </script>")


def page(path, *, seo_title, description, current, main, crumbs=None, og_type="website",
         published=None, org=False, is_404=False, in_sitemap=True, note=""):
    """Write one page. `path` is relative to SITE_BASE_PATH ('index.html', 'about/index.html')."""
    depth = path.count("/")
    p = "" if is_404 else "../" * depth
    url_path = "" if path == "index.html" else path.replace("index.html", "")
    canonical = abs_url(url_path)
    indexable = IS_PRODUCTION and not is_404
    robots = "index, follow" if indexable else "noindex, nofollow"
    review_cls = "" if IS_PRODUCTION else ' class="is-review"'
    banner = "" if IS_PRODUCTION else '\n  <aside class="pfo-review-banner" aria-label="測試版本提示"><p>測試版本（不被搜尋引擎收錄）｜正式上線前移除此橫幅</p></aside>\n'
    t, d = escape(seo_title), escape(description)
    og_title = escape(seo_title.split("｜")[0])
    head_extra = []
    if is_404:
        head_extra.append(f'  <!-- 404 可能在任何深度被伺服器回傳，所以固定 base（= SITE_BASE_PATH） -->\n  <base href="{SITE_BASE_PATH}">')
    else:
        head_extra.append(f'  <link rel="canonical" href="{canonical}">')
    seo = f"""
  <!-- SEO（PHASE 8）：由 tools/gen_pages.py 產生，網域設定見 SITE_ORIGIN / SITE_BASE_PATH -->
  <meta name="robots" content="{robots}">
{chr(10).join(head_extra)}
  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="theme-color" content="#151A4D">

  <!-- Favicon：暫用圖檔，G1 正式 Logo 取得後覆蓋同名檔案 -->
  <link rel="icon" href="{p}{FAVICON_ICO}" sizes="32x32">
  <link rel="icon" href="{p}{FAVICON_SVG}" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{p}{APPLE_TOUCH_ICON}">

  <!-- Open Graph / 社群分享（og:image 為暫用圖，G1 後覆蓋同名檔案） -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{COMPANY}">
  <meta property="og:locale" content="zh_TW">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{d}">"""
    if not is_404:
        seo += f'\n  <meta property="og:url" content="{canonical}">'
    seo += f"""
  <meta property="og:image" content="{abs_url(OG_IMAGE)}">
  <meta property="og:image:width" content="{OG_IMAGE_W}">
  <meta property="og:image:height" content="{OG_IMAGE_H}">
  <meta property="og:image:alt" content="{COMPANY}">
  <meta name="twitter:card" content="summary_large_image">"""
    if published:
        seo += f'\n  <meta property="article:published_time" content="{published}">'
    schemas = []
    if org:
        schemas.append(jsonld(org_schema()))
    if crumbs:
        schemas.append(jsonld(breadcrumb_schema(crumbs)))
    if schemas:
        seo += "\n\n  <!-- 結構化資料（Schema.org JSON-LD） -->\n" + "\n".join(schemas)

    html = f'''<!doctype html>
<!--
  PFO_NewWeb — {SITE_BASE_PATH}{path}
  {note}
  - 本檔由 tools/gen_pages.py 產生，請勿直接修改。
  - 內容來源：舊站原文或經濟部登記資料；建議文字以 [PROPOSED COPY] 註解標示。
-->
<html lang="zh-Hant-TW"{review_cls}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{seo}

{asset_tags(p)}
</head>
<body class="pfo">

  <a class="pfo-skip" href="#main">跳至主要內容</a>
{banner}
{header(p, current)}

  <main id="main" tabindex="-1">
{main(p)}
  </main>

{footer(p)}

</body>
</html>
'''
    out = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    if not is_404 and in_sitemap:
        SITEMAP.append(canonical)
    print("wrote", path)


def page_head(p, title, crumbs, meta=None, article=False):
    parts = [f'<li><a href="{p if p else "./"}">首頁</a></li>']
    for label, href in crumbs:
        parts.append(f'<li><a href="{p}{href}">{label}</a></li>' if href else f'<li><span aria-current="page">{label}</span></li>')
    m = f'\n        <p class="pfo-page-head__meta">{meta}</p>' if meta else ""
    cls = " pfo-page-head--article" if article else ""
    return f'''    <div class="pfo-page-head{cls}">
      <div class="pfo-container">
        <nav class="pfo-breadcrumb" aria-label="麵包屑">
          <ol>{"".join(parts)}</ol>
        </nav>{m}
        <h1>{title}</h1>
      </div>
    </div>'''


def office_cards(p, with_map=False):
    cards = []
    for n, a, t, h, f in OFFICES:
        mp = ""
        if with_map:
            mp = f'''
            <!-- [PROPOSED] 外部地圖連結，不嵌入 iframe -->
            <p class="pfo-office__actions"><a class="pfo-link-arrow" href="{maps_url(a)}" target="_blank" rel="noopener">在 Google 地圖開啟<span class="visually-hidden">：{n}（另開新視窗）</span>
                {I_EXT}
              </a></p>'''
        cards.append(f'''          <article class="pfo-card pfo-office">
            <span class="pfo-icon-badge" aria-hidden="true">
              {I_PIN}
            </span>
            <h3>{n}</h3>
            <dl>
              <dt>地址</dt><dd>{addr_html(a)}</dd>
              <dt>電話</dt><dd><a href="tel:{h}">{t}</a></dd>
              <dt>傳真</dt><dd>{f}</dd>
            </dl>{mp}
          </article>''')
    return '        <div class="pfo-grid pfo-grid--3">\n' + "\n".join(cards) + "\n        </div>"


def product_media(p, label, sub, name, note):
    """代理產品卡片圖區：業主提供的 product-podium 情境圖（空展示台，不是產品照片，所以 alt 為空、
    不宣稱是產品本身）。沒有照片時回到 Media Fallback。"""
    img = photo(p, "product-podium", SIZES_HALF)
    if img:
        return f'<!-- {note}；改用業主提供的展示台情境圖（裝飾用途） -->\n            <div class="pfo-card__media">{img}</div>'
    return f"""<!-- {note}：使用 Media Fallback -->
            <div class="pfo-media-fallback" role="img" aria-label="{name}">
              <div aria-hidden="true">
                <p class="pfo-media-fallback__label">{label}</p>
                <p class="pfo-media-fallback__sub">{sub}</p>
              </div>
            </div>"""


def product_line_cards(p):
    return f'''        <div class="pfo-grid pfo-grid--2">
          <article class="pfo-card pfo-card--link pfo-product-card">
            {product_media(p, "Trixo", "萃詩系列", "Trixo 萃詩系列", "無授權產品圖（G5）")}
            <div class="pfo-product-card__body">
              <p class="pfo-eyebrow">B'BRAUN</p>
              <h3>Trixo 萃詩系列</h3>
              <ul class="pfo-plain-list">
                {"".join(f"<li>{zh}</li>" for _, _, zh, _, _ in PRODUCTS)}
              </ul>
              {arrow_link(p, "products/trixo/", "查看產品", "Trixo 萃詩系列")}
            </div>
          </article>

          <article class="pfo-card pfo-card--link pfo-product-card">
            {product_media(p, "IDPN", "B'BRAUN", "IDPN", "不使用原廠產品圖（H11 定案）")}
            <div class="pfo-product-card__body">
              <p class="pfo-eyebrow">B'BRAUN</p>
              <h3>IDPN</h3>
              <p>{IDPN_FACT}</p>
              {arrow_link(p, "products/idpn/", "查看產品", "IDPN")}
            </div>
          </article>
        </div>'''


def news_items(p, heading_level=3, clamp=True):
    h = f"h{heading_level}"
    cl = ' class="pfo-clamp-2"' if clamp else ""
    return f'''        <ul class="pfo-news">
          <li class="pfo-news__item">
            <time class="pfo-news__date" datetime="2018-12-10">2018.12.10</time>
            <div>
              <!-- 舊站首頁原文；無標題、無內頁（H13 定案）→ 只顯示摘要 -->
              <p>{IDPN_FACT}</p>
            </div>
          </li>
          <li class="pfo-news__item">
            <time class="pfo-news__date" datetime="2014-02-21">2014.02.21</time>
            <div>
              <{h} class="pfo-news__title"><a href="{p}{NEWS14_SLUG}">{NEWS14_TITLE}</a></{h}>
              <!-- 舊站 news_list.html 摘要原文 -->
              <p{cl}>{NEWS14_SUM}</p>
            </div>
          </li>
        </ul>'''


def cta(p):
    return f'''    <section class="pfo-section" aria-labelledby="cta-title">
      <div class="pfo-container">
        <div class="pfo-cta on-inverse">
          <!-- [PROPOSED COPY] -->
          <h2 id="cta-title">想進一步了解？請聯絡我們</h2>
          <a class="pfo-btn pfo-btn--inverse" href="{p}contact/">聯絡我們</a>
        </div>
      </div>
    </section>'''


# =====================================================================
# PHASE 10 — ASSET BUILD（CSS／JS 合併壓縮 + 版本號）
#   來源檔（可直接編輯）：assets/css/tokens.css、components.css、site.css、assets/js/main.js
#   產出檔（勿手動修改）：assets/css/site.min.css、assets/js/main.min.js
#   HTML 以 ?v=<內容雜湊> 引用產出檔：內容一變網址就變，伺服器可放心設定長期快取。
# =====================================================================
import hashlib

CSS_SOURCES = ["tokens.css", "components.css", "site.css"]   # 順序＝原本 <link> 的順序（cascade 不變）
USE_BUNDLE = True   # False = 回到三個原始 CSS + main.js（除錯用）


def minify_css(css):
    """保守的 CSS 壓縮：只移除註解與多餘空白，不改寫任何規則。
    字串與 url(...) 先抽出保護（data URI 內的空白與符號原樣保留）。"""
    keep = []
    def stash(m):
        if m.group(0).startswith("/*"):
            return ""                      # 註解：刪除（一次掃描，避免註解裡的引號被當成字串）
        keep.append(m.group(0))
        return f"\x00{len(keep) - 1}\x00"
    css = re.sub(r'/\*.*?\*/|url\((?:"[^"]*"|\'[^\']*\'|[^)]*)\)|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
                 stash, css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    # 只在「一定不影響語意」的符號兩側去空白。不處理 ':' 前、'(' 前與 '+ -'（calc、後代選擇器需要）
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    css = css.replace(";}", "}")
    css = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], css)
    return css.strip() + "\n"


def minify_js(js):
    """保守的 JS 壓縮：移除區塊註解、整行 // 註解與縮排；保留換行（不依賴 ASI 改寫）。"""
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    lines = [ln.strip() for ln in js.splitlines()]
    return "\n".join(ln for ln in lines if ln and not ln.startswith("//")) + "\n"


def build_assets():
    css_dir = os.path.join(OUT, "assets", "css")
    js_dir = os.path.join(OUT, "assets", "js")
    src = ""
    for name in CSS_SOURCES:
        with open(os.path.join(css_dir, name), encoding="utf-8") as fh:
            src += fh.read() + "\n"
    css = minify_css(src)
    with open(os.path.join(js_dir, "main.js"), encoding="utf-8") as fh:
        js = minify_js(fh.read())
    banner = f"/* {COMPANY} PFO-v2 — generated by tools/gen_pages.py from {' + '.join(CSS_SOURCES)}. Do not edit. */\n"
    with open(os.path.join(css_dir, "site.min.css"), "w", encoding="utf-8") as fh:
        fh.write(banner + css)
    with open(os.path.join(js_dir, "main.min.js"), "w", encoding="utf-8") as fh:
        fh.write("/* generated from main.js by tools/gen_pages.py. Do not edit. */\n" + js)
    ver = lambda t: hashlib.sha256(t.encode()).hexdigest()[:10]
    print(f"assets: site.min.css {len((banner + css).encode()):,} B (from {len(src.encode()):,} B), "
          f"main.min.js {len(js.encode()):,} B")
    return ver(css), ver(js)


CSS_VER, JS_VER = build_assets()


def asset_tags(p):
    if not USE_BUNDLE:
        links = "\n".join(f'  <link rel="stylesheet" href="{p}assets/css/{n}">' for n in CSS_SOURCES)
        return links + f'\n  <script src="{p}assets/js/main.js" defer></script>'
    return (f'  <link rel="stylesheet" href="{p}assets/css/site.min.css?v={CSS_VER}">\n'
            f'  <script src="{p}assets/js/main.min.js?v={JS_VER}" defer></script>')


# ======================= PAGES =======================

def hero_open(p):
    """首頁 Hero 開頭。有 hero-lobby 照片時：照片＋深藍漸層遮罩，移除十字裝飾（避免與照片搶視覺、
    也避免十字壓到文字降低對比）；沒有照片時沿用原本的無照片版本。"""
    img = photo(p, "hero-lobby", "100vw", priority=True)
    if not img:
        return f"""    <!-- ================= Hero（無照片版，G2／G3） ================= -->
    <section class="pfo-hero on-inverse" aria-labelledby="hero-title">
      <!-- 裝飾圖形：取自 Logo 圓徽與十字，不承載資訊 -->
      {HERO_MARK}"""
    return f"""    <!-- ================= Hero（情境照片版：業主提供 hero-lobby，AI 生成情境圖，非本公司實景） ================= -->
    <section class="pfo-hero pfo-hero--photo on-inverse" aria-labelledby="hero-title">
      <!-- 背景照片＋深藍漸層遮罩（::after）。裝飾用途，alt 為空；白字對比已驗證 ≥ 4.5:1 -->
      <div class="pfo-hero__media" aria-hidden="true">{img}</div>"""


def service_media(p, kind):
    """首頁服務卡片上方的圖區。
    照護相關：service-care 照片。透析通路：沒有可用照片（IDPN 為醫師用藥，H11 不放產品圖），
    [PROPOSED] 用同尺寸的品牌紋樣＋圖示，讓兩張卡片高度與視覺重量一致。
    沒有 service-care 照片時，兩張卡片都回到原本的圖示徽章。"""
    has = bool(PHOTOS.get("service-care"))
    if kind == "care":
        if has:
            return f'<div class="pfo-card__media">{photo(p, "service-care", SIZES_HALF)}</div>'
        return f'<span class="pfo-icon-badge" aria-hidden="true">{I_CARE}</span>'
    if has:
        return f'<div class="pfo-card__media pfo-card__media--motif" aria-hidden="true">{I_DROP}</div>'
    return f'<span class="pfo-icon-badge pfo-icon-badge--accent" aria-hidden="true">{I_DROP}</span>'


def hero_caption():
    """情境示意標註（業主 2026-09-23 指示）：Hero 照片為 AI 生成的情境圖，不是本公司實景。
    放在 Hero 右下角、字級 xs、半透明深藍底，確保小字也 ≥ 4.5:1。沒有照片時不輸出。
    放在文字區之後，報讀器依序讀完標題與按鈕才讀到這句說明。"""
    if not PHOTOS.get("hero-lobby"):
        return ""
    return '\n      <p class="pfo-hero__caption">圖片為情境示意</p>'


def home(p):
    return f'''
{hero_open(p)}
      <div class="pfo-hero__inner">
        <!-- H1：公司正式名稱（經濟部登記） -->
        <h1 id="hero-title">保富齡健康事業<br>股份有限公司</h1>
        <!-- 副標：舊站「願景」原文 -->
        <p class="pfo-hero__lead">{VISION}</p>
        <!-- 按鈕文字：[PROPOSED COPY] -->
        <div class="pfo-hero__actions">
          <a class="pfo-btn pfo-btn--inverse" href="services/">查看服務項目</a>
          <a class="pfo-btn pfo-btn--ghost-inverse" href="contact/">聯絡我們</a>
        </div>
      </div>{hero_caption()}
    </section>

    <!-- ================= 服務項目 ================= -->
    <section class="pfo-section pfo-section--subtle" aria-labelledby="services-title">
      <div class="pfo-container">
        <div class="pfo-section__head">
          <h2 id="services-title">服務項目</h2>
        </div>

        <div class="pfo-grid pfo-grid--2">
          <article class="pfo-card pfo-card--link{" pfo-card--media" if PHOTOS.get("service-care") else ""}">
            {service_media(p, "care")}
            <h3>照護相關</h3>
            <!-- 舊站 service.html 原文 -->
            <p>{CARE[0]}</p>
            <div class="pfo-card__footer">
              {arrow_link(p, "services/#care", "了解更多", "照護相關")}
            </div>
          </article>

          <article class="pfo-card pfo-card--link{" pfo-card--media" if PHOTOS.get("service-care") else ""}">
            {service_media(p, "dialysis")}
            <h3>透析通路</h3>
            <!-- H7 定案：只放一句經銷事實（舊站 2018 消息原文）。不得引用舊站彩新公司數據 -->
            <p>{IDPN_FACT}</p>
            <div class="pfo-card__footer">
              {arrow_link(p, "services/#dialysis", "了解更多", "透析通路")}
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ================= 代理產品（品牌寫法 B'BRAUN，H12 定案） ================= -->
    <section class="pfo-section" aria-labelledby="products-title">
      <div class="pfo-container">
        <div class="pfo-section__head pfo-section__head--split">
          <h2 id="products-title">代理產品</h2>
          <!-- [PROPOSED COPY] -->
          {arrow_link(p, "products/", "全部產品")}
        </div>
{product_line_cards(p)}
      </div>
    </section>

    <!-- ================= 最新消息（新→舊，最多 3 則） ================= -->
    <section class="pfo-section pfo-section--subtle" aria-labelledby="news-title">
      <div class="pfo-container">
        <div class="pfo-section__head pfo-section__head--split">
          <h2 id="news-title">最新消息</h2>
          <!-- [PROPOSED COPY] -->
          {arrow_link(p, "news/", "所有消息")}
        </div>
{news_items(p)}
      </div>
    </section>

    <!-- ================= 服務據點（H4 定案：沿用舊站） ================= -->
    <section class="pfo-section" aria-labelledby="offices-title">
      <div class="pfo-container">
        <div class="pfo-section__head">
          <h2 id="offices-title">服務據點</h2>
        </div>
        <!-- 地址：總公司依經濟部登記寫法「3樓」；其餘照舊站原文。據點名稱為 [PROPOSED COPY] -->
{office_cards(p)}
        <div class="pfo-section__actions">
          <a class="pfo-btn pfo-btn--primary" href="contact/">聯絡我們</a>
        </div>
      </div>
    </section>
'''


def about(p):
    return f'''{page_head(p, "關於我們", [("關於我們", None)])}

    <section class="pfo-section" aria-labelledby="vision-title">
      <div class="pfo-container">
        <div class="pfo-split">
          <div class="pfo-split__head"><h2 id="vision-title">願景</h2></div>
          <div class="pfo-split__body">
            <!-- 舊站 intro.html「願景」原文 -->
            <p class="pfo-lead">{VISION}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="pfo-section pfo-section--subtle" aria-labelledby="profile-title">
      <div class="pfo-container">
        <div class="pfo-split">
          <div class="pfo-split__head"><h2 id="profile-title">公司簡介</h2></div>
          <div class="pfo-split__body">
            <!-- 經濟部商業司公司登記資料（2026-09-23 查詢）。
                 代表人、資本額、統一編號：Phase 2 決定在業主確認公開前不顯示（H3） -->
            <dl class="pfo-facts">
              <div><dt>公司名稱</dt><dd>{COMPANY}</dd></div>
              <div><dt>設立日期</dt><dd><time datetime="2011-09-05">中華民國 100 年 9 月 5 日</time></dd></div>
              <div><dt>登記地址</dt><dd>{addr_html("新北市中和區中正路928號3樓")}</dd></div>
            </dl>
          </div>
        </div>
      </div>
    </section>

    <section class="pfo-section" aria-labelledby="offices-title">
      <div class="pfo-container">
        <div class="pfo-section__head pfo-section__head--split">
          <h2 id="offices-title">服務據點</h2>
          {arrow_link(p, "contact/", "聯絡資訊")}
        </div>
{office_cards(p)}
      </div>
    </section>
'''


def services(p):
    return f'''{page_head(p, "服務項目", [("服務項目", None)])}

    <nav class="pfo-anchor-nav" aria-label="本頁段落">
      <div class="pfo-container">
        <ul><li><a href="#care">照護相關</a></li><li><a href="#dialysis">透析通路</a></li></ul>
      </div>
    </nav>

    <section class="pfo-section" id="care" aria-labelledby="care-title">
      <div class="pfo-container">
        <div class="pfo-split">
          <div class="pfo-split__head">
            <span class="pfo-icon-badge" aria-hidden="true">{I_CARE}</span>
            <h2 id="care-title">照護相關</h2>
          </div>
          <div class="pfo-split__body">
            <!-- 舊站 service.html 原文 -->
            <ul class="pfo-list">
              <li>{CARE[0]}</li>
              <li>{CARE[1]}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="pfo-section pfo-section--subtle" id="dialysis" aria-labelledby="dialysis-title">
      <div class="pfo-container">
        <div class="pfo-split">
          <div class="pfo-split__head">
            <span class="pfo-icon-badge pfo-icon-badge--accent" aria-hidden="true">{I_DROP}</span>
            <h2 id="dialysis-title">透析通路</h2>
          </div>
          <div class="pfo-split__body">
            <!-- H7 定案：只放一句經銷事實（舊站 2018 消息原文）。
                 舊站本段原為彩新公司的合作單位數據，絕對不可引用 -->
            <p>{IDPN_FACT}</p>
            <p>{arrow_link(p, "products/idpn/", "相關產品：IDPN")}</p>
          </div>
        </div>
      </div>
    </section>

{cta(p)}
'''


def products(p):
    return f'''{page_head(p, "代理產品", [("代理產品", None)])}

    <section class="pfo-section" aria-labelledby="brand-title">
      <div class="pfo-container">
        <div class="pfo-brand-block">
          <h2 id="brand-title">B'BRAUN</h2>
          <!-- 舊站首頁 B'BRAUN 說明原文 -->
          <p>{BRAND_DESC}</p>
        </div>
{product_line_cards(p)}
      </div>
    </section>

{cta(p)}
'''


def trixo(p):
    blocks = []
    for anchor, en, zh, feats, spec in PRODUCTS:
        fl = "\n".join(f"                <li>{f}</li>" for f in feats)
        blocks.append(f'''          <article class="pfo-product" id="{anchor}" aria-labelledby="{anchor}-title">
            <!-- 無授權高解析產品圖（G5）：使用 Media Fallback -->
            <div class="pfo-media-fallback pfo-media-fallback--product" role="img" aria-label="{zh}">
              <div aria-hidden="true">
                <p class="pfo-media-fallback__label">Trixo</p>
                <p class="pfo-media-fallback__sub">{en}</p>
              </div>
            </div>
            <div class="pfo-product__body">
              <h2 id="{anchor}-title">{zh}</h2>
              <p class="pfo-product__en" lang="en">{en}</p>
              <h3>產品特點</h3>
              <ol class="pfo-list">
{fl}
              </ol>
              <h3>產品規格</h3>
              <p>{spec}</p>
            </div>
          </article>''')
    chips = "".join(f'<li><a href="#{a}">{zh}</a></li>' for a, en, zh, f, s in PRODUCTS)
    return f'''{page_head(p, "Trixo 萃詩系列", [("代理產品", "products/"), ("Trixo 萃詩系列", None)], meta="品牌：B'BRAUN")}

    <nav class="pfo-anchor-nav" aria-label="本頁品項">
      <div class="pfo-container">
        <ul>{chips}</ul>
      </div>
    </nav>

    <section class="pfo-section" aria-label="Trixo 萃詩系列品項">
      <div class="pfo-container">
        <!-- 品名、特點、規格：舊站 product_b.html 原文（舊站以「1.」「2.」編號，此處改用有序清單呈現，文字不變） -->
        <div class="pfo-product-list">
{chr(10).join(blocks)}
        </div>
      </div>
    </section>

    <section class="pfo-section pfo-section--subtle" aria-labelledby="related-title">
      <div class="pfo-container">
        <div class="pfo-section__head"><h2 id="related-title">相關消息</h2></div>
        <ul class="pfo-news">
          <li class="pfo-news__item">
            <time class="pfo-news__date" datetime="2014-02-21">2014.02.21</time>
            <div><h3 class="pfo-news__title"><a href="{p}{NEWS14_SLUG}">{NEWS14_TITLE}</a></h3></div>
          </li>
        </ul>
      </div>
    </section>

{cta(p)}
'''


def idpn(p):
    return f'''{page_head(p, "B'BRAUN IDPN", [("代理產品", "products/"), ("IDPN", None)])}

    <section class="pfo-section" aria-label="經銷資訊">
      <div class="pfo-container">
        <!-- H11 定案：避免藥事法風險，本頁不放成分、適應症、療效描述與原廠圖片，
             只放經銷事實（舊站 2018 消息原文）與洽詢醫療團隊的警語（舊站 product_idpn.html 原句） -->
        <div class="pfo-narrow">
          <p class="pfo-lead">{IDPN_FACT}</p>
          <p class="pfo-notice" role="note">{I_INFO}<span>{IDPN_NOTICE}</span></p>
        </div>
      </div>
    </section>

{cta(p)}
'''


def news(p):
    return f'''{page_head(p, "最新消息", [("最新消息", None)])}

    <section class="pfo-section" aria-label="消息列表">
      <div class="pfo-container">
{news_items(p, heading_level=2, clamp=False)}
      </div>
    </section>
'''


def article(p):
    f1 = ["油包水型乳劑 water-in-oil emulsion", "不含著色劑", "中性ph值(5.5)", "含有溫和之香料及防腐劑", "擦了後皮膚不會有黏膩感", "能夠被皮膚快速吸收", "維他命B5及尿囊素, 可以舒緩皮膚不適感"]
    f2 = ["油包水型乳劑 water-in-oil emulsion", "無香料及著色劑", "中性ph值(5.5)", "特別適合超敏感肌使用", "維他命B5及尿囊素, 可以舒緩皮膚不適感", "適用於乾性肌膚"]
    ol = lambda xs: "\n".join(f"            <li>{x}</li>" for x in xs)
    return f'''{page_head(p, NEWS14_TITLE, [("最新消息", "news/"), (NEWS14_TITLE, None)], meta='<time datetime="2014-02-21">2014.02.21</time>', article=True)}

    <article class="pfo-section" aria-labelledby="article-title">
      <div class="pfo-container">
        <!-- 內文：舊站 news/2014/news_140221.html 原文遷移。舊站粗體小標改為 H2／H3（僅修正標題階層），文字未改寫。
             舊站新聞圖 news_0521.jpg（190×171）解析度過低，未使用 -->
        <div class="pfo-prose">
          <h2 id="article-title">Trixo 萃詩護手霜</h2>
          <h3>什麼是羊毛脂?</h3>
          <p>羊毛脂是附著於羊毛纖維上的油狀分泌物,含脂肪酸,以及高級醇類等複雜混合物;它可經由許多方法提煉做為商業用途。羊毛脂的精製品為淺黃色膏狀半透明體,易與水乳化,可做為親水性軟膏.潤膚霜.化粧品與藥品軟膏。</p>
          <p>由於它具有乳化及潤滑作用,常被加入美容保養面霜之中。羊毛脂能預防皮膚過於乾燥,但有些皮膚專家則認為羊毛脂易導致敏感,引起皮膚過敏,並不是每一個人都適合。</p>
          <h3>商品介紹</h3>
          <p>Trixo萃詩護手霜是能被快速吸收之保濕乳液,適合洗手後讓手部保濕以免乾燥, 也適合在執行手術後使用。</p>
          <h3>產品特點</h3>
          <ol>
{ol(f1)}
          </ol>
          <hr>
          <h2>Trixo-lind Pure 萃詩純淨抗乾敏護手霜</h2>
          <p>針對有敏感肌膚且對香料過敏者適用的護手霜,Trixo-lind Pure萃詩純淨抗乾敏護手霜是最低敏感性的手部護理保濕乳液。</p>
          <h3>產品特點</h3>
          <ol>
{ol(f2)}
          </ol>
        </div>

        <!-- 按鈕文字：[PROPOSED COPY] -->
        <div class="pfo-article-actions">
          <a class="pfo-btn pfo-btn--secondary" href="{p}products/trixo/">相關產品：Trixo 萃詩系列</a>
          <a class="pfo-btn pfo-btn--secondary" href="{p}news/">回最新消息列表</a>
        </div>
      </div>
    </article>
'''


def contact(p):
    return f'''{page_head(p, "聯絡我們", [("聯絡我們", None)])}

    <section class="pfo-section" aria-labelledby="offices-title">
      <div class="pfo-container">
        <div class="pfo-section__head"><h2 id="offices-title">服務據點</h2></div>
        <!-- H4 定案：沿用舊站據點資料（總公司地址依經濟部登記寫「3樓」）。營業時間：舊站無資料，不顯示 -->
{office_cards(p, with_map=True)}
      </div>
    </section>

    <section class="pfo-section pfo-section--subtle" aria-labelledby="email-title">
      <div class="pfo-container">
        <div class="pfo-section__head"><h2 id="email-title">電子郵件</h2></div>
        <!-- H5 定案：沿用舊站 Email。目前不設聯絡表單（H14） -->
        <div class="pfo-contact-email">
          <span class="pfo-icon-badge" aria-hidden="true">{I_MAIL}</span>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </div>
      </div>
    </section>
'''


def error404(p):
    links = "".join(f'<li><a href="{href}">{label}</a></li>' for k, label, href in NAV) + '<li><a href="contact/">聯絡我們</a></li>'
    return f'''    <section class="pfo-section" aria-labelledby="error-title">
      <div class="pfo-container">
        <!-- 文案：[PROPOSED COPY] -->
        <div class="pfo-error">
          <p class="pfo-error__code">404</p>
          <h1 id="error-title">找不到您要的頁面</h1>
          <p>您要找的頁面可能已移除或網址有誤。</p>
          <div><a class="pfo-btn pfo-btn--primary" href="./">回首頁</a></div>
          <nav aria-label="主要頁面"><ul class="pfo-list">{links}</ul></nav>
        </div>
      </div>
    </section>
'''


# =====================================================================
#  SEO FILES — sitemap.xml、robots.txt、301 對照表（PHASE 8）
# =====================================================================
# 舊網址 → 新網址（新網址為相對 SITE_BASE_PATH 的路徑）
REDIRECTS = [
    ("", ""),                                            # /PFO/
    ("index.html", ""),
    ("intro.html", "about/"),
    ("service.html", "services/"),                       # 錨點 #s_01/#s_02 無法由伺服器轉址
    ("product_b.html", "products/trixo/"),               # 舊頁實際內容為 Trixo
    ("product_idpn.html", "products/idpn/"),
    ("news/news_list.html", "news/"),
    ("news/2014/news_140221.html", NEWS14_SLUG),
]


def same_folder():
    """情境 B：新網站直接放在舊網站的路徑（同網域、同資料夾）。"""
    return SITE_ORIGIN == OLD_ORIGIN and SITE_BASE_PATH == OLD_BASE_PATH


def scenario():
    if SITE_BASE_PATH == "/":
        return "A", "獨立網域（或網域根目錄）"
    if same_folder():
        return "B", f"同網域，新站直接取代舊路徑 {OLD_BASE_PATH}"
    return "C", f"同網域子路徑 {SITE_BASE_PATH}，舊路徑 {OLD_BASE_PATH} 轉址過來"


def redirect_rules():
    """301 規則（給 OLD_BASE_PATH 資料夾內的 .htaccess 使用）與 CSV 對照表。"""
    rules = ["<IfModule mod_rewrite.c>", "RewriteEngine On"]
    csv = ["old_url,new_url,status"]
    for old, new in REDIRECTS:
        old_path = OLD_BASE_PATH + old
        target = abs_url(new)
        if OLD_ORIGIN + old_path == target:
            csv.append(f"{OLD_ORIGIN}{old_path},{target},same-url (no redirect)")
            continue
        csv.append(f"{OLD_ORIGIN}{old_path},{target},301")
        pat = re.escape(old)          # 相對於 OLD_BASE_PATH 資料夾
        if old in ("", "index.html"):
            # 只比對瀏覽器實際送出的網址（避免 DirectoryIndex 造成轉址迴圈）
            rules.append(f"RewriteCond %{{THE_REQUEST}} \\s{re.escape(old_path)}[\\s?]")
        rules.append(f"RewriteRule ^{pat}$ {target} [R=301,L]")
    rules.append("</IfModule>")
    return rules, csv


def write_seo_files():
    root = os.path.normpath(os.path.join(OUT, ".."))

    # --- sitemap.xml（放在網站根目錄 = SITE_BASE_PATH） ---
    urls = "\n".join(
        f"  <url>\n    <loc>{escape(u)}</loc>\n    <lastmod>{SITE_LASTMOD}</lastmod>\n  </url>" for u in SITEMAP)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap)

    # --- robots.txt ---
    # 注意：搜尋引擎只讀「網域根目錄」的 /robots.txt。
    #  - 獨立網域（SITE_BASE_PATH = "/"）：本檔直接生效。
    #  - 寄居 newimage2023.com.tw：根目錄屬於彩新網站，需由網域管理者把以下內容併入根目錄 robots.txt。
    if IS_PRODUCTION:
        robots = (f"# {COMPANY} — generated by tools/gen_pages.py\n"
                  "User-agent: *\n"
                  f"Allow: {SITE_BASE_PATH}\n\n"
                  f"Sitemap: {abs_url('sitemap.xml')}\n")
    else:
        robots = (f"# {COMPANY} — TEST BUILD (IS_PRODUCTION = False): block all crawling\n"
                  "User-agent: *\n"
                  f"Disallow: {SITE_BASE_PATH}\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots)

    # --- 301 redirect map（.htaccess 片段 + CSV） ---
    # PHASE 11：規則改為放在「舊網站資料夾」（OLD_BASE_PATH，例如 /PFO/.htaccess），
    # 不需要網域根目錄的權限。比對字串相對於該資料夾（per-directory 規則）。
    os.makedirs(os.path.join(root, "deploy"), exist_ok=True)
    rules, csv = redirect_rules()
    head = [] if IS_PRODUCTION else [
        "# ⚠ 由測試設定（IS_PRODUCTION = False）產生：僅供檢閱，Cutover 前請勿部署。",
        "#   正式部署前：設定好 SITE_ORIGIN / SITE_BASE_PATH、IS_PRODUCTION = True 後重新產生。",
    ]
    head += [
        f"# {COMPANY} — 舊網址 301 轉址（generated by tools/gen_pages.py）",
        f"# 舊網站：{OLD_ORIGIN}{OLD_BASE_PATH}　→　新網站：{abs_url()}",
    ]
    if same_folder():
        head += ["# 情境 B（新站直接放在舊路徑）：以下規則已併入 deploy/htaccess-performance.txt，本檔不需另外部署。"]
    else:
        head += [f"# 放置位置：舊網站資料夾 {OLD_BASE_PATH} 內的 .htaccess（伺服器路徑 {OLD_BASE_PATH}.htaccess）。",
                 f"#   舊網頁檔可以刪除，但 {OLD_BASE_PATH} 資料夾與這個 .htaccess 要保留，轉址才會繼續有效。",
                 f"#   若 {OLD_BASE_PATH} 原本已有 .htaccess，請把以下內容加在原檔最前面，不要覆蓋。"]
    head += ["# 需 Apache / LiteSpeed mod_rewrite。網址中的 #錨點（例如 service.html#s_01）不會傳到伺服器，無法轉址。"]
    with open(os.path.join(root, "deploy", "htaccess-301.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(head + rules) + "\n")
    with open(os.path.join(root, "deploy", "redirect-map.csv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(csv) + "\n")
    print("wrote sitemap.xml, robots.txt, deploy/htaccess-301.txt, deploy/redirect-map.csv")


# =====================================================================
#  PAGES — title／description 定稿（PHASE 8, [PROPOSED COPY]）
#  全部由本站既有文字組成，不加入新的事實。title 後綴：｜保富齡健康事業
# =====================================================================
H = ("首頁", "")
page("index.html", org=True,
     seo_title=f"{COMPANY}｜照護相關產品與透析通路",
     description=f"{COMPANY}提供糖尿病患及安養長照相關耗材儀器、專業傷口照護產品，經銷B'Braun原廠IDPN靜脈營養注射液，代理B'BRAUN Trixo萃詩系列，於新北、台中、高雄設有服務據點。",
     current=None, main=home, note="P-01 首頁")
page("about/index.html", org=True, crumbs=[H, ("關於我們", "about/")],
     seo_title=f"關於我們｜{SHORT_NAME}",
     description=f"{COMPANY}成立於中華民國100年9月5日，總公司位於新北市中和區，於新北、台中、高雄設有服務據點。願景：以創新的理念提供專業的產品服務，成為讓大眾幸福樂活的優質企業。",
     current="about", main=about, note="P-02 關於我們")
page("services/index.html", crumbs=[H, ("服務項目", "services/")],
     seo_title=f"服務項目：照護相關・透析通路｜{SHORT_NAME}",
     description="照護相關：提供糖尿病患及安養長照相關耗材儀器及專業傷口照護之有效產品，以及腸道健康照護系統設備合作規劃。透析通路：經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。",
     current="services", main=services, note="P-03 服務項目")
page("products/index.html", crumbs=[H, ("代理產品", "products/")],
     seo_title=f"代理產品：B'BRAUN Trixo 萃詩・IDPN｜{SHORT_NAME}",
     description="保富齡代理B'BRAUN產品，包含Trixo萃詩護手霜與護手乳液系列，並經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。",
     current="products", main=products, note="P-04 代理產品總覽")
page("products/trixo/index.html", crumbs=[H, ("代理產品", "products/"), ("Trixo 萃詩系列", "products/trixo/")],
     seo_title=f"Trixo 萃詩護手霜・護手乳液（B'BRAUN）｜{SHORT_NAME}",
     description="B'BRAUN Trixo萃詩系列：萃詩正常肌膚用護手霜、萃詩抗乾敏護膚護手乳液、萃詩純淨抗乾敏護膚護手乳液(無香)。含維他命B5及尿囊素，規格20ml/100ml/500ml。",
     current="products", main=trixo, note="P-05 Trixo 萃詩系列")
page("products/idpn/index.html", in_sitemap=True,  # [PROPOSED] 若不列入 sitemap 改為 False
     crumbs=[H, ("代理產品", "products/"), ("B'BRAUN IDPN", "products/idpn/")],
     seo_title=f"B'BRAUN IDPN 靜脈營養注射液經銷｜{SHORT_NAME}",
     description="本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。產品資訊請洽專業醫療團隊。",
     current="products", main=idpn, note="P-06 IDPN（精簡版，H11）")
page("news/index.html", crumbs=[H, ("最新消息", "news/")],
     seo_title=f"最新消息｜{SHORT_NAME}",
     description=f"{COMPANY}最新消息：經銷B'Braun原廠IDPN靜脈營養注射液；Trixo萃詩護手霜產品介紹。",
     current="news", main=news, note="P-07 最新消息")
page("news/2014-02-21-trixo-hand-cream/index.html", og_type="article", published="2014-02-21",
     crumbs=[H, ("最新消息", "news/"), (NEWS14_TITLE, NEWS14_SLUG)],
     seo_title=f"{NEWS14_TITLE}｜{SHORT_NAME}",
     description="羊毛脂易導致部分人皮膚敏感。Trixo萃詩護手霜是能被快速吸收之保濕乳液，油包水型乳劑、中性ph值(5.5)，含維他命B5及尿囊素，適合洗手後讓手部保濕。",
     current="news", main=article, note="P-08 新聞內頁（2014.02.21）")
page("contact/index.html", org=True, crumbs=[H, ("聯絡我們", "contact/")],
     seo_title=f"聯絡我們：北中南服務據點｜{SHORT_NAME}",
     description="北部據點（總公司）(02)8221-5123、中部據點 (04)2376-2333、南部據點 (07)716-8518，Email pfl@pfl.tw。提供各據點地址、電話與傳真。",
     current="contact", main=contact, note="P-09 聯絡我們")
page("404.html", is_404=True,
     seo_title=f"找不到頁面｜{SHORT_NAME}",
     description="找不到您要的頁面。",
     current=None, main=error404, note="P-10 404（永遠 noindex）")

write_seo_files()


def write_perf_htaccess():
    """PHASE 10／11：由樣板產生 deploy/htaccess-performance.txt（壓縮、快取、安全標頭、404）。
    情境 B（新站放在舊路徑）時，301 規則一併寫入本檔。"""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "perf", "htaccess-performance.tpl"), encoding="utf-8") as fh:
        tpl = fh.read().replace("{{BASE}}", SITE_BASE_PATH)
    if same_folder():
        tpl += "\n# ---------- 舊網址 301 轉址（情境 B：新站就在舊路徑，規則併入本檔） ----------\n"
        tpl += "\n".join(redirect_rules()[0]) + "\n"
    root = os.path.normpath(os.path.join(OUT, ".."))
    os.makedirs(os.path.join(root, "deploy"), exist_ok=True)
    with open(os.path.join(root, "deploy", "htaccess-performance.txt"), "w", encoding="utf-8") as fh:
        fh.write(tpl)
    print("wrote deploy/htaccess-performance.txt")


def write_deploy_manifest():
    """PHASE 11：依目前設定列出「哪個檔案放到主機哪裡」。"""
    code, label = scenario()
    root = os.path.normpath(os.path.join(OUT, ".."))
    base = SITE_BASE_PATH
    rows = [
        ("`PFO-v2/` 資料夾內**全部內容**（不含資料夾本身）", f"`{base}`",
         "上傳前先執行 optimize_images.py 與 preflight.py；**不要上傳 `assets/img/src/`**（照片原始檔，網頁不會用到）"),
        ("`deploy/htaccess-performance.txt`", f"`{base}.htaccess`", "改名為 .htaccess" + ("；已含 301 轉址" if code == "B" else "")),
    ]
    if code != "B":
        rows.append(("`deploy/htaccess-301.txt`", f"`{OLD_BASE_PATH}.htaccess`（舊網站所在主機）",
                     f"保留 {OLD_BASE_PATH} 資料夾；原本已有 .htaccess 時加在最前面"))
    if code == "A":
        robots = "`robots.txt` 在網域根目錄，**直接生效**（已含 Sitemap 行）。"
    else:
        robots = ("`robots.txt` 放在子路徑**不會被搜尋引擎讀取**（只讀網域根目錄 `/robots.txt`）。"
                  f"請網域管理者在根目錄 `/robots.txt` 加上一行 `Sitemap: {abs_url('sitemap.xml')}`，"
                  "或改在 Search Console 直接提交 sitemap。子路徑的 robots.txt 仍會上傳，無害。")
    lines = [
        "# 部署清單（DEPLOY MANIFEST）",
        "",
        "> 由 `tools/gen_pages.py` 依目前設定自動產生，請勿手改。設定改變後重跑即更新。",
        "",
        f"- 產生時設定：`SITE_ORIGIN = {SITE_ORIGIN}`、`SITE_BASE_PATH = {base}`、`IS_PRODUCTION = {IS_PRODUCTION}`",
        f"- 部署情境：**{code}：{label}**",
        f"- 新網站首頁：{abs_url()}",
        "",
    ]
    if not IS_PRODUCTION:
        lines += ["> ⚠ **目前是測試設定**：本清單只能用於部署測試版。正式上線前請改 `IS_PRODUCTION = True` 後重跑。", ""]
    lines += ["| 本機檔案 | 放到主機 | 注意 |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    lines += ["", "**robots.txt**：" + robots, "",
              f"**sitemap.xml**：位於 `{base}sitemap.xml`（{abs_url('sitemap.xml')}），隨網站一起上傳。", ""]
    with open(os.path.join(root, "deploy", "DEPLOY_MANIFEST.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote deploy/DEPLOY_MANIFEST.md（情境 {code}）")


write_perf_htaccess()
write_deploy_manifest()
