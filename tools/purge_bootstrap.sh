#!/usr/bin/env bash
# حذف کلاس‌های بلااستفادهٔ بوت‌استرپ (نیازمند Node.js). هر وقت کلاس بوت‌استرپ تازه‌ای به HTML/JS اضافه کردید یک بار اجرا کنید.
# ورودی: tools/originals/bootstrap.rtl.min.css   خروجی: assets/css/bootstrap.rtl.purged.css
set -e
cd "$(dirname "$0")/.."
npx --yes purgecss@6 --config tools/purgecss.config.js
# minify ساده
python3 - <<'PY'
import re
p="assets/css/bootstrap.rtl.purged.css"
s=open(p,encoding="utf-8").read()
s=re.sub(r"/\*.*?\*/","",s,flags=re.S); s=re.sub(r"\s+"," ",s); s=re.sub(r"\s*([{};,>~])\s*",r"\1",s)
open(p,"w",encoding="utf-8").write(s)
PY
ls -la assets/css/bootstrap.rtl.purged.css
