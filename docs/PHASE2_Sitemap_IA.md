# PFO_NewWeb — PHASE 2：Sitemap 與資訊架構（IA）定稿

- 版本：v1.0（2026-09-23）
- 依據：`PHASE1_Reverse_Engineering.md`，以及文末「H 決策紀錄」（H1／H2／H6／H8／H10／H11 已由業主確認）
- 標記說明：
  - **[SOURCE: 舊站 x]**：內容直接來自舊網站的某一頁，原文沿用
  - **[SOURCE: 官方登記]**：來自經濟部商業司公司登記開放資料
  - **[NEEDS CONFIRMATION]**：需要業主確認
  - **[PROPOSED]**：架構或設計建議
  - **[PROPOSED COPY]**：新寫的文案（例如 SEO title、按鈕文字），不是公司正式資料
- 本文件只做規劃，**不包含任何網站程式碼**。

---

## 0. 規劃前提（已確認）

| # | 前提 |
|---|---|
| P1 | 保富齡是**獨立網站**。任何頁面都不放彩新網站連結，也不使用任何彩新資料，包括「28 家、500 床、22,000 人」這組數據。（H1） |
| P2 | 只使用中文正式名稱「保富齡健康事業股份有限公司」，不放英文名稱。（H2） |
| P3 | 站內連結一律用相對路徑。canonical、sitemap.xml、og:url 的網域留到 Phase 8 再填。（H6） |
| P4 | 全站不放任何統計數字。（H8） |
| P5 | 代理產品只放舊網站既有的：Trixo 3 品項、IDPN。結構要能再加品項。（H10） |
| P6 | IDPN 頁保留，但不放成分、適應症和原廠圖片，只放經銷事實與聯絡方式。（H11） |
| P7 | 舊網站的內容不足以撐起一個區塊時，**寧可不放**，不為了填版面而新寫內容。 |
| P8 | 以下內容在確認前**不上網站**：「營運目標方向」（H9）、代表人／資本額／統編（H3）、聯絡表單與隱私權頁（H14）、英文版（H16）。 |

---

## 1. Sitemap 定稿

```
/PFO-v2/                                   [P-01] 首頁
├── about/                                 [P-02] 關於我們
├── services/                              [P-03] 服務項目
│   ├── #care                                     照護相關（頁內錨點）
│   └── #dialysis                                 透析通路（頁內錨點）
├── products/                              [P-04] 代理產品總覽
│   ├── trixo/                             [P-05] Trixo 萃詩系列
│   └── idpn/                              [P-06] IDPN
├── news/                                  [P-07] 最新消息列表
│   └── 2014-02-21-trixo-hand-cream/       [P-08] 新聞內頁（2014.02.21）
├── contact/                               [P-09] 聯絡我們
└── 404.html                               [P-10] 找不到頁面

系統檔（位置見 §7.3）：sitemap.xml、robots.txt、favicon、site.webmanifest
```

**這次定稿刻意不做的頁面** [PROPOSED]

| 頁面 | 不做的原因 | 什麼條件下再加 |
|---|---|---|
| 服務項目子頁（每項服務一頁） | 舊網站每項服務只有 1–2 句，拆頁會變空頁 | 業主提供各服務的完整內容 |
| Trixo 各品項獨立頁 | 只有 3 個品項，而且特點高度重複 | 品項增加，或每項有獨立內容與圖片 |
| 品牌頁（B'BRAUN） | 舊「B'BRAUN」頁實際內容只有 Trixo；品牌介紹只有首頁的一句話 | 取得品牌授權與完整資料 |
| 隱私權政策 | 沒有表單，也還沒決定要不要裝分析工具 | H14（表單）或決定使用 GA4 時**必須**加 |
| 合作夥伴、客戶案例、徵才、FAQ | 沒有任何既有內容 | 業主提供真實內容 |
| 英文版 | H16 未確認 | 確認需要後另行規劃 `/en/` |

---

## 2. 頁面清單

狀態：✅ 內容已足夠｜⚠ 部分內容待確認｜⛔ 主要內容缺少

