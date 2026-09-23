# PFO_NewWeb — PHASE 9：Accessibility（WCAG 2.1 AA）

- 版本：v1.0（2026-09-23）
- 範圍：10 頁，桌機 1440 與手機 375，另測行動選單展開狀態
- 修改檔案：`tools/gen_pages.py`（重新產生 HTML）、`PFO-v2/assets/css/site.css`、`PFO-v2/assets/js/main.js`。設計系統（`tokens.css`／`components.css`）**沒有更動**。

## 1. 測試方法

| 項目 | 工具 | 內容 |
|---|---|---|
| 自動規則檢查 | **axe-core 4.13**（Playwright 注入） | 規則集：wcag2a、wcag2aa、wcag21a、wcag21aa、best-practice；共 22 個頁面狀態 |
| 鍵盤與焦點 | `tools/a11y/kbd.py` | 逐頁按 Tab 走完全頁，記錄每個停點，檢查：焦點框是否存在（≥ 2px）、是否被 sticky header 遮住（用畫面上實際位置判斷）、是否在畫面外、是否落在 aria-hidden 內、會不會卡住；第一個停點是否為跳至主內容連結、按 Enter 後焦點是否進到 `<main>`；行動選單開啟、焦點移動、Tab 循環、Esc 關閉 |
| 焦點框對比 | `tools/a11y/sr_zoom.py` | 逐一聚焦每個連結和按鈕，計算焦點框顏色與背景的對比（WCAG 1.4.11 要求 ≥ 3:1） |
| 報讀器結構 | `sr_zoom.py` ＋ Chromium 無障礙樹 | 地標與名稱、導覽區塊標籤是否重複、連結與按鈕是否都有名稱、同樣的連結文字是否指到不同網址、SVG 是否對報讀器隱藏、`role="img"` 是否有名稱、另開新視窗是否有告知 |
| 減少動態 | `sr_zoom.py` | 模擬 `prefers-reduced-motion: reduce`，檢查轉場時間、平滑捲動、卡片浮起效果 |
| 200%／400% 縮放 | `sr_zoom.py` | 整頁縮放：1280 寬放大 200% 等於 640 CSS px，放大 400% 等於 320 CSS px（WCAG 1.4.10 版面重排）；檢查橫向捲動與文字裁切 |
| 只放大文字 200% | `tools/a11y/textzoom.py` | 1280 寬、根字級 200%（WCAG 1.4.4） |
| 文字間距 | `sr_zoom.py` | 套用 WCAG 1.4.12 的間距（行高 1.5、字距 .12em、詞距 .16em、段距 2em） |
| 高對比模式 | Playwright `forced-colors: active` | 截圖目視檢查 |

## 2. 發現的問題與修正

| # | 問題 | WCAG | 修正 | 檔案 |
|---|---|---|---|---|
| A1 | 測試橫幅 `<p role="note">` 不在任何地標內（axe `region`，所有頁面都有） | best practice | 改成 `<aside aria-label="測試版本提示">`。正式上線時整段移除 | gen_pages.py |
| A2 | 行動選單打開時，被遮住的主內容和頁尾仍可被報讀器讀到（選單像彈出視窗，但背景沒有鎖住） | 1.3.2 / 2.4.3 | 選單開啟時，把跳至主內容連結、`<main>`、`<footer>`、測試橫幅設成 `inert`；關閉時恢復 | main.js |
| A3 | 頁尾三據點使用 `<section aria-label>`，每頁多出 3 個「區域」地標，報讀器的地標清單很雜亂 | best practice | 改成 `<div>`，由原本的 H3 提供結構 | gen_pages.py |
| A4 | 關於我們與服務頁的欄位標題用 `<header>` 元素，容易被誤判成頁首 | 1.3.1 | 改成 `<div class="pfo-split__head">` | gen_pages.py、site.css |
| A5 | 麵包屑分隔符號「›」是 CSS 產生的文字，有些報讀器會唸出來 | 1.1.1 | `content: "›" / ""`：畫面照常顯示，報讀器讀到空字串 | site.css |
| A6 | 無照片產品卡的 `role="img"` 已有名稱，但 Chromium 仍把卡內「Trixo」「Trixo Bottle "WEST"」等文字放進無障礙樹，可能被重複朗讀 | 1.1.1 | 卡內文字包一層 `aria-hidden="true"`，只保留 `aria-label` | gen_pages.py |
| A7 | **文字放大 200% 時**，桌機選單每個詞被拆成一字一行 | 1.4.4 | 選單文字不換行，改成整列換到第二列 | site.css |
| A8 | **文字放大 200% 時**，Hero 副標壓到綠色十字上，淺藍文字在綠底上對比低於 4.5:1 | 1.4.3 / 1.4.4 | 寬度 ≥ 768 的文字欄一律最多 62%（原本只限 768–1279） | site.css |
| A9 | Windows 高對比模式下，背景色被移除，按鈕和卡片失去邊界 | 1.4.11（加強） | `@media (forced-colors: active)`：按鈕、卡片、CTA、警語框加上系統色邊框，焦點框改用 Highlight，隱藏裝飾十字 | site.css |
| A10 | 往回按 Tab 時，焦點可能被 sticky header 蓋住（實測沒有發生，預防性處理） | 2.4.7 | 可聚焦元素加 `scroll-margin-top` | site.css |

