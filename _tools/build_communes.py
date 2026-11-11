#!/usr/bin/env python3
"""Generate the commune specs (_tools/communes/<fr-slug>.json) for the Brussels communes, then build them.

Usage:  python3 _tools/build_communes.py            # all communes except the hand-written Woluwe-Saint-Lambert
        python3 _tools/build_communes.py uccle      # one commune

Data: _tools/communes/_data.json (Statbel medians S1 2025/S1 2026, neighbourhoods and photo credits from
Wikimedia Commons). Every figure in the texts is computed from that data; nothing else is claimed.
The service texts (checks, steps, price block, FAQ) are reused from the Woluwe-Saint-Lambert spec.
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "_tools", "communes")
NB = " "

# key: (FR name, NL name, EN name, FR slug part, NL slug part, EN slug part, postcode, short FR name for titles)
C = {
 "anderlecht": ("Anderlecht", "Anderlecht", "Anderlecht", "anderlecht", "anderlecht", "anderlecht", "1070", "Anderlecht"),
 "auderghem": ("Auderghem", "Oudergem", "Auderghem", "auderghem", "oudergem", "auderghem", "1160", "Auderghem"),
 "berchem-sainte-agathe": ("Berchem-Sainte-Agathe", "Sint-Agatha-Berchem", "Berchem-Sainte-Agathe", "berchem-sainte-agathe", "sint-agatha-berchem", "berchem-sainte-agathe", "1082", "Berchem-Ste-Agathe"),
 "bruxelles-ville": ("Bruxelles-Ville", "Brussel-Stad", "the City of Brussels", "bruxelles-ville", "brussel-stad", "brussels-city", "1000", "Bruxelles-Ville"),
 "etterbeek": ("Etterbeek", "Etterbeek", "Etterbeek", "etterbeek", "etterbeek", "etterbeek", "1040", "Etterbeek"),
 "evere": ("Evere", "Evere", "Evere", "evere", "evere", "evere", "1140", "Evere"),
 "forest": ("Forest", "Vorst", "Forest", "forest", "vorst", "forest", "1190", "Forest"),
 "ganshoren": ("Ganshoren", "Ganshoren", "Ganshoren", "ganshoren", "ganshoren", "ganshoren", "1083", "Ganshoren"),
 "ixelles": ("Ixelles", "Elsene", "Ixelles", "ixelles", "elsene", "ixelles", "1050", "Ixelles"),
 "jette": ("Jette", "Jette", "Jette", "jette", "jette", "jette", "1090", "Jette"),
 "koekelberg": ("Koekelberg", "Koekelberg", "Koekelberg", "koekelberg", "koekelberg", "koekelberg", "1081", "Koekelberg"),
 "molenbeek-saint-jean": ("Molenbeek-Saint-Jean", "Sint-Jans-Molenbeek", "Molenbeek-Saint-Jean", "molenbeek-saint-jean", "sint-jans-molenbeek", "molenbeek-saint-jean", "1080", "Molenbeek"),
 "saint-gilles": ("Saint-Gilles", "Sint-Gillis", "Saint-Gilles", "saint-gilles", "sint-gillis", "saint-gilles", "1060", "Saint-Gilles"),
 "saint-josse-ten-noode": ("Saint-Josse-ten-Noode", "Sint-Joost-ten-Node", "Saint-Josse-ten-Noode", "saint-josse-ten-noode", "sint-joost-ten-node", "saint-josse-ten-noode", "1210", "Saint-Josse"),
 "schaerbeek": ("Schaerbeek", "Schaarbeek", "Schaerbeek", "schaerbeek", "schaarbeek", "schaerbeek", "1030", "Schaerbeek"),
 "uccle": ("Uccle", "Ukkel", "Uccle", "uccle", "ukkel", "uccle", "1180", "Uccle"),
 "watermael-boitsfort": ("Watermael-Boitsfort", "Watermaal-Bosvoorde", "Watermael-Boitsfort", "watermael-boitsfort", "watermaal-bosvoorde", "watermael-boitsfort", "1170", "Watermael-Boitsfort"),
 "woluwe-saint-lambert": ("Woluwe-Saint-Lambert", "Sint-Lambrechts-Woluwe", "Woluwe-Saint-Lambert", "woluwe-saint-lambert", "sint-lambrechts-woluwe", "woluwe-saint-lambert", "1200", "Woluwe-St-Lambert"),
 "woluwe-saint-pierre": ("Woluwe-Saint-Pierre", "Sint-Pieters-Woluwe", "Woluwe-Saint-Pierre", "woluwe-saint-pierre", "sint-pieters-woluwe", "woluwe-saint-pierre", "1150", "Woluwe-St-Pierre"),
 "waterloo": ("Waterloo", "Waterloo", "Waterloo", "waterloo", "waterloo", "waterloo", "1410", "Waterloo"),
 "la-hulpe": ("La Hulpe", "Terhulpen", "La Hulpe", "la-hulpe", "terhulpen", "la-hulpe", "1310", "La Hulpe"),
 "wavre": ("Wavre", "Waver", "Wavre", "wavre", "waver", "wavre", "1300", "Wavre"),
 "rixensart": ("Rixensart", "Rixensart", "Rixensart", "rixensart", "rixensart", "rixensart", "1330", "Rixensart"),
}
NEAR = {
 "anderlecht": ["molenbeek-saint-jean", "forest", "saint-gilles", "berchem-sainte-agathe", "bruxelles-ville"],
 "auderghem": ["watermael-boitsfort", "woluwe-saint-pierre", "ixelles", "etterbeek", "uccle"],
 "berchem-sainte-agathe": ["ganshoren", "koekelberg", "molenbeek-saint-jean", "jette", "anderlecht"],
 "bruxelles-ville": ["saint-josse-ten-noode", "schaerbeek", "ixelles", "molenbeek-saint-jean", "saint-gilles"],
 "etterbeek": ["ixelles", "woluwe-saint-pierre", "woluwe-saint-lambert", "auderghem", "schaerbeek"],
 "evere": ["schaerbeek", "woluwe-saint-lambert", "bruxelles-ville", "etterbeek", "saint-josse-ten-noode"],
 "forest": ["saint-gilles", "uccle", "anderlecht", "ixelles", "watermael-boitsfort"],
 "ganshoren": ["jette", "koekelberg", "berchem-sainte-agathe", "molenbeek-saint-jean", "bruxelles-ville"],
 "ixelles": ["etterbeek", "uccle", "saint-gilles", "bruxelles-ville", "watermael-boitsfort"],
 "jette": ["ganshoren", "koekelberg", "bruxelles-ville", "berchem-sainte-agathe", "molenbeek-saint-jean"],
 "koekelberg": ["jette", "ganshoren", "berchem-sainte-agathe", "molenbeek-saint-jean", "bruxelles-ville"],
 "molenbeek-saint-jean": ["koekelberg", "bruxelles-ville", "anderlecht", "berchem-sainte-agathe", "jette"],
 "saint-gilles": ["ixelles", "forest", "anderlecht", "bruxelles-ville", "uccle"],
 "saint-josse-ten-noode": ["schaerbeek", "bruxelles-ville", "etterbeek", "evere", "ixelles"],
 "schaerbeek": ["saint-josse-ten-noode", "evere", "woluwe-saint-lambert", "etterbeek", "bruxelles-ville"],
 "uccle": ["ixelles", "forest", "watermael-boitsfort", "saint-gilles", "auderghem"],
 "watermael-boitsfort": ["auderghem", "uccle", "ixelles", "woluwe-saint-pierre", "forest"],
 "woluwe-saint-lambert": ["woluwe-saint-pierre", "schaerbeek", "evere", "etterbeek", "auderghem"],
 "woluwe-saint-pierre": ["woluwe-saint-lambert", "auderghem", "etterbeek", "watermael-boitsfort", "evere"],
 "waterloo": ["la-hulpe", "rixensart", "wavre", "uccle", "watermael-boitsfort"],
 "la-hulpe": ["rixensart", "waterloo", "wavre", "watermael-boitsfort", "auderghem"],
 "wavre": ["rixensart", "la-hulpe", "waterloo", "auderghem", "woluwe-saint-pierre"],
 "rixensart": ["la-hulpe", "wavre", "waterloo", "watermael-boitsfort", "auderghem"],
}
BW = {"fr": "vendre-maison-brabant-wallon/", "en": "selling-property-brabant-wallon/", "nl": "woning-verkopen-waals-brabant/"}
GUIDE = {  # existing articles to link from the market section
 "waterloo": BW, "la-hulpe": BW, "wavre": BW, "rixensart": BW,
 "schaerbeek": {"fr": "vendre-maison-schaerbeek/", "en": "sell-house-schaerbeek-brussels/", "nl": "woning-verkopen-schaarbeek/"},
 "ixelles": {"fr": "vendre-appartement-ixelles-uccle/", "en": "sell-apartment-ixelles-uccle/", "nl": "appartement-verkopen-elsene-ukkel/"},
 "uccle": {"fr": "vendre-appartement-ixelles-uccle/", "en": "sell-apartment-ixelles-uccle/", "nl": "appartement-verkopen-elsene-ukkel/"},
 "etterbeek": {"fr": "vendre-appartement-ixelles-uccle/", "en": "sell-apartment-ixelles-uccle/", "nl": "appartement-verkopen-elsene-ukkel/"},
}
HOODS_BXL = [{"fr": "Pentagone (centre-ville)", "nl": "Vijfhoek (centrum)", "en": "Pentagon (city centre)"}, {"fr": "Laeken", "nl": "Laken"},
             {"fr": "Neder-Over-Heembeek", "nl": "Neder-Over-Heembeek"}, {"fr": "Haren", "nl": "Haren"},
             {"fr": "Quartier européen", "nl": "Europese wijk", "en": "European Quarter"}, {"fr": "Quartier Louise", "nl": "Louizawijk", "en": "Louise quarter"}]
P = {  # real sales (projects page)
 "wb_apt": ("img/projets/appart-boitsfort.webp", "watermael-boitsfort", "gg", "apt"),
 "and_h1": ("img/projets/maison-anderlecht-conciliation.webp", "anderlecht", "vp", "house"),
 "and_h2": ("img/projets/maison-schaerbeek-1.webp", "anderlecht", "vp", "house"),
 "sch_apt": ("img/projets/maison-schaerbeek-3.webp", "schaerbeek", "gg", "apt"),
 "sch_at": ("img/projets/atelier-schaerbeek.webp", "schaerbeek", "vp", "atelier"),
 "sch_h": ("img/projets/maison-schaerbeek-2.webp", "schaerbeek", "vp", "house"),
 "ucc_apt": ("img/projets/appart-uccle.webp", "uccle", "vp", "apt"),
 "ett_apt": ("img/projets/appart-etterbeek.webp", "etterbeek", "vp", "apt"),
 "haren": ("img/projets/maison-haren.webp", "haren", "gg", "house"),
 "wsl_apt": ("img/projets/appart-woluwe-lambert-vp.webp", "woluwe-saint-lambert", "vp", "apt"),
 "wsl_com": ("img/projets/commerce-woluwe.webp", "woluwe-saint-lambert", "gg", "commerce"),
 "rix": ("img/projets/maison-rixensart.webp", "rixensart", "gg", "plot"),
}
SALES = {
 "anderlecht": ["and_h1", "and_h2"], "schaerbeek": ["sch_apt", "sch_at", "sch_h"], "uccle": ["ucc_apt", "wb_apt"],
 "etterbeek": ["ett_apt", "wsl_apt"], "bruxelles-ville": ["haren", "sch_apt"], "watermael-boitsfort": ["wb_apt", "ucc_apt"],
 "woluwe-saint-pierre": ["wsl_apt", "wsl_com"], "evere": ["sch_apt", "sch_h"], "saint-josse-ten-noode": ["sch_apt", "sch_at"],
 "ixelles": ["ett_apt", "ucc_apt"], "forest": ["ucc_apt", "and_h1"], "saint-gilles": ["ucc_apt", "and_h1"],
 "auderghem": ["wb_apt", "wsl_apt"], "molenbeek-saint-jean": ["and_h1", "haren"], "koekelberg": ["and_h1", "haren"],
 "berchem-sainte-agathe": ["and_h1", "and_h2"], "ganshoren": ["haren", "and_h1"], "jette": ["haren", "and_h1"],
 "rixensart": ["rix", "wb_apt"], "la-hulpe": ["rix", "wb_apt"], "waterloo": ["rix", "ucc_apt"], "wavre": ["rix", "wb_apt"],
}
MODE = {"vp": {"fr": "Conclu · Vente publique", "en": "Sold · Public auction", "nl": "Verkocht · Openbare verkoop"},
        "gg": {"fr": "Conclu · Gré à gré", "en": "Sold · Private sale", "nl": "Verkocht · Onderhandse verkoop"}}
KIND = {"apt": {"fr": "Appartement", "en": "Apartment", "nl": "Appartement"}, "house": {"fr": "Maison", "en": "House", "nl": "Woning"},
        "atelier": {"fr": "Atelier + habitation", "en": "Workshop + home", "nl": "Atelier + woning"},
        "commerce": {"fr": "Commerce + habitation", "en": "Shop + home", "nl": "Handelspand + woning"},
        "plot": {"fr": "Maison + terrain à bâtir", "en": "House + building plot", "nl": "Woning + bouwgrond"}}
CAP = {  # photo captions: role -> per commune override, else town hall
 "main": {"auderghem": ("Prieuré du Rouge-Cloître", "Rouge-Cloître priory", "Rood Klooster"),
          "bruxelles-ville": ("Hôtel de Ville, Grand-Place", "City Hall, Grand-Place", "Stadhuis, Grote Markt"),
          "evere": ("Rue à Evere", "Street in Evere", "Straat in Evere"),
          "ganshoren": ("Marais de Ganshoren", "Ganshoren marsh", "Moeras van Ganshoren"),
          "waterloo": ("Église Saint-Joseph", "Saint Joseph's Church", "Sint-Jozefskerk"),
          "la-hulpe": ("Château de La Hulpe", "La Hulpe castle", "Kasteel van Terhulpen"),
          "wavre": ("Église Saint-Jean-Baptiste", "St John the Baptist's Church", "Sint-Jan-de-Doperkerk"),
          "rixensart": ("Château de Rixensart", "Rixensart castle", "Kasteel van Rixensart")},
 "street": {"anderlecht": ("Rue Walcourt", "Rue Walcourt", "Walcourtstraat"), "auderghem": ("Avenue Théo Vanpé", "Avenue Théo Vanpé", "Théo Vanpélaan"),
            "schaerbeek": ("Avenue Maréchal Foch", "Avenue Maréchal Foch", "Maarschalk Fochlaan"),
            "woluwe-saint-pierre": ("Clos du Manoir", "Clos du Manoir", "Burchtgaarde"),
            "rixensart": ("Lac de Genval", "Lake Genval", "Meer van Genval")},
}
LI = {"fr": 0, "en": 1, "nl": 2}


def money(v, l):
    if v is None: return {"fr": "n.d.", "en": "n/a", "nl": "n.b."}[l]
    if l == "fr": return f"{v:,}".replace(",", NB) + NB + "€"
    if l == "en": return f"€{v:,}"
    return "€" + NB + f"{v:,}".replace(",", ".")


def pct(v, l):
    s = f"{v:+.1f}%" if l == "en" else f"{v:+.1f}{NB}%".replace(".", ",") if l == "fr" else f"{v:+.1f}%".replace(".", ",")
    return s.replace("-", "−")


def build_spec(k, data, base):
    fr, nl, en, sfr, snl, sen, pc, short = C[k]
    nm = {"fr": fr, "en": en, "nl": nl}
    s26 = data["communes"][k]["statbel"]["2026"]; s25 = data["communes"][k]["statbel"]["2025"]
    wal = data["communes"][k].get("region") == "wal"
    reg = data["region_wal"] if wal else data["region"]
    RN = ({"fr": "la médiane du Brabant wallon", "en": "the Walloon Brabant median", "nl": "de mediaan van Waals-Brabant"} if wal else
          {"fr": "la médiane régionale", "en": "the regional median", "nl": "de gewestelijke mediaan"})
    H, Hn, A, An = s26["house"], s26["house_n"] or 0, s26["apt"], s26["apt_n"]
    tr = lambda a, b: round((a / b - 1) * 100, 1) if a and b else None
    Ht, At = tr(H, s25["house"]), tr(A, s25["apt"])
    share = An / (An + Hn)
    k10 = round(share * 10)
    h23 = (s26["h23_n"] or 0) / Hn if Hn else 0
    h4 = (s26.get("h4_n") or 0) / Hn if Hn else 0
    bxl = [c for c in data["communes"] if data["communes"][c].get("region") != "wal"]
    ranks = sorted(bxl, key=lambda c: -(data["communes"][c]["statbel"]["2026"]["apt"] or 0))
    rank = ranks.index(k) + 1 if k in ranks else 10
    hoods = HOODS_BXL if k == "bruxelles-ville" else data["communes"][k]["hoods"]
    photos = {}
    ph = data["communes"][k]["photos"]
    for role, sect in (("main", "house"), ("street", "apartment")):
        if role in ph:
            p = ph[role]; cap = CAP[role].get(k)
            capt = {"fr": cap[0], "en": cap[1], "nl": cap[2]} if cap else {"fr": "Maison communale", "en": "Town hall", "nl": "Gemeentehuis"}
            where = {"fr": f"à {fr}", "en": f"in {en}", "nl": f"in {nl}"}
            photos[sect] = {"src": p["src"], "author": p["author"], "license": p["license"], "url": p["url"],
                            "alt": {l: f"{capt[l]} {where[l]}" for l in LI}, "caption": capt}
    stats = {"house": H, "house_n": Hn, "apt": A, "apt_n": An, "house_trend": Ht, "apt_trend": At,
             "region_house": reg["house"], "region_apt": reg["apt"], "period": "S1 2026"}
    if wal:
        stats["region_label"] = {"fr": "Médiane Brabant wallon", "en": "Walloon Brabant median", "nl": "Mediaan Waals-Brabant"}
    sales = []
    for sid in SALES.get(k, ["wb_apt", "and_h1"]):
        img, ck, mode, kind = P[sid]
        cn = {"fr": "Haren (Bruxelles-Ville)", "en": "Haren (City of Brussels)", "nl": "Haren (Brussel-Stad)"} if ck == "haren" else \
             {"fr": C[ck][0], "en": C[ck][2].replace("the City", "City"), "nl": C[ck][1]}
        sales.append({"img": img, "commune": cn, "meta": MODE[mode], "title": KIND[kind]})
    spec = {"postcode": pc, "stats": stats, "photos": photos, "sales": sales}

    def cmp(x, r, l):
        d = round((x / r - 1) * 100)
        if d >= 3: return {"fr": f"environ {d}{NB}% au-dessus de {RN['fr']}", "en": f"about {d}% above {RN['en']}", "nl": f"ongeveer {d}% boven {RN['nl']}"}[l]
        if d <= -3: return {"fr": f"environ {-d}{NB}% en dessous de {RN['fr']}", "en": f"about {-d}% below {RN['en']}", "nl": f"ongeveer {-d}% onder {RN['nl']}"}[l]
        return {"fr": f"proche de {RN['fr']}", "en": f"close to {RN['en']}", "nl": f"dicht bij {RN['nl']}"}[l]

    def word(t, l):
        if t is None: return None
        i = 0 if abs(t) < 2 else (1 if t > 0 else 2)
        return {"fr": ["stables", "en hausse", "en baisse"], "en": ["stable", "up", "down"], "nl": ["stabiel", "gestegen", "gedaald"]}[l][i]

    for l in ("fr", "en", "nl"):
        b = json.loads(json.dumps(base[l]))  # copy service texts
        sw = {"fr": ("attestation du sol", "informations sur l'état du sol"), "en": ("soil certificate", "soil information"), "nl": ("bodemattest", "informatie over de bodemtoestand")}[l]
        if wal:
            b["steps"] = [[h, t.replace(*sw)] for h, t in b["steps"]]
        X = nm[l]; Xc = X[0].upper() + X[1:]
        old = base[l]["commune"]
        for f in ("checks", "trust", "steps", "price", "house_p", "apt_p"):
            pass
        b["slug"] = {"fr": "vendre-" + sfr, "en": "sell-property-" + sen, "nl": "verkopen-" + snl}[l]
        b["commune"] = X
        title_x = {"fr": short, "en": X.replace("the City of Brussels", "the City of Brussels"), "nl": nl}[l]
        b["seo_title"] = {"fr": f"Vendre maison ou appartement à {title_x} | 2% HTVA",
                          "en": f"Sell your house or apartment in {title_x} | 2% excl. VAT",
                          "nl": f"Huis of appartement verkopen in {title_x} | 2% excl. btw"}[l]
        b["description"] = {"fr": f"Vendez votre maison ou appartement à {X} : 2% HTVA tout compris, premier rendez-vous gratuit, visites et négociation jusqu'à l'acte.",
                            "en": f"Sell your house or apartment in {X}: 2% excl. VAT, all-in, free first meeting, viewings and negotiation through to the notary deed.",
                            "nl": f"Verkoop uw huis of appartement in {X}: 2% excl. btw, alles inbegrepen, gratis eerste afspraak, bezoeken en onderhandeling tot aan de akte."}[l]
        b["h1"] = {"fr": f"Vendre votre bien à {X}.", "en": f"Sell your property in {X}.", "nl": f"Uw woning verkopen in {X}."}[l]
        b["house_h2"] = {"fr": f"Vendre votre maison à {X}", "en": f"Selling your house in {X}", "nl": f"Uw huis verkopen in {X}"}[l]
        b["apt_h2"] = {"fr": f"Vendre votre appartement à {X}", "en": f"Selling your apartment in {X}", "nl": f"Uw appartement verkopen in {X}"}[l]
        b["market_h2"] = {"fr": f"Le marché immobilier à {X} en 2026", "en": f"The {X} property market in 2026".replace("The the", "The"), "nl": f"De vastgoedmarkt in {X} in 2026"}[l]
        b["cta_h2"] = {"fr": f"Vous vendez à {X} ?", "en": f"Selling in {X}?", "nl": f"Verkoopt u in {X}?"}[l]
        # house paragraph 1
        if H:
            p1 = {"fr": f"Au 1er semestre 2026, le prix médian d'une maison à {X} était de <strong>{money(H,l)}</strong>, pour {Hn} ventes (Statbel).",
                  "en": f"In the first half of 2026, the median house price in {X} was <strong>{money(H,l)}</strong>, across {Hn} sales (Statbel).",
                  "nl": f"In het eerste semester van 2026 bedroeg de mediaanprijs van een huis in {X} <strong>{money(H,l)}</strong>, voor {Hn} verkopen (Statbel)."}[l]
            if h23 >= 0.9: p1 += {"fr": " Presque toutes sont des maisons mitoyennes ou semi-mitoyennes, à 2 ou 3 façades.", "en": " Almost all were terraced or semi-detached houses.", "nl": " Bijna allemaal rijwoningen of halfopen bebouwing."}[l]
            elif h23 >= 0.7: p1 += {"fr": " La grande majorité sont des maisons mitoyennes ou semi-mitoyennes.", "en": " Most were terraced or semi-detached houses.", "nl": " Vooral rijwoningen of halfopen bebouwing."}[l]
            elif h4 > 0.5: p1 += {"fr": " Plus de la moitié sont des maisons 4 façades.", "en": " More than half were detached houses.", "nl": " Meer dan de helft waren open bebouwing."}[l]
        else:
            p1 = {"fr": f"Les ventes de maisons sont rares à {X} : {Hn} au 1er semestre 2026, trop peu pour que Statbel publie un prix médian. Pour une maison, la fixation du prix repose d'autant plus sur les ventes comparables du quartier.",
                  "en": f"House sales are rare in {X}: {Hn} in the first half of 2026, too few for Statbel to publish a median price. For a house, setting the price relies even more on comparable sales in the neighbourhood.",
                  "nl": f"Huizen worden zelden verkocht in {X}: {Hn} in het eerste semester van 2026, te weinig voor een mediaanprijs van Statbel. Voor een huis steunt de prijsbepaling dus nog meer op vergelijkbare verkopen in de wijk."}[l]
        b["house_p"] = [p1, base[l]["house_p"][1].replace(*sw) if wal else base[l]["house_p"][1]]
        sp = ("most" if share >= 0.75 else "major" if share >= 0.5 else "minor")
        lead = {"fr": {"most": "Les appartements font l'essentiel du marché", "major": "Les appartements représentent la majorité des ventes", "minor": "Les appartements représentent une part plus réduite du marché"},
                "en": {"most": "Apartments make up most of the market", "major": "Apartments account for the majority of sales", "minor": "Apartments account for a smaller share of the market"},
                "nl": {"most": "Appartementen vormen het grootste deel van de markt", "major": "Appartementen zijn goed voor de meerderheid van de verkopen", "minor": "Appartementen vormen een kleiner deel van de markt"}}[l][sp]
        q1, q3 = s26["apt_q1"], s26["apt_q3"]
        b["apt_p"] = [{"fr": f"{lead} : {An} ventes au 1er semestre 2026, pour un prix médian de <strong>{money(A,l)}</strong>. La moitié de ces ventes se situe entre {money(q1,l)} et {money(q3,l)} (Statbel).",
                       "en": f"{lead}: {An} sales in the first half of 2026, with a median price of <strong>{money(A,l)}</strong>. Half of these sales were between {money(q1,l)} and {money(q3,l)} (Statbel).",
                       "nl": f"{lead}: {An} verkopen in het eerste semester van 2026, met een mediaanprijs van <strong>{money(A,l)}</strong>. De helft van die verkopen lag tussen {money(q1,l)} en {money(q3,l)} (Statbel)."}[l],
                      base[l]["apt_p"][1]]
        if not A:
            b["apt_p"][0] = {"fr": f"Les ventes d'appartements sont rares à {X} : {An} au 1er semestre 2026, trop peu pour que Statbel publie un prix médian. La fixation du prix repose donc d'autant plus sur les ventes comparables du quartier.",
                             "en": f"Apartment sales are rare in {X}: {An} in the first half of 2026, too few for Statbel to publish a median price. Setting the price therefore relies even more on comparable sales in the neighbourhood.",
                             "nl": f"Appartementen worden zelden verkocht in {X}: {An} in het eerste semester van 2026, te weinig voor een mediaanprijs van Statbel. De prijsbepaling steunt dus nog meer op vergelijkbare verkopen in de wijk."}[l]
        # market paragraphs
        if H and A:
            m1 = {"fr": f"Au 1er semestre 2026, le prix médian des maisons à {X} se situait {cmp(H,reg['house'],l)}, et celui des appartements {cmp(A,reg['apt'],l)} (Statbel).",
                  "en": f"In the first half of 2026, the median house price in {X} was {cmp(H,reg['house'],l)}, and the median apartment price {cmp(A,reg['apt'],l)} (Statbel).",
                  "nl": f"In het eerste semester van 2026 lag de mediaanprijs van huizen in {X} {cmp(H,reg['house'],l)}, en die van appartementen {cmp(A,reg['apt'],l)} (Statbel)."}[l]
        elif H:
            m1 = {"fr": f"Au 1er semestre 2026, le prix médian des maisons à {X} se situait {cmp(H,reg['house'],l)} (Statbel).",
                  "en": f"In the first half of 2026, the median house price in {X} was {cmp(H,reg['house'],l)} (Statbel).",
                  "nl": f"In het eerste semester van 2026 lag de mediaanprijs van huizen in {X} {cmp(H,reg['house'],l)} (Statbel)."}[l]
        else:
            m1 = {"fr": f"Au 1er semestre 2026, le prix médian des appartements à {X} se situait {cmp(A,reg['apt'],l)} (Statbel).",
                  "en": f"In the first half of 2026, the median apartment price in {X} was {cmp(A,reg['apt'],l)} (Statbel).",
                  "nl": f"In het eerste semester van 2026 lag de mediaanprijs van appartementen in {X} {cmp(A,reg['apt'],l)} (Statbel)."}[l]
        if rank <= 5: m1 += {"fr": f" {Xc} figure parmi les 5 communes bruxelloises où les appartements sont les plus chers.", "en": f" {Xc} is among the 5 Brussels municipalities with the most expensive apartments.", "nl": f" {Xc} hoort bij de 5 Brusselse gemeenten met de duurste appartementen."}[l]
        elif rank >= 15: m1 += {"fr": f" {Xc} figure parmi les 5 communes bruxelloises où les appartements sont les plus abordables.", "en": f" {Xc} is among the 5 Brussels municipalities with the most affordable apartments.", "nl": f" {Xc} hoort bij de 5 Brusselse gemeenten met de meest betaalbare appartementen."}[l]
        if share >= 0.75: m2 = {"fr": f"C'est avant tout un marché d'appartements : {k10} ventes sur 10.", "en": f"It is above all an apartment market: {k10} sales out of 10.", "nl": f"Het is vooral een appartementsmarkt: {k10} op 10 verkopen."}[l]
        elif share >= 0.5: m2 = {"fr": f"Sur l'ensemble des ventes, {k10} sur 10 concernent des appartements.", "en": f"Out of all sales, {k10} in 10 were apartments.", "nl": f"Van alle verkopen waren er {k10} op 10 appartementen."}[l]
        elif wal: m2 = {"fr": f"C'est avant tout un marché de maisons : {10-k10} ventes sur 10.", "en": f"It is above all a market for houses: {10-k10} sales out of 10.", "nl": f"Het is vooral een markt van huizen: {10-k10} op 10 verkopen."}[l]
        else: m2 = {"fr": f"Les maisons y pèsent plus qu'ailleurs : {10-k10} ventes sur 10.", "en": f"Houses account for more of the market than elsewhere: {10-k10} sales out of 10.", "nl": f"Huizen wegen hier zwaarder dan elders: {10-k10} op 10 verkopen."}[l]
        if Ht is not None and At is not None and word(Ht, l) == word(At, l):
            m2 += {"fr": f" Sur un an, les prix médians sont {word(Ht,l)} pour les maisons ({pct(Ht,l)}) comme pour les appartements ({pct(At,l)}).",
                   "en": f" Over one year, median prices are {word(Ht,l)} for both houses ({pct(Ht,l)}) and apartments ({pct(At,l)}).",
                   "nl": f" Op een jaar zijn de mediaanprijzen {word(Ht,l)} voor huizen ({pct(Ht,l)}) en ook voor appartementen ({pct(At,l)})."}[l]
        elif Ht is not None and At is not None:
            m2 += {"fr": f" Sur un an, les prix médians sont {word(Ht,l)} pour les maisons ({pct(Ht,l)}) et {word(At,l)} pour les appartements ({pct(At,l)}).",
                   "en": f" Over one year, median prices are {word(Ht,l)} for houses ({pct(Ht,l)}) and {word(At,l)} for apartments ({pct(At,l)}).",
                   "nl": f" Op een jaar zijn de mediaanprijzen {word(Ht,l)} voor huizen ({pct(Ht,l)}) en {word(At,l)} voor appartementen ({pct(At,l)})."}[l]
        elif Ht is not None:
            m2 += {"fr": f" Sur un an, le prix médian des maisons est {word(Ht,l)[:-1] if word(Ht,l).endswith('s') else word(Ht,l)} ({pct(Ht,l)}).",
                   "en": f" Over one year, the median house price is {word(Ht,l)} ({pct(Ht,l)}).",
                   "nl": f" Op een jaar is de mediaanprijs van huizen {word(Ht,l)} ({pct(Ht,l)})."}[l]
        elif At is not None:
            m2 += {"fr": f" Sur un an, le prix médian des appartements est {word(At,l)[:-1] if word(At,l).endswith('s') else word(At,l)} ({pct(At,l)}).",
                   "en": f" Over one year, the median apartment price is {word(At,l)} ({pct(At,l)}).",
                   "nl": f" Op een jaar is de mediaanprijs van appartementen {word(At,l)} ({pct(At,l)})."}[l]
        if Ht is not None and abs(Ht) >= 15:
            m2 += {"fr": " Une variation aussi forte s’explique en partie par le type de maisons vendues pendant le semestre.",
                   "en": " Such a large change also reflects which houses happened to sell during the semester.",
                   "nl": " Zo'n grote schommeling hangt ook af van welke huizen in dat semester verkocht werden."}[l]
        if H and Hn < 40:
            m2 += {"fr": f" Avec {Hn} ventes de maisons sur le semestre, cette médiane peut varier fortement d'un semestre à l'autre.",
                   "en": f" With {Hn} house sales over the semester, this median can vary sharply from one semester to the next.",
                   "nl": f" Met {Hn} verkochte huizen in het semester kan deze mediaan sterk schommelen van semester tot semester."}[l]
        if hoods:
            names = [h.get(l, h["fr"]) if l != "nl" else h["nl"] for h in hoods][:5]
            m2 += {"fr": f" Parmi ses quartiers : {', '.join(names)}.", "en": f" Its neighbourhoods include {', '.join(names)}.", "nl": f" Enkele wijken: {', '.join(names)}."}[l]
        mp = [m1, m2]
        if k in GUIDE:
            mp.append({"fr": f'<a href="../{GUIDE[k]["fr"]}">Lire aussi notre guide pour vendre à {X} →</a>',
                       "en": f'<a href="../{GUIDE[k]["en"]}">Read our guide to selling in {X} →</a>',
                       "nl": f'<a href="../{GUIDE[k]["nl"]}">Lees ook onze gids over verkopen in {X} →</a>'}[l])
        b["market_p"] = mp
        b["quartiers"] = [h.get(l, h["fr"]) if l != "nl" else h["nl"] for h in hoods]
        # FAQ: replace commune name, rewrite the value question
        faq = []
        for q, a in base[l]["faq"]:
            q = q.replace(old, X); a = a.replace(old, X)
            faq.append([q, a])
        if H and A:
            val = {"fr": f"À titre indicatif, au 1er semestre 2026, le prix médian était de {money(H,l)} pour une maison et de {money(A,l)} pour un appartement (Statbel).",
                   "en": f"As a guide, in the first half of 2026 the median price was {money(H,l)} for a house and {money(A,l)} for an apartment (Statbel).",
                   "nl": f"Ter indicatie: in het eerste semester van 2026 bedroeg de mediaanprijs {money(H,l)} voor een huis en {money(A,l)} voor een appartement (Statbel)."}[l]
        elif H:
            val = {"fr": f"À titre indicatif, au 1er semestre 2026, le prix médian d'une maison était de {money(H,l)} (Statbel) ; les ventes d'appartements étaient trop peu nombreuses pour une médiane.",
                   "en": f"As a guide, in the first half of 2026 the median house price was {money(H,l)} (Statbel); there were too few apartment sales for a median.",
                   "nl": f"Ter indicatie: in het eerste semester van 2026 bedroeg de mediaanprijs van een huis {money(H,l)} (Statbel); er waren te weinig verkopen van appartementen voor een mediaan."}[l]
        else:
            val = {"fr": f"À titre indicatif, au 1er semestre 2026, le prix médian d'un appartement était de {money(A,l)} (Statbel) ; les ventes de maisons étaient trop peu nombreuses pour une médiane.",
                   "en": f"As a guide, in the first half of 2026 the median apartment price was {money(A,l)} (Statbel); there were too few house sales for a median.",
                   "nl": f"Ter indicatie: in het eerste semester van 2026 bedroeg de mediaanprijs van een appartement {money(A,l)} (Statbel); er waren te weinig huisverkopen voor een mediaan."}[l]
        rest = {"fr": " Le prix de votre bien, nous le fixons avec vous lors du premier rendez-vous, à partir des ventes comparables du quartier, de son état et de son PEB.",
                "en": " We set the price of your property with you at the first meeting, based on comparable sales in the neighbourhood, its condition and its EPC.",
                "nl": " De prijs van uw woning bepalen we samen met u tijdens de eerste afspraak, op basis van vergelijkbare verkopen in de wijk, de staat en het EPB."}[l]
        faq[2][1] = (val + rest).replace(NB, " ")
        if wal:
            faq[5] = {"fr": ["Quels documents faut-il pour vendre en Wallonie ?", "Certificat PEB, informations sur l'état du sol, renseignements urbanistiques et titre de propriété ; pour un appartement, aussi les PV des 3 dernières assemblées générales, les décomptes de charges et le règlement de copropriété. Nous vous aidons à les rassembler."],
                      "en": ["Which documents do I need to sell in Wallonia?", "EPC certificate, soil information, planning information and title deed; for an apartment, also the minutes of the last 3 general meetings, the service charge statements and the co-ownership rules. We help you gather them."],
                      "nl": ["Welke documenten heb ik nodig om in Wallonië te verkopen?", "EPB-certificaat, informatie over de bodemtoestand, stedenbouwkundige inlichtingen en eigendomstitel; voor een appartement ook de notulen van de laatste 3 algemene vergaderingen, de afrekeningen van de lasten en het reglement van mede-eigendom. We helpen u ze te verzamelen."]}[l]
            faq.insert(3, {"fr": ["Quels droits d'enregistrement paie l'acheteur en Wallonie ?", "Depuis le 1er janvier 2025, 3 % pour l'achat d'une habitation propre et unique, au lieu de 12,5 % (wallonie.be). Ces droits sont payés par l'acheteur."],
                           "en": ["What registration duties does the buyer pay in Wallonia?", "Since 1 January 2025, 3% for the purchase of a sole own home, instead of 12.5% (wallonie.be). These duties are paid by the buyer."],
                           "nl": ["Welke registratierechten betaalt de koper in Wallonië?", "Sinds 1 januari 2025 3% voor de aankoop van een enige eigen woning, in plaats van 12,5% (wallonie.be). Die rechten betaalt de koper."]}[l])
        b["faq"] = faq
        b["nearby"] = [{"name": {"fr": C[n][0], "en": C[n][2].replace("the City", "City"), "nl": C[n][1]}[l],
                        "href": {"fr": "vendre-" + C[n][3], "en": "sell-property-" + C[n][5], "nl": "verkopen-" + C[n][4]}[l] + "/"} for n in NEAR[k]]
        spec[l] = b
    # hero/cta copy that names the commune
    return spec


def main(only=None):
    data = json.load(open(os.path.join(D, "_data.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(D, "vendre-woluwe-saint-lambert.json"), encoding="utf-8"))
    for k in C:
        if k == "woluwe-saint-lambert" or (only and k != only):
            continue
        spec = build_spec(k, data, base)
        path = os.path.join(D, spec["fr"]["slug"] + ".json")
        json.dump(spec, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        r = subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "new_commune.py"), path], capture_output=True, text=True)
        print(k, "OK" if r.returncode == 0 else "FAILED\n" + r.stderr[-800:])
    # keep Woluwe-Saint-Lambert's nearby links pointing at the commune pages
    for l in ("fr", "en", "nl"):
        base[l]["nearby"] = [{"name": {"fr": C[n][0], "en": C[n][2], "nl": C[n][1]}[l],
                              "href": {"fr": "vendre-" + C[n][3], "en": "sell-property-" + C[n][5], "nl": "verkopen-" + C[n][4]}[l] + "/"}
                             for n in NEAR["woluwe-saint-lambert"]]
    json.dump(base, open(os.path.join(D, "vendre-woluwe-saint-lambert.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "new_commune.py"), os.path.join(D, "vendre-woluwe-saint-lambert.json")], check=True, stdout=subprocess.DEVNULL)
    print("woluwe-saint-lambert nearby links updated")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