| ID | 頁面 | URL（相對 /PFO-v2/） | 範本 | H1 | 主要目的 | 內容來源 | 狀態 | 列入 sitemap.xml |
|---|---|---|---|---|---|---|---|---|
| P-01 | 首頁 | `./` | T-Home | 保富齡健康事業股份有限公司 | 建立信任、導向服務／產品／聯絡 | 舊站 index、intro | ✅ | ✓ |
| P-02 | 關於我們 | `about/` | T-Content | 關於我們 | 公司身分、願景、據點 | 舊站 intro、官方登記 | ⚠（H3、H4） | ✓ |
| P-03 | 服務項目 | `services/` | T-Content | 服務項目 | 說明兩項服務 | 舊站 service | ⚠（H7；透析通路內容不足） | ✓ |
| P-04 | 代理產品 | `products/` | T-Listing | 代理產品 | 產品線入口 | 舊站 index、product_b、product_idpn | ⚠（H12） | ✓ |
| P-05 | Trixo 萃詩系列 | `products/trixo/` | T-ProductLine | Trixo 萃詩系列 | 3 品項規格與特點 | 舊站 product_b | ⚠（仍在販售？品名寫法） | ✓ |
| P-06 | IDPN | `products/idpn/` | T-ProductLine（精簡版） | [NEEDS CONFIRMATION] | 說明經銷事實、引導聯絡 | 舊站 index 2018 消息 | ⛔（H11） | [NEEDS CONFIRMATION] |
| P-07 | 最新消息 | `news/` | T-Listing | 最新消息 | 公告列表 | 舊站 news_list、index | ✅ | ✓ |
| P-08 | 新聞內頁 | `news/2014-02-21-trixo-hand-cream/` | T-Article | 對於羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜 | 單則消息 | 舊站 news_140221 | ✅ | ✓ |
| P-09 | 聯絡我們 | `contact/` | T-Content | 聯絡我們 | 三據點、電話、Email | 舊站 footer、側欄 | ⚠（H4、H5） | ✓ |
| P-10 | 404 | `404.html` | T-Error | 找不到您要的頁面 [PROPOSED COPY] | 引導回主要頁面 | — | ✅ | ✗ |

**範本（Template）清單** [PROPOSED]：T-Home、T-Content、T-Listing、T-ProductLine、T-Article、T-Error，共 6 種。Phase 3 wireframe 依這 6 種範本來畫。

---

## 3. 導覽架構

### 3.1 主導覽（Global Header）

| 順序 | 標籤 | 連到 | 備註 |
|---|---|---|---|
| — | Logo（舊站 logo.gif，暫用） | `./` | alt：保富齡健康事業股份有限公司 |
| 1 | 關於我們 | `about/` | [SOURCE: 舊站選單] |
| 2 | 服務項目 | `services/` | 舊站這一項不能點，新站改成可點 [PROPOSED] |
| 3 | 代理產品 | `products/` | 標籤沿用舊站；「代理」或「經銷」的用法待確認（H12） |
| 4 | 最新消息 | `news/` | [SOURCE: 舊站選單] |
| 5 | 聯絡我們 | `contact/` | 在桌機上用按鈕樣式凸顯，不再重複一個 CTA [PROPOSED] |

- **不使用下拉選單** [PROPOSED]：第二層只有「服務 2 項」和「產品 2 項」，由各總覽頁導向就夠了，可以減少鍵盤操作與行動版的複雜度。
- 目前頁面標示 `aria-current="page"`。

### 3.2 行動版導覽（< 1024px）[PROPOSED]

- Header：Logo、「電話」icon 按鈕、選單按鈕（漢堡）
- 電話按鈕撥打總公司 (02)8221-5123 [SOURCE: 舊站]（據點是否有效：H4）
- 展開的選單：同 3.1 的 5 項，加上三據點電話

### 3.3 Footer

