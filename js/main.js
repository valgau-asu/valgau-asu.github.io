/* Small enhancements. No dependencies, no build step. */

// Mobile menu toggle
(function () {
  var btn = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (!btn || !links) return;

  btn.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
})();

// Keep the footer year current without editing it every January
(function () {
  var el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();

// Light / dark toggle.
// With nothing stored the site follows the operating system, which is how it
// behaved before this existed. Choosing a theme stores it and overrides the OS
// from then on; the small inline script in each page's <head> re-applies that
// choice before first paint so the page never flashes the wrong theme.
(function () {
  var KEY = 'theme';
  var root = document.documentElement;
  var btn = document.querySelector('.theme-toggle');
  if (!btn) return;

  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.2 4.2l1.6 1.6M18.2 18.2l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.2 19.8l1.6-1.6M18.2 5.8l1.6-1.6"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.5 8.5 0 1 1 9.8 3.5a6.8 6.8 0 0 0 10.7 10.7z"/></svg>';

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  // What the visitor is actually looking at right now.
  function current() {
    var s = stored();
    if (s) return s;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function paint() {
    var now = current();
    // The icon shows where the button will take you, not where you are.
    btn.innerHTML = now === 'dark' ? SUN : MOON;
    btn.setAttribute('aria-label', 'Switch to ' + (now === 'dark' ? 'light' : 'dark') + ' theme');
    btn.setAttribute('title', btn.getAttribute('aria-label'));
    btn.setAttribute('aria-pressed', now === 'dark' ? 'true' : 'false');
  }

  btn.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem(KEY, next); } catch (e) {}
    paint();
  });

  // Follow the OS live, but only while the visitor has made no choice.
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  var onChange = function () { if (!stored()) paint(); };
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else if (mq.addListener) mq.addListener(onChange);

  paint();
  btn.classList.add('is-ready');
})();
