/* فرم استعلام عمده: پیام آماده را در واتساپ باز می‌کند */
(function () {
    var form = document.getElementById('wsForm');
    if (!form) return;
    var status = document.getElementById('wsStatus');
    var say = function (t) { if (status) status.textContent = t; };
    var fields = ['wsQty', 'wsSize'].map(function (id) { return document.getElementById(id); });

    // با اصلاح فیلد، وضعیت خطا به‌روز شود
    fields.forEach(function (f) {
        if (!f) return;
        f.addEventListener('input', function () {
            f.setAttribute('aria-invalid', f.checkValidity() && f.value.trim() ? 'false' : 'true');
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var v = function (id) { return (document.getElementById(id).value || '').trim(); };
        // فیلد خالی یا فقط فاصله معتبر نیست
        var bad = fields.filter(function (f) { return f && (!f.checkValidity() || !f.value.trim()); });
        fields.forEach(function (f) { if (f) f.setAttribute('aria-invalid', bad.indexOf(f) > -1 ? 'true' : 'false'); });
        if (bad.length) {
            form.classList.add('was-validated');
            bad.forEach(function (f) { f.classList.add('is-invalid'); });
            say('لطفاً ' + (bad.length > 1 ? 'تعداد و سایز' : (bad[0].id === 'wsQty' ? 'تعداد' : 'سایز')) + ' را وارد کنید.');
            bad[0].focus();
            return;
        }
        fields.forEach(function (f) { if (f) f.classList.remove('is-invalid'); });
        var lines = ['سلام، برای خرید عمده لاستیک استعلام قیمت و موجودی دارم.'];
        if (v('wsName')) lines.push('نام: ' + v('wsName'));
        if (v('wsType')) lines.push('نوع مشتری: ' + v('wsType'));
        if (v('wsCat')) lines.push('دسته لاستیک: ' + v('wsCat'));
        if (v('wsSize')) lines.push('سایز(ها): ' + v('wsSize'));
        if (v('wsQty')) lines.push('تعداد تقریبی: ' + v('wsQty'));
        if (v('wsNote')) lines.push('توضیحات: ' + v('wsNote'));
        say('پیام آماده شد؛ واتساپ باز می‌شود.');
        window.open('https://wa.me/989120346053?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
})();
