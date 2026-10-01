module.exports = {
  content: ["*.html", "partials/*.html", "templates/*.html", "assets/js/location.js", "assets/js/mobile.js", "assets/js/theme.js", "assets/js/wholesale.js", "build.py", "products.json"],
  css: ["tools/originals/bootstrap.rtl.min.css"],
  output: "assets/css/bootstrap.rtl.purged.css",
  safelist: {
    standard: ["show", "fade", "collapse", "collapsing", "active", "disabled", "was-validated", "is-invalid", "is-valid", "modal-open"],
    greedy: [/^(offcanvas|accordion|dropdown|navbar|modal|tooltip|toast|carousel|bs-|tab-|placeholder|spinner)/]
  }
};
