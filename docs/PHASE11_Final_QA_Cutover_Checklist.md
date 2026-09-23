# PFO_NewWeb — PHASE 11：Final QA 與上線檢查表（Cutover Checklist）

- 版本：**v1.2（2026-09-23）— 程式碼凍結版**。v1.1 新增 §6 情境照片與進場動畫；v1.2 新增 Hero「圖片為情境示意」標註（§6.6）
- **程式碼凍結**：自 v1.2 起不再修改程式。之後只依 §1 補資料、依 §2–§4 部署與測試；若補資料需要改頁面，再開變更單處理。
- 用法：從第 1 節往下逐項打勾。**第 1 節標「⛔ 必要」的項目完成前，不要做第 3 節的正式部署。**
- 本階段新增或修改的檔案：`tools/gen_pages.py`（301 改放舊站資料夾、情境判斷、`deploy/DEPLOY_MANIFEST.md`）、`tools/perf/htaccess-performance.tpl`（安全標頭改為已核准）、`tools/qa/preflight.py`（新增）、`tools/qa/cutover_dryrun.py`（新增，QA 紀錄用）
- v1.0 時網站 HTML、CSS、JS 與 Phase 10 相同。v1.1 依業主要求加入情境照片與進場動畫（§6），並重跑全部測試與 Lighthouse，結果都通過。

---

## 0. 上線流程總覽

```
① 補齊必要資料（§1）
   → ② 決定部署情境 A／B／C（§3.1）
   → ③ 先部署「測試版」到主機，給業主審閱（Owner Review，§3.4）
   → ④ 本機產生正式版並執行檢查（§2）
   → ⑤ 正式部署：先上傳新站，確認沒問題後才啟用 301（§3.3）
   → ⑥ 上線後實測（§4）
   → ⑦ 1 週與 4 週後追蹤（§4.7）→ 結案
```

---

## 1. 業主需要提供或決定的事項

### 1.1 ⛔ 上線前必須完成

| # | 項目 | 目前狀態 | 需要您提供或決定 | 提供後要改哪裡 |
|---|---|---|---|---|
| ☐ H6 | **最終網域與部署情境** | [NEEDS CONFIRMATION] | 選擇情境 A、B 或 C（§3.1）。若選 A，另外提供新網域 | `gen_pages.py`：`SITE_ORIGIN`、`SITE_BASE_PATH` |
| ☐ H15／G9 | **主機環境** | 您正在確認 | ① Apache 或 LiteSpeed ② 已啟用 `mod_rewrite`、`mod_headers`、`mod_expires`、`mod_deflate`（`mod_brotli` 可有可無）③ `AllowOverride` 允許 `FileInfo`、`Indexes`、`Options` ④ FTP 或 cPanel 帳號，可寫入 `/PFO/` 與新站路徑 | 不需要改程式；若某個模組不能用，我再調整 `.htaccess` 樣板 |
| ☐ H6-2 | **HTTPS 與 www** | [NEEDS CONFIRMATION] | 確認正式網址是 `https://www.…`，SSL 憑證有效，`http://` 會轉到 `https://`（網域層級設定，由網域管理者處理） | 所有 canonical、sitemap、OG 網址都以 `SITE_ORIGIN` 為準；如果不是 `https://www.`，就改 `SITE_ORIGIN` |
| ☐ G1-a | **分享預覽圖（OG 圖）** | 暫用圖，圖上印著「PLACEHOLDER — 待正式 Logo（G1）後替換」 | 三選一：① 等正式 Logo，由我產生正式 OG 圖 ② [PROPOSED] 上線前先由我用現有 logo.gif ＋公司名稱做一張**不含 PLACEHOLDER 字樣**的過渡版 ③ 接受現況（網址分享到 LINE／Facebook 時會出現 PLACEHOLDER 字樣，**不建議**） | `assets/img/og-default.png` |
| ☐ C1 | **文案審閱**（[PROPOSED COPY]） | 等待業主過目 | 看過下方清單並同意，或提供修改文字 | `gen_pages.py` 對應位置 |

**C1 需要業主過目的 [PROPOSED COPY]**：以下都是 AI 撰寫的介面文字，其餘內文都是舊站原文或經濟部登記資料。

| 位置 | 文字 |
|---|---|
| 10 頁的 title／description | Phase 8 文件 §2 表格 |
| 首頁 Hero 按鈕 | 「查看服務項目」「聯絡我們」 |
| 首頁區塊連結 | 「全部產品」「所有消息」 |
| 各頁底部 CTA | 「想進一步了解？請聯絡我們」 |
| 據點名稱 | 「北部據點（總公司）」「中部據點」「南部據點」 |
| 新聞內頁按鈕 | 「相關產品：Trixo 萃詩系列」「回最新消息列表」 |
| 404 頁 | 「找不到您要的頁面」「您要找的頁面可能已移除或網址有誤。」 |
| 頁尾版權年份 | 「© 2026」（[PROPOSED] 以上線年份為準） |