| 區塊 | 內容 | 來源 |
|---|---|---|
| 公司 | 保富齡健康事業股份有限公司 | 官方登記 |
| 據點 | 北／中／南三據點的地址、TEL、FAX | 舊站 footer（H4） |
| Email | pfl@pfl.tw（`mailto:` 連結） | 舊站（H5） |
| 快速連結 | 同主導覽 5 項 | — |
| 版權 | © {年份} 保富齡健康事業股份有限公司 All rights reserved. | 舊站格式；年份規則待定 [PROPOSED] |
| **不放** | 彩新連結、統編、代表人、資本額、社群連結 | P1、P8；目前也沒有社群帳號資料 |

### 3.4 麵包屑（Breadcrumb）[PROPOSED]

- 首頁不顯示，其餘頁面都顯示。
- 範例：`首頁 › 代理產品 › Trixo 萃詩系列`、`首頁 › 最新消息 › 對於羊毛脂…護手霜`
- Phase 8 對應 `BreadcrumbList` 結構化資料。

### 3.5 跨頁連結（Contextual Links）[PROPOSED]

| 從 | 到 | 依據 |
|---|---|---|
| 首頁「代理產品」卡片 | P-05、P-06 | 舊站首頁 |
| P-05 Trixo | P-08 相關新聞 | 同一產品 |
| P-08 新聞 | P-05 Trixo | 同一產品 |
| P-03 透析通路 | P-06 IDPN | 2018 消息「經銷 B'Braun 原廠 IDPN」 |
| 每個內頁底部 | P-09 聯絡我們 | 通用 CTA |

---

## 4. 各頁內容大綱

### P-01 首頁（T-Home）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | Hero | H1：保富齡健康事業股份有限公司；副標：舊站「願景」全文 | 官方登記；舊站 intro | ✅ |
| 1a | Hero 按鈕 | 「查看服務項目」→ P-03；「聯絡我們」→ P-09 | [PROPOSED COPY] | ✅ |
| 1b | Hero 圖片 | 舊站 main.jpg（大樓照）**不預設沿用**；沒有授權照片時改用純色／幾何設計 | G2、G3 | ⚠ |
| 2 | 服務項目 | 2 張卡片：照護相關（舊站第一句）、透析通路（見 P-03 的處理方式） | 舊站 service | ⚠ |
| 3 | 代理產品 | 2 張卡片：Trixo 萃詩系列、IDPN | 舊站 index | ⚠ |
| 4 | 最新消息 | 最新 3 則，依日期新→舊（目前只有 2 則） | 舊站 index | ✅ |
| 5 | 聯絡據點 | 北中南三張卡片＋「聯絡我們」按鈕 | 舊站 footer | ⚠ H4 |
| — | **不放** | 統計數字、客戶／醫院 logo、推薦語、彩新相關內容 | P1、P4 | — |

### P-02 關於我們（T-Content）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 願景 | 舊站原文 | 舊站 intro | ✅ |
| 2 | 公司簡介 | 公司名稱；設立日期（民國 100 年 9 月 5 日）；登記地址（新北市中和區中正路928號3樓） | 官方登記 | ✅ |
| 2a | 代表人、資本額、統一編號 | **暫不顯示**；資料欄位保留在內容模型中 | 官方登記（H3） | ⛔ 待是否公開 |
| 3 | 服務據點 | 北中南三據點（取代舊站的台灣地圖圖片），連到 P-09 | 舊站 | ⚠ H4 |
| — | **不放** | 營運目標方向（H9）、英文名稱（H2）、舊資本額 112,000,000 | P2、P8 | — |

> 注意：地址寫法——舊站寫「3F」，官方登記寫「3樓」。本站統一採**官方登記寫法「3樓」** [PROPOSED]。這只是格式統一，不改變地址本身。

### P-03 服務項目（T-Content）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 照護相關 `#care` | 舊站兩句原文：「提供糖尿病患及安養長照相關耗材儀器及專業傷口照護之有效產品。」「腸道健康照護系統設備合作規劃。」 | 舊站 service | ⚠ H7 |
| 2 | 透析通路 `#dialysis` | 舊站這一段**唯一的內容是彩新數據，已排除**。暫定只放舊站首頁的一句事實：「本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。」並連到 P-06 | 舊站 index 2018 消息 | ⛔ 需業主提供內容（H7） |
| 3 | 聯絡 CTA | 「想進一步了解？請聯絡我們」→ P-09 | [PROPOSED COPY] | ✅ |

