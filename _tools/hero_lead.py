#!/usr/bin/env python3
"""Homepage hero (FR/EN/NL): replaces the right-hand photo with a lead card
(commission calculator + short appointment form, Web3Forms). Re-runnable.

Usage:  python3 _tools/hero_lead.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = "ac28f9a0-206e-48e7-a1b1-3e0f8be82cb9"
COMMUNES = ["Anderlecht", "Auderghem", "Berchem-Sainte-Agathe", "Bruxelles-Ville", "Etterbeek", "Evere", "Forest",
            "Ganshoren", "Ixelles", "Jette", "Koekelberg", "Molenbeek-Saint-Jean", "Saint-Gilles", "Saint-Josse-ten-Noode",
            "Schaerbeek", "Uccle", "Watermael-Boitsfort", "Woluwe-Saint-Lambert", "Woluwe-Saint-Pierre",
            "Waterloo", "La Hulpe", "Wavre", "Rixensart"]
CHECK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

T = {
    "fr": dict(file="index.html", url="https://www.diamantconsult.com/",
               calc_t="Combien coûte notre service ?", price="Prix de vente envisagé",
               fee="Notre commission", htva="HTVA", tvac="soit {x} TVAC (TVA 21 %)",
               incl="Photos, annonces, visites, négociation et suivi jusqu’à l’acte : tout est compris.",
               form_t="Parlons de votre bien", type="Type de bien", types=["Maison", "Appartement", "Autre"],
               commune="Commune", commune_ph="Ex. Schaerbeek", email="Votre e-mail",
               send="Demander un rendez-vous", form_t2="Premier rendez-vous gratuit pour en parler", trust=["Notaire partenaire : Stephan Borremans", "Bureau à Schaerbeek", "23 communes · Bruxelles &amp; Brabant wallon"],
               note="Sans engagement · Réponse par e-mail",
               thanks="Merci ! Votre demande est bien envoyée. Nous vous répondons par e-mail.",
               subject="Demande de rendez-vous · page d’accueil", stat="Communes · Bruxelles &amp; Brabant wallon",
               cta="Vendre mon bien"),
    "en": dict(file="en/index.html", url="https://www.diamantconsult.com/en/",
               calc_t="What does our service cost?", price="Expected sale price",
               fee="Our commission", htva="excl. VAT", tvac="i.e. {x} incl. VAT (21% VAT)",
               incl="Photos, listings, viewings, negotiation and follow-up until the deed: all included.",
               form_t="Tell us about your property", type="Property type", types=["House", "Apartment", "Other"],
               commune="Municipality", commune_ph="e.g. Schaerbeek", email="Your e-mail",
               send="Book a meeting", form_t2="Free first meeting to talk it through", trust=["Partner notary: Stephan Borremans", "Office in Schaerbeek", "23 municipalities · Brussels &amp; Walloon Brabant"],
               note="No obligation · We reply by e-mail",
               thanks="Thank you! Your request has been sent. We will reply by e-mail.",
               subject="Meeting request · homepage (EN)", stat="Municipalities · Brussels &amp; Walloon Brabant",
               cta="Sell my property"),
    "nl": dict(file="nl/index.html", url="https://www.diamantconsult.com/nl/",
               calc_t="Wat kost onze dienst?", price="Beoogde verkoopprijs",
               fee="Onze commissie", htva="excl. btw", tvac="of {x} incl. btw (21% btw)",
               incl="Foto’s, advertenties, bezoeken, onderhandeling en opvolging tot de akte: alles inbegrepen.",
               form_t="Vertel ons over uw woning", type="Type woning", types=["Huis", "Appartement", "Ander"],
               commune="Gemeente", commune_ph="Bv. Schaarbeek", email="Uw e-mailadres",
               send="Afspraak aanvragen", form_t2="Gratis eerste afspraak om erover te praten", trust=["Partnernotaris: Stephan Borremans", "Kantoor in Schaarbeek", "23 gemeenten · Brussel &amp; Waals-Brabant"],
               note="Vrijblijvend · Antwoord per e-mail (FR/EN)",
               thanks="Bedankt! Uw aanvraag is verzonden. We antwoorden per e-mail.",
               subject="Afspraakaanvraag · startpagina (NL)", stat="Gemeenten · Brussel &amp; Waals-Brabant",
               cta="Mijn woning verkopen"),
}


def card(t):
    e = html.escape
    return f'''<div class="hero-lead" id="demande">
        <div class="hl-calc">
          <p class="hl-kicker">{t["calc_t"]}</p>
          <label class="hl-range"><span>{t["price"]} <output id="hl-price">400 000 €</output></span>
            <input type="range" id="hl-slider" min="100000" max="1500000" step="10000" value="400000" aria-label="{e(t["price"])}">
          </label>
          <div class="hl-fee">
            <span>{t["fee"]}</span>
            <strong><output id="hl-fee">8 000 €</output> <small>{t["htva"]}</small></strong>
          </div>
          <p class="hl-sub" id="hl-tvac" data-tpl="{e(t["tvac"])}">{e(t["tvac"].replace("{x}", "9 680 €"))}</p>
          <p class="hl-incl">{CHECK}<span>{t["incl"]}</span></p>
        </div>
        <form class="hl-form" action="https://api.web3forms.com/submit" method="POST">
          <p class="hl-title">{t["form_t2"]}</p>
          <p class="hl-thanks" id="hl-thanks" hidden>{t["thanks"]}</p>
          <input type="hidden" name="access_key" value="{KEY}">
          <input type="hidden" name="subject" value="{e(t["subject"])}">
          <input type="hidden" name="from_name" value="Site Diamant Consult">
          <input type="hidden" name="redirect" value="{t["url"]}?merci=1#demande">
          <input type="hidden" name="prix_envisage" id="hl-hidden-price" value="400 000 €">
          <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
          <div class="hl-inline">
            <input type="email" name="email" required autocomplete="email" placeholder="{e(t["email"])}" aria-label="{e(t["email"])}">
            <button type="submit" class="hl-btn">{t["send"]}</button>
          </div>
          <p class="hl-note">{t["note"]}</p>
        </form>
      </div>'''


def main():
    for lang, t in T.items():
        p = os.path.join(ROOT, t["file"])
        s = open(p, encoding="utf-8").read()
        start = s.find('<div class="hero-visual">')
        if start < 0:
            start = s.index('<div class="hero-lead"')
        end = s.index("    </div>\n  </div>\n</section>", start)
        s = s[:start] + card(t) + "\n" + s[end:]
        # stats row -> one quiet trust line (the 2% is in the calculator, the 600 € pack in the offers section)
        trust = "".join(f"<li>{CHECK}<span>{x}</span></li>" for x in t["trust"])
        s = re.sub(r'<div class="hero-stats">.*?\n        </div>\n(?=      </div>)|<ul class="hero-trust">.*?</ul>\n',
                   f'<ul class="hero-trust">{trust}</ul>\n', s, count=1, flags=re.S)
        # main CTA goes to the form
        s = re.sub(r'<a href="contact/" class="btn-primary">(\s*)' + re.escape(t["cta"]),
                   rf'<a href="#demande" class="btn-primary">\1{t["cta"]}', s, count=1)
        if "/hero-lead.js" not in s:
            s = s.replace('<script src="/chatbot.js', '<script src="/hero-lead.js?v=1" defer></script>\n<script src="/chatbot.js', 1)
        open(p, "w", encoding="utf-8").write(s)
        print("updated", t["file"])


if __name__ == "__main__":
    main()
