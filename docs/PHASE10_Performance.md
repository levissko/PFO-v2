# PFO_NewWeb — PHASE 10：Performance Optimization

- 版本：v1.0（2026-09-23）
- 工具：Lighthouse 12.8.2、Chromium 141、Apache 2.4.58（本機測試用）
- 修改檔案：`tools/gen_pages.py`（重新產生 HTML 與 deploy 檔）、`PFO-v2/assets/img/*`、`PFO-v2/assets/icons/*`；新增 `tools/perf/`、`deploy/htaccess-performance.txt`
- 設計系統（`tokens.css`、`components.css`）與 `site.css` **原始檔沒有更動**。

## 1. 量測方式

| 項目 | 設定 |
|---|---|
| 頁面 | 首頁、關於我們、服務項目、代理產品、Trixo、新聞內頁、聯絡我們（7 頁） |
| 模式 | Mobile（Lighthouse 預設：Moto G Power 模擬、4 倍 CPU 降速、慢速 4G）與 Desktop |
| 版本 | **A. 正式版設定**：以 `PFO_PRODUCTION=1` 暫時產生一份 `IS_PRODUCTION = True` 的版本到暫存資料夾（不改動 `PFO-v2/`），放在 Apache 並套用 `.htaccess` 量測 |
|  | **B. 目前測試版**：`PFO-v2/` 原樣，用 `python -m http.server` 量測（沒有壓縮與快取標頭） |
| 為何要量正式版 | 測試版有 `noindex`，Lighthouse SEO 的「可被搜尋引擎檢索」會固定不及格，SEO 分數最多 66。這是 Phase 2 決定的測試期保護，不是問題 |

重新量測：`python tools/perf/lighthouse_run.py --base <網址> --label <名稱>`（需 Node.js 與 `npm install lighthouse`）。

## 2. Lighthouse 結果

### 2.1 最終結果 — 正式版設定＋Apache＋.htaccess

| 頁面 | Mobile P / A / BP / SEO | Mobile LCP | Desktop P / A / BP / SEO | Desktop LCP | 傳輸量 |
|---|---|---|---|---|---|
| 首頁 | **100 / 100 / 100 / 100** | 1.0 s | **100 / 100 / 100 / 100** | 0.3 s | 18.1 KiB |
| 關於我們 | 100 / 100 / 100 / 100 | 0.9 s | 100 / 100 / 100 / 100 | 0.3 s | 16.9 KiB |
| 服務項目 | 100 / 100 / 100 / 100 | 0.9 s | 100 / 100 / 100 / 100 | 0.3 s | 16.4 KiB |
| 代理產品 | 100 / 100 / 100 / 100 | 1.0 s | 100 / 100 / 100 / 100 | 0.3 s | 16.3 KiB |
| Trixo | 100 / 100 / 100 / 100 | 1.0 s | 100 / 100 / 100 / 100 | 0.3 s | 16.7 KiB |
| 新聞內頁 | 100 / 100 / 100 / 100 | 1.0 s | 100 / 100 / 100 / 100 | 0.3 s | 16.8 KiB |
| 聯絡我們 | 100 / 100 / 100 / 100 | 1.0 s | 100 / 100 / 100 / 100 | 0.3 s | 16.9 KiB |

所有頁面：TBT 0–40 ms、CLS 0。沒有任何計分項目低於 100%。
完整報告：`tools/perf/reports/final-prod-apache/mobile-home.report.html`、`desktop-home.report.html`（用瀏覽器開啟）。

### 2.2 最佳化前後比較（首頁，Mobile）

| 指標 | 最佳化前 | 最佳化後 |
|---|---|---|
| 分數 P / A / BP / SEO | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| FCP | 1.2 s | **0.8 s** |
| LCP | 1.5 s | **1.0 s** |
| 傳輸量 | 88.3 KiB | **18.1 KiB（−79%）** |
| 請求數（不含 data URI） | 7 | **5** |
| 阻擋畫面的資源 | 3 個 CSS，估計可省 230 ms | 1 個 CSS，估計 20 ms |
| 未壓縮文字 | 可省 49 KiB | 已壓縮 |
| 快取時間不足 | 可省 59 KiB | 通過 |
| 圖片傳遞 | 可省 8 KiB | 通過 |

說明：這個網站本來就很輕（沒有字型檔、沒有第三方程式、沒有大圖），所以最佳化前分數已經是 100。這次的效果主要是**實際載入速度與流量**，在慢速手機網路上最明顯。

### 2.3 目前測試版（PFO-v2/ 原樣、無伺服器設定）

7 頁 × 2 種模式：Performance 100、Accessibility 100、Best Practices 100、**SEO 66**（原因見 §1，正式版設定為 100）。

## 3. 實作內容

### 3.1 CSS／JS 合併與壓縮（`tools/gen_pages.py` → `build_assets()`）

