/* Cookie consent (Google Consent Mode v2).
   The <head> sets every consent signal to "denied" before Google Tag Manager loads, so Analytics/Ads
   cookies are only written after "Accept". This file shows the banner and records the choice.
   window.dcCookieSettings() reopens the banner (link on the privacy page). */
(function () {
  var KEY = 'dc_cookie_consent';
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var T = {
    fr: { t: 'Cookies', p: 'Avec votre accord, nous utilisons des cookies de mesure d’audience et de publicité (Google) pour améliorer le site. Sans accord, aucun de ces cookies n’est déposé.', a: 'Accepter', r: 'Refuser', m: 'En savoir plus', u: '/confidentialite/' },
    en: { t: 'Cookies', p: 'With your consent, we use audience measurement and advertising cookies (Google) to improve the site. Without consent, none of these cookies are set.', a: 'Accept', r: 'Decline', m: 'Learn more', u: '/confidentialite/' },
    nl: { t: 'Cookies', p: 'Met uw toestemming gebruiken we cookies voor bezoekersmeting en advertenties (Google) om de site te verbeteren. Zonder toestemming worden deze cookies niet geplaatst.', a: 'Aanvaarden', r: 'Weigeren', m: 'Meer info', u: '/confidentialite/' }
  }[lang] || null;
  if (!T) T = { t: 'Cookies', p: '', a: 'OK', r: 'No', m: '', u: '/confidentialite/' };

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function apply(granted) {
    var s = granted ? 'granted' : 'denied';
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'update', { ad_storage: s, ad_user_data: s, ad_personalization: s, analytics_storage: s });
    window.dataLayer.push({ event: granted ? 'consent_granted' : 'consent_denied' });
  }

  function show() {
    var old = document.getElementById('cookie-banner');
    if (old) old.remove();
    var b = document.createElement('div');
    b.id = 'cookie-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', T.t);
    b.innerHTML = '<p><strong>' + T.t + '.</strong> ' + T.p + ' <a href="' + T.u + '">' + T.m + '</a></p>' +
      '<div class="cookie-actions"><button type="button" class="cookie-btn cookie-btn-decline">' + T.r + '</button>' +
      '<button type="button" class="cookie-btn cookie-btn-accept">' + T.a + '</button></div>';
    document.body.appendChild(b);
    document.body.classList.add('has-cookie-banner');
    function choose(ok) {
      set(ok ? 'accepted' : 'declined');
      apply(ok);
      b.remove();
      document.body.classList.remove('has-cookie-banner');
    }
    b.querySelector('.cookie-btn-accept').addEventListener('click', function () { choose(true); });
    b.querySelector('.cookie-btn-decline').addEventListener('click', function () { choose(false); });
  }

  window.dcCookieSettings = show;
  if (!get()) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', show); else show();
  }
})();
