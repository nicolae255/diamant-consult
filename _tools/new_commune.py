#!/usr/bin/env python3
"""Build a commune landing page (SEO + SEM) in French, Dutch and English from one JSON spec.

Usage:  python3 _tools/new_commune.py _tools/communes/<fr-slug>.json

Pages: FR /<fr-slug>/, NL /nl/<nl-slug>/, EN /en/<en-slug>/. The page shell (head, header, footer,
language buttons) comes from _tools/article_template_<lang>.html; the content sections are built here.
Contact is by e-mail request only (Web3Forms, like the contact page): no phone number on these pages.
Only sourced figures (Statbel) in "stats"; photos need their credit (author, licence, link).
After building, seo.py links the three versions (hreflang) and updates sitemap + llms.txt.
"""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.diamantconsult.com"
FORM_ACTION = "https://api.web3forms.com/submit"
FORM_KEY = "ac28f9a0-206e-48e7-a1b1-3e0f8be82cb9"
PREFIX = {"fr": "", "en": "en/", "nl": "nl/"}
BTN = {"fr": 0, "nl": 1, "en": 2}
esc = lambda s: html.escape(s, quote=True)

L = {
    "fr": dict(home="Accueil", locale="fr_BE", in_lang="fr-BE", type_label="Type de bien", house="Maison", apt="Appartement",
               address="Adresse du bien", address_ph="Rue, numéro", email="E-mail", message="Votre demande",
               message_ph="Votre projet, vos questions, votre calendrier…", send="Envoyer ma demande",
               form_note="Premier rendez-vous gratuit et sans engagement · Réponse par e-mail",
               thanks="Merci, votre demande est bien envoyée. Nous vous répondons par e-mail.",
               steps_title="Un service tout-en-un, de la mise en vente à l'acte.", sales_title="Nos ventes récentes, près de chez vous",
               faq_title="Questions fréquentes", near_title="Nous vendons aussi dans d'autres communes",
               cta_btn="Envoyer une demande", stat_house="Prix médian maison", stat_apt="Prix médian appartement",
               stat_trend="Évolution sur 1 an", stat_region="Médiane Région bruxelloise", sales_n="ventes",
               trend_sub="maisons · appartements", region_sub="maisons · appartements", photo="Photo", mail_subject="Demande — page commune", few="trop peu de ventes pour une médiane"),
    "en": dict(home="Home", locale="en_GB", in_lang="en", type_label="Property type", house="House", apt="Apartment",
               address="Property address", address_ph="Street, number", email="Email", message="Your request",
               message_ph="Your project, your questions, your timing…", send="Send my request",
               form_note="Free first meeting, no obligation · We reply by email",
               thanks="Thank you, your request has been sent. We will reply by email.",
               steps_title="An all-in-one service, from listing to deed.", sales_title="Our recent sales, close to you",
               faq_title="Frequently asked questions", near_title="We also sell in other municipalities",
               cta_btn="Send a request", stat_house="Median house price", stat_apt="Median apartment price",
               stat_trend="1-year change", stat_region="Brussels Region median", sales_n="sales",
               trend_sub="houses · apartments", region_sub="houses · apartments", photo="Photo", mail_subject="Request — commune page", few="too few sales for a median"),
    "nl": dict(home="Startpagina", locale="nl_BE", in_lang="nl-BE", type_label="Type woning", house="Huis", apt="Appartement",
               address="Adres van de woning", address_ph="Straat, nummer", email="E-mail", message="Uw vraag",
               message_ph="Uw project, uw vragen, uw timing…", send="Verstuur mijn aanvraag",
               form_note="Gratis eerste afspraak, vrijblijvend · Antwoord per e-mail",
               thanks="Bedankt, uw aanvraag is verstuurd. We antwoorden per e-mail.",
               steps_title="Een alles-in-één dienst, van verkoop tot akte.", sales_title="Onze recente verkopen, bij u in de buurt",
               faq_title="Veelgestelde vragen", near_title="We verkopen ook in andere gemeenten",
               cta_btn="Verstuur een aanvraag", stat_house="Mediaanprijs huis", stat_apt="Mediaanprijs appartement",
               stat_trend="Evolutie op 1 jaar", stat_region="Mediaan Brussels Gewest", sales_n="verkopen",
               trend_sub="huizen · appartementen", region_sub="huizen · appartementen", photo="Foto", mail_subject="Aanvraag — gemeentepagina", few="te weinig verkopen voor een mediaan"),
}
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'

