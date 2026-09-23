# PFO_NewWeb — PHASE 8：SEO

- 版本：v1.0（2026-09-23）
- 所有 SEO 輸出都由 `tools/gen_pages.py` 產生：改設定值後重跑腳本即可，不需手改 HTML。
- 驗證工具：新增 `tools/seo_audit.py`（只用 Python 標準函式庫）。

## 1. 網域／環境全域設定

位置：`tools/gen_pages.py` 最上方的 `SITE CONFIG` 區塊。

| 變數 | 目前值 | 說明 |
|---|---|---|
| `SITE_ORIGIN` | `https://www.newimage2023.com.tw` | H6 [NEEDS CONFIRMATION]。改用獨立網域時，只要改這一行 |
| `SITE_BASE_PATH` | `/PFO-v2/` | 網站所在路徑。Cutover 時改成 `/PFO/`（沿用舊路徑）或 `/`（獨立網域） |
| `IS_PRODUCTION` | `False` | 一個開關同時控制：robots meta（noindex ↔ index）、測試橫幅與 `is-review`、robots.txt（全擋 ↔ 開放加 Sitemap）、301 檔的「勿部署」警語 |
| `OLD_BASE_PATH` | `/PFO/` | 舊網站路徑，產生 301 對照表用 |
| `SITE_LASTMOD` | `2026-09-23` | sitemap 的 `<lastmod>`，內容有更新時手動改 |
| `OG_IMAGE`、`FAVICON_*`、`APPLE_TOUCH_ICON` | 見 §5 | 暫用圖檔路徑 |

`abs_url()` 函式統一組出所有絕對網址，用在 canonical、og:url、og:image、sitemap、Schema、301。**網域相關的值只存在這個區塊**。

**Cutover 模擬**（驗證設定真的能切換）：把設定改為 `SITE_BASE_PATH="/PFO/"`、`IS_PRODUCTION=True` 後重跑，確認結果如下：
- robots meta 變成 `index, follow`
- 測試橫幅和 `is-review` 消失
- canonical 變成 `/PFO/about/`
- robots.txt 開放並附上 Sitemap
- 404 的 `<base>` 自動變成 `/PFO/`
- 301 對照表自動略過 `/PFO/` → `/PFO/` 這條同網址規則，避免無限轉址

## 2. 各頁 title／description 定稿 [PROPOSED COPY]

- 內容全部由本站既有文字組成（舊網站原文、經濟部登記資料），**沒有加入任何新事實**。
- title 格式：首頁為「公司全名｜主題」，內頁為「頁名｜保富齡健康事業」。
- 長度：title 12–34 字，description 47–99 字，全站沒有重複。

| 頁面 | title | description |
|---|---|---|
| `/` | 保富齡健康事業股份有限公司｜照護相關產品與透析通路 | 保富齡健康事業股份有限公司提供糖尿病患及安養長照相關耗材儀器、專業傷口照護產品，經銷B'Braun原廠IDPN靜脈營養注射液，代理B'BRAUN Trixo萃詩系列，於新北、台中、高雄設有服務據點。 |
| `about/` | 關於我們｜保富齡健康事業 | 保富齡健康事業股份有限公司成立於中華民國100年9月5日，總公司位於新北市中和區，於新北、台中、高雄設有服務據點。願景：以創新的理念提供專業的產品服務，成為讓大眾幸福樂活的優質企業。 |
| `services/` | 服務項目：照護相關・透析通路｜保富齡健康事業 | 照護相關：提供糖尿病患及安養長照相關耗材儀器及專業傷口照護之有效產品，以及腸道健康照護系統設備合作規劃。透析通路：經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。 |
| `products/` | 代理產品：B'BRAUN Trixo 萃詩・IDPN｜保富齡健康事業 | 保富齡代理B'BRAUN產品，包含Trixo萃詩護手霜與護手乳液系列，並經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。 |
| `products/trixo/` | Trixo 萃詩護手霜・護手乳液（B'BRAUN）｜保富齡健康事業 | B'BRAUN Trixo萃詩系列：萃詩正常肌膚用護手霜、萃詩抗乾敏護膚護手乳液、萃詩純淨抗乾敏護膚護手乳液(無香)。含維他命B5及尿囊素，規格20ml/100ml/500ml。 |
| `products/idpn/` | B'BRAUN IDPN 靜脈營養注射液經銷｜保富齡健康事業 | 本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。產品資訊請洽專業醫療團隊。 |
| `news/` | 最新消息｜保富齡健康事業 | 保富齡健康事業股份有限公司最新消息：經銷B'Braun原廠IDPN靜脈營養注射液；Trixo萃詩護手霜產品介紹。 |
| `news/2014-02-21-trixo-hand-cream/` | 對於羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜｜保富齡健康事業 | 羊毛脂易導致部分人皮膚敏感。Trixo萃詩護手霜是能被快速吸收之保濕乳液，油包水型乳劑、中性ph值(5.5)，含維他命B5及尿囊素，適合洗手後讓手部保濕。 |
| `contact/` | 聯絡我們：北中南服務據點｜保富齡健康事業 | 北部據點（總公司）(02)8221-5123、中部據點 (04)2376-2333、南部據點 (07)716-8518，Email pfl@pfl.tw。提供各據點地址、電話與傳真。 |
| `404.html` | 找不到頁面｜保富齡健康事業 | 找不到您要的頁面。 |