| 項目 | 內容 |
|---|---|
| 做法 | 每次執行 `gen_pages.py`，自動把 `tokens.css + components.css + site.css`（原本的 `<link>` 順序）合併壓縮成 `assets/css/site.min.css`；`main.js` 壓縮成 `main.min.js` |
| 大小 | CSS 43,952 B → 27,952 B（壓縮傳輸 6.2 KB）；JS 3,380 B → 2,270 B（壓縮傳輸 1.4 KB） |
| 版本號 | HTML 以 `site.min.css?v=<內容雜湊>` 引用。內容一改網址就變，所以伺服器可以設定一年快取，不會出現「改了樣式、訪客還看到舊版」 |
| 安全性 | 壓縮器只移除註解與多餘空白，**不改寫任何規則**；字串與 `url(...)`（含 data URI）先保護起來；JS 保留換行 |
| 驗證 | `tools/perf/verify_bundle.py`：10 頁 × 1440／375 ＋ 行動選單展開，共 30 個頁面狀態、5,619 個元素，逐一比對所有 computed style（含 `::before`／`::after`）。**差異 0** |
| 原始檔 | 繼續編輯 `tokens.css`、`components.css`、`site.css`、`main.js`；`*.min.*` 是產出檔，不要手改 |
| 除錯 | `gen_pages.py` 的 `USE_BUNDLE = False` 可以改回三個原始 CSS |

未做：移除未使用的 CSS（約 15 KiB，大多是設計系統中目前頁面沒用到的元件）。設計系統已凍結，而且壓縮後整份 CSS 只有 6 KB、瀏覽器快取一年，拆掉的效益很小，風險較大。

### 3.2 圖片（`tools/perf/optimize_images.py`，全部無損）

| 檔案 | 前 | 後 | 做法 |
|---|---|---|---|
| `img/logo.webp`（新增） | — | 3,878 B | 由 logo.gif 無損轉 WebP，像素逐點比對相同 |
| `img/logo.gif`（備援） | 12,163 B | 5,290 B | 移除 6.6 KB 的 XMP 中繼資料，像素相同 |
| `icons/favicon.svg` | 8,102 B | 212 B | 移除內嵌的 C2PA 中繼資料與註解 |
| `icons/apple-touch-icon.png` | 14,871 B | 8,775 B | 無損重新壓縮 |
| `img/og-default.png` | 73,962 B | 68,192 B | 無損重新壓縮（分享預覽用，不影響網頁載入） |

HTML：
- Header Logo 改為 `<picture>`：`<source type="image/webp">` ＋ GIF 備援。保留 `width="273" height="68"`（CLS 0）。
- Logo 是首屏圖片，**不設** `loading="lazy"`（首屏圖片延遲載入會讓 LCP 變慢）。
- 網站目前**沒有其他 `<img>`**：產品與新聞的圖位是 Phase 2 決定的佔位區塊（未取得授權圖片），所以 `loading="lazy"` 目前沒有套用對象。
- [PROPOSED] 將來取得授權照片時的做法：原圖放 `assets/img/src/`，執行 `optimize_images.py`，會產生 480／960／1440 寬的 WebP（品質 80、不放大）；HTML 用 `srcset` + `sizes` + `width/height`，非首屏的圖加 `loading="lazy" decoding="async"`。

建議（待 G1 正式 Logo）：
- Logo 顯示尺寸是 160×40 CSS px，原檔 273×68，在 2 倍以上螢幕（多數手機）稍微不夠清晰。**改用 SVG 向量 Logo 最好**：檔案通常 2–5 KB，任何螢幕都清晰。取得後放 `assets/img/logo.svg`，`gen_pages.py` header 改一行即可。
- favicon、apple-touch-icon、OG 圖也在 G1 後覆蓋，再執行一次 `optimize_images.py`。

### 3.3 伺服器設定（`deploy/htaccess-performance.txt`）

由 `gen_pages.py` 依 `tools/perf/htaccess-performance.tpl` 產生（路徑跟著 `SITE_BASE_PATH`）。部署時改名為 `.htaccess` 放在新網站資料夾。

| 項目 | 設定 |
|---|---|
| 壓縮 | Brotli 優先、gzip 備援（`BROTLI_COMPRESS;DEFLATE`，順序已實測）。HTML、CSS、JS、SVG、XML、JSON、ICO |
| HTML、sitemap、robots | `Cache-Control: no-cache`（每次用 ETag 確認，內容更新立即生效） |
| CSS／JS（`*.min.*`） | `max-age=31536000, immutable`（有 `?v=` 版本號） |
| 圖片、圖示 | 30 天（檔名沒有版本號，所以不設一年） |
| MIME／編碼 | WebP、AVIF、SVG、ICO、webmanifest；UTF-8 |
| 其他 | `Options -Indexes`（不列出資料夾內容）、`ErrorDocument 404 /PFO-v2/404.html` |
| 安全標頭（業主 2026-09-23 核准） | `X-Content-Type-Options: nosniff`、`Referrer-Policy`、`X-Frame-Options: SAMEORIGIN` |
| 安全性 | 模組指令都包在 `<IfModule>` 內；只影響 `/PFO-v2/`，不影響舊站 `/PFO/` |

