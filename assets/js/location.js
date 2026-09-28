        (function () {
            var btn = document.getElementById('gtCopyAddress');
            var addr = document.getElementById('gtAddress');
            if (!btn || !addr) return;
            btn.addEventListener('click', function () {
                var label = btn.querySelector('span');
                var done = function () {
                    label.textContent = 'کپی شد ✓';
                    setTimeout(function () { label.textContent = 'کپی آدرس'; }, 2000);
                };
                var text = addr.textContent.trim();
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(done, done);
                } else {
                    var t = document.createElement('textarea');
                    t.value = text; document.body.appendChild(t); t.select();
                    try { document.execCommand('copy'); } catch (e) {}
                    document.body.removeChild(t); done();
                }
            });
        })();
    
