# PFO_NewWeb — PHASE 1：現有網站 Reverse Engineering

- 分析對象：https://www.newimage2023.com.tw/PFO/index.html
- 分析日期：2026-09-23
- 方法：以瀏覽器載入頁面，同源抓取全部 HTML／CSS／圖片，逐頁擷取內容與 HTTP header；未修改任何線上檔案。
- 標記說明：
  - **[CONFIRMED]** 直接從現有網站原始碼 / HTTP 回應取得
  - **[INFERENCE]** 由觀察推論，未經證實
  - **[NEEDS CONFIRMATION]** 需業主確認
  - **[PROPOSED]** 本分析的建議，非公司正式資料

> 限制：本次未執行 Lighthouse（雲端環境無法連到該網域），效能數據來自實際下載檔案大小與單次瀏覽器載入量測，不是 Lighthouse 分數。

---

## 1. 現有網站總覽（Findings 1–16）

### 1.1 Sitemap / 所有頁面 / 所有 URL [CONFIRMED]

爬蟲自首頁遞迴追蹤所有 `/PFO/` 內部連結，共找到 **7 個 HTML 頁面**：

| # | 頁面 | URL | 狀態 |
|---|------|-----|------|
| 1 | 首頁 | `/PFO/index.html`（`/PFO/` 同內容） | 200 |
| 2 | 關於我們 | `/PFO/intro.html` | 200 |
| 3 | 服務項目 | `/PFO/service.html`（錨點 `#s_01` 照護相關、`#s_02` 透析通路；`#s_03` 為空區塊） | 200 |
| 4 | 代理產品 – B'BRAUN | `/PFO/product_b.html`（錨點 `#p_03` TRIXO 系列） | 200 |
| 5 | 代理產品 – B'BRAUN IDPN | `/PFO/product_idpn.html` | 200 |
| 6 | 最新消息列表 | `/PFO/news/news_list.html` | 200 |
| 7 | 最新消息內頁 | `/PFO/news/2014/news_140221.html` | 200 |

其他：
- **沒有**獨立「聯絡我們」頁；聯絡資訊放在每頁左側欄與 footer。
- `robots.txt`、`sitemap.xml`、`favicon.ico`（根目錄與 /PFO/）皆 **404**。
- 首頁新聞「2018.12.10」**沒有內頁**。
- 新聞列表有被註解掉的「歷年最新消息 2014 / 2013」區塊（HTML comment）。

### 1.2 主要文字內容 [CONFIRMED，原文節錄]

**全站 meta description**（7 頁完全相同）：
> 保富齡健康事業股份有限公司以創新的理念提供專業的產品服務,專注的態度提供全方位的通路規劃,讓公司創造一個全新領域的健康照護產業,成為讓大眾幸福樂活的優質企業。

**首頁**
- 主視覺：`main.jpg`（大樓外觀照片）
- 最新消息：2014.02.21 Trixo 萃詩護手霜（有 More）；2018.12.10「本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。」（無內頁）
- 代理產品卡片：
  - B'BRAUN —「柏朗集團為全球性跨國企業,總部設於德國,成立至今已逾百年,為歐洲市場醫療器材領域之領導品牌。」
  - B'BRAUN IDPN —「台灣柏朗對透析中靜脈營養補充(IDPN)的現代方法使您能夠快速識別成功的治療。」

**關於我們（intro.html）**
- 願景：同 meta description 文字
- 公司簡介：
  - 保富齡健康事業股份有限公司 / PFL renal service co.,Ltd.
  - 負責人：白靖騰 先生
  - 成立日期：中華民國 100年 9月 5日
  - 資本額：新台幣 112,000,000元
  - 公司登記地址：新北市中和區中正路928號3F
  - 公司統一編號：53599511
  - 北／中／南三據點（見 1.6）
- 圖片：台灣地圖標示 Taipei / Taichung / Kaohsiung Office（`intro_01.jpg`）
- 營運目標方向：
  - 電子商務：熟齡保養品、老人輔具、生活照護用品之銷售；長青族電子商務網購平台
  - 整合照護中心：糖尿病病友會員中心；血漿置換中心；相關藥品及健食銷售
  - 透析通路：相關透析產品之行銷；專業透析中心合作規劃
  - 結腸灌洗：設備儀器銷售與租賃（水天使專案）；結腸灌洗治療中心合作

**服務項目（service.html）**
- 照護相關：「提供糖尿病患及安養長照相關耗材儀器及專業傷口照護之有效產品。」「腸道健康照護系統設備合作規劃。」
- 透析通路：「**目前彩新公司**合作單位計有28家, 超過500床,每月治療約22,000人。」← 見 Problems：這是**彩新公司**的數據

