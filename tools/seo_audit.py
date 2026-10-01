#!/usr/bin/env python3
"""
بررسی سئوی سایت بعد از build:   python tools/seo_audit.py

خطاها (ERR) باید رفع شوند؛ هشدارها (WARN) پیشنهاد بهبودند.
کد خروج 1 یعنی حداقل یک خطا وجود دارد.
"""
import collections
import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
SEO = json.loads(Path("seo.json").read_text(encoding="utf-8"))
SITE_URL = (os.environ.get("SITE_URL") or SEO.get("site_url") or "").strip().rstrip("/")
# URLهای قدیمی محصولات جدید فقط redirect هستند و نباید مثل صفحات محصول اصلی audit شوند.
try:
    catalog = json.loads(Path("products.json").read_text(encoding="utf-8"))
except Exception:
    catalog = []
try:
    _articles = json.loads(Path("articles.json").read_text(encoding="utf-8"))
except Exception:
    _articles = []

SKIP = {"404.html", "product-4.html"} | {
    f"product-{p.get('id')}.html" for p in catalog
    if str(p.get("id", "")).startswith("new-")
}
# تا وقتی هیچ مقاله‌ای منتشر نشده، articles.html عمداً از sitemap/canonical معاف است (مثل صفحهٔ 404).
if not _articles:
    SKIP.add("articles.html")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title = "", False
        self.meta, self.links, self.h, self.imgs, self.hrefs, self.ld = {}, [], collections.Counter(), [], [], []
        self._ld = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "title": self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key: self.meta[key] = a.get("content", "")
        elif tag == "link": self.links.append(a)
        elif tag in ("h1", "h2", "h3"): self.h[tag] += 1
        elif tag == "img": self.imgs.append(a)
        elif tag == "a" and a.get("href"): self.hrefs.append(a["href"])
        elif tag == "script" and a.get("type") == "application/ld+json": self._ld = ""

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        elif tag == "script" and self._ld is not None:
            self.ld.append(self._ld); self._ld = None

    def handle_data(self, d):
        if self.in_title: self.title += d
        if self._ld is not None: self._ld += d


errs, warns = [], []
def err(p, m): errs.append(f"{p}: {m}")
def warn(p, m): warns.append(f"{p}: {m}")


pages = sorted(f for f in glob.glob("*.html"))
info = {}
for f in pages:
    pg = Page(); pg.feed(Path(f).read_text(encoding="utf-8")); info[f] = pg

titles, descs = collections.defaultdict(list), collections.defaultdict(list)
for f, pg in info.items():
    if f in SKIP:
        if f == "404.html" and "noindex" not in pg.meta.get("robots", ""):
            err(f, "صفحهٔ 404 باید noindex باشد")
        continue
    t, d = re.sub(r"\s+", " ", pg.title).strip(), pg.meta.get("description", "").strip()
    titles[t].append(f); descs[d].append(f)
    if not t: err(f, "title ندارد")
    elif len(t) > 75: warn(f, f"title بلند است ({len(t)} نویسه؛ ممکن است در گوگل کوتاه شود)")
    if not d: err(f, "meta description ندارد")
    elif len(d) < 70: warn(f, f"description کوتاه است ({len(d)})")
    elif len(d) > 175: warn(f, f"description بلند است ({len(d)})")
    if pg.h["h1"] != 1: err(f, f"تعداد h1 باید ۱ باشد (الان {pg.h['h1']})")
    for im in pg.imgs:
        if not im.get("alt", "").strip(): err(f, f"تصویر بدون alt: {im.get('src')}")
    if SITE_URL:
        canon = [l for l in pg.links if l.get("rel") == "canonical"]
        if len(canon) != 1: err(f, "canonical باید دقیقاً یکی باشد")
        if "og:image" not in pg.meta: warn(f, "og:image ندارد (پیش‌نمایش لینک بدون تصویر)")
        if "og:title" not in pg.meta: err(f, "Open Graph ندارد")
    for raw in pg.ld:
        try: json.loads(raw)
        except Exception as e: err(f, f"JSON-LD نامعتبر: {e}")
    # لینک‌های داخلی شکسته
    for h in pg.hrefs:
        if re.match(r"(https?:|tel:|mailto:|#|javascript:)", h): continue
        target = h.split("#")[0].split("?")[0]
        if target and not os.path.exists(target): err(f, f"لینک داخلی شکسته: {h}")
    for im in pg.imgs:
        src = im.get("src", "")
        if src and not src.startswith(("http", "data:")) and not os.path.exists(src.split("?")[0]):
            err(f, f"فایل تصویر پیدا نشد: {src}")

for t, fs in titles.items():
    if len(fs) > 1: warn("محتوای تکراری", f"عنوان یکسان «{t}» در: {', '.join(fs)}")
for d, fs in descs.items():
    if d and len(fs) > 1: warn("محتوای تکراری", f"توضیح یکسان در: {', '.join(fs)}")

# robots / sitemap
if not os.path.exists("robots.txt"): err("robots.txt", "وجود ندارد")
if not SITE_URL:
    warn("تنظیمات", "site_url در seo.json خالی است؛ canonical/Open Graph/sitemap غیرفعال‌اند")
elif not os.path.exists("sitemap.xml"): err("sitemap.xml", "وجود ندارد")
else:
    locs = set(re.findall(r"<loc>([^<]+)</loc>", Path("sitemap.xml").read_text(encoding="utf-8")))
    for f in pages:
        if f in SKIP: continue
        url = SITE_URL + "/" if f == "index.html" else f"{SITE_URL}/{f}"
        if html.escape(url) not in locs: err("sitemap.xml", f"{f} در sitemap نیست")
if not os.path.exists(SEO.get("default_og_image", "")):
    warn("تنظیمات", f"تصویر اشتراک‌گذاری پیش‌فرض ({SEO.get('default_og_image')}) وجود ندارد")

print(f"صفحه‌های بررسی‌شده: {len([p for p in pages if p not in SKIP])}")
for m in errs: print("ERR ", m)
for m in warns: print("WARN", m)
print(f"\n{len(errs)} خطا، {len(warns)} هشدار")
sys.exit(1 if errs else 0)
