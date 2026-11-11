#!/usr/bin/env python3
"""Adds (or refreshes) a "Sell in your municipality" block in every blog article (FR/EN/NL),
just before the FAQ. It links to the 23 commune landing pages; communes named in the article
come first. Internal links help Google and AI engines connect articles and commune pages.

Usage:  python3 _tools/commune_links.py        (idempotent; new_article.py runs it automatically)
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_communes import C  # key: (fr, nl, en, fr_slug, nl_slug, en_slug, postcode, short)

START, END = "<!-- COMMUNES -->", "<!-- /COMMUNES -->"
T = {
    "fr": dict(h2="Vendre dans votre commune",
               p="Prix médians Statbel, quartiers et accompagnement à 2 % HTVA : retrouvez la page de votre commune.",
               faq=r"Questions fréquentes"),
    "en": dict(h2="Selling in your municipality",
               p="Statbel median prices, neighbourhoods and our 2% excl. VAT service: find the page for your municipality.",
               faq=r"Frequently asked questions"),
    "nl": dict(h2="Verkopen in uw gemeente",
               p="Mediaanprijzen van Statbel, wijken en onze begeleiding aan 2% excl. btw: vind de pagina van uw gemeente.",
               faq=r"Veelgestelde vragen"),
}
IDX = {"fr": (0, 3, "vendre-"), "nl": (1, 4, "verkopen-"), "en": (2, 5, "sell-property-")}


def names(lang):
    n, s, pre = IDX[lang]
    out = []
    for key, c in C.items():
        name = c[n].replace("the City of Brussels", "City of Brussels")
        out.append((name, f"../{pre}{c[s]}/", [c[0], c[1], c[2].replace("the ", ""), c[7]]))
    return out


def block(lang, text):
    items = names(lang)
    low = text.lower()
    count = {i[0]: sum(len(re.findall(r"(?<![\w-])" + re.escape(a.lower()) + r"(?![\w-])", low)) for a in set(i[2])) for i in items}
    mentioned = sorted((i for i in items if count[i[0]]), key=lambda i: -count[i[0]])
    rest = [i for i in items if not count[i[0]]]
    lis = "".join(f'<li class="has-page"><a href="{u}">{n}</a></li>' for n, u, _ in mentioned + rest)
    t = T[lang]
    return (f'{START}\n      <h2>{t["h2"]}</h2>\n      <p>{t["p"]}</p>\n'
            f'      <ul class="zone-list" style="margin:1rem 0 2.5rem;padding:0">{lis}</ul>\n      {END}\n      ')


def lang_of(path):
    rel = os.path.relpath(path, ROOT)
    return "en" if rel.startswith("en/") else "nl" if rel.startswith("nl/") else "fr"


def main():
    n = 0
    for p in glob.glob(os.path.join(ROOT, "*", "index.html")) + glob.glob(os.path.join(ROOT, "*", "*", "index.html")):
        s = open(p, encoding="utf-8").read()
        if '"BlogPosting"' not in s or 'http-equiv="refresh"' in s:
            continue
        lang = lang_of(p)
        s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n\s*", "", s, flags=re.S)
        body = re.sub(r"<[^>]+>", " ", s.split("</header>", 1)[-1].split('<section class="cta-final"', 1)[0])
        m = re.search(r'<h2[^>]*>\s*' + T[lang]["faq"] + r'\s*</h2>', s) or re.search(r'<h2[^>]*>\s*(Sources|Bronnen)\s*</h2>', s)
        if not m:
            print("  no FAQ/Sources heading:", os.path.relpath(p, ROOT))
            continue
        s = s[:m.start()] + block(lang, body) + s[m.start():]
        open(p, "w", encoding="utf-8").write(s)
        n += 1
    print(f"  commune links: {n} articles")


if __name__ == "__main__":
    main()