CSS = """<style>
.cm-wrap{max-width:1200px;margin:0 auto;padding-left:clamp(1rem,4vw,2.5rem);padding-right:clamp(1rem,4vw,2.5rem)}
.cm-sec{padding-block:clamp(3.5rem,7vw,5.5rem)}
.cm-soft{background:var(--bg-soft)}
.cm-dark{background:var(--ink);color:var(--bg)}
.cm-row{display:flex;flex-wrap:wrap;gap:clamp(2rem,5vw,3.5rem);align-items:center}
.cm-col{flex:1 1 420px;min-width:0;display:flex;flex-direction:column;gap:1rem}
.cm-h1{font-family:var(--display);font-weight:700;font-size:clamp(2.4rem,5.5vw,4rem);line-height:1.02;letter-spacing:-0.03em;margin:0}
.cm-h2{font-family:var(--display);font-weight:700;font-size:clamp(1.8rem,3.4vw,2.5rem);line-height:1.1;letter-spacing:-0.02em;margin:0}
.cm-lead{font-size:1.2rem;line-height:1.5;margin:0;max-width:36rem}
.cm-p{margin:0;line-height:1.65;color:var(--ink-2,#2a2a28)}
.cm-dark .cm-p{color:#CFCBC2}
.cm-crumb{font-size:.85rem;color:var(--mute);margin-bottom:1.5rem}
.cm-crumb a{color:inherit}
.cm-checks{list-style:none;margin:.5rem 0 0;padding:0;display:flex;flex-direction:column;gap:.6rem}
.cm-checks li{display:flex;gap:.6rem;align-items:flex-start}
.cm-checks svg{flex-shrink:0;margin-top:.2rem}
.cm-form{flex:1 1 380px;min-width:0;background:#fff;border:1px solid var(--line);border-radius:20px;padding:1.75rem;display:flex;flex-direction:column;gap:1rem;box-sizing:border-box}
.cm-form h2{font-family:var(--display);font-size:1.6rem;margin:0}
.cm-form label{display:flex;flex-direction:column;gap:.35rem;font-size:.9rem;font-weight:600}
.cm-form input,.cm-form textarea{font:inherit;font-weight:400;padding:.8rem .9rem;border:1px solid var(--line);border-radius:12px;background:#fff}
.cm-form textarea{min-height:110px;resize:vertical}
.cm-radios{display:flex;gap:.6rem;flex-wrap:wrap;border:0;padding:0;margin:0}
.cm-radios legend{font-size:.9rem;font-weight:600;margin-bottom:.35rem}
.cm-radios label{flex:1 1 120px;flex-direction:row;align-items:center;gap:.5rem;border:1px solid var(--line);border-radius:12px;padding:.75rem .9rem;font-weight:500}
.cm-btn{font:inherit;font-weight:600;font-size:1rem;padding:1rem 1.4rem;border:0;border-radius:999px;background:var(--ink);color:var(--bg);cursor:pointer;text-decoration:none;display:inline-flex;justify-content:center}
.cm-btn.light{background:var(--bg);color:var(--ink)}
.cm-note{margin:0;font-size:.85rem;color:var(--mute);text-align:center}
.cm-thanks{background:#E7F3EA;color:#1F5130;border-radius:12px;padding:.9rem 1rem;font-weight:600}
.cm-trust{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.25rem;padding-block:1.75rem;border-bottom:1px solid var(--line)}
.cm-trust strong{display:block;font-family:var(--display);font-size:1.6rem}
.cm-trust span{font-size:.9rem;color:var(--mute)}
.cm-fig{margin:0;display:flex;flex-direction:column;gap:.5rem}
.cm-fig img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:20px;display:block}
.cm-fig figcaption{font-size:.75rem;color:var(--mute)}
.cm-fig figcaption a{color:inherit}
.cm-price{flex:1 1 420px;min-width:0;background:#1C1C1B;border:1px solid #3A3936;border-radius:20px;padding:1.75rem;box-sizing:border-box}
.cm-price .lbl{font-size:.8rem;letter-spacing:.12em;color:#CFCBC2;margin-bottom:1rem}
.cm-price .ln{display:flex;justify-content:space-between;gap:1rem;padding:.85rem 0;border-bottom:1px solid #3A3936}
.cm-price .ln:last-of-type{border-bottom:0}
.cm-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}
.cm-steps li{border:1px solid var(--line);border-radius:16px;padding:1.4rem}
.cm-steps .n{font-size:.8rem;color:var(--mute);font-weight:600}
.cm-steps h3{margin:.4rem 0 .3rem;font-size:1.15rem}
.cm-steps p{margin:0;font-size:.95rem;color:var(--mute)}
.cm-chips{display:flex;flex-wrap:wrap;gap:.5rem}
.cm-chips span,.cm-chips a{padding:.5rem .9rem;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:.9rem;color:var(--ink);text-decoration:none}
.cm-stats{flex:1 1 360px;min-width:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;align-content:start}
.cm-stat{background:#fff;border-radius:16px;padding:1.1rem}
.cm-stat .k{font-size:.8rem;color:var(--mute)}
.cm-stat .v{font-family:var(--display);font-size:1.5rem;font-weight:700}
.cm-stat .s{font-size:.8rem;color:var(--mute)}
.cm-src{grid-column:1/-1;margin:0;font-size:.8rem;color:var(--mute)}
.cm-src a{color:inherit}
.cm-sales{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}
.cm-sale{border:1px solid var(--line);border-radius:16px;overflow:hidden}
.cm-sale img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block}
.cm-sale div{padding:1rem 1.1rem}
.cm-sale .m{font-size:.8rem;color:var(--mute)}
.cm-sale .t{font-weight:600;font-size:1.05rem}
.cm-faq details{border-bottom:1px solid var(--line);padding:1rem 0}
.cm-faq summary{font-weight:600;font-size:1.1rem;cursor:pointer}
.cm-faq p{margin:.6rem 0 0;line-height:1.6}
.cm-cta{background:var(--ink);color:var(--bg);border-radius:28px;padding:clamp(2rem,5vw,3.5rem);display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;justify-content:space-between}
</style>"""


