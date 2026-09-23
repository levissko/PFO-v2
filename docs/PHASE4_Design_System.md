# PFO_NewWeb — PHASE 4：Visual Design System

- 版本：v1.0（2026-09-23）
- 交付檔案（`design-system/`）：
  - `tokens.css`：完整 CSS Variables，唯一的樣式來源
  - `components.css`：核心元件樣式，只使用 tokens
  - `styleguide.html`：視覺預覽頁，本機開啟，引用上面兩個檔案
- 線上預覽：Artifact「保富齡 Design System」（私人；要分享需從頁面的 Share 選單開啟）
- 本階段沒有建立 `/PFO-v2/` 頁面。`components.css` 是元件參考樣式，Phase 5 會直接沿用。

---

## 1. 品牌色來源 [CONFIRMED 取樣；PROPOSED 延伸]

沒有向量檔，所以我**沒有用目測**，而是從舊站 `logo.gif`（273×68）逐像素統計實際顏色：

| 取樣結果 | 像素數 | 對應 Token | 白底對比 | 用法 |
|---|---|---|---|---|
| `#2E3092` Logo 藍（Logo 中數量最多的彩色） | 606 | `--color-navy-700` | 10.75:1 | 主要按鈕、連結，直接使用 |
| `#27903A` Logo 綠（十字） | 133 | `--color-green-600` | **4.09:1** | 只能用在 ≥24px 大字、圖示、指示線 |
| `#000000` 黑（中文字標） | — | 不使用 | — | 文字改用 `gray-900 #161A26` |

由此延伸 [PROPOSED]：

- **Deep Navy** `navy-900 #151A4D`：和 Logo 藍同色相再加深，用於 Hero 和 CTA 區塊；Footer 用更深的 `navy-950 #0E1238`。
- **綠色小字** `green-700 #1B7431`：Logo 綠的對比不到 4.5:1，所以一般大小的綠色文字一律改用這個色（5.85:1）。
- **中性灰**：帶一點藍的冷灰（色相約 228°）。

取得 Logo 向量檔（G1）後要再比對一次。如果向量檔的官方色碼不同，只需要改 `navy-700` 和 `green-600`，再重跑一次對比驗證。

## 2. Design Tokens 概要（完整內容見 `tokens.css`）

| 類別 | 內容 |
|---|---|
| 色階 | Navy 10 階、Green 8 階、Neutral 11 階（含白色）、Red 2 階（只用於錯誤訊息） |
| 語意色 | brand／bg／text／border／focus，共約 30 個角色；**元件只能用語意變數** |
| 字型 | `--font-sans` 系統字型堆疊，不下載字型檔：英數用各平台 UI 字型，中文依序為 PingFang TC → Noto Sans TC → 微軟正黑體 |
| 字級 | 9 級，用 `clamp()` 在 375px 到 1440px 之間平滑縮放：Display 32→52、H1 30→44、H2 24→32、H3 20→24、H4 18、Lead 17→19、內文 16→17、Small 15、XS 13（只用於標籤） |
| 行高 | 標題 1.3、介面元件 1.5、中文內文 1.75；閱讀寬度上限約 38 個中文字 |
| 間距 | 4px 基準，14 階（0–128）；另有 3 個流動間距：section 48→96、stack 24→40、gutter 20→40 |
| 版面 | 內容最大寬 1200、Header／Footer 1320、文章 760；12 欄格線；Header 高度桌機 72、手機 64；觸控目標至少 44 |
| 圓角 | xs 4、sm 6、md 8（按鈕）、lg 12（卡片）、xl 20（CTA／Hero）、pill |
| 陰影 | xs、sm、md、lg，以及 header 專用；陰影帶深藍色調（navy-900），不用純黑 |
| 斷點 | sm 480、md 768、lg 1024、xl 1280、2xl 1440（min-width）；CSS 變數不能用在 `@media`，所以 media query 要直接寫數字 |
| Focus | 3px 實線，偏移 2px；淺色底用 navy-600，深色底用白色 |
| 動態 | fast 120ms、base 200ms；使用者設定減少動態（prefers-reduced-motion）時全部歸零 |
| 元件 Token | button、nav、card、media-fallback、tag、input（input 先預留，目前沒有表單） |