> [NEEDS CONFIRMATION] 如果業主無法提供「透析通路」的說明，可以選擇：(a) 保留標題加上那一句經銷事實；(b) 暫時移除這一段，服務頁只放「照護相關」。**Phase 3 先以 (a) 繪製。**

### P-04 代理產品總覽（T-Listing）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 頁首 | H1 代理產品；說明文字 **[NEEDS CONFIRMATION]**（舊站沒有這頁的說明，不新寫） | — | ⚠ |
| 2 | 產品線卡片 | Trixo 萃詩系列（品牌：B'BRAUN）→ P-05；IDPN（品牌：B'BRAUN）→ P-06 | 舊站 index／product_b | ✅ |
| 3 | 品牌說明 | 舊站首頁那一句：「柏朗集團為全球性跨國企業,總部設於德國,成立至今已逾百年,為歐洲市場醫療器材領域之領導品牌。」 | 舊站 index | ⚠ 品牌授權與寫法 |

> 品牌寫法：舊站用「B'BRAUN」／「B'Braun」，原廠官方標示是「B. Braun」。本站**暫時沿用舊站寫法**，改不改由業主決定 [NEEDS CONFIRMATION]。

### P-05 Trixo 萃詩系列（T-ProductLine）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 頁首 | H1 Trixo 萃詩系列；品牌 B'BRAUN | 舊站 product_b | ✅ |
| 2 | 品項 ×3（頁內錨點） | 各品項：英文品名、中文品名、產品特點、產品規格、產品照 | 舊站 product_b | ⚠ 仍在販售？ |
| 3 | 相關消息 | 連到 P-08 | 舊站 | ✅ |
| 4 | 詢問 CTA | → P-09 | [PROPOSED COPY] | ✅ |

三個品項（名稱**完全照舊站產品頁原文**）：

| 錨點 | 英文品名 | 中文品名 | 規格 |
|---|---|---|---|
| `#trixo-bottle-west` | Trixo Bottle "WEST" | 萃詩正常肌膚用護手霜 | 20ml/100ml/500ml |
| `#trixolind-bottle-west` | TRIXOLIND Bottle WEST | 萃詩抗乾敏護膚護手乳液 | 20ml/100ml/500ml |
| `#trixolind-pure-tube-west` | TRIXOLIND PURE TUBE WEST | 萃詩純淨抗乾敏護膚護手乳液(無香) | 20ml/100ml/500ml |

> [NEEDS CONFIRMATION] 新聞頁把同系列產品稱為「Trixo-lind Pure 萃詩純淨抗乾敏**護手霜**」，產品頁則寫「**護手乳液**」。產品頁以產品頁的名稱為準；新聞內頁照原文保存（屬於歷史內容）。

### P-06 IDPN（T-ProductLine 精簡版）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 頁首 | H1 與頁面名稱 [NEEDS CONFIRMATION]（舊站用「B'BRAUN IDPN」） | 舊站 | ⛔ |
| 2 | 經銷事實 | 「本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。」 | 舊站 index 2018 消息 | ⚠ |
| 3 | 洽詢 | 「產品資訊請洽專業醫療團隊」（舊站原句）＋ P-09 連結 | 舊站 product_idpn | ⚠ |
| — | **不放** | 成分、適應症、電解質表、原廠圖片、療效描述、參考文獻 | H11 | — |

> 是否要加上「本頁僅供醫療專業人員參考」這類聲明、這一頁是否列入 sitemap.xml、是否加 `noindex`，全部等法務確認 [NEEDS CONFIRMATION]。

### P-07 最新消息列表（T-Listing）