def esc_nb(s):
    return esc(s).replace(" ", "&nbsp;")


def build(spec, lang):
    b, t = spec[lang], L[lang]
    pre = PREFIX[lang]; url = f"{BASE}/{pre}{b['slug']}/"
    up = "../" if lang == "fr" else "../../"
    name = b["commune"]
    name = name[0].upper() + name[1:]
    st = spec["stats"]
    # ---------- hero + form
    checks = "".join(f"<li>{CHECK}<span>{esc_nb(x)}</span></li>" for x in b["checks"])
    form = f'''<form class="cm-form" id="demande" action="{FORM_ACTION}" method="POST">
        <h2>{esc_nb(b["form_title"])}</h2>
        <p class="cm-thanks" id="cm-thanks" hidden>{esc(t["thanks"])}</p>
        <input type="hidden" name="access_key" value="{FORM_KEY}">
        <input type="hidden" name="subject" value="{esc(t["mail_subject"])} · {esc(name)}">
        <input type="hidden" name="from_name" value="Site Diamant Consult">
        <input type="hidden" name="redirect" value="{url}?merci=1#demande">
        <input type="hidden" name="commune" value="{esc(name)}">
        <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
        <fieldset class="cm-radios"><legend>{t["type_label"]}</legend>
          <label><input type="radio" name="type" value="{t["house"]}" checked> {t["house"]}</label>
          <label><input type="radio" name="type" value="{t["apt"]}"> {t["apt"]}</label>
        </fieldset>
        <label>{t["address"]}<input type="text" name="adresse" placeholder="{esc(t["address_ph"])} · {esc(spec["postcode"])} {esc(name)}"></label>
        <label>{t["email"]}<input type="email" name="email" required autocomplete="email"></label>
        <label>{t["message"]}<textarea name="message" placeholder="{esc(t["message_ph"])}"></textarea></label>
        <button type="submit" class="cm-btn">{t["send"]}</button>
        <p class="cm-note">{esc(t["form_note"])}</p>
      </form>'''
    hero = f'''<section class="cm-soft" style="padding-top: 7rem">
  <div class="cm-wrap" style="padding-bottom: clamp(3rem,6vw,4.5rem)">
    <nav class="cm-crumb" aria-label="Breadcrumb"><a href="../">{t["home"]}</a> › {esc(name)}</nav>
    <div class="cm-row" style="align-items:flex-start">
      <div class="cm-col" style="flex:999 1 480px">
        <h1 class="cm-h1">{esc_nb(b["h1"])}</h1>
        <p class="cm-lead">{b["hero_sub"]}</p>
        <ul class="cm-checks">{checks}</ul>
      </div>
      {form}
    </div>
  </div>
</section>'''
    trust = '<section><div class="cm-wrap"><div class="cm-trust">' + "".join(
        f"<div><strong>{esc_nb(a)}</strong><span>{esc_nb(c)}</span></div>" for a, c in b["trust"]) + "</div></div></section>"
    # ---------- house / apartment
    def fig(key):
        p = spec["photos"].get(key)
        if not p:
            return ""
        return (f'<figure class="cm-fig"><img src="{up}{p["src"]}" alt="{esc(p["alt"][lang])}" loading="lazy" width="1400" height="1050">'
                f'<figcaption>{esc(p["caption"][lang])} · {t["photo"]} {esc(p["author"])}, <a href="{p["url"]}" target="_blank" rel="noopener">Wikimedia Commons</a>, {p["license"]}</figcaption></figure>')
    def paras(lst): return "".join(f'<p class="cm-p">{x}</p>' for x in lst)
    hv = f'''<section class="cm-sec"><div class="cm-wrap" style="display:flex;flex-direction:column;gap:clamp(3rem,6vw,4.5rem)">
  <div class="cm-row"><div class="cm-col"><h2 class="cm-h2">{esc_nb(b["house_h2"])}</h2>{paras(b["house_p"])}<a href="#demande" style="font-weight:600;color:var(--ink)">{esc(b["house_link"])} →</a></div>{('<div class="cm-col">' + fig("house") + '</div>') if fig("house") else ''}</div>
  <div class="cm-row" style="flex-wrap:wrap-reverse">{('<div class="cm-col">' + fig("apartment") + '</div>') if fig("apartment") else ''}<div class="cm-col"><h2 class="cm-h2">{esc_nb(b["apt_h2"])}</h2>{paras(b["apt_p"])}<a href="#demande" style="font-weight:600;color:var(--ink)">{esc(b["apt_link"])} →</a></div></div>
</div></section>'''
    # ---------- price block
    pr = b["price"]
    price = f'''<section class="cm-sec cm-dark"><div class="cm-wrap"><div class="cm-row">
  <div class="cm-col"><h2 class="cm-h2">{esc_nb(pr["h2"])}</h2><p class="cm-p">{esc_nb(pr["p"])}</p></div>
  <div class="cm-price"><div class="lbl">{esc_nb(pr["example"])}</div>
    <div class="ln"><span>{esc_nb(pr["ours"][0])}</span><strong style="font-size:1.2rem">{esc_nb(pr["ours"][1])}</strong></div>
    <div class="ln" style="color:#CFCBC2"><span>{esc_nb(pr["other"][0])}</span><span style="font-size:1.2rem">{esc_nb(pr["other"][1])}</span></div>
    <div class="ln"><span>{esc_nb(pr["diff"][0])}</span><strong style="font-size:1.4rem">{esc_nb(pr["diff"][1])}</strong></div>
    <p style="margin:.8rem 0 0;font-size:.8rem;color:#CFCBC2">{esc_nb(pr["note"])}</p></div>
</div></div></section>'''
    # ---------- steps
    steps = "".join(f'<li><div class="n">{i+1:02d}</div><h3>{esc(h)}</h3><p>{esc_nb(p)}</p></li>' for i, (h, p) in enumerate(b["steps"]))
    steps_sec = f'<section class="cm-sec"><div class="cm-wrap" style="display:flex;flex-direction:column;gap:2rem"><h2 class="cm-h2" style="max-width:40rem">{esc(t["steps_title"])}</h2><ol class="cm-steps">{steps}</ol></div></section>'
    # ---------- local market
    def money(v):
        if v is None: return "—"
        return {"fr": f"{v:,} €".replace(",", " "), "en": f"€{v:,}", "nl": f"€ {v:,}".replace(",", ".")}[lang]
    def pct(v):
        if v is None: return "—"
        s = f"{v:+.1f}%" if lang == "en" else f"{v:+.1f} %".replace(".", ",")
        return s.replace("-", "−")
    chips = "".join(f"<span>{esc(q)}</span>" for q in b["quartiers"])
    stats = f'''<div class="cm-stats">
      <div class="cm-stat"><div class="k">{t["stat_house"]}</div><div class="v">{esc_nb(money(st["house"]))}</div><div class="s">{(str(st["house_n"]) + " " + t["sales_n"]) if st["house"] else t["few"]}</div></div>
      <div class="cm-stat"><div class="k">{t["stat_apt"]}</div><div class="v">{esc_nb(money(st["apt"]))}</div><div class="s">{(str(st["apt_n"]) + " " + t["sales_n"]) if st["apt"] else t["few"]}</div></div>
      <div class="cm-stat"><div class="k">{t["stat_trend"]}</div>{(f'<div class="v">{esc_nb(pct(st["house_trend"]))} · {esc_nb(pct(st["apt_trend"]))}</div><div class="s">{t["trend_sub"]}</div>') if st["house_trend"] is not None else (f'<div class="v">{esc_nb(pct(st["apt_trend"]))}</div><div class="s">{t["trend_sub"].split(" · ")[1]}</div>')}</div>
      <div class="cm-stat"><div class="k">{st.get("region_label", {}).get(lang, t["stat_region"])}</div><div class="v">{esc_nb(money(st["region_house"]))}</div><div class="s">{t["region_sub"].split(" · ")[1]} {esc_nb(money(st["region_apt"]))}</div></div>
      <p class="cm-src">{b["stats_source"]}</p></div>'''
    market = f'''<section class="cm-sec cm-soft"><div class="cm-wrap"><div class="cm-row" style="align-items:flex-start">
  <div class="cm-col"><h2 class="cm-h2">{esc_nb(b["market_h2"])}</h2>{paras(b["market_p"])}{('<div class="cm-chips">' + chips + '</div>') if chips else ''}{fig("market")}</div>
  {stats}
</div></div></section>'''
    # ---------- sales
    cname = lambda s: s["commune"][lang] if isinstance(s["commune"], dict) else s["commune"]
    sales = "".join(f'<div class="cm-sale"><img src="{up}{s["img"]}" alt="{esc(s["title"][lang])} · {esc(cname(s))}" loading="lazy"><div><div class="m">{esc(cname(s))} · {esc(s["meta"][lang])}</div><div class="t">{esc(s["title"][lang])}</div></div></div>' for s in spec["sales"])
    sales_sec = f'<section class="cm-sec"><div class="cm-wrap" style="display:flex;flex-direction:column;gap:1.75rem"><h2 class="cm-h2">{esc(t["sales_title"])}</h2><div class="cm-sales">{sales}</div></div></section>'
    # ---------- FAQ
    faq = "".join(f'<details{" open" if i < 3 else ""}><summary>{esc_nb(q)}</summary><p>{esc_nb(a)}</p></details>' for i, (q, a) in enumerate(b["faq"]))
    faq_sec = f'<section class="cm-sec" style="border-top:1px solid var(--line)"><div class="cm-wrap cm-faq" style="max-width:900px"><h2 class="cm-h2" style="margin-bottom:1rem">{esc(t["faq_title"])}</h2>{faq}</div></section>'
    # ---------- nearby
    near = "".join((f'<a href="{up}{pre}{n["href"]}">{esc(n["name"])}</a>' if n.get("href") else f"<span>{esc(n['name'])}</span>") for n in b["nearby"])
    near_sec = f'<section class="cm-soft" style="padding-block:3rem"><div class="cm-wrap" style="display:flex;flex-direction:column;gap:1rem"><h2 style="margin:0;font-size:1.3rem">{esc(t["near_title"])}</h2><div class="cm-chips">{near}</div></div></section>'
    cta = f'''<section class="cm-sec"><div class="cm-wrap"><div class="cm-cta">
  <div style="flex:1 1 420px;min-width:0"><h2 class="cm-h2" style="margin-bottom:.6rem">{esc_nb(b["cta_h2"])}</h2><p class="cm-p" style="color:#CFCBC2">{esc_nb(b["cta_p"])}</p></div>
  <a href="#demande" class="cm-btn light">{t["cta_btn"]}</a></div></div></section>'''
    thanks_js = '<script>if(/[?&]merci=1/.test(location.search)){var t=document.getElementById("cm-thanks");if(t)t.hidden=false;}</script>'
    content = "\n".join([CSS, hero, trust, hv, price, steps_sec, market, sales_sec, faq_sec, near_sec, cta, thanks_js])

    # ---------- page shell from the article template
    tpl = open(os.path.join(ROOT, "_tools", f"article_template_{lang}.html"), encoding="utf-8").read()
    start = tpl.index('<section class="page-hero">'); end = tpl.index("<footer")
    shell = tpl[:start] + "{{CONTENT}}\n\n" + tpl[end:]
    others = []
    for ol in ("fr", "nl", "en"):
        if ol != lang:
            others.append(f"  lb[{BTN[ol]}].onclick = () => location.href = '/{PREFIX[ol]}{spec[ol]['slug']}/';")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "RealEstateAgent", "@id": BASE + "/#organization", "name": "Diamant Consult Immobilier",
         "alternateName": "Diamant Consult", "url": BASE + "/", "email": "borremans.helpinfo@gmail.com",
         "image": BASE + "/img/og-default.jpg", "priceRange": "€",
         "address": {"@type": "PostalAddress", "streetAddress": "Avenue du Diamant 138", "addressLocality": "Schaerbeek",
                     "postalCode": "1030", "addressRegion": "Bruxelles", "addressCountry": "BE"},
         "areaServed": {"@type": "City", "name": name}},
        {"@type": "WebPage", "url": url, "name": b["seo_title"].split(" | ")[0], "description": b["description"],
         "inLanguage": t["in_lang"], "about": {"@id": BASE + "/#organization"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"], "item": f"{BASE}/{pre}"},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in b["faq"]]},
    ]}
    rep = {"{{SEO_TITLE}}": esc(b["seo_title"]), "{{DESCRIPTION}}": esc(b["description"]), "{{URL}}": url,
           "{{OG_TITLE}}": esc(b["seo_title"]), "{{OG_IMAGE}}": f"{BASE}/{spec['photos']['house']['src']}",
           "{{OG_LOCALE}}": t["locale"], "{{JSONLD}}": json.dumps(ld, ensure_ascii=False, indent=2),
           "{{LANG_JS}}": "\n".join(others), "{{CONTENT}}": content}
    page = shell
    for k, v in rep.items():
        page = page.replace(k, v)
    page = page.replace('<meta property="og:type" content="article" />', '<meta property="og:type" content="website" />')
    page = page.replace('class="active">Blog', '>Blog')
    if "{{" in page:
        raise SystemExit(f"[{lang}] unreplaced: {re.findall(r'{{[A-Z_]+}}', page)}")
    for m in re.findall(r'ld\+json">\s*(.*?)\s*</script>', page, re.S):
        json.loads(m)
    if re.search(r'tel:|\+32 ?4', page):
        raise SystemExit(f"[{lang}] phone number found: contact must stay e-mail only")
    return page


def main(path):
    spec = json.load(open(path, encoding="utf-8"))
    pages = {l: build(spec, l) for l in ("fr", "en", "nl")}
    for l, page in pages.items():
        d = os.path.join(ROOT, PREFIX[l], spec[l]["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
        print(f"  [{l}] /{PREFIX[l]}{spec[l]['slug']}/")
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "seo.py")], check=True, stdout=subprocess.DEVNULL)
    print("  hreflang + sitemap + llms.txt updated")


if __name__ == "__main__":
    main(sys.argv[1])