## 3. 色彩對比驗證（WCAG 2.1 AA）

計算方式：WCAG 相對亮度公式，用 Python 程式逐一計算，不是目測。下表是設計系統**允許使用的全部前景／背景組合**，34 組全部通過。不在表內的組合不得使用。

| 用途 | 前景 | 背景 | 對比 | 標準 | 結果 |
|---|---|---|---|---|---|
| 標題文字 / 白底 | `gray-900` #161A26 | `white` #FFFFFF | **17.36:1** | 4.5:1 | ✅ |
| 內文 / 白底 | `gray-700` #3A4050 | `white` #FFFFFF | **10.35:1** | 4.5:1 | ✅ |
| 次要文字 / 白底 | `gray-600` #555C6D | `white` #FFFFFF | **6.69:1** | 4.5:1 | ✅ |
| 標題 / Off-white 區塊 | `gray-900` #161A26 | `gray-50` #F7F8FA | **16.33:1** | 4.5:1 | ✅ |
| 內文 / Off-white | `gray-700` #3A4050 | `gray-50` #F7F8FA | **9.74:1** | 4.5:1 | ✅ |
| 次要文字 / Off-white | `gray-600` #555C6D | `gray-50` #F7F8FA | **6.30:1** | 4.5:1 | ✅ |
| 內文 / 品牌淡底 | `gray-700` #3A4050 | `navy-50` #F3F4FC | **9.44:1** | 4.5:1 | ✅ |
| 次要文字 / 品牌淡底 | `gray-600` #555C6D | `navy-50` #F3F4FC | **6.10:1** | 4.5:1 | ✅ |
| 連結或標籤 / 品牌淡底 | `navy-700` #2E3092 | `navy-50` #F3F4FC | **9.80:1** | 4.5:1 | ✅ |
| 連結 / 白底 | `navy-700` #2E3092 | `white` #FFFFFF | **10.75:1** | 4.5:1 | ✅ |
| 連結 / Off-white | `navy-700` #2E3092 | `gray-50` #F7F8FA | **10.11:1** | 4.5:1 | ✅ |
| 連結 hover / 白底 | `navy-800` #1E2466 | `white` #FFFFFF | **14.01:1** | 4.5:1 | ✅ |
| 綠色小字（eyebrow）/ 白底 | `green-700` #1B7431 | `white` #FFFFFF | **5.85:1** | 4.5:1 | ✅ |
| 綠色小字 / Off-white | `green-700` #1B7431 | `gray-50` #F7F8FA | **5.51:1** | 4.5:1 | ✅ |
| 綠色標籤文字 / 綠淡底 | `green-800` #15612A | `green-50` #F1F9F3 | **7.06:1** | 4.5:1 | ✅ |
| Logo 綠：僅限大字(≥24px)或圖示 | `green-600` #27903A | `white` #FFFFFF | **4.09:1** | 3:1 | ✅ |
| 主要按鈕文字 | `white` #FFFFFF | `navy-700` #2E3092 | **10.75:1** | 4.5:1 | ✅ |
| 主要按鈕 hover | `white` #FFFFFF | `navy-800` #1E2466 | **14.01:1** | 4.5:1 | ✅ |
| 主要按鈕 active / 深色區塊內文 | `white` #FFFFFF | `navy-900` #151A4D | **16.32:1** | 4.5:1 | ✅ |
| Footer 標題 | `white` #FFFFFF | `navy-950` #0E1238 | **18.07:1** | 4.5:1 | ✅ |
| Footer 次要文字 | `gray-300` #C9CED8 | `navy-950` #0E1238 | **11.45:1** | 4.5:1 | ✅ |
| Hero 副標 / 深藍底 | `navy-200` #CDD0F1 | `navy-900` #151A4D | **10.79:1** | 4.5:1 | ✅ |
| 深藍底上的綠色小字 | `green-200` #C4E7CC | `navy-900` #151A4D | **12.16:1** | 4.5:1 | ✅ |
| 白色按鈕文字（深色區塊內反白按鈕） | `navy-900` #151A4D | `white` #FFFFFF | **16.32:1** | 4.5:1 | ✅ |
| 綠色徽章文字（少量使用） | `white` #FFFFFF | `green-700` #1B7431 | **5.85:1** | 4.5:1 | ✅ |
| 錯誤訊息 | `red-700` #B42318 | `white` #FFFFFF | **6.57:1** | 4.5:1 | ✅ |
| 錯誤訊息 / 淡紅底 | `red-700` #B42318 | `red-50` #FEF3F2 | **6.05:1** | 4.5:1 | ✅ |
| 表單邊框（非文字 3:1） | `gray-500` #6E7585 | `white` #FFFFFF | **4.62:1** | 3:1 | ✅ |
| Focus ring / 白底（非文字 3:1） | `navy-600` #3F45A8 | `white` #FFFFFF | **7.99:1** | 3:1 | ✅ |
| Focus ring / Off-white | `navy-600` #3F45A8 | `gray-50` #F7F8FA | **7.52:1** | 3:1 | ✅ |
| Focus ring（白）/ 深藍底 | `white` #FFFFFF | `navy-900` #151A4D | **16.32:1** | 3:1 | ✅ |
| 選單目前頁指示線（非文字 3:1） | `green-600` #27903A | `white` #FFFFFF | **4.09:1** | 3:1 | ✅ |
| 次要按鈕邊框（非文字 3:1） | `navy-700` #2E3092 | `white` #FFFFFF | **10.75:1** | 3:1 | ✅ |
| 反白框線按鈕邊框 / 深藍底（非文字 3:1） | `navy-300` #A9ADE3 | `navy-900` #151A4D | **7.60:1** | 3:1 | ✅ |

