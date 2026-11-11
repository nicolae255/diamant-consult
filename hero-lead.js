/* Homepage lead card: commission comparison (our 2% HTVA vs other rates) + thank-you message after the form redirect. */
(function () {
  var slider = document.getElementById('hl-slider');
  if (!slider) return;
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var loc = lang === 'nl' ? 'nl-BE' : lang === 'en' ? 'en-GB' : 'fr-BE';
  var fmt = new Intl.NumberFormat(loc, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var price = document.getElementById('hl-price');
  var amounts = document.querySelectorAll('.hl-compare strong[data-rate]');
  var diffs = document.querySelectorAll('.hl-compare em[data-diff]');
  var bars = document.querySelectorAll('.hl-compare .bar i[data-rate]');
  var maxRate = 0;
  bars.forEach(function (b) { maxRate = Math.max(maxRate, +b.getAttribute('data-rate')); });
  var hidden = document.getElementById('hl-hidden-price');
  function update() {
    var v = +slider.value;
    price.textContent = fmt.format(v);
    amounts.forEach(function (a) { a.textContent = fmt.format(Math.round(v * a.getAttribute('data-rate') / 100)); });
    diffs.forEach(function (d) { d.textContent = '+' + fmt.format(Math.round(v * (d.getAttribute('data-diff') - 2) / 100)); });
    bars.forEach(function (b) { b.style.width = (b.getAttribute('data-rate') / maxRate * 100) + '%'; });
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