## 3. Canonical 與 Open Graph

- **canonical**：每頁（404 除外）都有，指向 `abs_url()` 組出的絕對網址，也就是 sitemap 裡的網址。
- **Open Graph**：`og:type`（新聞內頁為 `article` 並加上 `article:published_time`）、`og:site_name`、`og:locale=zh_TW`、`og:title`（頁名，不含後綴）、`og:description`、`og:url`（等於 canonical）、`og:image` 與寬高、`og:image:alt`；另有 `twitter:card=summary_large_image`。
- **robots meta**：測試期為 `noindex, nofollow`；`IS_PRODUCTION=True` 時改為 `index, follow`。404 永遠 `noindex`，也不加 canonical。

## 4. 結構化資料（Schema.org JSON-LD）

| 類型 | 放在哪些頁 | 內容 |
|---|---|---|
| Organization | 首頁、關於我們、聯絡我們 | 見下方欄位說明 |
| BreadcrumbList | 所有內頁（首頁與 404 除外） | 與畫面上的麵包屑一致，使用絕對網址，最後一項等於 canonical |

**Organization 欄位**
- 有放：name、legalName、url、logo（暫用 logo.gif）、email、telephone／faxNumber（國際格式 +886）、foundingDate（2011-09-05，經濟部登記）、總公司地址（新北市中和區中正路928號3樓）、三據點 `location`。
- **刻意不放**：郵遞區號（沒有來源資料）、統編、代表人、資本額（H3）、英文名稱（H2）、營業時間、社群帳號。

**驗證限制**：這個環境無法連到 Google 複合式搜尋結果測試工具。上線後請用 Rich Results Test 與 Search Console 再驗證一次（列入 Phase 11）。

## 5. Favicon 與 OG 圖（暫用圖檔）

| 檔案 | 規格 | 取得正式 Logo（G1）後 |
|---|---|---|
| `PFO-v2/assets/icons/favicon.ico` | 16／32／48 | 覆蓋同名檔案 |
| `PFO-v2/assets/icons/favicon.svg` | 向量 | 覆蓋同名檔案 |
| `PFO-v2/assets/icons/apple-touch-icon.png` | 180×180 | 覆蓋同名檔案 |
| `PFO-v2/assets/img/og-default.png` | 1200×630 | 覆蓋同名檔案（或改 `OG_IMAGE` 設定） |

- 暫用圖是用 Logo 的圓徽和綠十字元素畫成的**示意圖**；OG 圖上直接印著「PLACEHOLDER — 待正式 Logo（G1）後替換」。
- **只要覆蓋同名檔案，HTML 不必改**。
- 另外修正：`logo.gif` 檔案曾被改成 12,163 bytes。像素和原檔完全相同，只是檔案內容不同，原因不明。已還原成原始的 6,367 bytes。

## 6. sitemap.xml 與 robots.txt

- **`PFO-v2/sitemap.xml`**：9 個網址（404 以外的所有頁面），全部是絕對網址，並附 `lastmod`。
  - [PROPOSED] IDPN 頁有列入。它依 H11 只放經銷事實和警語，列入沒有法規疑慮；如果要排除，把 `gen_pages.py` 裡 IDPN 頁的 `in_sitemap=True` 改成 `False` 後重跑即可。
- **`PFO-v2/robots.txt`**：
  - 測試期：`Disallow: /PFO-v2/`
  - 正式：`Allow` 加上 `Sitemap:`
