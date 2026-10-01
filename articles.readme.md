# افزودن مقاله جدید

1. یک آبجکت به `articles.json` اضافه کنید با این فیلدها:
   - `id`: شناسه یکتا (انگلیسی، با خط تیره) — مثلاً `"size-guide"`
   - `title`: عنوان مقاله
   - `category`: برچسب دسته (مثلاً «راهنمای خرید»، «نگهداری»)
   - `updated`: تاریخ به‌فرمت YYYY-MM-DD
   - `meta_description`: توضیح متا (۷۰ تا ۱۷۵ کاراکتر)
   - `intro`: یک خط معرفی کوتاه (در لیست مقالات هم نمایش داده می‌شود)
   - `body_html`: متن کامل مقاله به‌صورت HTML (می‌توانید از `<h2>`, `<h3>`, `<p>`, `<ul>` استفاده کنید)

2. اجرا کنید: `python3 build.py`

این کار صفحه اختصاصی مقاله (`article-<id>.html`)، ورودی در `articles.html`،
breadcrumb، Article schema (JSON-LD) و ورود به sitemap.xml را خودکار می‌سازد.

تا وقتی `articles.json` خالی است، `articles.html` ساخته می‌شود اما از sitemap و
بررسی سئو (seo_audit.py) معاف است تا صفحه خالی ایندکس نشود.