另外有一組不需要達標的裝飾性組合：卡片邊框 `gray-300` 在白底上是 1.58:1。它只用來區隔版面、不承載資訊，所以不需要 3:1。

**使用規則**
1. Logo 綠 `#27903A` 不能當一般大小的文字。
2. 表單邊框用 `gray-500`（4.62:1），不能用 `gray-200`／`gray-300`。
3. 灰色文字最淺只能到 `gray-600`；`gray-500` 以下不能用於文字（停用狀態除外，WCAG 豁免）。
4. 深藍底上只能放白色、`navy-200`、`green-200`、`gray-300` 這幾種文字色。

## 4. 核心元件：沒有照片時如何維持份量 [PROPOSED]

整體策略有四點：

1. **大色塊**：用深藍大面積色塊建立重量與信任感。
2. **品牌圖形**：用取自 Logo 的十字圖形代替照片。
3. **字級對比**：用明顯的字級差拉出層級。
4. **陰影節制**：只在可以點擊的物件上用陰影。

| 元件 | Class | 規格 |
|---|---|---|
| Header／導覽列 | `.pfo-header` `.pfo-nav` | 白底，底部細線加極淡陰影，sticky。目前頁：深藍粗體加 3px 綠色指示線（綠色呼應 Logo 十字）。「聯絡我們」是唯一的實心按鈕。寬度小於 1024px 時改成電話按鈕加漢堡選單（兩者都是 44×44） |
| 主要按鈕 | `.pfo-btn--primary` | navy-700 底白字（10.75:1），高 48，圓角 8，字重 700；hover 變 navy-800 並加陰影 md；不做縮放或彈跳動畫 |
| 次要按鈕 | `.pfo-btn--secondary` | 白底，1.5px navy-700 邊框與文字；hover 換成 navy-50 底 |
| 深色底按鈕 | `.pfo-btn--inverse` `.pfo-btn--ghost-inverse` | 白底深藍字；外框版為 navy-300 邊框（7.60:1） |
| 箭頭連結 | `.pfo-link-arrow` | 「了解更多 →」，最小高度 44 |
| Hero（無照片） | `.pfo-hero` | navy-900 滿版色塊，Display 字級白字，副標用 navy-200。右側放大的 Logo 圓徽十字作裝飾（`aria-hidden`，外圈 navy-800，十字 green-600） |
| 服務卡片 | `.pfo-card` `.pfo-icon-badge` | 白卡、1px gray-200 邊框、圓角 12、陰影 xs。用 56×56 品牌淡底圖示徽章代替照片（照護用深藍、透析用綠）。整張卡可點擊時，hover 浮起 2px 並加深陰影；使用者設定減少動態時關閉 |
| 產品卡片 | `.pfo-product-card` `.pfo-media-fallback` | 圖片區用 navy-50 底加上 Logo 十字紋樣，中間放大字產品線名稱。**這是可以直接上線的正式樣式，不是佔位框**；取得授權圖片後，只要把這個區塊換成 `<picture>` |
| 最新消息 | `.pfo-news` | 平板以上日期與內容左右並排；日期用等寬數字；只用分隔線，不做成卡片 |
| 據點卡片 | `.pfo-office` | 地點圖示徽章加上 `<dl>` 地址、電話、傳真 |
| CTA 區塊 | `.pfo-cta` | navy-900 圓角 20 的區塊，搭配白色按鈕 |
| 標籤 | `.pfo-tag` `.pfo-eyebrow` | 綠色淡底加 green-800 文字（7.06:1）；Eyebrow 用 green-700，13px，字距加寬 |
| 跳至主內容 | `.pfo-skip` | 只在鍵盤 focus 時出現 |

