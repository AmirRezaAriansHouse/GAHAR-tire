#!/usr/bin/env python3
"""زیرمجموعهٔ فونت وزیرمتن (فارسی/عربی + لاتین + ارقام + علائم) با حفظ وزن‌های متغیر.
اجرا:  python3 tools/make_font.py     (نیازمند fonttools و brotli)
ورودی: tools/originals/Vazirmatn-VF.full.woff2 (نسخهٔ اصلی؛ اگر نبود از نسخهٔ فعلی ساخته می‌شود)"""
import os, shutil, subprocess, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
full, out = "tools/originals/Vazirmatn-VF.full.woff2", "assets/fonts/Vazirmatn-VF.woff2"
if not os.path.exists(full): shutil.copy(out, full)
uni = "U+0020-007E,U+00A0-00BF,U+00D7,U+00F7,U+0600-06FF,U+0750-077F,U+200B-200F,U+2010-2027,U+202A-202F,U+2030-203A,U+2212,U+FB50-FDFF,U+FE70-FEFF"
subprocess.check_call([sys.executable, "-m", "fontTools.subset", full, f"--unicodes={uni}", "--flavor=woff2",
                       "--layout-features=*", f"--output-file={out}"])
print(os.path.getsize(full), "->", os.path.getsize(out))
