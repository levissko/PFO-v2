# 部署清單（DEPLOY MANIFEST）

> 由 `tools/gen_pages.py` 依目前設定自動產生，請勿手改。設定改變後重跑即更新。

- 產生時設定：`SITE_ORIGIN = https://www.newimage2023.com.tw`、`SITE_BASE_PATH = /PFO-v2/`、`IS_PRODUCTION = False`
- 部署情境：**C：同網域子路徑 /PFO-v2/，舊路徑 /PFO/ 轉址過來**
- 新網站首頁：https://www.newimage2023.com.tw/PFO-v2/

> ⚠ **目前是測試設定**：本清單只能用於部署測試版。正式上線前請改 `IS_PRODUCTION = True` 後重跑。

| 本機檔案 | 放到主機 | 注意 |
|---|---|---|
| `PFO-v2/` 資料夾內**全部內容**（不含資料夾本身） | `/PFO-v2/` | 上傳前先執行 optimize_images.py 與 preflight.py；**不要上傳 `assets/img/src/`**（照片原始檔，網頁不會用到） |
| `deploy/htaccess-performance.txt` | `/PFO-v2/.htaccess` | 改名為 .htaccess |
| `deploy/htaccess-301.txt` | `/PFO/.htaccess`（舊網站所在主機） | 保留 /PFO/ 資料夾；原本已有 .htaccess 時加在最前面 |

**robots.txt**：`robots.txt` 放在子路徑**不會被搜尋引擎讀取**（只讀網域根目錄 `/robots.txt`）。請網域管理者在根目錄 `/robots.txt` 加上一行 `Sitemap: https://www.newimage2023.com.tw/PFO-v2/sitemap.xml`，或改在 Search Console 直接提交 sitemap。子路徑的 robots.txt 仍會上傳，無害。

**sitemap.xml**：位於 `/PFO-v2/sitemap.xml`（https://www.newimage2023.com.tw/PFO-v2/sitemap.xml），隨網站一起上傳。