**刻意避免**（依專案規範）：大面積漸層、卡片左側色條、到處都用同樣的圓角加陰影、emoji 圖示、圖庫照片、過度動畫。

## 5. 樣式預覽頁使用的文案

所有示範內容都取自舊站原文或官方登記。以下為 [PROPOSED COPY]：

- 按鈕文字：「查看服務項目」「了解更多」「查看產品」
- 據點名稱：「北部據點（總公司）」等
- Hero 的 eyebrow：「健康照護・透析通路」
- CTA：「想進一步了解？請聯絡我們」

Trixo 產品卡上的 3 個品名照舊站原文列出。

---

## Phase 4 Status

**Completed**
- 從 Logo 逐像素取樣出品牌色，建立 Navy／Green／Neutral 完整色階與語意角色
- `tokens.css`：色彩、字型、字級、行高、間距、版面、圓角、陰影、斷點、Focus、動態、Z-index、元件 Token
- 34 組前景／背景組合的 WCAG 2.1 AA 驗證，全部通過
- `components.css`：Header／導覽、按鈕 4 種、Hero、服務卡、產品卡加 Media Fallback、消息列表、據點卡、CTA、Footer、標籤、跳至主內容
- 視覺預覽頁（本機 `styleguide.html` 與線上 Artifact）

**Pending**
- Logo 向量檔（G1）：取得後重新確認品牌色，並產生 SVG Logo、favicon、OG 圖
- 表單元件：目前沒有表單（H14），只預留 input token

**Needs Confirmation**
- 業主認可這組品牌色延伸：Deep Navy `#151A4D`、綠色文字 `#1B7431`
- 營運資料 H3／H4／H5／H7／H12 等，依業主安排在 Phase 5 前確認

**Problems Found**
- Logo 綠 `#27903A` 對白底只有 4.09:1，**不能**直接當一般文字色，已用 green-700 取代並寫進規則。
- 舊站 Logo 的中文字標是純黑 `#000000`。新網站的文字用 gray-900，Logo 本身不改。將來做 SVG 時，字標要不要維持純黑，由業主決定 [NEEDS CONFIRMATION]。
- 系統字型在 Windows（微軟正黑體）只有 Regular／Bold，沒有 500 字重，會顯示成 Regular。因此設計上只依賴 400／700 兩種字重。

**Next Step**
- 業主確認設計系統，並在 Phase 5 前回覆營運資料後，進入 **PHASE 5：Homepage**。
- 首頁會建在 `/PFO-v2/`：語意化 HTML，套用 `tokens.css` 加 `components.css`，測試期間全頁加 `noindex`。