### 1.2 🔶 上線前建議完成（不擋上線）

| # | 項目 | 目前處理 | 建議 |
|---|---|---|---|
| ☐ R1 | 網域根目錄 `/robots.txt` 的管理者（情境 B、C） | 本站的 robots.txt 放在子路徑，搜尋引擎不會讀 | 請網域管理者在根目錄 robots.txt 加一行 `Sitemap: …`（確切內容見 `deploy/DEPLOY_MANIFEST.md`）；做不到也沒關係，改在 Search Console 提交 sitemap（§4.4） |
| ☐ H11-L | IDPN 頁文字 | 業主已定案：只放經銷事實＋「產品資訊請洽專業醫療團隊。」 | 此產品為「限由醫師使用」藥品，建議上線前請法務或原廠看過這兩句（Phase 1 H11 背景資料） |
| ☐ G11 | 是否安裝 GA4 等分析工具 | 未安裝 | 如果要安裝：①**必須**新增隱私權政策頁 ② 需要處理 Cookie 告知 ③ 會增加第三方 JavaScript，Lighthouse 分數可能下降。請先決定，再由我評估 |
| ☐ B1 | 舊網站備份 | — | 部署前從主機下載整個 `/PFO/` 資料夾存檔（情境 B 會覆蓋舊檔，**必須**備份） |

### 1.3 ⏳ 上線後再補即可（網站目前的處理方式已可上線）

| # | 項目 | 網站目前的處理 | 提供後的工作 |
|---|---|---|---|
| G1 | 正式 Logo 向量檔（SVG／AI／EPS） | 使用舊站 Logo（WebP＋GIF 備援）；favicon、apple-touch-icon 是依 Logo 圓徽畫的示意圖 | 換 Header Logo（改用 SVG）、favicon 三個檔、OG 圖 → 重跑 §2 的步驟 |
| H1 | 保富齡與彩新的關係 | 獨立網站，不放彩新連結與數據 | 依結論調整頁尾或關於我們 |
| H2 | 英文名稱 | 不顯示 | 加到頁尾與 Schema |
| H3 | 代表人、資本額、統編是否公開 | 不顯示（資料已備妥） | 決定公開後加到關於我們 |
| H9 | 營運目標方向 | 不顯示 | 確認後加到關於我們 |
| H10 | 其他代理產品（Tsukuru、創姿等） | 只有 Trixo 與 IDPN | 提供品名、規格、授權圖片後新增產品頁 |
| H13／G7 | 2018 年以後的新聞 | 只有既有兩則 | 提供內容後新增 |
| H14 | 聯絡表單 | 不做；以電話、Email 聯絡 | 需要時一併做隱私權政策頁與表單無障礙 |
| H16 | 英文版 | 只有中文 | 另外規劃 `/en/` |
| G2–G5 | 公司實景照、產品高解析圖與授權 | 首頁已使用業主提供的 3 張情境圖（§6）；其他頁面仍用圖形佔位 | 有實景照或產品照時：原圖放 `assets/img/src/` → `optimize_images.py` 產生 WebP → 告訴我要放在哪裡 |
| G8 | 各據點營業時間 | 不顯示（舊站沒有這項資料） | 加到聯絡我們與 Schema |

**已定案、不需再提供**：H4 據點資料、H5 Email、H7 透析通路（只放一句經銷事實）、H8 不放統計數字、H11 IDPN 範圍、H12 品牌寫法「B'BRAUN」與「代理產品」、H13 2018 新聞維持摘要、安全標頭（2026-09-23 核准）。

---

## 2. 部署前：本機執行順序（Windows）

在專案資料夾 `D:\claude_code_project_demo\Coding\PFO_NewWeb` 開啟 PowerShell 或命令提示字元。

### 2.1 第一次準備（只做一次）

```
python --version                 # 需要 Python 3.8 以上
python -m pip install pillow     # optimize_images.py 需要；其他腳本只用標準函式庫
```

### 2.2 每次正式部署都照這個順序