- ⚠ **重要限制：搜尋引擎只讀網域根目錄的 `/robots.txt`。**
  - 如果使用**獨立網域**（`SITE_BASE_PATH="/"`）：這個檔案放在根目錄就直接生效。
  - 如果**寄居在 newimage2023.com.tw**：網域根目錄屬於彩新網站，本站的 robots.txt 放在子目錄不會被讀取。需要由網域管理者把本站的 `Sitemap:` 行併入根目錄的 robots.txt，或者改到 Search Console 直接提交 sitemap。[NEEDS CONFIRMATION：網域管理者是誰]

## 7. 301 轉址對照表

- **`deploy/htaccess-301.txt`**：Apache／LiteSpeed 用的 mod_rewrite 規則，放在舊網站網域根目錄的 `.htaccess`。
- **`deploy/redirect-map.csv`**：舊網址、新網址、狀態，供檢閱與 Search Console 網址變更使用。

| 舊網址（/PFO/…） | 新網址（相對新站根目錄） |
|---|---|
| `/PFO/`、`/PFO/index.html` | `/` |
| `intro.html` | `about/` |
| `service.html` | `services/` |
| `product_b.html` | `products/trixo/` |
| `product_idpn.html` | `products/idpn/` |
| `news/news_list.html` | `news/` |
| `news/2014/news_140221.html` | `news/2014-02-21-trixo-hand-cream/` |

- 首頁的規則使用 `THE_REQUEST` 條件，只比對使用者實際輸入的網址，避免伺服器預設首頁（DirectoryIndex）造成轉址迴圈。
- 網址中的 `#錨點`（例如 `service.html#s_01`）不會傳到伺服器，無法轉址，只能轉到 `services/`。
- ⚠ 目前的檔案是用測試設定產生的，檔頭有「勿部署」警語。**Cutover 時要先設好正式設定再重新產生**，否則會把舊網站轉到 `/PFO-v2/`。

## 8. 驗證結果

| 工具 | 結果 |
|---|---|
| `tools/seo_audit.py` | **0 個問題**：10 頁 title／description 存在且沒有重複；OG 10 個必要欄位齊全；canonical 等於 og:url 且等於 sitemap；JSON-LD 全部可解析；BreadcrumbList 位置連續、最後一項等於 canonical；Organization 必要欄位齊全；favicon 檔案存在；404 為 noindex 且沒有 canonical |
| HTML 結構與連結檢查 | 10 頁通過，0 個壞連結 |
| `tools/rwd_audit.py`（回歸） | 80 種組合 0 個問題 |
| Cutover 模擬 | §1 所列的每個切換都符合預期 |

## Phase 8 Status

**Completed**
- 全域網域／環境設定與 `abs_url()`
- 10 頁 title／description 定稿
- canonical、Open Graph、Twitter Card、favicon 標籤
- Organization、BreadcrumbList 結構化資料
- sitemap.xml、robots.txt、301 對照表（.htaccess 片段加 CSV）
- 暫用 favicon／OG 圖
- `tools/seo_audit.py`

**Pending**
- 正式 Logo（G1）：覆蓋 §5 的 4 個檔案；logo.gif 也可以換成 SVG（改 `LOGO_FOR_SCHEMA` 與 Header）
- 上線後：Google Rich Results Test、Search Console 提交 sitemap、網址變更通知（Phase 11）

**Needs Confirmation**
- H6 最終網域：決定後改 `SITE_ORIGIN`／`SITE_BASE_PATH`
- 如果沿用 newimage2023.com.tw：根目錄 robots.txt 與 `.htaccess` 由誰管理、能否加入本站規則
- IDPN 頁是否列入 sitemap（目前列入）
- title／description 文案（[PROPOSED COPY]），請業主過目

**Problems Found**
- robots.txt 只能放在網域根目錄；如果寄居在舊網域，需要網域管理者配合（§6）
- logo.gif 被改寫的原因不明，已還原（§5）

**Next Step**
- 進入 **PHASE 9：Accessibility**：
  - 以 WCAG 2.1 AA 逐項檢查：鍵盤操作、焦點順序與可見度、螢幕報讀器地標與名稱、色彩對比實測、`prefers-reduced-motion`、200% 縮放、表單（目前沒有）。
  - 使用自動化工具（axe-core）加上人工檢查，並修正發現的問題。
