#!/usr/bin/env python3
"""
ساخت صفحه‌ها: هدر و فوتر مشترک را از پوشه partials/ در همه فایل‌های .html قرار می‌دهد.

روش استفاده:
    1) partials/header.html یا partials/footer.html را ویرایش کنید
       (مثلاً شماره تلفن، آدرس یا آیتم‌های منو)
    2) در پوشه سایت این دستور را اجرا کنید:  python3 build.py
"""
import glob, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def active_for(name):
    if name == "index.html": return "home"
    if name == "about.html": return "about"
    if name == "contact.html": return "contact"
    if name.startswith("product"): return "products"
    return None

header, footer = read("partials/header.html").strip(), read("partials/footer.html").strip()

for page in sorted(glob.glob("*.html")):
    s = read(page)
    act = active_for(page)
    h = re.sub(r"\{\{active:(\w+)\}\}", lambda m: "active" if m.group(1) == act else "", header)
    h = h.replace('sub-nav-link "', 'sub-nav-link"')
    s = re.sub(r"<!-- @@header:start -->.*?<!-- @@header:end -->",
               lambda m: "<!-- @@header:start -->\n" + h + "\n<!-- @@header:end -->", s, flags=re.S)
    s = re.sub(r"<!-- @@footer:start -->.*?<!-- @@footer:end -->",
               lambda m: "<!-- @@footer:start -->\n" + footer + "\n<!-- @@footer:end -->", s, flags=re.S)
    with open(page, "w", encoding="utf-8") as f:
        f.write(s)
    print("ok", page)
