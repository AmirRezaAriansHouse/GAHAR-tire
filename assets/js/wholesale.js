/* فرم استعلام عمده: پیام آماده را در واتساپ باز می‌کند */
(function () {
    var form = document.getElementById('wsForm');
    if (!form) return;
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var v = function (id) { return (document.getElementById(id).value || '').trim(); };
        var lines = ['سلام، برای خرید عمده لاستیک استعلام قیمت و موجودی دارم.'];
        if (v('wsName')) lines.push('نام: ' + v('wsName'));
        if (v('wsType')) lines.push('نوع مشتری: ' + v('wsType'));
        if (v('wsCat')) lines.push('دسته لاستیک: ' + v('wsCat'));
        if (v('wsSize')) lines.push('سایز(ها): ' + v('wsSize'));
        if (v('wsQty')) lines.push('تعداد تقریبی: ' + v('wsQty'));
        if (v('wsNote')) lines.push('توضیحات: ' + v('wsNote'));
        window.open('https://wa.me/989120346053?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
})();