## 3. 修正後結果

| 檢查 | 修正前 | 修正後 |
|---|---|---|
| axe-core 違規（22 個頁面狀態） | 22（每頁 1 個 `region`） | **0** |
| axe「需人工確認」 | 無照片產品卡的 color-contrast（背景為紋樣，工具無法判斷）；選單開啟時的 skip-link | color-contrast **人工計算通過**：標題 navy-700 對紋樣色 navy-100 為 8.83:1，副標 gray-600 對 navy-100 為 5.50:1；skip-link 項目已消除 |
| 鍵盤 | 0 問題 | **0**（每頁 15–29 個停點，都有焦點框、不被遮住、不會卡住；第一個停點都是跳至主內容，按 Enter 焦點進入 main） |
| 行動選單鍵盤流程 | 可操作，但背景未設 inert | 開啟後焦點到「關於我們」→ Tab 只在選單內循環 → Esc 關閉並把焦點還給按鈕；背景為 inert |
| 焦點框對比 | — | **全部 ≥ 3:1**：淺色底用 navy-600，對白色 7.99:1；深色底用白色，對 navy-900 16.32:1 |
| 報讀器結構 | 地標數量多 | 每頁地標：banner、主選單、main、麵包屑、各內容區、contentinfo、頁尾連結；**所有連結與按鈕都有名稱**；沒有「同名連結指到不同網址」；SVG 全部 aria-hidden；另開新視窗都有告知 |
| 減少動態 | — | 轉場 0s、捲動改為 auto、卡片不浮起、沒有任何動畫 |
| 整頁縮放 200%／400%（640／320px） | 0 問題 | **0**：沒有橫向捲動，文字沒有被裁切 |
| 只放大文字 200% | 選單被拆字、Hero 文字壓到圖形 | **0** |
| 文字間距（1.4.12） | 0 問題 | **0** |
| 回歸：RWD 80 種組合、SEO、HTML 結構與連結 | — | 全部 0 |

## 4. 其他人工確認項目（無需修改）

- **語言**：`lang="zh-Hant-TW"`；產品英文名稱標 `lang="en"`。
- **標題階層**：每頁只有一個 H1，沒有跳級；頁尾有一個隱藏的 H2「公司資訊」。
- **連結用途**：「了解更多」「查看產品」都附上隱藏的完整說明（例如「了解更多：照護相關」）。
- **地圖連結**：另開新視窗，連結名稱中含「（另開新視窗）」。
- **觸控目標**：寬度 < 1024 時都 ≥ 44px（Phase 7 已驗證）。
- **表單**：目前沒有表單（H14），不適用 3.3.x；將來加表單時，要補 label、錯誤訊息、`autocomplete`。
- **色彩對比**：Phase 4 已驗證 34 組；這次 axe 在實際頁面上也沒有發現對比違規。

## 5. 測試工具（可重複執行）

| 檔案 | 用途 |
|---|---|
| `tools/a11y/axe_run.py` | axe-core 規則檢查（需先 `npm install axe-core`） |
| `tools/a11y/kbd.py` | 鍵盤、焦點、跳至主內容、行動選單 |
| `tools/a11y/sr_zoom.py` | 報讀器結構、焦點框對比、減少動態、200%／400% 縮放、文字間距 |
| `tools/a11y/textzoom.py` | 只放大文字 200% |

執行前先在專案根目錄啟動本機伺服器：`python -m http.server 8765`。

## 6. 限制

- 這次沒有使用實際的報讀器（NVDA、VoiceOver、TalkBack）逐頁收聽。無障礙樹與規則檢查能涵蓋大部分問題，但發音、朗讀順序、中英混排這些細節，**要到 Phase 11 用 NVDA（Windows）與 VoiceOver（iOS）實測**。
- 自動化工具只能抓到部分 WCAG 問題，所以另外做了第 1 節的人工項目。認知類的準則（例如文字易讀性）不在這次範圍。

## Phase 9 Status

**Completed**
- axe-core 22 個頁面狀態 0 違規
- 鍵盤、焦點、報讀器結構、焦點框對比、減少動態、縮放、文字間距、高對比模式全部檢查
- 10 項修正（A1–A10）
- `tools/a11y/` 四支測試工具

**Pending**
- Phase 11：NVDA 與 VoiceOver 實機報讀測試

**Needs Confirmation**
- 無

**Problems Found**
- A1–A10（§2），全部已修正；其中 A7、A8 只有在「只放大文字」時才會出現

**Next Step**
- 進入 **PHASE 10：Performance Optimization**：
  - 以 Lighthouse 量測 4 項分數，目標各 > 90。
  - 最佳化 CSS（壓縮、移除註解或合併檔案）。
  - 圖片：Logo 轉 WebP 或 SVG 的準備、OG 圖壓縮。
  - 快取標頭建議，以及 `.htaccess` 的壓縮與快取設定。