| 步驟 | 動作 | 指令／位置 | 成功的樣子 |
|---|---|---|---|
| ☐ 1 | **備份**：複製整個專案資料夾（例如 `PFO_NewWeb_backup_YYYYMMDD`） | 檔案總管 | — |
| ☐ 2 | 如果有新的 Logo、favicon 或 OG 圖，覆蓋到 `PFO-v2/assets/img/`、`PFO-v2/assets/icons/`（檔名不變） | 檔案總管 | — |
| ☐ 3 | 編輯 `tools/gen_pages.py` 最上方的設定（見下表） | 文字編輯器 | — |
| ☐ 4 | 圖片最佳化 | `python tools\perf\optimize_images.py` | 列出每個圖檔的大小；最後一行是 `img/logo.webp (lossless)` |
| ☐ 5 | 產生網站 | `python tools\gen_pages.py` | 最後一行是 `wrote deploy/DEPLOY_MANIFEST.md（情境 X）`，X 是您選的情境 |
| ☐ 6 | SEO 檢查 | `python tools\seo_audit.py` | `PROBLEMS 0` |
| ☐ 7 | **上線前總檢查** | `python tools\qa\preflight.py` | `FAIL 0` 且顯示「→ 可以上傳」（WARN「assets/img/src/ 請排除」是提醒，不是錯誤） |
| ☐ 8 | 閱讀部署清單 | 開啟 `deploy\DEPLOY_MANIFEST.md` | 顯示的情境、網址與您的選擇相同 |

**順序說明**：步驟 4 要在步驟 5 之前，因為 HTML 會引用 `logo.webp`，要先產生 WebP 檔。步驟 7 會同時檢查圖片中繼資料、CSS／JS 版本號、測試橫幅、robots 設定、301 目標；只要有一項 FAIL，就回頭修正後從步驟 4 重跑。

**步驟 3 的設定值**：

| 設定 | 情境 A（獨立網域） | 情境 B（取代 /PFO/） | 情境 C（沿用 /PFO-v2/） |
|---|---|---|---|
| `SITE_ORIGIN` | `"https://www.新網域"` | `"https://www.newimage2023.com.tw"` | `"https://www.newimage2023.com.tw"` |
| `SITE_BASE_PATH` | `"/"` | `"/PFO/"` | `"/PFO-v2/"` |
| `IS_PRODUCTION` | `True` | `True` | `True` |
| `SITE_LASTMOD` | 上線日期，例如 `"2026-10-15"` | 同左 | 同左 |
| `OLD_BASE_PATH`、`OLD_ORIGIN` | 不改 | 不改 | 不改 |

### 2.3 選用：完整回歸測試（需要 Node.js 與 Playwright）

需要本機伺服器：先執行 `python -m http.server 8765`。Phase 7–11 的測試工具（`tools/rwd_audit.py`、`tools/a11y/*`、`tools/perf/verify_bundle.py`、`tools/perf/lighthouse_run.py`、`tools/qa/hero_contrast.py`）可以再跑一次。v1.1 的版本已經在開發環境跑過全部測試（§6.4），所以**這一步可以省略**。之後有修改內容、CSS 或更換 Hero 照片時才需要跑（換照片一定要跑 `hero_contrast.py`）。

---

## 3. 部署：檔案放置位置與注意事項

### 3.1 三種部署情境

| | A 獨立網域 | B 取代舊路徑 /PFO/ | C 沿用 /PFO-v2/ |
|---|---|---|---|
| 新網站網址 | `https://www.新網域/` | `…/PFO/` | `…/PFO-v2/` |
| 舊網址處理 | 舊網域 `/PFO/.htaccess` 轉到新網域 | 新站 `.htaccess` 內含轉址 | `/PFO/.htaccess` 轉到 `/PFO-v2/` |
| robots.txt | **直接生效** | 需要網域管理者協助（R1） | 需要網域管理者協助（R1） |
| 舊網站檔案 | 保留 `/PFO/` 資料夾與 .htaccess | **被覆蓋**（先備份 B1） | 原封不動 |
| 退回舊版（rollback） | 刪除 `/PFO/.htaccess` | 用備份還原 `/PFO/` | 刪除 `/PFO/.htaccess` |
| 需要的外部資源 | 購買網域、DNS、SSL | 無 | 無 |
| 優點 | 網址最乾淨，品牌獨立 | 網址不變，不需要額外網域 | 測試網址就是正式網址；舊站不動，隨時可退回 |
| 缺點 | 成本與設定最多 | 覆蓋舊檔，退回較麻煩 | 網址帶「v2」 |

**[PROPOSED] 建議**：目前還沒有獨立網域，建議**第一次上線採情境 C**。理由：
- 審閱時的網址就是正式網址，上線只要改 `IS_PRODUCTION` 後重新上傳。
- 舊站檔案完全不動，符合專案「舊網站先保留不動」的原則。
- 要退回舊版只要刪掉一個檔案。

之後若取得獨立網域，改用情境 A 重新產生即可：轉址規則會讓舊網址直接轉到新網域，不會多轉一次。

### 3.2 檔案放置位置（`deploy/DEPLOY_MANIFEST.md` 會依您的設定自動列出）

