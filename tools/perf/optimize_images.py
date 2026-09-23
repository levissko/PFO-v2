"""PHASE 10 — image optimisation for PFO-v2/assets.

Run after replacing any image (e.g. the official logo / favicon / OG image, G1):
    python tools/perf/optimize_images.py

What it does (all lossless — pixels are verified identical before writing):
  1. SVG  (assets/icons/*.svg, assets/img/*.svg):
       strips <metadata> blocks (e.g. embedded C2PA/XMP manifests), editor
       namespaces and comments, collapses whitespace.
  2. GIF/PNG in assets/img and assets/icons:
       re-saves without metadata chunks (XMP, text) when that is smaller.
  3. Logo: writes assets/img/logo.webp (lossless) next to logo.gif; the header
     uses <picture> so modern browsers load the WebP and old ones the GIF.
  4. Photos: every JPG/PNG in assets/img/src/ becomes responsive WebP files in
     assets/img/ named <name>-<width>.webp (widths 480/720/960/1440/1920 that are
     smaller than the original, plus the original width; quality 80; never
     upscaled), and one JPEG fallback <name>-<width>.jpg (≤ 960 wide) for the
     <img> inside <picture>. Sizes are written to tools/perf/photos.json, which
     tools/gen_pages.py reads to build srcset / width / height.
     assets/img/src/ holds the originals only — do not upload it.

Requires Pillow (pip install pillow). Pillow is only needed here, not at runtime.
"""
import io, json, os, re, sys
from PIL import Image, ImageChops

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "PFO-v2", "assets")
IMG, ICONS, SRC = (os.path.join(ROOT, d) for d in ("img", "icons", os.path.join("img", "src")))
PHOTO_WIDTHS = (480, 720, 960, 1440, 1920)
PHOTO_QUALITY = 80
# Hero sits under a 82–94% navy overlay, so compression artefacts are invisible:
# a lower quality roughly halves the LCP image (mobile LCP 1.7 s → see PHASE 11 doc).
PHOTO_QUALITY_BY_STEM = {"hero-lobby": 60}
FALLBACK_MAX = 960
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos.json")
report = []


def same_pixels(a_bytes, b_bytes):
    a = Image.open(io.BytesIO(a_bytes)).convert("RGBA")
    b = Image.open(io.BytesIO(b_bytes)).convert("RGBA")
    return a.size == b.size and ImageChops.difference(a, b).getbbox() is None


def write_if_smaller(path, new):
    old = open(path, "rb").read()
    if len(new) < len(old) and same_pixels(old, new):
        open(path, "wb").write(new)
        report.append(f"{os.path.relpath(path, ROOT)}: {len(old):,} → {len(new):,} B")
    else:
        report.append(f"{os.path.relpath(path, ROOT)}: {len(old):,} B (already optimal)")


def svg_min(path):
    s = open(path, encoding="utf-8").read()
    old = len(s.encode())
    s = re.sub(r"<metadata\b.*?</metadata>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r'\s+xmlns:(c2pa|dc|cc|rdf|sodipodi|inkscape)="[^"]*"', "", s)
    s = re.sub(r">\s+<", "><", s).strip() + "\n"
    new = len(s.encode())
    if new < old:
        open(path, "w", encoding="utf-8").write(s)
    report.append(f"{os.path.relpath(path, ROOT)}: {old:,} → {new:,} B")


def raster_min(path):
    im = Image.open(path)
    buf = io.BytesIO()
    fmt = "GIF" if path.lower().endswith(".gif") else "PNG"
    # save() without passing info drops XMP / text chunks
    im.save(buf, fmt, optimize=True)
    write_if_smaller(path, buf.getvalue())


def logo_webp():
    gif = os.path.join(IMG, "logo.gif")
    if not os.path.exists(gif):
        return
    rgba = Image.open(gif).convert("RGBA")
    buf = io.BytesIO()
    rgba.save(buf, "WEBP", lossless=True, method=6, quality=100)
    assert same_pixels(open(gif, "rb").read(), buf.getvalue())
    open(os.path.join(IMG, "logo.webp"), "wb").write(buf.getvalue())
    report.append(f"img/logo.webp (lossless): {len(buf.getvalue()):,} B")


def photos():
    """Responsive WebP set + one JPEG fallback per original; sizes go to photos.json."""
    manifest = {}
    if os.path.isdir(SRC):
        for name in sorted(os.listdir(SRC)):
            stem, ext = os.path.splitext(name)
            if ext.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            im = Image.open(os.path.join(SRC, name)).convert("RGB")   # drops metadata
            widths = [w for w in PHOTO_WIDTHS if w < im.width]
            top = min(im.width, max(PHOTO_WIDTHS))
            if not widths or top > widths[-1] * 1.05:   # add the original width unless ~equal
                widths.append(top)
            for w in widths:
                h = round(im.height * w / im.width)
                out = os.path.join(IMG, f"{stem}-{w}.webp")
                q = PHOTO_QUALITY_BY_STEM.get(stem, PHOTO_QUALITY)
                im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=q, method=6)
                report.append(f"img/{stem}-{w}.webp ({w}×{h}): {os.path.getsize(out):,} B")
            fw = max([w for w in widths if w <= FALLBACK_MAX] or [widths[0]])
            fh = round(im.height * fw / im.width)
            fb = os.path.join(IMG, f"{stem}-{fw}.jpg")
            im.resize((fw, fh), Image.LANCZOS).save(fb, "JPEG", quality=PHOTO_QUALITY_BY_STEM.get(stem, PHOTO_QUALITY), optimize=True, progressive=True)
            report.append(f"img/{stem}-{fw}.jpg (fallback): {os.path.getsize(fb):,} B")
            manifest[stem] = {"widths": widths, "ratio": [im.width, im.height], "fallback": fw}
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    report.append(f"photos.json: {', '.join(manifest) or '(no photos)'}")


if __name__ == "__main__":
    for d in (IMG, ICONS):
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.endswith(".svg"):
                svg_min(p)
            elif f.lower().endswith((".gif", ".png")) and os.path.isfile(p):
                raster_min(p)
    logo_webp()
    photos()
    print("\n".join(report))
    sys.exit(0)
