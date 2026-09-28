/* اندازه هدر ثابت (موبایل) را اندازه‌گیری می‌کند تا محتوا زیر آن نرود */
(function () {
    var root = document.documentElement;
    function setH() {
        var h = document.querySelector('.gt-header');
        if (!h) return;
        root.style.setProperty('--gt-header-h', h.offsetHeight + 'px');
    }
    setH();
    window.addEventListener('load', setH);
    window.addEventListener('resize', setH);
    window.addEventListener('orientationchange', setH);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(setH);
})();