**代理產品 – B'BRAUN（product_b.html）**：只有 TRIXO 系列 3 項
| 產品名稱（原文） | 規格 |
|---|---|
| Trixo Bottle "WEST" / 萃詩正常肌膚用護手霜 | 20ml/100ml/500ml |
| TRIXOLIND Bottle WEST / 萃詩抗乾敏護膚護手乳液 | 20ml/100ml/500ml |
| TRIXOLIND PURE TUBE WEST / 萃詩純淨抗乾敏護膚護手乳液(無香) | 20ml/100ml/500ml |

每項附「產品特點」3 點（pH 5.5、維他命 B5 及尿囊素等）。

**代理產品 – B'BRAUN IDPN（product_idpn.html）**
- 唯一 HTML 文字：「台灣柏朗對透析中靜脈營養補充(IDPN)的現代方法使您能夠快速識別成功的治療，產品資訊請洽專業醫療團隊。間歇性營養治療可被選擇性地使用，並且當患者的狀態穩定時可以隨時停止，該療法具有相當多的優點。」
- 其餘全部是**圖片中的文字**（6 張圖，alt 全空）：標題「血液透析與營養 兩項治療，同一個目標」、B|BRAUN logo、產品「NuTRIflex® Lipid Special (625ml) 欣保富□靜脈營養輸注液」（圖片解析度不足以辨識第 4 字；醫院藥品資料寫作「欣保富瀀」，正式名稱 [NEEDS CONFIRMATION]）、適應症、成分／電解質表、「Complete Nutrition 全方位營養治療」圖解、4 篇參考文獻。

**最新消息內頁（news_140221.html）**
- 標題：「對於羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜」
- 內容：羊毛脂說明、Trixo 萃詩護手霜 7 項特點、Trixo-lind Pure 萃詩純淨抗乾敏護手霜 6 項特點

### 1.3 圖片與 Logo [CONFIRMED]

| 檔案 | 用途 | 顯示尺寸 | 檔案大小 | alt |
|---|---|---|---|---|
| `img/logo.gif` | Logo（PFO 圓形徽章 + 綠十字 +「保富齡健康事業」） | 273×68 | 6.4 KB | 保富齡健康事業股份有限公司 |
| `img/main.jpg` | 首頁主視覺（大樓照片） | 680×260 | **316.9 KB** | main image |
| `img/intro_01.jpg` | 台灣據點地圖 | 655×617 | 146.7 KB | **#** |
| `img/product_i01–06.jpg` | IDPN 圖文 | 655 寬 | 合計 **722 KB** | **空** |
| `img/product_b12–14.jpg` | Trixo 產品照 | ~110–150 px | 11–16 KB | 產品名 |
| `img/topics_01.jpg` / `topics_03.jpg` | 首頁產品卡縮圖 | 90×90 | 6 / 13 KB | 皆為「Bbraun」 |
| `img/links_03.jpg` | 側欄 Trixo banner | — | 6.8 KB | Trixo news |
| `news/2014/img/news_0521.jpg` | 新聞圖 | 190×171 | 5.1 KB | Trixo 萃詩護手霜 |
| `img/logolink1.png` | Header 右上連結圖：「new image 彩新健康事業」 | 207×18 | 5.2 KB | （CSS 背景，無文字） |
| `img/line_03.jpg` 等 | 1px 分隔線、背景圖、icon | — | 小 | 無 |

- Logo 只有 **GIF 點陣檔**，無向量檔、無 favicon。
- Logo 顏色 [INFERENCE，目視]：深藍圓徽 + 綠色十字 → 與本專案「Deep Navy + Healthcare Green」方向相容。
- 圖片版權來源皆未標示 [NEEDS CONFIRMATION]。

### 1.4 公司資訊 [CONFIRMED，原文]

見 1.2「關於我們」。注意資料之間的不一致，列於 Problems 與 H。

**與經濟部商業司公開資料比對**（2026-09-23 查詢，來源：data.gcis.nat.gov.tw 公司登記開放資料 API）：