## 4. 回歸測試（修改後重跑，全部通過）

| 測試 | 結果 |
|---|---|
| HTML 結構與連結（10 頁） | bad 0 |
| SEO 稽核（title、description、canonical、OG、JSON-LD、sitemap） | 0 problems |
| RWD（8 種寬度 × 10 頁） | 0 issues |
| axe-core（22 個頁面狀態） | 0 violations |
| 鍵盤與焦點、行動選單 | 0 |
| 報讀器結構、焦點框對比、減少動態、縮放、文字間距 | 0 |
| 只放大文字 200% | 0 |
| CSS 壓縮前後 computed style 比對 | 差異 0 |

## 5. 部署後確認方式

上傳後可在任何電腦執行（網址換成實際網址）：

```
curl -sI -H "Accept-Encoding: br, gzip" https://www.newimage2023.com.tw/PFO-v2/assets/css/site.min.css
```

應看到：`Content-Encoding: br`（或 `gzip`）、`Cache-Control: public, max-age=31536000, immutable`。
HTML 頁面應看到 `Cache-Control: no-cache`。也可以用 PageSpeed Insights（https://pagespeed.web.dev/）量測實際主機。

## 6. 限制

- 本次在本機 Apache 量測，不是實際主機。實際分數會受主機回應速度、距離、是否有 HTTP/2 影響（本網站檔案少，影響不大）。
- 主機類型與設定未知：[NEEDS CONFIRMATION] 是否為 Apache／LiteSpeed、是否啟用 mod_brotli／mod_deflate／mod_expires／mod_headers、`AllowOverride` 權限。若主機在伺服器層級已設定 gzip（很常見），會一律回 gzip，仍有壓縮效果。
- 測試版 SEO 66 是 `noindex` 造成的預期結果。

## Phase 10 Status

**Completed**
- Lighthouse：7 頁 × Mobile／Desktop，正式版設定 4 項全部 100
- CSS／JS 合併壓縮＋內容雜湊版本號（整合進 `gen_pages.py`），computed style 驗證差異 0
- 圖片無損最佳化、Logo WebP＋`<picture>`、明確寬高
- `.htaccess` 壓縮／快取／404 設定，並在 Apache 2.4 實測
- 新增工具：`tools/perf/lighthouse_run.py`、`optimize_images.py`、`verify_bundle.py`、`htaccess-performance.tpl`
- 全部回歸測試 0 問題
- 您電腦上的圖片已就地重新最佳化，與量測版本 checksum 相同

**Pending**
- 部署到實際主機後，用 PageSpeed Insights 與 curl 再量一次（Phase 11）
- G1 正式 Logo（SVG）到位後替換 Logo、favicon、OG 圖，並重跑 `optimize_images.py`

**Needs Confirmation**
- 主機類型與模組、`AllowOverride` 權限（決定 `.htaccess` 能否生效）
- ~~是否採用安全標頭~~ → 業主已核准（2026-09-23，見 Phase 11）

**Problems Found**
- P1：圖片內含大量中繼資料（XMP、C2PA 來源資訊），佔檔案一半以上。已用 `optimize_images.py` 無損移除，像素相同。
  **原因已確認**：本工作環境把圖片檔傳回您電腦時，會自動在圖片中加入 C2PA 中繼資料（實測：logo.webp 3,878 B 傳回後變成 9,646 B；文字檔不受影響，checksum 相同）。Phase 8 看到的 logo.gif 大小變化也是同一原因，像素一直沒有變。
  **處理**：已直接在您電腦的專案資料夾執行 `optimize_images.py`，目前 5 個圖檔與測試環境 checksum 完全相同。
  **規則**：**上傳主機前，最後一步在本機執行一次 `python tools/perf/optimize_images.py`**（需 Pillow：`pip install pillow`。這次是在連結的專案資料夾內直接執行，您 Windows 上的 Python 是否已裝 Pillow 尚未確認）。已列入 Phase 11 Cutover 檢查表。
- P2：三個 CSS 分開載入會阻擋首次繪製（估計 230 ms）→ 已合併為一個檔案。
- P3：測試用伺服器沒有壓縮與快取 → 已提供並實測 `.htaccess`。

**Next Step**
- 進入 **PHASE 11：Final QA**：實機（iOS Safari、Android Chrome）、NVDA／VoiceOver、部署到主機後的 Lighthouse／PageSpeed、Owner Review 清單、Cutover 檢查表（`IS_PRODUCTION`、404 路徑、301、robots、**上傳前執行 `optimize_images.py`**、部署 `.htaccess` 並用 curl 驗證）。
