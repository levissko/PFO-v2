# PFO_NewWeb — PHASE 5：Homepage

- 版本：v1.0（2026-09-23）
- 交付：`/PFO-v2/`（測試版，全頁 `noindex, nofollow`）
- 設計系統：`tokens.css` 已凍結、未修改；`components.css` 修了 3 個錯誤，升為 v1.0.1（見 §4）

## 1. 檔案結構

```
PFO-v2/
├── index.html              首頁
└── assets/
    ├── css/
    │   ├── tokens.css      ← design-system/tokens.css 的部署副本（凍結）
    │   ├── components.css  ← design-system/components.css v1.0.1 的部署副本
    │   └── site.css        全站基礎樣式、行動版選單、Footer 版面、審閱模式
    ├── js/main.js          只負責行動版選單（約 2 KB，defer 載入）
    └── img/logo.gif        舊站 Logo 原檔（6,367 bytes，逐像素比對與原檔相同）
```

- **修改規則**：`design-system/` 是設計系統的唯一來源。如需改動，先改那裡，再複製到 `PFO-v2/assets/css/`。
- **CSS 載入順序**：tokens → components → site。
- 沒有使用任何框架或第三方套件，也不從外部網站載入任何檔案。

## 2. 首頁結構（依 Phase 2 P-01、Phase 3 T-Home）

| 區塊 | 內容 | 來源 |
|---|---|---|
| 跳至主內容連結 | 只在鍵盤 focus 時出現 | — |
| 審閱橫幅 | 「測試版本…正式上線前會全部移除」 | 只在審閱模式顯示 |
| Header | Logo（GIF 暫用）、4 項選單、「聯絡我們」按鈕；寬度小於 1024px 時改為電話按鈕加漢堡選單 | 舊站選單 |
| Hero | H1 公司名稱、副標為願景原文、2 顆按鈕；右側 Logo 十字裝飾圖形（手機版隱藏） | 經濟部登記、舊站 intro |
| 服務項目 | 照護相關（舊站原文）；透析通路（採 Phase 2 方案 (a)：一句經銷事實） | 舊站 service、2018 消息 |
| 代理產品 | Trixo 系列 3 品名；IDPN 經銷事實；兩張卡都使用 Media Fallback，不放照片 | 舊站 product_b、2018 消息 |
| 最新消息 | 新→舊；2018 那則只有摘要、不放連結；2014 那則有標題，摘要以兩行截斷（原文不改） | 舊站 index、news_list |
| 服務據點 | 三張據點卡，電話可直接撥打 | 舊站 footer；總公司地址依官方登記寫「3樓」 |
| Footer | 公司名稱、Email（mailto 連結）、三據點、頁尾連結、版權 | 不放彩新連結、統編、代表人、資本額 |

**[PROPOSED COPY]**（在程式碼中以 HTML 註解標示）

- 按鈕：「查看服務項目」「聯絡我們」「了解更多」「查看產品」「全部產品」「所有消息」
- 據點名稱：「北部據點（總公司）」「中部據點」「南部據點」
- 行動版選單標題：「撥打電話」
- 版權年份：2026

## 3. 審閱模式（Review Mode）

- `<html class="is-review">` 會顯示頂部紅色測試橫幅，以及 8 個紅色虛線「待確認」框：
  - H4（含據點名稱）、H5、H7 ×2、H11、H12、H13
  - Trixo 品項是否仍在販售
- **正式上線前**只要刪掉 `class="is-review"`，這些標註就會全部隱藏，版面不需要調整。上線前也要一併把這些標註的 HTML 清除（列入 Phase 11 QA 清單）。

## 4. 設計系統修正：components.css v1.0.1

這 3 處是用實際瀏覽器截圖驗證時發現的錯誤。**只修錯誤，沒有更動任何設計決策或 token**：

| # | 問題 | 修正 |
|---|---|---|
| 1 | `.pfo-container` 同時設了 `width:100%` 和 padding，寬度 390px 時頁面會橫向捲動（實測頁面寬 431px） | 移除 `width:100%` |
| 2 | 通用連結色 `.pfo a` 的權重高於按鈕 class，主要按鈕的白字被蓋成深藍，**在深藍底上看不到字** | 通用連結色改用零權重的 `:where()` |
| 3 | 手機版 Hero 的十字裝飾圖形疊在按鈕後方 | 寬度 767px 以下隱藏裝飾圖形 |

- 樣式預覽頁（本機 `styleguide.html` 與線上 Artifact）已同步更新。
- 第 2 點在 Phase 4 的預覽頁中也存在，只是沒有被發現；修正後，所有按鈕都經過計算樣式檢查，確認文字色與背景色正確。

## 5. 驗證結果

| 項目 | 結果 |
|---|---|
| HTML 結構 | 所有標籤正確閉合、無重複 id、圖片都有 alt |
| 標題階層 | 一個 H1，接著 H2 各區塊、H3 卡片；Footer 用隱藏的 H2「公司資訊」接住 H3 |
| 橫向捲動 | 寬度 1440、390 皆無 |
| JS 錯誤 | 無 |
| 行動版選單 | 點擊開啟後焦點移到第一個連結；按 Esc 關閉，焦點回到選單按鈕；按 Tab 時焦點留在選單內；調整到桌機寬度時自動關閉 |
| 按鈕顏色 | 實際計算樣式：主要按鈕白字配 #2E3092，反白按鈕 #151A4D 配白底 |
| 無障礙細節 | 有跳至主內容連結；「了解更多」連結附隱藏文字（例如「了解更多：照護相關」）；裝飾圖形與圖示設 aria-hidden；觸控目標 ≥ 44px |

## 6. 已知限制

- 內頁 `about/`、`services/`、`products/`、`news/`、`contact/` 尚未建立（Phase 6），目前點擊會 404。
- Logo 是 273×68 的 GIF，在高解析螢幕上會略顯模糊；取得向量檔（G1）後改用 SVG，中文字標改為 gray-900 `#161A26`（業主已決定）。
- 還沒有 favicon、canonical、Open Graph（Phase 8，需先確認網域 H6）。
- 還沒有跑 Lighthouse（Phase 10）。依頁面組成預估負擔很輕：CSS 約 33 KB（未壓縮，含大量註解）、JS 約 2.5 KB、圖片 6 KB、不下載字型，但以實測為準。

## Phase 5 Status

**Completed**
- `/PFO-v2/index.html` 首頁，語意化 HTML5，套用設計系統
- `site.css`、`main.js`（行動版選單）、Logo 資產
- 審閱模式機制
- components.css v1.0.1 錯誤修正
- 1440、390 實際瀏覽器截圖檢查

**Pending**
- Phase 6 內頁
- Phase 7 在 1920／1280／1024／768／430／375 等寬度逐一驗證

**Needs Confirmation**
- H3、H4、H5、H7、H11、H12、H13（業主表示會在 Phase 6 內容上稿前提供）
- Trixo 品項是否仍在販售

**Problems Found**
- components.css 的 3 個錯誤，已修正（§4）

**Next Step**
- 業主檢閱首頁後，進入 **PHASE 6：Inner Pages**：about、services、products（含 trixo、idpn）、news（含 2014 新聞內頁）、contact、404。