| 欄位 | 舊網站 | 官方登記 | 結果 |
|---|---|---|---|
| 統一編號 | 53599511 | 53599511 | 一致 |
| 公司名稱 | 保富齡健康事業股份有限公司 | 同 | 一致 |
| 公司狀況 | — | 核准設立 | — |
| 代表人 | 白靖騰 | 白靖騰 | 一致 |
| 核准設立日期 | 民國100年9月5日 | 1000905 | 一致 |
| 所在地 | 新北市中和區中正路928號3F | 新北市中和區中正路928號3樓 | 一致 |
| 資本額 | 新台幣 112,000,000元 | 資本總額 200,000,000；實收 190,000,000 | **不一致（舊網站過時）** |
| 最後核准變更日期 | — | 1150714（2026-07-14） | — |
| 登記機關 | — | 新北市政府 | — |
| 英文名稱 | PFL renal service co.,Ltd. | 此 API 無英文名稱欄位 | 無法驗證 |

- 所營事業登記共 47 項，包含醫療器材批發/零售（F108031/F208031）、西藥批發/零售（F108021/F208021）、化粧品批發/零售等。所營事業只代表「可以做」，**不代表**實際提供的服務，不可當作服務內容使用。
- 部分第三方公司資料網站顯示不同的代表人與地址，資料日期不明；本文件只採用官方開放資料。

### 1.5 服務內容 / 代理產品 / 最新消息

見 1.2。重點：
- 服務：2 項（照護相關、透析通路），文字各 1–2 句。
- 代理產品：2 頁（B'BRAUN → 實際只有 Trixo 3 品項；B'BRAUN IDPN → 1 品項，內容為圖片）。
- 最新消息：2 則（2014.02.21、2018.12.10），最近一則距今約 8 年。

### 1.6 聯絡資訊 [CONFIRMED]

| 據點 | 地址 | 電話 | 傳真 |
|---|---|---|---|
| 北（總公司／登記地址） | 新北市中和區中正路928號3F | (02)8221-5123 | (02)8221-5122 |
| 中 | 台中市西區五權路2-107號15樓 | (04)2376-2333 | (04)2376-1177 |
| 南 | 高雄市苓雅區三多二路171號9F-1 | (07)716-8518 | (07)716-8730 |

- Email：pfl@pfl.tw（純文字，非 `mailto:` 連結）
- 電話非 `tel:` 連結；無地圖、無聯絡表單、無營業時間、無社群連結。

### 1.7 外部連結 [CONFIRMED]

- 全站唯一對外連結：Header 右上「new image 彩新健康事業」圖片 → `../index.html`，即 **網域根目錄的「彩新健康事業股份有限公司」網站**。
- 無 B. Braun 原廠、無社群、無地圖外連。

**重要發現**：`newimage2023.com.tw` 網域根目錄是「**彩新健康事業股份有限公司**」網站（© 2014，Email new.image@msa.hinet.net，總公司台中）。兩站**共用相同的北中南三個地址與電話**、相同版型結構。保富齡網站是寄居在彩新網域下的子目錄。兩家公司的關係 [NEEDS CONFIRMATION]。

### 1.8 技術架構 [CONFIRMED]

| 項目 | 現況 |
|---|---|
| 類型 | 純靜態 HTML，7 個檔案，手工維護（header／menu／footer 每頁複製） |
| Doctype | XHTML 1.0 Transitional，`lang="ja"`（**日文**） |
| CSS | 單檔 `css/layout_pfo.css`（11.7 KB），float 版面、固定 px 寬、大量背景圖 |
| JavaScript | **0 個** |
| 字型 | Verdana, Geneva, sans-serif, "新細明體"；body 13px |
| 配色 | 粉紅／玫瑰系：#eec3c8 背景、#d98888、#944180、#cc4c4c |
| Server | LiteSpeed，HTTPS，HTTP/2 |
| 壓縮 | HTML 有 brotli |
| 快取 | 圖片 `max-age=604800`（7 天）；HTML 無 Cache-Control |
| Last-Modified | 全部 2024-02-15（[INFERENCE] 多半是整批上傳時間，不代表內容更新日） |
| 模板來源 | [INFERENCE] 與彩新網站共用同一套模板（相同 doctype、`lang="ja"`、id 命名） |

### 1.9 RWD 狀況 [CONFIRMED]

- **沒有** `<meta name="viewport">`。
- `#WRAPPER` 固定 `width:1024px`，側欄 200px + 主區 700px，全部 float。
- 手機（375/390/430）會以縮小的桌面版顯示，需要雙指放大；平板直向 768 會出現水平捲軸（實測 765px 寬視窗已出現水平捲軸）。
- 結論：**完全不支援 RWD**。

### 1.10 SEO 狀況 [CONFIRMED]