| 日期 | 標題 | 摘要 | 有內頁 | 來源 |
|---|---|---|---|---|
| 2018.12.10 | — （舊站沒有標題） | 本公司經銷B'Braun原廠IDPN靜脈營養注射液，銷售各醫療診所。 | ✗ | 舊站 index |
| 2014.02.21 | 對於羊毛脂萃取物過敏者可使用的Trixo萃詩護手霜 | 舊站列表摘要原文 | ✓ → P-08 | 舊站 news_list |

- 排序改成**新→舊** [PROPOSED]。
- 沒有內頁的消息只顯示日期與摘要，不做「More」連結。
- 暫時不做分頁或年份篩選（只有 2 則）；消息超過 10 則時再加 [PROPOSED]。
- 2018 年那則要不要補標題與內頁：H13 [NEEDS CONFIRMATION]。

### P-08 新聞內頁（T-Article）

- 標題、日期、內文、圖片全部照舊站 news_140221 原文遷移，內文不改寫。
- 圖片：`news_0521.jpg`（190×171，解析度偏低）。
- 底部放「相關產品：Trixo 萃詩系列」→ P-05、「回最新消息列表」。

### P-09 聯絡我們（T-Content）

| # | 區塊 | 內容 | 來源 | 狀態 |
|---|---|---|---|---|
| 1 | 據點卡片 ×3 | 名稱、地址、TEL（`tel:` 連結）、FAX、地圖連結 | 舊站 | ⚠ H4 |
| 2 | Email | pfl@pfl.tw（`mailto:` 連結） | 舊站 | ⚠ H5 |
| 3 | 營業時間 | **不顯示**（舊站沒有這項資料）[NEEDS CONFIRMATION] | — | ⛔ |
| — | 地圖 | 用外部 Google Maps 連結，**不嵌入 iframe**（效能、隱私）[PROPOSED] | — | — |
| — | 表單 | 不做（H14） | — | — |

據點名稱：舊站 footer 寫「北／中／南」，地圖圖片寫「Taipei／Taichung／Kaohsiung Office」。本站暫時顯示為「北部據點（總公司）／中部據點／南部據點」[PROPOSED COPY]，正式名稱 [NEEDS CONFIRMATION]。總公司的標示依據是舊站側欄的「總公司連絡地址」和官方登記地址。

### P-10 404（T-Error）

- 一句說明＋回首頁按鈕＋主導覽 5 項連結 [PROPOSED COPY]
- 加 `noindex`，不列入 sitemap.xml

---

## 5. 內容模型（Content Model）

設計原則 [PROPOSED]：

- 每一個欄位都要有 `source`（來源）和 `status`（確認狀態），避免 AI 建議混進正式資料。
- 目前網站用純 HTML 手寫也能照這個模型寫；如果之後導入靜態產生器，這個模型可以直接轉成 JSON／Markdown front-matter。
- `visibility: hidden` 代表「資料已經有，但確認前不顯示」。

欄位型別：`string`、`text`（多段文字）、`date`、`enum`、`ref`（參照其他實體）、`image`、`list<…>`。

### 5.1 SiteSettings（全站設定，1 筆）

| 欄位 | 型別 | 必填 | 目前的值 | 來源 | 狀態 |
|---|---|---|---|---|---|
| legalNameZh | string | ✓ | 保富齡健康事業股份有限公司 | 官方登記 | ✅ |
| englishName | string | — | null | — | H2，不顯示 |
| logo | image | ✓ | img/logo.gif（暫用） | 舊站 | 需要向量檔（G1） |
| primaryEmail | string | ✓ | pfl@pfl.tw | 舊站 | H5 |
| primaryPhone | string | ✓ | (02)8221-5123 | 舊站 | H4 |
| baseUrl | string | ✓（Phase 8） | null | — | H6 |
| defaultOgImage | image | ✓（Phase 8） | null | — | G10 |
| copyrightText | string | ✓ | © {年份} 保富齡健康事業股份有限公司 All rights reserved. | 舊站格式 | [PROPOSED] |
| externalLinks | list | — | [] | — | P1：不放彩新 |

### 5.2 CompanyProfile（公司資料，1 筆）