| 本機檔案 | 情境 A | 情境 B | 情境 C |
|---|---|---|---|
| `PFO-v2\` 內的**全部內容**（不含 PFO-v2 資料夾本身） | 新網域根目錄 `/` | `/PFO/` | `/PFO-v2/` |
| `deploy\htaccess-performance.txt` → 改名 `.htaccess` | `/.htaccess` | `/PFO/.htaccess`（已含 301 規則） | `/PFO-v2/.htaccess` |
| `deploy\htaccess-301.txt` → 改名 `.htaccess` | **舊網域**的 `/PFO/.htaccess` | 不需要（已併入上一列） | `/PFO/.htaccess` |
| `robots.txt`（隨網站上傳） | 在網域根目錄，直接生效 | 在子路徑，不生效，無害 | 在子路徑，不生效，無害 |
| `sitemap.xml`（隨網站上傳） | `/sitemap.xml` | `/PFO/sitemap.xml` | `/PFO-v2/sitemap.xml` |
| 404 頁 | `.htaccess` 已設定 `ErrorDocument 404`，路徑會自動對應 | 同左 | 同左 |

**注意事項**

- ☐ **`.htaccess` 是隱藏檔**：在 Windows 先存成 `htaccess.txt` 上傳，再到 FTP 或 cPanel 改名成 `.htaccess`。FTP 軟體要開啟「顯示隱藏檔」才看得到。
- ☐ **FTP 用二進位（Binary）模式或自動模式**：用 ASCII 模式上傳，圖片會損毀。
- ☐ **原本已有 .htaccess**：如果 `/PFO/` 已經有 .htaccess，把 `htaccess-301.txt` 的內容**加在原檔最前面**，不要整個覆蓋。
- ☐ **情境 A、C 要保留 `/PFO/` 資料夾**：舊網頁檔可以刪除，但 `/PFO/` 資料夾和裡面的 `.htaccess` 必須保留，否則轉址失效。這點已實測：刪除舊網頁檔後轉址仍然有效。
- ☐ **只上傳正式版**：`preflight.py` 顯示 FAIL 0 的版本才上傳。測試版（`IS_PRODUCTION = False`）的 301 檔開頭有「⚠ 請勿部署」警語。
- ☐ **網域根目錄的 `.htaccess` 不需要動**：301 規則已改放在 `/PFO/` 資料夾內，不需要網域根目錄的權限（Phase 8 版本需要）。
- ☐ **不要上傳的檔案**：`PFO-v2\assets\img\src\`（照片原始檔）、`tools\`、`deploy\`（除了上面兩個 .htaccess）、`docs\`、`design-system\`、`temp-file\`、`Design.html`。

### 3.3 正式上線當天的順序

| 步驟 | 動作 | 為什麼 |
|---|---|---|
| ☐ 1 | 完成 §2 的步驟 1–8（FAIL 0） | — |
| ☐ 2 | 上傳新網站與它的 `.htaccess`（§3.2 前兩列） | 新站先上，舊站此時仍正常運作 |
| ☐ 3 | 用瀏覽器開新站首頁與 3 個內頁，執行 §4.1 的標頭檢查 | 確認新站正常、`.htaccess` 生效（沒有出現 500 錯誤） |
| ☐ 4 | **最後才**上傳 `htaccess-301.txt` 到 `/PFO/.htaccess`（情境 A、C） | 這一步完成，舊網址才開始轉向新站 |
| ☐ 5 | 逐一點 §4.2 的 8 個舊網址 | 確認每一個都轉到正確頁面 |
| ☐ 6 | 出錯時依 §3.1「退回舊版」處理 | 情境 A、C 刪除 `/PFO/.htaccess` 即可 |

**如果上傳 `.htaccess` 後出現「500 Internal Server Error」**：表示主機不允許其中某個指令（通常是 `Options` 或 `AddDefaultCharset`）。請先把該 `.htaccess` 改名停用，網站就會恢復，再把錯誤告訴我，我依主機限制調整樣板。

### 3.4 正式上線前：先部署測試版給業主審閱（Owner Review）

- ☐ 以目前的測試設定（`IS_PRODUCTION = False`、`SITE_BASE_PATH = "/PFO-v2/"`）執行 §2 的步驟 4–7。步驟 7 改用 `python tools\qa\preflight.py --test`。
- ☐ 上傳到 `/PFO-v2/` 和 `/PFO-v2/.htaccess`。**不要上傳 301 檔**，舊站照常運作。
- ☐ 測試版每頁都是 `noindex`、有測試橫幅，不會被搜尋引擎收錄。
- ☐ 利用這個機會在真實主機上做 §4.1 的標頭檢查，並完成 §4.5 的實機測試。
- ☐ 業主審閱通過後，才進行 §3.3 的正式上線。

---

## 4. 上線後實測

以下網址以情境 C 為例（`https://www.newimage2023.com.tw/PFO-v2/`），請換成實際網址。