| 項目 | 現況 |
|---|---|
| `<title>` | 7 頁**全部相同**「保富齡健康事業股份有限公司」 |
| meta description | 7 頁全部相同 |
| meta keywords | 有（搜尋引擎已不採用），列出 Tsukuru、創姿、血糖機、胰島素空針、Prontosan、Linovera oil 等**網站上不存在的產品** |
| canonical / Open Graph / Twitter Card | 無 |
| favicon | 無 |
| robots.txt / sitemap.xml | 404 |
| lang | `ja`（錯誤，應為 `zh-Hant-TW`） |
| Heading | 每頁 H1 = Logo 圖；產品頁又有第二個 H1；區塊標題用 `<h2><p>…</p></h2>`（無效巢狀） |
| 結構化資料 | 無（無 Organization / LocalBusiness schema） |
| URL | 檔名式（`product_b.html`、`news_140221.html`），可讀性普通 |
| 網域 | 使用彩新的網域 `newimage2023.com.tw/PFO/`，非保富齡自有網域 |
| 內容 | 內容量極少且過期；IDPN 頁主要內容是圖片，搜尋引擎無法讀取 |

### 1.11 Accessibility 問題 [CONFIRMED]

1. `lang="ja"`，螢幕報讀器會用日文發音。
2. 無 `<header>/<nav>/<main>/<footer>` 地標、無 skip link。
3. Header「彩新」連結是**空的 `<a>`**（只有 CSS 背景圖）→ 報讀器讀不到連結名稱。
4. IDPN 6 張資訊圖 `alt=""`，重要資訊（適應症、成分）對視障者完全不可得；地圖 `alt="#"`；主圖 `alt="main image"`；兩張不同縮圖 alt 都是「Bbraun」。
5. Heading 階層混亂（多 H1；產品頁 H1 出現在 H2 之後；新聞內頁 H4 日期在 H3 標題之前；`<h2><p>` 無效巢狀）。
6. HTML 結構無效：`<p>` 放在 `<dl>` 內、`<br>` 放在 `<dl>` 內、重複 id（`#bigimg`、`#product_img` 在同頁出現多次）。
7. 色彩對比不足（依 CSS 色碼計算，WCAG AA 一般文字需 4.5:1）：
   - `More` 按鈕：白字 / #d98888 = **2.68:1** ✗
   - 新聞日期：#d18181 / 白 = **2.93:1** ✗（且 12px）
   - 其餘主要文字（#333、#944180、#717171）通過
8. 字級 12–13px，加上 `letter-spacing`，閱讀負擔高。
9. 導覽中「服務項目」「代理產品」是不可點的 `<h2>` 文字，與可點的項目外觀相同，易混淆。
10. 「TOP」連結 `href="#"`；Email 與電話不是可點的連結。

### 1.12 Performance 問題 [CONFIRMED 檔案大小；INFERENCE 影響]

- 首頁估算傳輸量約 **0.43 MB**（HTML 4 KB + CSS 12 KB + 圖片約 0.41 MB），其中 `main.jpg` **317 KB** 只顯示在 680×260 → 過大約 3–5 倍 [INFERENCE]。
- IDPN 頁圖片合計 **722 KB**，且全是 JPG 文字圖。
- 無 WebP/AVIF、無 `srcset`、無 `loading="lazy"`；部分 `<img>` 無 width/height（造成版面位移 CLS）。
- 大量 1px 分隔線、按鈕背景都用圖片（多餘請求）。
- 單次瀏覽器量測（非 Lighthouse）：TTFB 241 ms、load 831 ms。因為內容少、無 JS，**絕對速度並不差**；問題在於圖片未最佳化與無法在行動裝置正常使用。

---

## A. Current Sitemap [CONFIRMED]

```
/PFO/index.html  首頁
├── /PFO/intro.html                      關於我們
├── /PFO/news/news_list.html             最新消息
│   └── /PFO/news/2014/news_140221.html  Trixo 萃詩護手霜（2014.02.21）
│       （2018.12.10 IDPN 消息：僅首頁摘要，無內頁）
├── 服務項目（不可點的分類標題）
│   ├── /PFO/service.html#s_01           照護相關
│   └── /PFO/service.html#s_02           透析通路
├── 代理產品（不可點的分類標題）
│   ├── /PFO/product_b.html              B'BRAUN（實際內容：TRIXO 系列）
│   └── /PFO/product_idpn.html           B'BRAUN IDPN
└── 外連：../index.html                  彩新健康事業網站
```

## B. Current Content Inventory