| 欄位 | 型別 | 值 | 來源 | 顯示 |
|---|---|---|---|---|
| vision | text | 以創新的理念提供專業的產品服務,專注的態度提供全方位的通路規劃,讓公司創造一個全新領域的健康照護產業,成為讓大眾幸福樂活的優質企業。 | 舊站 intro | visible |
| foundedDate | date | 2011-09-05（顯示為「中華民國 100 年 9 月 5 日」） | 官方登記 | visible |
| registeredAddress | string | 新北市中和區中正路928號3樓 | 官方登記 | visible |
| representative | string | 白靖騰 | 官方登記 | **hidden**（H3） |
| capitalTotal | number | 200,000,000 | 官方登記 | **hidden**（H3） |
| capitalPaidIn | number | 190,000,000 | 官方登記 | **hidden**（H3） |
| taxId | string | 53599511 | 官方登記 | **hidden**（H3） |
| registryCheckedAt | date | 2026-09-23 | — | 內部欄位 |
| businessGoals | list | 舊站「營運目標方向」4 項 | 舊站 intro | **hidden**（H9） |

### 5.3 Office（據點，3 筆）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| id | string | ✓ | `north`／`central`／`south` |
| label | string | ✓ | 見 P-09（[PROPOSED COPY]，待確認） |
| isHeadquarters | boolean | ✓ | 只有 north 為 true |
| address | string | ✓ | 照舊站原文；總公司地址照官方登記寫法 |
| tel | string | ✓ | 顯示格式 `(02)8221-5123`；連結格式 `tel:+886282215123` |
| fax | string | — | |
| mapUrl | string | — | Google Maps 查詢連結，依地址產生 [PROPOSED] |
| openingHours | string | — | null（無資料） |
| status | enum | ✓ | `needs-confirmation`（H4） |

目前的資料（照舊站原文）：

| id | address | tel | fax |
|---|---|---|---|
| north | 新北市中和區中正路928號3樓 | (02)8221-5123 | (02)8221-5122 |
| central | 台中市西區五權路2-107號15樓 | (04)2376-2333 | (04)2376-1177 |
| south | 高雄市苓雅區三多二路171號9F-1 | (07)716-8518 | (07)716-8730 |

### 5.4 ServiceCategory（服務項目，2 筆）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| id / anchor | string | ✓ | `care`／`dialysis` |
| title | string | ✓ | 照護相關／透析通路（舊站原文） |
| summary | string | ✓ | 首頁卡片用的一句話；只能從舊站原文擷取 |
| body | list\<text\> | — | 服務頁內文 |
| relatedProductLines | list\<ref ProductLine\> | — | dialysis → idpn |
| status | enum | ✓ | care：`needs-confirmation`；dialysis：`content-missing` |

### 5.5 Brand（品牌，1 筆）

| 欄位 | 型別 | 值 | 狀態 |
|---|---|---|---|
| id | string | `bbraun` | — |
| displayName | string | B'BRAUN（沿用舊站） | 寫法待確認 |
| description | text | 舊站首頁那一句品牌說明 | 待確認授權 |
| logo | image | null | 需要原廠授權（G4） |
| relationship | enum | `agent`／`distributor` | H12（舊站同時出現「代理」與「經銷」） |

### 5.6 ProductLine（產品線，2 筆）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| id / slug | string | ✓ | `trixo`／`idpn` |
| name | string | ✓ | Trixo 萃詩系列／IDPN（頁名待確認） |
| brand | ref Brand | ✓ | bbraun |
| summary | text | ✓ | 只能用舊站原文 |
| products | list\<ref Product\> | — | idpn 目前是空的（H11） |
| audience | enum | ✓ | `public`／`healthcare-professional`（idpn 待法務確認） |
| indexable | boolean | ✓ | idpn 待確認 |
| relatedNews | list\<ref NewsItem\> | — | trixo → 2014-02-21 |
| status | enum | ✓ | |

