#!/usr/bin/env python3
"""
ساخت نسخهٔ سبک Font Awesome (فقط آیکون‌هایی که در سایت استفاده شده‌اند).
هر وقت آیکون تازه‌ای به سایت اضافه کردید یک بار اجرا کنید:  python3 tools/make_icons.py
نیازمند:  pip install fonttools brotli
خروجی:  assets/fa/fa-subset.css  و  assets/fa/webfonts/subset-*.woff2
"""
import glob, os, re, subprocess, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

css = open("tools/originals/fa/all.min.css", encoding="utf-8").read()

# ۱) کدپوینت هر آیکون
codes = {}
for sels, cp in re.findall(r'((?:\.fa-[a-z0-9-]+:before,?)+)\{content:"\\([0-9a-f]+)"\}', css):
    for name in re.findall(r"\.(fa-[a-z0-9-]+):before", sels):
        codes[name] = cp

# ۲) کلاس‌های استفاده‌شده در HTML/JS/partials/templates (نه فایل‌های خود FA)
files = glob.glob("*.html") + glob.glob("partials/*.html") + glob.glob("templates/*.html") \
      + glob.glob("assets/js/*.js") + glob.glob("*.json") + ["build.py"]
used = set()
for f in files:
    if f.endswith("bootstrap.bundle.min.js"): continue
    used |= set(re.findall(r"\bfa-[a-z0-9-]+", open(f, encoding="utf-8").read()))
icons = sorted(u for u in used if u in codes)

BRANDS = {"fa-whatsapp", "fa-instagram", "fa-telegram", "fa-telegram-plane", "fa-linkedin", "fa-twitter", "fa-x-twitter", "fa-facebook", "fa-youtube"}
# آیکون‌هایی که با fa-regular استفاده می‌شوند
regular = set()  # فونت regular حذف شده؛ همهٔ آیکون‌ها (به‌جز برندها) از solid می‌آیند
groups = {"brands": [], "regular": [], "solid": []}
for i in icons:
    if i in BRANDS: groups["brands"].append(i)
    elif i in regular: groups["regular"].append(i)
    else: groups["solid"].append(i)

# ۳) subset فونت‌ها
src = {"brands": "fa-brands-400", "regular": "fa-regular-400", "solid": "fa-solid-900"}
for g, names in groups.items():
    if not names: continue
    uni = ",".join("U+" + codes[n] for n in names)
    out = f"assets/fa/webfonts/subset-{g}.woff2"
    subprocess.check_call([sys.executable, "-m", "fontTools.subset", f"tools/originals/fa/{src[g]}.woff2",
                           f"--unicodes={uni}", "--flavor=woff2", f"--output-file={out}", "--layout-features="])
    print(g, len(names), "icons ->", os.path.getsize(out), "bytes")

# ۴) CSS: قوانین پایه (بدون font-face و آیکون‌ها) + آیکون‌های استفاده‌شده
base = css.split("@font-face")[0]
base = re.sub(r"/\*!.*?\*/", "", base, flags=re.S)
base = base.split(".fa-0:before")[0] if ".fa-0:before" in base else base
# قوانین ابزاری (fa-fw, fa-lg, ...) در base هستند؛ قوانین :before آیکون‌ها را خودمان می‌سازیم
base = re.sub(r"\.fa-[a-z0-9-]+:before[^{}]*\{[^{}]*\}", "", base)
faces = ""
for g, w in (("brands", 400), ("solid", 900)):
    if not groups[g]: continue
    fam = "Font Awesome 6 Brands" if g == "brands" else "Font Awesome 6 Free"
    faces += ('@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:block;'
              'src:url(webfonts/subset-%s.woff2) format("woff2")}\n' % (fam, w, g))
rules = "".join('.%s:before{content:"\\%s"}' % (n, codes[n]) for n in icons)
open("assets/fa/fa-subset.css", "w", encoding="utf-8").write(faces + base + "\n" + rules + "\n")
print("icons used:", len(icons), "| missing from FA:", sorted(u for u in used if u not in codes and u not in
      {"fa-solid","fa-brands","fa-regular","fa-fw","fa-lg","fa-xs","fa-sm","fa-xl","fa-2xl","fa-2x","fa-3x"})[:20])