| 內容 | 位置 | 可沿用？ | 備註 |
|---|---|---|---|
| 公司正式中文名、負責人、成立日、資本額、登記地址、統編 | intro | ✓ 待確認是否仍正確 | 資料可能已變更（多年未更新） |
| 英文名「PFL renal service co.,Ltd.」 | intro | ? | 與 Logo「PFO」不一致 |
| 願景文字 | intro / meta | ✓ | 可作首頁主標語來源 |
| 營運目標方向（4 大方向） | intro | ? | 屬「規劃」，是否已實現或仍有效不明 |
| 北中南據點、電話、傳真、Email | 全站 | ✓ 待確認 | 與彩新共用 |
| 台灣據點地圖圖片 | intro | ✗ | 畫質低、無 alt，建議以 HTML 重做 |
| 服務：照護相關 2 句 | service | ✓ | 內容太薄 |
| 服務：透析通路（28 家、500 床、22,000 人） | service | **✗** | 明寫「彩新公司」的數據，不可直接當保富齡數據 |
| Trixo 3 品項 + 規格 + 特點 | product_b | ✓ 待確認 | 仍在販售？名稱「霜／乳液」與新聞不一致 |
| IDPN 產品說明（NuTRIflex Lipid Special） | product_idpn | **?** | 需法規與原廠授權確認（見 H） |
| 新聞 2014.02.21 Trixo | news | ✓ | 過期，可歸入「歷史消息」 |
| 新聞 2018.12.10 IDPN | 首頁 | ? | 只有一句，無內文 |
| Logo GIF | 全站 | △ | 僅能暫用，需向量檔 |
| 首頁大樓照片 | index | ? | 來源、授權、是否為公司所在大樓不明 |

## C. Current Problems

**C1. 內容／資料正確性（最高優先）**
1. 服務頁引用「**彩新公司**」的合作單位與治療人數數據。
2. 公司身分混淆：寄居彩新網域、header 連到彩新、兩站共用地址電話；保富齡與彩新的關係未說明。
3. 名稱不一致：Logo「PFO」／英文名「PFL renal service co.,Ltd.」／Email「pfl.tw」。
4. 年份不一致：成立日期民國 100 年（2011）但 footer 為 © 2014。
5. meta keywords 列出大量網站上不存在的品牌與品項。
6. 首頁 B'BRAUN IDPN 卡片標題連到 `product_b.html`（錯誤），More 才連到 IDPN 頁。
7. 最新消息停在 2018 年，且排序為舊→新。
8. 「B'BRAUN」頁實際只有 Trixo 系列，頁名與內容不符。
9. Trixo 產品名在產品頁（乳液）與新聞頁（護手霜）不一致。
10. IDPN 頁以圖片呈現「限由醫師使用」之靜脈營養藥品資訊，法規與授權風險待確認。

**C2. 設計／UX**：2010 年代固定寬版型、粉紅色系與醫療專業形象不符、大量背景圖與框線、字級過小、無 CTA、無聯絡頁與地圖。

**C3. 技術**：無 RWD、XHTML 過時 doctype、`lang="ja"`、共用區塊每頁複製、無效 HTML、重複 id。

**C4. SEO**：全站 title/description 相同、無 canonical/OG/favicon/robots/sitemap、內容以圖片呈現、非自有網域。

**C5. Accessibility**：見 1.11，約 10 類問題，現況明顯未達 WCAG 2.1 AA。

**C6. Performance**：見 1.12，主要是圖片未最佳化；絕對載入量不大。

## D. Recommended New Sitemap [PROPOSED]

原則：**只為有真實內容的頁面建頁**；內容不足時合併而非拆分。部署於 `/PFO-v2/`，採「目錄 + index.html」URL，在靜態主機上即可得到乾淨網址，不需伺服器 rewrite。

```
/PFO-v2/                         首頁
├── /about/                      關於我們（願景、公司簡介、據點）
├── /services/                   服務項目（照護相關、透析通路；單頁錨點）
├── /products/                   代理產品總覽
│   ├── /products/trixo/         Trixo 萃詩系列（B. Braun）
│   └── /products/idpn/          IDPN（⚠ 視法規確認結果決定是否公開、或改為「醫療專業人員」導向內容）
├── /news/                       最新消息列表
│   └── /news/2014-02-21-trixo/  （既有新聞，保留）
├── /contact/                    聯絡我們（三據點、電話、Email、地圖外連）
├── /privacy/                    隱私權政策 ⚠ 僅在有表單或分析工具時需要，內容須由業主/法務提供
├── 404.html
├── sitemap.xml
└── robots.txt
```