### 5.7 Product（品項，目前 3 筆）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| id / anchor | string | ✓ | 見 P-05 表格 |
| productLine | ref ProductLine | ✓ | |
| nameEn | string | ✓ | 照舊站原文，不修改 |
| nameZh | string | ✓ | 照舊站原文，不修改 |
| features | list\<string\> | ✓ | 舊站「產品特點」原文 |
| specs | list\<string\> | ✓ | 舊站「產品規格」原文 |
| image | ref ImageAsset | — | 舊站 product_b12–14.jpg（低解析度） |
| status | enum | ✓ | `needs-confirmation`（仍在販售？） |

### 5.8 NewsItem（消息，目前 2 筆）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| id / slug | string | 有內頁時必填 | 格式 `YYYY-MM-DD-英文關鍵字` |
| date | date | ✓ | |
| title | string | 有內頁時必填 | 2018 那則為 null（舊站沒有標題） |
| summary | text | ✓ | 列表用 |
| body | rich text | — | |
| image | ref ImageAsset | — | |
| hasDetail | boolean | ✓ | 2018：false；2014：true |
| relatedProductLine | ref ProductLine | — | |
| status | enum | ✓ | |

### 5.9 ImageAsset（圖片）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| src | string | ✓ | |
| alt | string | ✓（裝飾性圖片用空字串，並標為 decorative） | |
| width / height | number | ✓ | 避免版面位移（CLS） |
| formats | list | ✓ | WebP + JPG 備援（Phase 10） |
| source | string | ✓ | 舊站檔名／業主提供／原廠提供 |
| licenseStatus | enum | ✓ | `owner-confirmed`／`needs-confirmation`／`not-allowed` |

**只有 `licenseStatus = owner-confirmed` 的圖片可以在正式版上線。**

### 5.10 PageMeta（每頁 SEO／導覽資料）

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| pageId | string | ✓ | P-01…P-10 |
| path | string | ✓ | 相對路徑 |
| title | string | ✓ | 格式：`{頁名}｜保富齡健康事業股份有限公司`；首頁只放公司名 [PROPOSED] |
| description | string | ✓ | 只能從該頁既有內容摘寫，標 [PROPOSED COPY]，不新增事實 |
| h1 | string | ✓ | 每頁只有一個 |
| breadcrumb | list | 首頁以外必填 | |
| robots | enum | ✓ | `index,follow`／`noindex` |
| inSitemap | boolean | ✓ | |
| ogImage | ref ImageAsset | — | 預設使用 SiteSettings.defaultOgImage |

### 5.11 實體關係

```
SiteSettings ── 1 : 3 ── Office
CompanyProfile
ServiceCategory ── n : n ── ProductLine
Brand ── 1 : n ── ProductLine ── 1 : n ── Product
ProductLine ── n : n ── NewsItem
Product／NewsItem ── n : 1 ── ImageAsset
每個頁面 ── 1 : 1 ── PageMeta
```

---

## 6. 舊 URL → 新 URL 對照（Cutover 301 用）

| 舊 URL | 新 URL | 備註 |
|---|---|---|
| `/PFO/index.html`、`/PFO/` | `./` | |
| `/PFO/intro.html` | `about/` | |
| `/PFO/service.html` | `services/` | 舊錨點 `#s_01`→`#care`、`#s_02`→`#dialysis`（錨點不會被伺服器轉址，只能盡量對應） |
| `/PFO/product_b.html` | `products/trixo/` | 舊頁實際內容是 Trixo |
| `/PFO/product_idpn.html` | `products/idpn/` | 依 H11 結果；如果不公開，改轉到 `products/` |
| `/PFO/news/news_list.html` | `news/` | |
| `/PFO/news/2014/news_140221.html` | `news/2014-02-21-trixo-hand-cream/` | |

轉址的實作方式要看最終網域與主機是否支援 `.htaccess`（H6、H15），Phase 8 再定。

---

## 7. URL 與檔案結構規則

### 7.1 URL 規則 [PROPOSED]