### 4.1 伺服器標頭（任何有 curl 的電腦；Windows 10 以上內建 curl）

| ☐ | 指令 | 應看到 |
|---|---|---|
| ☐ | `curl -sI -H "Accept-Encoding: br, gzip" https://www.newimage2023.com.tw/PFO-v2/` | `200`、`Cache-Control: no-cache`、`Content-Encoding: br` 或 `gzip`、`X-Content-Type-Options: nosniff`、`X-Frame-Options: SAMEORIGIN` |
| ☐ | `curl -sI -H "Accept-Encoding: br, gzip" "https://www.newimage2023.com.tw/PFO-v2/assets/css/site.min.css"` | `Cache-Control: public, max-age=31536000, immutable`、有壓縮 |
| ☐ | `curl -sI https://www.newimage2023.com.tw/PFO-v2/assets/img/logo.webp` | `Content-Type: image/webp`、`max-age=2592000` |
| ☐ | `curl -sI https://www.newimage2023.com.tw/PFO-v2/no-such-page/` | `404`（瀏覽器開啟時顯示新站的 404 頁，樣式正常） |
| ☐ | `curl -sI https://www.newimage2023.com.tw/PFO-v2/assets/` | `403`（不列出資料夾內容） |

### 4.2 舊網址 301 轉址（`deploy/redirect-map.csv`）

每個舊網址用瀏覽器開啟，確認轉到正確的新頁面；或執行 `curl -sI <舊網址>`，確認看到 `301` 與正確的 `Location`。

| ☐ | 舊網址（/PFO/…） | 應轉到（新站） |
|---|---|---|
| ☐ | `/PFO/` | 首頁 |
| ☐ | `/PFO/index.html` | 首頁 |
| ☐ | `/PFO/intro.html` | `about/` |
| ☐ | `/PFO/service.html` | `services/` |
| ☐ | `/PFO/product_b.html` | `products/trixo/` |
| ☐ | `/PFO/product_idpn.html` | `products/idpn/` |
| ☐ | `/PFO/news/news_list.html` | `news/` |
| ☐ | `/PFO/news/2014/news_140221.html` | `news/2014-02-21-trixo-hand-cream/` |

情境 B：`/PFO/` 本身不轉址，直接顯示新首頁；`/PFO/index.html` 轉到 `/PFO/`。

### 4.3 效能與結構化資料

| ☐ | 工具 | 做法 | 通過標準 |
|---|---|---|---|
| ☐ | PageSpeed Insights（https://pagespeed.web.dev/） | 測首頁、關於我們、服務項目、代理產品、Trixo、新聞內頁、聯絡我們；手機與電腦都測 | 4 項 ≥ 90（本機實測全部 100）。網站流量低時，上方的「實際使用者資料」會顯示資料不足，屬正常，看下方「診斷效能問題」的分數即可 |
| ☐ | Rich Results Test（https://search.google.com/test/rich-results） | 測首頁與一個內頁（例如 `products/trixo/`） | 內頁偵測到「導覽標記（Breadcrumbs）」且 0 錯誤 |
| ☐ | Schema Markup Validator（https://validator.schema.org/） | 測首頁、關於我們、聯絡我們 | Organization、BreadcrumbList 0 錯誤、0 警告 |
| ☐ | Facebook 分享偵錯工具（https://developers.facebook.com/tools/debug/） | 輸入首頁網址 | 顯示正確的標題、描述、OG 圖（1200×630） |
| ☐ | LINE | 把首頁網址傳到自己的聊天室 | 預覽顯示正確標題與圖片（G1-a 沒處理的話，會看到 PLACEHOLDER 字樣） |

### 4.4 Google Search Console（https://search.google.com/search-console）

| ☐ | 步驟 | 說明 |
|---|---|---|
| ☐ | 新增資源 | 情境 A：「網域」資源（需在 DNS 加 TXT 記錄）。情境 B、C：「網址前置字元」資源，填新站完整網址（例如 `https://www.newimage2023.com.tw/PFO-v2/`） |
| ☐ | 驗證擁有權 | 選「HTML 檔案」：下載 Google 提供的 `googleXXXX.html`，放到 Search Console 畫面指示的位置（網址前置字元資源通常是新站資料夾，與 index.html 同層）。**這個檔案之後不要刪除** |
| ☐ | 提交 Sitemap | 「Sitemap」→ 輸入 `sitemap.xml` → 提交。狀態應為「成功」、已發現 9 個網址 |
| ☐ | 要求建立索引 | 「網址審查」→ 輸入首頁網址 → 「要求建立索引」；主要內頁也可以依序送出 |
| 說明 | 網址變更工具 | Google 的「網址變更」工具只適用整個網域搬家。本案的舊站是子資料夾，靠 301 轉址讓 Google 更新即可，不需要使用這個工具 |