- 前提（2026-09-23 決定）：以**保富齡獨立網站**規劃；彩新網站連結**不列入**正式 Sitemap、Header、Footer，待 H1 確認後再調整。
- 「營運目標方向」是否放上網站 → 依 H 確認結果。
- 不建議新增「合作夥伴、徵才、客戶案例」等頁，除非業主提供真實內容。
- 舊 URL → 新 URL 的 301 對照表於 Production Cutover 前建立（Phase 8）。

## E. Recommended Information Architecture [PROPOSED]

**Global Navigation**（5 項 + 1 CTA）：關於我們｜服務項目｜代理產品｜最新消息｜聯絡我們 ＋ 右側「聯絡我們」主按鈕（手機版：電話可一鍵撥打）

**Footer**：Logo、公司正式名稱、三據點地址/電話/傳真、Email、統一編號（待確認是否公開）、快速連結、版權年份。

**首頁模組順序**
1. Hero：公司名 + 以既有「願景」文字為主標語（不另創口號，改寫時標 [PROPOSED COPY]）
2. 服務項目：2 張卡片（照護相關、透析通路）
3. 代理產品：Trixo、IDPN（視確認結果）
4. 最新消息：最新 3 則（新→舊）
5. 據點與聯絡：北中南三卡片 + CTA

**不放入**：任何數字統計（因現有數據屬彩新）、客戶/醫院 logo、推薦語，除非業主提供。

**內容模型**（供之後模板化）：Page、Service、Product（名稱、品牌、規格、特點、圖片）、News（日期、標題、摘要、內文、圖片）、Office（名稱、地址、電話、傳真）。

## F. Recommended Design Direction [PROPOSED]

- 延續專案定義：Professional / Healthcare / Trust / Clean / Modern。
- **色彩**：以現有 Logo 的深藍 + 綠十字為錨點 → Primary Deep Navy / Deep Teal、Secondary Healthcare Green；**淘汰現有粉紅色系**。精確色碼待取得 Logo 向量檔後於 Phase 4 取樣並驗證對比。
- **字型**：系統中文字型堆疊（PingFang TC / Microsoft JhengHei / Noto Sans TC），不載入大型 webfont，兼顧效能；內文 16px 起、行高 1.7。
- **版面**：12 欄 grid、最大內容寬約 1200px、大量留白、卡片式但少框線。
- **影像**：以真實照片為優先；無可用照片時使用純色/幾何圖形區塊，不使用來源不明的圖庫照片。
- **資訊圖改 HTML**：IDPN 成分表、據點地圖改用 HTML 表格/卡片，兼顧 SEO 與無障礙。
- **動態**：僅保留 hover/focus 微互動，尊重 `prefers-reduced-motion`。

**技術建議**：純 HTML5 + CSS3（CSS Variables）+ 少量 ES6。理由：頁數少（約 8–10 頁）、無會員/交易需求、現有主機為 LiteSpeed 靜態主機，Framework 只會增加維護成本。共用 header/footer 的重複問題，建議在 Phase 4–5 決定：(a) 手動維護，或 (b) 加入輕量靜態產生器（如 Eleventy）只在建置時產出純 HTML。→ [NEEDS CONFIRMATION：團隊是否接受 Node 建置步驟]

## G. Required Assets

| # | 資產 | 用途 | 現況 |
|---|---|---|---|
| G1 | Logo 向量檔（AI/SVG/EPS）+ 標準色 | Header、favicon、OG | 只有 GIF |
| G2 | 公司實景照片（辦公室、團隊、倉儲等）及授權 | Hero、關於我們 | 無 |
| G3 | 首頁大樓照片的來源與授權 | 決定是否沿用 | 不明 |
| G4 | B. Braun 品牌與 logo 使用授權、官方高解析產品圖 | 產品頁 | 僅小圖 |
| G5 | Trixo 產品高解析圖、最新品項與規格 | 產品頁 | 11–16 KB 小圖 |
| G6 | IDPN 可公開的文字資料（非圖片）與原廠授權 | IDPN 頁 | 僅圖片 |
| G7 | 2018 年後的新聞/公告內容 | 最新消息 | 無 |
| G8 | 各據點 Google Maps 連結、營業時間 | 聯絡頁 | 無 |
| G9 | 網域與主機（FTP/cPanel）存取權 | 部署 /PFO-v2/ | 未知 |
| G10 | OG 分享圖（1200×630） | SEO | 無（可由 G1 產生） |
| G11 | 是否使用 GA4 / Search Console | 分析 | 未知 |

## H. Information That Needs Owner Confirmation

> 2026-09-23 更新：H1、H2、H3、H6、H8、H10、H11 已有處理方式，詳見文末「H 決策紀錄」。

