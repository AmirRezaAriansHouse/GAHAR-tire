/* رفتارهای ظریف سایت: اسکلتون تصاویر + انیمیشن ورود بخش‌ها */
(function () {
    var root = document.documentElement;

    /* ---- اسکلتون لود تصویر ---- */
    function skeletons() {
        var imgs = document.querySelectorAll('main img');
        imgs.forEach(function (img, i) {
            if (i > 3 && !img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
            if (img.complete && img.naturalWidth) return;
            var box = img.parentElement;
            if (!box) return;
            box.classList.add('gt-skel');
            var done = function () { box.classList.remove('gt-skel'); };
            img.addEventListener('load', done, { once: true });
            img.addEventListener('error', done, { once: true });
        });
    }

    /* ---- انیمیشن ورود هنگام اسکرول ---- */
    function reveal() {
        if (!('IntersectionObserver' in window)) return;
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        var sel = '.gt-trust, .gt-dark-panel, .gt-about, .gt-stat, .gt-location, .gt-cta, .gt-faq .accordion-item,' +
                  '.gt-service, .gt-feature, .card-product, .ws-card, .ws-step, .ws-form-box, .product-showcase .gt-product-card,' +
                  'main .card.rounded-5, .mb-5.mt-5, section.mb-5 > .text-center';
        var els = document.querySelectorAll(sel);
        var seen = new Set();
        root.classList.add('gt-js');
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (en) {
                if (!en.isIntersecting) return;
                var el = en.target;
                io.unobserve(el);
                el.classList.add('in');
                /* بعد از پایان انیمیشن، کلاس‌ها حذف می‌شوند تا hover و ... مختل نشوند */
                setTimeout(function () { el.classList.remove('reveal', 'in'); el.style.transitionDelay = ''; }, 1100);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
        els.forEach(function (el) {
            /* اگر والدش هم در لیست است، دوبار انیمیت نشود */
            var p = el.parentElement, nested = false;
            while (p && p !== document.body) { if (seen.has(p)) { nested = true; break; } p = p.parentElement; }
            if (nested) return;
            seen.add(el);
            var idx = Array.prototype.indexOf.call(el.parentElement.children, el);
            el.style.transitionDelay = Math.min(idx, 5) * 70 + 'ms';
            el.classList.add('reveal');
            io.observe(el);
        });
    }

    function init() { skeletons(); reveal(); }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