### 4.5 實機測試

每台裝置都要測首頁、一個內頁、聯絡我們、404 頁。

| ☐ | 裝置／瀏覽器 | 測試項目 |
|---|---|---|
| ☐ | iPhone（Safari） | 選單開關、點電話號碼會詢問撥號、點 Email 開啟郵件 App、Google 地圖連結開啟地圖、沒有左右滑動、橫向畫面、瀏海與底部安全區域沒有遮到內容 |
| ☐ | Android 手機（Chrome） | 同上 |
| ☐ | iPad 或 Android 平板（直向與橫向） | 版面在 768–1024 寬時正常（直向是手機選單、橫向是桌機選單） |
| ☐ | Windows 電腦（Chrome、Edge） | 1920／1440／1280 寬度、鍵盤 Tab 走完一頁、焦點框清楚可見 |
| ☐ | Mac（Safari）或 Firefox（任一平台） | 版面、字型（中文使用系統字型：蘋方、微軟正黑體） |
| ☐ | 瀏覽器縮放 200% | 沒有文字被切掉，沒有左右捲動 |

### 4.6 螢幕報讀器（Phase 9 待辦）

| ☐ | 工具 | 測試項目 |
|---|---|---|
| ☐ | NVDA（Windows，免費）＋ Chrome 或 Firefox | 按 `H` 依標題跳轉（每頁一個 H1）、按 `D` 依地標跳轉、第一次按 Tab 出現「跳至主要內容」、產品英文名稱的發音、「另開新視窗」有被唸出 |
| ☐ | VoiceOver（iPhone：設定 → 輔助使用） | 轉子選「標題」可以逐一瀏覽；選單按鈕唸出「開啟選單」「關閉選單」；選單開啟時不會讀到後面的內容 |

### 4.7 上線後追蹤

| ☐ | 時間 | 項目 |
|---|---|---|
| ☐ | 上線當天 | §4.1–4.3 全部完成 |
| ☐ | 1 週後 | Search Console「網頁」報告：新網址開始被索引；「Sitemap」狀態成功 |
| ☐ | 1 週後 | Search Console 的 404 錯誤：如果出現 §4.2 以外的舊網址（例如舊圖片或其他舊頁），把網址給我，我補進 `REDIRECTS` |
| ☐ | 4 週後 | Google 搜尋「保富齡健康事業」：結果顯示新網址與新標題 |
| ☐ | 4 週後 | 確認沒問題後，可以刪除舊網頁檔（情境 A、C：**保留** `/PFO/` 資料夾與 `.htaccess`） |

---

## 5. Phase 11 QA：這次實際驗證了什麼

### 5.1 Cutover 演練（Apache 2.4.58，三種情境實際部署）

`tools/qa/cutover_dryrun.py` 會複製專案、**照 §2 的方式修改設定**、依序執行 `optimize_images → gen_pages → preflight`，再依 §3.2 放到 Apache 上逐項驗證。

| 情境 | 驗證內容 | 結果 |
|---|---|---|
| C：`/PFO-v2/`，舊檔保留 | 8 個舊網址一次 301 就到達目標（200）；9 頁 200、no-cache、br 壓縮、安全標頭、`index, follow`、沒有測試橫幅；CSS／JS immutable；WebP MIME；404 頁；資料夾清單 403；robots.txt | 全部通過 |
| C2：同上，舊網頁檔已刪除 | 只留 `/PFO/.htaccess` 時轉址仍有效 | 全部通過 |
| B：取代 `/PFO/`，舊檔殘留 | `/PFO/` 直接 200、沒有轉址迴圈；舊內頁轉到新頁；其餘同上 | 全部通過 |
| A：獨立網域 | 舊網域 `/PFO/…` 轉到新網域對應頁 | 全部通過 |
| 合計 | 126 項檢查、3 次 preflight | **0 失敗** |

### 5.2 preflight（`tools/qa/preflight.py`）

- 目前的測試版（`--test`）：**PASS 13、WARN 1、FAIL 0**。WARN 是暫用圖尚未替換（G1）。
- 用正式模式檢查目前的測試版：正確地擋下 5 項（noindex、測試橫幅、robots.txt、兩個 deploy 檔仍是測試設定）。這證明它能防止誤傳測試版。

### 5.3 回歸

網站 HTML、CSS、JS 與 Phase 10 驗收版 checksum 相同；HTML 結構與連結 0 問題、SEO 稽核 0 問題。

## 6. 情境照片與進場動畫（v1.1，業主 2026-09-23 要求）

### 6.1 圖片

