/* Homepage lead card: commission calculator (2% HTVA) + thank-you message after the form redirect. */
(function () {
  var slider = document.getElementById('hl-slider');
  if (!slider) return;
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var loc = lang === 'nl' ? 'nl-BE' : lang === 'en' ? 'en-GB' : 'fr-BE';
  var fmt = new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var price = document.getElementById('hl-price');
  var fee = document.getElementById('hl-fee');
  var tvac = document.getElementById('hl-tvac');
  var hidden = document.getElementById('hl-hidden-price');
  function update() {
    var v = +slider.value;
    var f = Math.round(v * 0.02);
    price.textContent = fmt.format(v);
    fee.textContent = fmt.format(f);
    tvac.textContent = tvac.getAttribute('data-tpl').replace('{x}', fmt.format(Math.round(f * 1.21)));
    hidden.value = fmt.format(v);
    slider.style.setProperty('--p', ((v - slider.min) / (slider.max - slider.min) * 100) + '%');
  }
  slider.addEventListener('input', update);
  update();
  if (/[?&]merci=1/.test(location.search)) {
    var t = document.getElementById('hl-thanks');
    if (t) t.hidden = false;
  }
})();
