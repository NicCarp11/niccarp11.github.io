(function () {
  var root = document.documentElement;
  var storageKey = 'theme';

  function applyTheme(theme) {
    if (theme === 'dark' || theme === 'light') {
      root.setAttribute('data-theme', theme);
    } else {
      root.removeAttribute('data-theme');
    }
  }

  var stored = localStorage.getItem(storageKey);
  applyTheme(stored);

  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      var current = root.getAttribute('data-theme') || (prefersDark ? 'dark' : 'light');
      var next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem(storageKey, next);
    });
  }

  var navToggle = document.getElementById('nav-toggle');
  var navInner = document.getElementById('nav-inner');
  if (navToggle && navInner) {
    navToggle.addEventListener('click', function () {
      navInner.classList.toggle('open');
    });
    navInner.querySelectorAll('.nav-links a').forEach(function (link) {
      link.addEventListener('click', function () {
        navInner.classList.remove('open');
      });
    });
  }

})();