| 原始檔（業主提供，位於 `temp-file\`） | 改名後（`PFO-v2\assets\img\src\`） | 用在 | 產生的檔案（`assets\img\`） |
|---|---|---|---|
| ChatGPT Image …(1).png，1672×941 | `hero-lobby.jpg` | 首頁 Hero 背景 | WebP 480／720／960／1440／1672 寬＋`hero-lobby-960.jpg` 備援 |
| ChatGPT Image …(2).png，1672×941 | `service-care.jpg` | 首頁「照護相關」卡片 | WebP 480／720／960／1440／1672＋JPG 備援 |
| ChatGPT Image …(3).png，1448×1086 | `product-podium.jpg` | 「代理產品」兩張卡片（首頁與代理產品頁） | WebP 480／720／960／1440＋JPG 備援 |

- 原始檔是 PNG，依要求轉成 JPG（品質 92）並改名；轉檔時同時去除中繼資料。
- `optimize_images.py` 擴充：依原圖寬度自動產生多個寬度的 WebP（品質 80，Hero 為 60，因為上面有 82–94% 的深藍遮罩，壓縮痕跡看不出來），另外產生一張 JPG 備援，尺寸資料寫入 `tools/perf/photos.json`。
- `gen_pages.py` 讀取 `photos.json` 自動產生 `<picture>`：WebP `srcset`＋`sizes`＋JPG 備援的 `<img>`，並寫入 `width`／`height`（CLS 0）。**如果刪掉照片，頁面會自動回到原本的無照片版本。**
- 載入方式：Hero 是首屏圖片，用 `fetchpriority="high"`，**不**延遲載入；卡片圖片用 `loading="lazy" decoding="async"`。
- CSS：`object-fit: cover`；卡片圖區 `aspect-ratio: 16 / 9`。Hero 圖片鋪滿整個區塊。
- `alt=""`：三張都是**情境示意圖**，不是本公司實景，也不是產品照，所以報讀器略過，也不以文字宣稱圖片內容。卡片標題已經說明內容。

### 6.2 版面決定（[PROPOSED]）

- **Hero 移除右側十字圖形**：照片本身已經有足夠的視覺份量。十字會和照片搶視覺焦點，在較窄的平板寬度也可能壓到文字、降低對比。沒有照片時會自動恢復十字。
- **遮罩**：手機（< 768）因為文字佔滿寬度，使用上下均勻的 82–90% 深藍遮罩；平板與桌機由左向右 94% 漸淡到 45%，左側文字區最深，右側透出大廳。
- **「透析通路」卡片**：沒有可用照片（IDPN 為醫師用藥，H11 不放產品圖）。改用和照片同尺寸的品牌淡藍色塊，中間放水滴圖示，讓兩張卡片高度與視覺重量一致。
- 強制色彩（Windows 高對比）模式下隱藏 Hero 照片，因為系統會移除遮罩，文字可能看不清楚。

### 6.3 進場動畫

- 全部包在 `@media (prefers-reduced-motion: no-preference)` 內。使用者開啟「減少動態」時，完全沒有動畫。
- **Hero**：頁面載入時，標題、副標、按鈕依序向上浮現（600ms，間隔 90ms）。
- **卡片**：`main.js` 用 IntersectionObserver，只把**載入時還在畫面下方**的卡片先隱藏，捲動進入畫面時向上浮現。已經在畫面上的卡片不會閃一下。
- 安全設計：
  - 沒有 JavaScript 時，卡片照常顯示。
  - 用鍵盤 Tab 進入卡片時，卡片一定會顯示。
  - 按 End 鍵或點錨點跳過去時，跳過的卡片也會顯示。
  - 列印時全部顯示。
- 使用 `animation`，不改卡片原本的 hover 浮起效果。

### 6.4 驗證結果

| 檢查 | 結果 |
|---|---|
| Lighthouse（正式版設定＋Apache，7 頁 × Mobile／Desktop） | **4 項全部 100**。首頁 Mobile LCP 1.0 s → 1.7 s（LCP 元素變成 Hero 照片，57 KB），仍在 100 分範圍；首頁傳輸量 18 KiB → 120 KiB（Mobile） |
| Hero 文字對比（`tools/qa/hero_contrast.py`，8 種寬度，取照片**最亮**的像素計算） | 最差 **5.48:1**（副標 navy-200，1024 寬），標題 8.7–11.5:1，框線按鈕 13.6:1 以上。全部 ≥ 4.5:1 |
| 動畫行為 | 一般：載入時畫面下方的 5 張卡片隱藏，捲動後浮現；減少動態：沒有隱藏也沒有動畫；關閉 JavaScript：全部顯示；按 End 鍵：全部顯示；列印：全部顯示 |
| axe-core（22 個頁面狀態） | 0 違規。首頁多出 4 項「需人工確認」的對比項目，因為文字在照片上，工具無法判斷背景；已由上一列的像素量測確認 |
| 鍵盤、報讀器結構、縮放、只放大文字 200%、文字間距 | 0 問題 |
| RWD 80 種組合、HTML 結構、SEO、CSS 壓縮比對、preflight | 全部 0 問題（preflight：FAIL 0） |

### 6.5 業主確認結果（2026-09-23）

- 圖片使用權：業主確認三張圖為 ChatGPT（DALL·E）生成，依其條款擁有商用權利，**沒有版權疑慮**。
- 標示情境示意：業主同意加註，已在 v1.2 實作（§6.6）。
- 代理產品卡片的展示台是空的，不代表特定產品。兩張產品卡片使用同一張圖，這是依要求處理。

### 6.6 「圖片為情境示意」標註（v1.2）

| 項目 | 內容 |
|---|---|
| 位置 | Hero 區塊**右下角**，所有寬度都在同一位置 |
| 文字 | 「圖片為情境示意」（業主指定文字） |
| 樣式 | 字級 xs（13px）、navy-200 文字、85% 深藍半透明圓角底。低調，但仍是一般對比標準的文字 |
| 對比 | 8 種寬度實測：9.9–11.7:1（取底色最亮的像素計算） |
| 版面 | 1440 與 390 寬、一般字級與「只放大文字 200%」都實測：不會壓到標題、副標或按鈕，也不會超出 Hero |
| 報讀器 | 放在按鈕之後，讀完主要內容才讀到這句說明 |
| 高對比模式 | 照片隱藏，標註改為一般文字排在內容下方 |
| 沒有照片時 | 不輸出（跟著照片一起出現或消失） |

**v1.2 最終驗證**：Lighthouse（正式版設定＋Apache，7 頁 × Mobile／Desktop）**4 項全部 100**；axe 22／22 個頁面狀態 0 違規；鍵盤、報讀器、縮放、只放大文字、文字間距、RWD 80 種組合、HTML 結構、SEO、CSS 壓縮比對、preflight（FAIL 0）全部通過；Hero 文字對比最差 5.49:1。

---

## Phase 11 Status

**Completed**
- 上線檢查表：業主資料（§1）、本機執行順序（§2）、檔案放置與上線當天順序（§3）、上線後實測（§4）
- 301 轉址改放在舊站資料夾 `/PFO/.htaccess`，不需要網域根目錄權限；情境 B 自動併入新站 `.htaccess`
- `gen_pages.py` 依設定自動判斷情境，並產生 `deploy/DEPLOY_MANIFEST.md`
- 新增 `tools/qa/preflight.py`：上線前總檢查，只用標準函式庫，Windows 可直接執行
- 三種情境在 Apache 上實際演練：126 項 0 失敗
- 安全標頭依業主核准，已移除 [PROPOSED] 標記
- v1.1：首頁情境照片（Hero 背景＋遮罩、照護卡片、代理產品卡片）與進場動畫；Lighthouse 維持全部 100，Hero 文字對比最差 5.48:1
- v1.2：Hero 右下角「圖片為情境示意」標註；全部測試重跑通過。**程式碼凍結**

**Pending**（業主端，依本檢查表進行）
- §1.1 必要事項、Owner Review（§3.4）、正式部署（§3.3）、上線後實測（§4）
- 實機與報讀器測試（§4.5、§4.6）需要實體裝置，無法在開發環境完成

**Needs Confirmation**
- H6 部署情境與網域（建議 C）、H15 主機環境、HTTPS／www
- G1-a：OG 圖怎麼處理（建議先做不含 PLACEHOLDER 字樣的過渡版）
- C1：[PROPOSED COPY] 文案審閱

**Problems Found**
- P1（已修正）：`redirect-map.csv` 的舊網址用的是新網站的網域。情境 A（獨立網域）時，舊網址會被寫成新網域，轉址對照表就錯了。已新增 `OLD_ORIGIN`（舊網址固定在 newimage2023.com.tw），並在情境 A 演練驗證。
- P2（已改善）：Phase 8 的 301 規則要放在網域根目錄，需要彩新網域管理者協助。現在改放 `/PFO/.htaccess`，只要有舊站資料夾的權限即可。
- P3（待決定）：OG 圖上印著「PLACEHOLDER」字樣，網址分享到 LINE／Facebook 時會被看到（G1-a）。
- P4（已防範）：本工作環境的圖片副本又出現被加入的中繼資料（Phase 10 P1 同一原因）。您電腦上的圖檔確認乾淨，這次**沒有**把圖檔傳回您的資料夾；`preflight.py` 會偵測這個問題並擋下上傳。

**Next Step**
- 依 §1.1 決定部署情境與 OG 圖處理方式，然後進行 §3.4 測試版部署與 Owner Review。
- 如果選 G1-a 的 ②（過渡版 OG 圖）或需要調整 `.htaccess`，告訴我即可。
- §4 全部打勾後，專案即完成。