1. [NEEDS CONFIRMATION] 保富齡與**彩新健康事業**的關係？新網站是否還要連到彩新？ → **維持未確認**；不推測、不引用彩新資料（見決策紀錄）
2. [NEEDS CONFIRMATION] 正式英文公司名稱與簡稱：PFO？PFL？「PFL renal service co.,Ltd.」是否仍正確？ → 暫不使用英文名
3. [NEEDS CONFIRMATION] 負責人、資本額、登記地址、統一編號是否仍正確，且是否要在網站公開？ → 已查官方登記，**舊網站資本額已過時**；是否公開仍待確認
4. [NEEDS CONFIRMATION] 北中南三個據點、電話、傳真是否仍有效？是否都屬於保富齡？
5. [NEEDS CONFIRMATION] Email pfl@pfl.tw 是否仍使用？（本次查詢 pfl.tw 無法解析 DNS，未能確認網站存在）
6. [NEEDS CONFIRMATION] 新網站最終網域：維持 `newimage2023.com.tw/PFO/`，或使用保富齡自有網域？（影響 canonical、sitemap、Email 品牌一致性）
7. [NEEDS CONFIRMATION] 服務項目是否仍為「照護相關」「透析通路」兩項？有無新增/停止？
8. [NEEDS CONFIRMATION] 服務頁「28 家、500 床、每月 22,000 人」屬彩新；保富齡是否有自己的可公開數據？若無，新網站不放數字。
9. [NEEDS CONFIRMATION] 「營運目標方向」（電子商務、整合照護中心、結腸灌洗/水天使專案等）是否已實現、仍在規劃或已停止？是否上網？
10. [NEEDS CONFIRMATION] 目前代理/經銷品項完整清單：Trixo 3 品項是否仍販售？keywords 中的 Tsukuru、創姿、血糖機、胰島素空針、Prontosan、Linovera oil 是否仍有代理？
11. [NEEDS CONFIRMATION] IDPN（NuTRIflex Lipid Special）屬「限由醫師使用」之靜脈營養藥品：是否可對一般大眾公開產品資訊？是否取得台灣柏朗/原廠授權使用其圖文？建議由業主法務或原廠確認（我不是法律顧問，這裡只指出風險）。
12. [NEEDS CONFIRMATION] 「保富齡是 B. Braun 的代理商或經銷商」的正式稱謂（首頁新聞寫「經銷」，選單寫「代理產品」）。
13. [NEEDS CONFIRMATION] 2018.12.10 那則新聞是否有完整內容？2018 年之後有無消息？
14. [NEEDS CONFIRMATION] 是否需要聯絡表單？（若需要，須決定收件信箱、後端寄信方式、個資告知與隱私權政策）
15. [NEEDS CONFIRMATION] 主機環境：是否可在同主機建立 `/PFO-v2/` 目錄？是否支援 .htaccess（301 轉址）？
16. [NEEDS CONFIRMATION] 是否需要英文版？

## I. Recommended Development Roadmap [PROPOSED]

| Phase | 內容 | 產出 | 前置條件 |
|---|---|---|---|
| 1 ✅ | Reverse Engineering | 本文件 | — |
| 2 | Sitemap + IA 定稿 | 定稿 sitemap、頁面清單、內容模型、舊→新 URL 對照 | **H1、H6、H7–H12 回覆** |
| 3 | Wireframe | 首頁 + 各內頁 Desktop/Mobile 低保真線框 | Phase 2 |
| 4 | Visual Design System | Design Tokens（色彩/字型/間距/圓角/陰影/斷點）、元件樣式、對比驗證 | G1 Logo 向量檔 |
| 5 | Homepage | `/PFO-v2/index.html` | Phase 3–4 |
| 6 | Inner Pages | about / services / products / news / contact / 404 | 內容確認 |
| 7 | Responsive | 1920/1440/1280/1024/768/430/390/375 逐一驗證 | — |
| 8 | SEO | 每頁 title/description/canonical/OG、favicon、sitemap.xml、robots.txt、Organization schema、301 對照 | H6 網域 |
| 9 | Accessibility | WCAG 2.1 AA 檢查（鍵盤、焦點、對比、報讀器） | — |
| 10 | Performance | WebP + srcset + lazy、Lighthouse 四項 > 90 | — |
| 11 | Final QA | 跨瀏覽器、連結檢查、內容核對表、Owner Review → Cutover | 業主簽核 |

---

## Phase 1 Status

