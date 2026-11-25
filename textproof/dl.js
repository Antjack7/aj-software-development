// Counts taps on App Store and Google Play buttons: which store, which app,
// which page. No cookies, nothing stored on the device, no personal details.
(function () {
  var KEY = 'phc_wF9Nsjnjwh2529qkwyCaiSFRKRnhzb9zK4BA8DWzKiZG';
  var URL_ = 'https://eu.i.posthog.com/i/v0/e/';
  var site = location.hostname.replace(/^www\./, '');
  var tapId = 'web-' + Math.random().toString(36).slice(2) + Date.now().toString(36);

  function storeOf(href) {
    if (/^https?:\/\/(apps|itunes)\.apple\.com\//.test(href)) return 'apple';
    if (/^https?:\/\/play\.google\.com\//.test(href)) return 'google';
    return null;
  }

  function onTap(e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var store = storeOf(a.href);
    if (!store) return;
    var m = a.href.match(/\/id(\d+)|[?&]id=([\w.]+)/);
    var ref = '';
    try { ref = document.referrer ? new URL(document.referrer).hostname.replace(/^www\./, '') : ''; } catch (_) {}
    var body = JSON.stringify({
      api_key: KEY,
      event: 'website_download_click',
      distinct_id: tapId,
      properties: {
        site: site,
        store: store,
        app_id: m ? (m[1] || m[2]) : '',
        page: location.pathname,
        button: (a.getAttribute('aria-label') || a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60),
        came_from: ref || 'direct',
        $current_url: location.origin + location.pathname,
        $process_person_profile: false,
        $ip: ''
      }
    });
    try {
      fetch(URL_, { method: 'POST', body: body, keepalive: true, headers: { 'Content-Type': 'text/plain' } }).catch(function () {});
    } catch (_) {}
  }

  document.addEventListener('click', onTap, true);
  document.addEventListener('auxclick', onTap, true);
})();