- 全部小寫英文，單字之間用 `-` 連接，不用中文 URL（避免編碼後變成一長串 %XX）。
- 一律採「目錄＋`index.html`」，網址以 `/` 結尾，在靜態主機上不需要 rewrite。
- 站內連結全部用相對路徑（P3），整個 `/PFO-v2/` 搬到正式位置時不用改連結。
- 新聞 slug 固定格式：`YYYY-MM-DD-關鍵字`。

### 7.2 目錄結構（規劃，尚未建立）

```
PFO-v2/
├── index.html
├── about/index.html
├── services/index.html
├── products/index.html
├── products/trixo/index.html
├── products/idpn/index.html
├── news/index.html
├── news/2014-02-21-trixo-hand-cream/index.html
├── contact/index.html
├── 404.html
└── assets/
    ├── css/
    ├── js/
    ├── img/  (brand/ products/ news/)
    └── icons/ (favicon 等)
```

### 7.3 測試環境注意事項 [PROPOSED]

- `robots.txt` 只在網域根目錄有效，放在 `/PFO-v2/` 底下不會作用。**在測試期間，每頁都加 `<meta name="robots" content="noindex">`**，避免測試版被搜尋引擎收錄、和舊站內容重複。Cutover 時再拿掉。
- `sitemap.xml` 等最終網域確定（H6）後，在 Phase 8 產生。

---

## 8. 內容缺口處理規則 [PROPOSED]

| 情況 | 處理方式 |
|---|---|
| 有舊站原文，但不確定是否仍正確 | 照原文顯示，內部標 `needs-confirmation`，列入 Owner Review 核對表 |
| 完全沒有內容 | 該區塊**不顯示**；wireframe 用灰色框標示「待業主提供」，正式版不會出現佔位文字 |
| 資料有，但待決定是否公開 | 資料存在內容模型裡，`visibility: hidden` |
| AI 新寫的文字（標題、按鈕、SEO） | 標 [PROPOSED COPY]，Owner Review 時逐條確認 |

---

## Phase 2 Status

**Completed**
- Sitemap 定稿：9 個內容頁＋404
- 頁面清單、6 種範本、主導覽／行動版導覽／Footer／麵包屑／跨頁連結
- 10 頁的內容大綱，每個區塊都標了來源與狀態
- 內容模型：10 種實體、欄位定義與目前的值
- 舊→新 URL 對照、URL 規則、目錄結構、內容缺口規則

**Pending**
- 各頁 SEO title／description 的實際文字（Phase 8）
- sitemap.xml、robots.txt、301 實作（Phase 8，要看 H6／H15）

**Needs Confirmation**（Phase 3 可以先畫，但上線前要回覆）

| # | 項目 | 影響頁面 |
|---|---|---|
| H3 | 代表人、資本額、統編是否公開 | P-02 |
| H4 | 三據點是否仍有效；據點的正式名稱 | P-01、P-02、P-09、Footer |
| H5 | Email 是否仍使用 | 全站 |
| H7 | 服務內容，特別是「透析通路」的說明 | P-01、P-03 |
| H11 | IDPN 頁名、聲明、是否被搜尋引擎收錄 | P-06、P-07 |
| H12 | 「代理」或「經銷」；品牌寫法 B'BRAUN 或 B. Braun | 主導覽、P-04～P-06 |
| H13 | 2018 消息是否補標題和內頁 | P-07 |
| 新 | Trixo 3 品項是否仍在販售；「霜」或「乳液」 | P-05 |
| 新 | 營業時間 | P-09 |

**Problems Found**
- 「透析通路」扣掉彩新數據後，已經沒有可用的說明，只剩一句經銷事實（P-03 標為 ⛔）。
- 目前沒有任何已確認授權的照片，首頁 Hero 與產品圖可能要用非照片的設計（見 G2–G5）。
- `robots.txt` 無法在子目錄生效，測試期間要改用 `noindex`（§7.3）。

**Next Step**
- 業主確認這份 Sitemap／IA 後，進入 **PHASE 3：Wireframe**。依 6 種範本畫 Desktop（1440）與 Mobile（390）低保真線框，缺內容的區塊會明確標示。仍不寫正式程式碼。