**Completed**
- 7 個頁面全數爬取與內容盤點；圖片 19 個資源全數檢查（皆 200）
- 技術架構、RWD、SEO、Accessibility、Performance 分析
- A–I 規劃文件

**Pending**
- Lighthouse 正式基準分數（本環境無法連線該網域；可於 Phase 10 由您本機 Chrome DevTools 或 PageSpeed Insights 執行，作為改版前後對照）
- 舊網站原始檔備份（建議您從主機下載 `/PFO/` 整個目錄存檔）

**Needs Confirmation**
- H1 維持 [NEEDS CONFIRMATION]；H2/H6/H8/H10/H11 已有暫定處理方式（見下方決策紀錄）
- 其餘待確認：H4、H5、H7、H9、H12–H16

**Problems Found**
- 最嚴重：服務頁使用彩新公司數據；公司身分與網域混淆；IDPN（限由醫師使用藥品）資訊公開與授權風險；全站不支援行動裝置

**Next Step**
- 影響 Sitemap 的前提已足夠，可進入 PHASE 2（Sitemap + Information Architecture 定稿）。仍不進行 Coding。


---

## H 決策紀錄（Phase 2 規劃前提）

更新日期：2026-09-23。以下為業主（Tim）回覆，以及據此採用的規劃方式。

| # | 項目 | 狀態 | Phase 2 採用方式 |
|---|---|---|---|
| H1 | 保富齡與彩新的關係 | **[NEEDS CONFIRMATION]**（目前無法確認） | 以「保富齡獨立網站」規劃；彩新連結不列入正式 Sitemap／Header／Footer；**不推測兩家公司關係，不使用任何彩新資料**（含服務頁 28 家／500 床／22,000 人數據、彩新網站內容）。確認後再調整。 |
| H2 | 英文名稱與簡稱 | [NEEDS CONFIRMATION] | 網站只使用中文正式名稱「保富齡健康事業股份有限公司」；不放英文名稱（PFO／PFL renal service co.,Ltd. 都不使用）。Logo 圖檔照舊使用。 |
| H3 | 公司登記資料 | 部分已驗證 | 以官方登記資料為準（見 1.4 比對表）。**舊網站資本額 112,000,000 已過時，不沿用**。代表人、資本額、統編是否公開於網站 → [NEEDS CONFIRMATION]；在確認前「關於我們」只放公司名稱、設立日期、登記地址。 |
| H6 | 最終網域 | [NEEDS CONFIRMATION]（未定） | `/PFO-v2/` 內一律使用相對路徑；canonical、`sitemap.xml`、Open Graph `og:url` 的絕對網址留到 Phase 8 再填。 |
| H8 | 保富齡自有服務數據 | 無資料 | 新網站**不放任何統計數字**。 |
| H10 | 代理產品範圍 | 暫定 | 只規劃舊網站既有產品：Trixo 系列 3 品項、IDPN。產品區採可擴充結構（總覽頁 + 品項頁），其他品項（keywords 中的 Tsukuru、創姿、血糖機、胰島素空針、Prontosan、Linovera oil）等業主提供資料後再加。 |
| H11 | IDPN 頁 | [NEEDS CONFIRMATION]（法規／授權） | Sitemap 保留 `/products/idpn/`，但**暫不放產品內容**（不放成分、適應症、原廠圖片），只放「本公司經銷 B. Braun IDPN 相關產品」這類舊網站既有事實陳述與聯絡方式；文案最終版待法務或原廠確認。 |

**H11 背景資料**（僅供業主與法務參考，非法律意見）：
- 醫院藥品資料顯示此產品為「欣保富瀀靜脈營養輸注液 / NuTRIflex Lipid special」，許可證「衛署藥輸字第 024901 號」，並註明「本藥限由醫師使用」。來源：[澄清綜合醫院藥品資訊 PDF](https://www.cth.org.tw/public/medi_news/3651e8c4f8cd48fd058b3171b584bb91.pdf)
- 藥事法對「須由醫師處方或經中央衛生主管機關公告指定之藥物」的廣告有限制，詳細規範可參考 [食藥署藥物化粧品廣告相關法規彙編](https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f636694942647010511)。適用與否須由法務判斷。

**Phase 2 仍待確認但不阻擋規劃的項目**：H4 據點是否有效（暫沿用舊網站北中南資料，標 [NEEDS CONFIRMATION]）、H5 Email、H7 服務項目、H9 營運目標方向（在確認前**不放上網站**）、H12 代理／經銷稱謂、H13 新聞、H14 聯絡表單（在確認前不規劃表單與隱私權頁）、H15 主機、H16 英文版（在確認前只做中文）。
