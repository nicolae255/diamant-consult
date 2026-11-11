/* Diamant Consult Immobilier — chat assistant (scripted, no AI).
   Flow: e-mail -> topic -> message -> sent by e-mail (Web3Forms, same inbox as the contact forms).
   Contact is by e-mail only: never add a phone number here. Language follows <html lang>. */
(function () {
  'use strict';
  if (window.__dcChat) return; window.__dcChat = true;

  var ENDPOINT = 'https://api.web3forms.com/submit';
  var KEY = 'ac28f9a0-206e-48e7-a1b1-3e0f8be82cb9';
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var T = {
    fr: { teaser: 'Une question sur la vente de votre bien ?', open: 'Ouvrir le chat', close: 'Fermer le chat',
          title: 'Diamant Consult', status: 'Réponse par e-mail',
          hello: 'Bonjour ! Vous pensez à vendre une maison ou un appartement ?<br>Indiquez d’abord votre adresse e-mail, pour que nous puissions vous répondre.',
          email_ph: 'votre@email.com', send_email: 'Valider l’e-mail', ask_topic: 'Merci ! Quel est l’objet de votre demande ?',
          topics: ['Vendre une maison', 'Vendre un appartement', 'Prix de mon bien', 'Vente publique (notaire)', 'Autre'],
          msg_ph: 'Votre demande : commune, type de bien, calendrier…', about: 'Votre demande concernant : ', send: 'Envoyer',
          you: 'Vous', ok: 'Merci, votre demande est bien envoyée.<br>Nous vous répondons par e-mail dans les plus brefs délais.',
          done_t: 'Demande envoyée', done_p: 'Premier rendez-vous gratuit et sans engagement.',
          err: 'L’envoi n’a pas fonctionné. Vous pouvez nous écrire via la <a href="/contact/">page contact</a> ou à <a href="mailto:borremans.helpinfo@gmail.com">borremans.helpinfo@gmail.com</a>.',
          subject: 'Chat site — ' },
    en: { teaser: 'A question about selling your property?', open: 'Open chat', close: 'Close chat',
          title: 'Diamant Consult', status: 'We reply by email',
          hello: 'Hello! Thinking of selling a house or an apartment?<br>First, enter your email address so we can reply to you.',
          email_ph: 'your@email.com', send_email: 'Confirm email', ask_topic: 'Thank you! What is your request about?',
          topics: ['Selling a house', 'Selling an apartment', 'Price of my property', 'Public auction (notary)', 'Other'],
          msg_ph: 'Your request: municipality, property type, timing…', about: 'Your request about: ', send: 'Send',
          you: 'You', ok: 'Thank you, your request has been sent.<br>We will reply by email as soon as possible.',
          done_t: 'Request sent', done_p: 'Free first meeting, no obligation.',
          err: 'Sending failed. You can write to us via the <a href="/en/contact/">contact page</a> or at <a href="mailto:borremans.helpinfo@gmail.com">borremans.helpinfo@gmail.com</a>.',
          subject: 'Website chat — ' },
    nl: { teaser: 'Een vraag over de verkoop van uw woning?', open: 'Chat openen', close: 'Chat sluiten',
          title: 'Diamant Consult', status: 'Antwoord per e-mail',
          hello: 'Hallo! Denkt u erover een huis of appartement te verkopen?<br>Vul eerst uw e-mailadres in, zodat we u kunnen antwoorden.',
          email_ph: 'uw@email.com', send_email: 'E-mail bevestigen', ask_topic: 'Bedankt! Waarover gaat uw vraag?',
          topics: ['Een huis verkopen', 'Een appartement verkopen', 'Prijs van mijn woning', 'Openbare verkoop (notaris)', 'Andere'],
          msg_ph: 'Uw vraag: gemeente, type woning, timing…', about: 'Uw vraag over: ', send: 'Versturen',
          you: 'U', ok: 'Bedankt, uw aanvraag is verstuurd.<br>We antwoorden zo snel mogelijk per e-mail.',
          done_t: 'Aanvraag verstuurd', done_p: 'Gratis eerste afspraak, vrijblijvend.',
          err: 'Het versturen is mislukt. U kunt ons schrijven via de <a href="/nl/contact/">contactpagina</a> of op <a href="mailto:borremans.helpinfo@gmail.com">borremans.helpinfo@gmail.com</a>.',
          subject: 'Chat website — ' }
  }[lang] || null;
  if (!T) return;

  var HOUSE = '<svg viewBox="0 0 120 136" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="M69.42 19.40 L80.00 19.40 L92.00 19.40 L102.58 19.40 L96.00 12.00 L76.00 12.00 Z M82.26 22.60 L86.00 33.19 L89.74 22.60 Z M69.69 22.60 L83.45 35.60 L78.87 22.60 Z M102.31 22.60 L93.13 22.60 L88.55 35.60 Z M92.00 66.67 L92.00 44.00 L80.00 44.00 L80.00 56.67 L60.00 40.00 L12.00 80.00 L20.00 80.00 L20.00 124.00 L52.00 124.00 L52.00 102.00 L68.00 102.00 L68.00 124.00 L100.00 124.00 L100.00 80.00 L108.00 80.00 Z"/></svg>';
  var ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CHAT = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke-linejoin="round"/></svg>';
  var X = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12" stroke-linecap="round"/></svg>';

  var css = [
    '#dcc-bubble{position:fixed;right:1.25rem;bottom:1.25rem;width:58px;height:58px;border-radius:50%;border:0;cursor:pointer;',
    'background:#0A0A0A;color:#F6F4EF;display:flex;align-items:center;justify-content:center;z-index:9998;',
    'box-shadow:0 10px 30px rgba(10,10,10,.25);transition:transform .2s ease,bottom .3s ease;}',
    '#dcc-bubble:hover{transform:translateY(-2px);}',
    '#dcc-bubble .x{display:none}#dcc-bubble.open .x{display:flex}#dcc-bubble.open .c{display:none}',
    'body:has(#cookie-banner[style*="flex"]) #dcc-bubble{bottom:7.5rem}',
    'body:has(#cookie-banner[style*="flex"]) #dcc-teaser{bottom:12rem}',
    'body:has(#cookie-banner[style*="flex"]) #dcc-win{bottom:12rem}',
    '#dcc-teaser{position:fixed;right:1.25rem;bottom:5.6rem;max-width:240px;background:#fff;color:#0A0A0A;',
    'border:1px solid #E2DED5;border-radius:16px 16px 4px 16px;padding:.8rem 1rem;font:500 .9rem/1.4 "Inter Tight",system-ui,sans-serif;',
    'box-shadow:0 10px 30px rgba(10,10,10,.12);z-index:9998;cursor:pointer;opacity:0;transform:translateY(8px);',
    'transition:opacity .3s,transform .3s;pointer-events:none;}',
    '#dcc-teaser.on{opacity:1;transform:none;pointer-events:auto}',
    '#dcc-teaser button{position:absolute;top:-8px;left:-8px;width:22px;height:22px;border-radius:50%;border:0;background:#0A0A0A;color:#F6F4EF;cursor:pointer;font-size:11px;line-height:1}',
    '#dcc-win{position:fixed;right:1.25rem;bottom:5.6rem;width:370px;max-width:calc(100vw - 2rem);height:min(560px,calc(100vh - 8rem));',
    'background:#fff;border:1px solid #E2DED5;border-radius:20px;box-shadow:0 24px 60px rgba(10,10,10,.18);display:flex;flex-direction:column;',
    'overflow:hidden;z-index:9999;font-family:"Inter Tight",system-ui,sans-serif;color:#0A0A0A;',
    'opacity:0;transform:translateY(12px) scale(.97);transform-origin:bottom right;pointer-events:none;transition:opacity .2s,transform .2s;}',
    '#dcc-win.open{opacity:1;transform:none;pointer-events:auto}',
    '.dcc-head{background:#0A0A0A;color:#F6F4EF;padding:1rem 1.1rem;display:flex;align-items:center;gap:.75rem}',
    '.dcc-av{width:38px;height:38px;border-radius:50%;background:#F6F4EF;color:#0A0A0A;display:flex;align-items:center;justify-content:center;flex-shrink:0}',
    '.dcc-av svg{width:20px;height:22px}',
    '.dcc-head h3{margin:0;font:700 1rem/1.2 "Bricolage Grotesque","Inter Tight",sans-serif}',
    '.dcc-head p{margin:.15rem 0 0;font-size:.78rem;color:#CFCBC2;display:flex;align-items:center;gap:.4rem}',
    '.dcc-head p i{width:7px;height:7px;border-radius:50%;background:#7CC48A;display:inline-block}',
    '.dcc-head button{margin-left:auto;background:transparent;border:0;color:#F6F4EF;cursor:pointer;padding:.35rem;border-radius:8px}',
    '.dcc-head button:hover{background:rgba(246,244,239,.12)}',
    '.dcc-msgs{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.7rem;background:#F6F4EF}',
    '.dcc-m{display:flex;gap:.5rem;align-items:flex-end;max-width:88%}',
    '.dcc-m .b{background:#fff;border:1px solid #E2DED5;border-radius:16px 16px 16px 4px;padding:.65rem .85rem;font-size:.9rem;line-height:1.5}',
    '.dcc-m .b a{color:#0A0A0A}',
    '.dcc-m .a{width:26px;height:26px;border-radius:50%;background:#0A0A0A;color:#F6F4EF;display:flex;align-items:center;justify-content:center;flex-shrink:0}',
    '.dcc-m .a svg{width:13px;height:15px}',
    '.dcc-m.u{align-self:flex-end;flex-direction:row-reverse}',
    '.dcc-m.u .b{background:#0A0A0A;color:#F6F4EF;border-color:#0A0A0A;border-radius:16px 16px 4px 16px}',
    '.dcc-dots{display:flex;gap:4px;padding:.2rem 0}.dcc-dots span{width:6px;height:6px;border-radius:50%;background:#9A968D;animation:dcc 1s infinite}',
    '.dcc-dots span:nth-child(2){animation-delay:.15s}.dcc-dots span:nth-child(3){animation-delay:.3s}',
    '@keyframes dcc{0%,60%,100%{opacity:.3}30%{opacity:1}}',
    '.dcc-foot{border-top:1px solid #E2DED5;padding:.85rem;background:#fff}',
    '.dcc-row{display:flex;gap:.5rem}',
    '.dcc-foot input,.dcc-foot textarea{flex:1;font:inherit;font-size:.92rem;padding:.7rem .8rem;border:1px solid #D6D2C8;border-radius:12px;outline:none;min-width:0;box-sizing:border-box}',
    '.dcc-foot input:focus,.dcc-foot textarea:focus{border-color:#0A0A0A}',
    '.dcc-foot textarea{width:100%;min-height:78px;resize:none;margin:.5rem 0}',
    '.dcc-btn{border:0;border-radius:12px;background:#0A0A0A;color:#F6F4EF;font:600 .9rem "Inter Tight",sans-serif;padding:.7rem .95rem;cursor:pointer;display:inline-flex;align-items:center;gap:.4rem;justify-content:center}',
    '.dcc-btn:disabled{opacity:.5;cursor:default}',
    '.dcc-chips{display:flex;flex-wrap:wrap;gap:.4rem}',
    '.dcc-chip{border:1px solid #D6D2C8;background:#fff;border-radius:999px;padding:.4rem .75rem;font:500 .8rem "Inter Tight",sans-serif;cursor:pointer;color:#0A0A0A}',
    '.dcc-chip[aria-pressed="true"]{background:#0A0A0A;color:#F6F4EF;border-color:#0A0A0A}',
    '.dcc-done{text-align:center;padding:.4rem 0}.dcc-done h4{margin:.4rem 0 .2rem;font-size:.95rem}.dcc-done p{margin:0;font-size:.82rem;color:#5C5A55}',
    '.dcc-bad{border-color:#B42318!important}',
    '@media (max-width:520px){#dcc-win{right:.75rem;left:.75rem;width:auto;max-width:none;top:5.5rem;bottom:5.2rem;height:auto}#dcc-teaser{display:none}}'
  ].join('');

  function el(html) { var d = document.createElement('div'); d.innerHTML = html; return d.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function init() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var teaser = el('<div id="dcc-teaser" role="button" tabindex="0"><button type="button" aria-label="' + T.close + '">✕</button>' + T.teaser + '</div>');
    var bubble = el('<button id="dcc-bubble" type="button" aria-label="' + T.open + '" aria-expanded="false" aria-controls="dcc-win"><span class="c">' + CHAT + '</span><span class="x">' + X + '</span></button>');
    var win = el('<div id="dcc-win" role="dialog" aria-label="' + T.title + '"><div class="dcc-head"><div class="dcc-av">' + HOUSE + '</div><div><h3>' + T.title + '</h3><p><i></i>' + T.status + '</p></div><button type="button" aria-label="' + T.close + '">' + X + '</button></div><div class="dcc-msgs" aria-live="polite"></div><div class="dcc-foot"></div></div>');
    document.body.appendChild(teaser); document.body.appendChild(win); document.body.appendChild(bubble);
    var msgs = win.querySelector('.dcc-msgs'), foot = win.querySelector('.dcc-foot');
    var state = 'idle', email = '', topic = '';

    try { if (!sessionStorage.getItem('dcc-seen')) setTimeout(function () { if (!win.classList.contains('open') && state === 'idle') teaser.classList.add('on'); }, 4000); } catch (e) {}
    function hideTeaser() { teaser.classList.remove('on'); try { sessionStorage.setItem('dcc-seen', '1'); } catch (e) {} }
    function open() { hideTeaser(); win.classList.add('open'); bubble.classList.add('open'); bubble.setAttribute('aria-expanded', 'true'); if (state === 'idle') start(); }
    function close() { win.classList.remove('open'); bubble.classList.remove('open'); bubble.setAttribute('aria-expanded', 'false'); }
    bubble.addEventListener('click', function () { win.classList.contains('open') ? close() : open(); });
    win.querySelector('.dcc-head button').addEventListener('click', close);
    teaser.addEventListener('click', open);
    teaser.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    teaser.querySelector('button').addEventListener('click', function (e) { e.stopPropagation(); hideTeaser(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && win.classList.contains('open')) close(); });

    function say(html, user, delay) {
      return new Promise(function (resolve) {
        var typing = null;
        if (!user && delay) { typing = el('<div class="dcc-m"><div class="a">' + HOUSE + '</div><div class="b"><div class="dcc-dots"><span></span><span></span><span></span></div></div></div>'); msgs.appendChild(typing); msgs.scrollTop = msgs.scrollHeight; }
        setTimeout(function () {
          if (typing) typing.remove();
          msgs.appendChild(el(user ? '<div class="dcc-m u"><div class="b">' + html + '</div></div>' : '<div class="dcc-m"><div class="a">' + HOUSE + '</div><div class="b">' + html + '</div></div>'));
          msgs.scrollTop = msgs.scrollHeight; resolve();
        }, delay || 0);
      });
    }
    function start() { state = 'email'; say(T.hello, false, 500).then(emailStep); }
    function emailStep() {
      foot.innerHTML = '<form class="dcc-row" novalidate><input type="email" required autocomplete="email" placeholder="' + T.email_ph + '" aria-label="E-mail"><button class="dcc-btn" type="submit" aria-label="' + T.send_email + '">' + ARROW + '</button></form>';
      var f = foot.querySelector('form'), i = f.querySelector('input'); i.focus();
      f.addEventListener('submit', function (e) {
        e.preventDefault(); var v = i.value.trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { i.classList.add('dcc-bad'); i.focus(); setTimeout(function () { i.classList.remove('dcc-bad'); }, 1500); return; }
        email = v; state = 'msg'; foot.innerHTML = '';
        say(esc(v), true).then(function () { return say(T.ask_topic, false, 700); }).then(msgStep);
      });
    }
    function msgStep() {
      foot.innerHTML = '<form novalidate><div class="dcc-chips">' + T.topics.map(function (t) { return '<button type="button" class="dcc-chip" aria-pressed="false">' + t + '</button>'; }).join('') +
        '</div><textarea required aria-label="Message" placeholder="' + T.msg_ph + '"></textarea><div style="text-align:right"><button class="dcc-btn" type="submit">' + T.send + ' ' + ARROW + '</button></div></form>';
      var f = foot.querySelector('form'), ta = f.querySelector('textarea');
      f.querySelectorAll('.dcc-chip').forEach(function (c) {
        c.addEventListener('click', function () {
          topic = c.textContent;
          f.querySelectorAll('.dcc-chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
          c.setAttribute('aria-pressed', 'true'); if (!ta.value) ta.placeholder = T.about + topic + '…'; ta.focus();
        });
      });
      f.addEventListener('submit', function (e) {
        e.preventDefault(); var m = ta.value.trim();
        if (!m) { ta.classList.add('dcc-bad'); ta.focus(); setTimeout(function () { ta.classList.remove('dcc-bad'); }, 1500); return; }
        f.querySelector('button[type=submit]').disabled = true; state = 'done'; foot.innerHTML = '';
        say(esc(m).replace(/\n/g, '<br>'), true).then(function () { return send(m); })
          .then(function () {
            try { (window.dataLayer = window.dataLayer || []).push({ event: 'chat_submit', chat_topic: topic || 'n/a', page_lang: lang }); } catch (e) {}
            return say(T.ok, false, 800);
          })
          .then(function () { foot.innerHTML = '<div class="dcc-done"><h4>' + T.done_t + '</h4><p>' + T.done_p + '</p></div>'; })
          .catch(function () { state = 'msg'; say(T.err, false, 400).then(msgStep); });
      });
    }
    function send(m) {
      return fetch(ENDPOINT, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ access_key: KEY, subject: T.subject + (topic || 'demande'), from_name: 'Chat diamantconsult.com', email: email, sujet: topic || '-', message: m, page: location.href, langue: lang, botcheck: '' })
      }).then(function (r) { return r.json(); })
        .then(function (j) { if (!j || j.success !== true) throw new Error((j && j.message) || 'fail'); });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
