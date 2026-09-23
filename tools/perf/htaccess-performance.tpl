# =====================================================================
# PFO_NewWeb — PHASE 10 效能設定（壓縮＋快取）
# 由 tools/gen_pages.py 依 tools/perf/htaccess-performance.tpl 產生（SITE_BASE_PATH = {{BASE}}），請勿直接修改。
#
# 放置位置：新網站資料夾內，檔名改為 .htaccess
#   測試期：/PFO-v2/.htaccess   （只影響 /PFO-v2/，不影響舊站 /PFO/）
#   Cutover 後：跟著網站移到正式路徑
# 適用：Apache 2.4（LiteSpeed 相容）。所有模組指令都包在 <IfModule> 內，
#       模組未啟用時該段會被略過，不會造成 500 錯誤。
#       [NEEDS CONFIRMATION] 主機的 AllowOverride 需允許 FileInfo、Indexes 與 Options，否則 .htaccess 會被忽略或回 500。
#       上線前請用 curl -I 確認標頭（見 docs/PHASE10_Performance.md §5）。
#
# 快取策略：
#   HTML、sitemap、robots  → 每次向伺服器確認（no-cache + ETag），內容更新立即生效
#   CSS / JS               → 1 年 + immutable。HTML 以 ?v=<內容雜湊> 引用（tools/gen_pages.py 產生），
#                             內容一改網址就變，所以可以放心長期快取
#   圖片 / 圖示            → 30 天。檔名沒有版本號；更換 Logo（G1）時，
#                             舊的最多快取 30 天，想立即生效請改檔名或加 ?v=
# =====================================================================

# ---------- 編碼與 MIME ----------
AddDefaultCharset utf-8
<IfModule mod_mime.c>
  AddCharset utf-8 .css .js .xml .txt .svg
  AddType image/webp                 .webp
  AddType image/avif                 .avif
  AddType image/svg+xml              .svg
  AddType image/x-icon               .ico
  AddType application/manifest+json  .webmanifest
  AddType text/javascript            .js
</IfModule>

# ---------- 壓縮：Brotli 優先，瀏覽器不支援時用 gzip ----------
# 兩個模組都有：寫成 BROTLI_COMPRESS;DEFLATE（順序不可顛倒；已在 Apache 2.4 實測）。
#   支援 br 的瀏覽器拿到 br，其餘拿到 gzip。
#   注意：若主機在伺服器層級已設定 DEFLATE（例如 Debian/Ubuntu 預設 deflate.conf），
#   會一律回 gzip——仍有壓縮，只是少了 br 約 5% 的額外節省，不影響功能。
<IfModule mod_filter.c>
  <IfModule mod_brotli.c>
    <IfModule mod_deflate.c>
      AddOutputFilterByType BROTLI_COMPRESS;DEFLATE text/html text/css text/javascript application/javascript \
        application/json application/ld+json application/xml text/xml text/plain image/svg+xml \
        image/x-icon application/manifest+json
    </IfModule>
    <IfModule !mod_deflate.c>
      AddOutputFilterByType BROTLI_COMPRESS text/html text/css text/javascript application/javascript \
        application/json application/ld+json application/xml text/xml text/plain image/svg+xml \
        image/x-icon application/manifest+json
    </IfModule>
  </IfModule>
  <IfModule !mod_brotli.c>
    <IfModule mod_deflate.c>
      AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript \
        application/json application/ld+json application/xml text/xml text/plain image/svg+xml \
        image/x-icon application/manifest+json
    </IfModule>
  </IfModule>
</IfModule>
<IfModule mod_headers.c>
  Header append Vary Accept-Encoding
</IfModule>
# 已壓縮的格式（webp、png、gif、jpg）不再壓縮

# ---------- 快取：過期時間（mod_expires） ----------
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault                          "access plus 1 hour"
  ExpiresByType text/html                 "access plus 0 seconds"
  ExpiresByType application/xml           "access plus 0 seconds"
  ExpiresByType text/xml                  "access plus 0 seconds"
  ExpiresByType text/plain                "access plus 0 seconds"
  ExpiresByType text/css                  "access plus 1 year"
  ExpiresByType text/javascript           "access plus 1 year"
  ExpiresByType application/javascript    "access plus 1 year"
  ExpiresByType image/webp                "access plus 30 days"
  ExpiresByType image/avif                "access plus 30 days"
  ExpiresByType image/png                 "access plus 30 days"
  ExpiresByType image/gif                 "access plus 30 days"
  ExpiresByType image/jpeg                "access plus 30 days"
  ExpiresByType image/svg+xml             "access plus 30 days"
  ExpiresByType image/x-icon              "access plus 30 days"
</IfModule>

# ---------- 快取：Cache-Control（mod_headers，會覆蓋上面的預設） ----------
<IfModule mod_headers.c>
  <FilesMatch "\.(html|xml|txt)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  <FilesMatch "\.min\.(css|js)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\.(webp|avif|png|gif|jpe?g|svg|ico)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>

  # 基本安全標頭（業主 2026-09-23 核准；不影響版面）
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
</IfModule>

# ETag 只用修改時間＋大小（多台主機時較一致）
FileETag MTime Size

# 不列出資料夾內容（直接開 /PFO-v2/assets/ 不會看到檔案清單）
Options -Indexes
DirectoryIndex index.html

# 找不到頁面時顯示新網站的 404 頁（404.html 內 <base href> 已處理子路徑）
ErrorDocument 404 {{BASE}}404.html
