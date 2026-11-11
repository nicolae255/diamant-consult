#!/usr/bin/env python3
"""Create a new blog article in French, English and Dutch from one JSON spec.

Usage:  python3 _tools/new_article.py _tools/articles/<fr-slug>.json

Spec format (see _tools/ARTICLE_GUIDE.md and the existing specs in _tools/articles/):
{
  "date": "2026-11-12",            # ISO publish date (shared)
  "read_min": 6,                   # shared
  "image": "img/banque/xxx.webp",  # shared; must come from the image bank and be unused (python3 _tools/images.py free)
  "sources": [{"name": "notaire.be: baromètre T3 2026", "url": "https://..."}],  # shared, every source used
  "fr": { ...language block... },
  "en": { ...language block... },
  "nl": { ...language block... }
}
Language block:
{
  "slug": "vendre-maison-uccle-2026",           # lowercase, no accents, keyword in the language
  "seo_title": "... · Diamant Consult",
  "description": "...",                          # 140-160 characters
  "h1": "Line 1:<br><span style=\"color: var(--mute);\">line 2.</span>",
  "hero_sub": "...",
  "breadcrumb": "...",
  "category": "...",
  "image_alt": "...",
  "card_title": "...", "card_excerpt": "...",
  "summary": ["3-5 short direct answers with the key figures", "..."],   # shown at the top
  "faq": [{"q": "...", "a": "..."}],                                       # 3-5 questions
  "body": "_tools/articles/<fr-slug>.<lang>.html"
}
Pages: FR /<slug>/, EN /en/<slug>/, NL /nl/<slug>/. For each language the card is added to that
language's blog and homepage (keeping 3 there). Then seo.py links the three versions (hreflang)
and rebuilds the sitemap. Nothing is written if any language fails validation.
"""
import json, os, re, sys, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import images

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.diamantconsult.com"
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M17 7H9M17 7V15" stroke-linecap="round" stroke-linejoin="round"/></svg>'

LANG = {
    "fr": dict(prefix="", depth="../", months=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
               faq="Questions fréquentes", summary="En bref", sources="Sources", home="Accueil", read_blog="Lire l'article", read_home="Lire", locale="fr_BE", in_lang="fr-BE", btn=0),
    "en": dict(prefix="en/", depth="../../", months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
               faq="Frequently asked questions", summary="Key points", sources="Sources", home="Home", read_blog="Read", read_home="Read", locale="en_GB", in_lang="en", btn=2),
    "nl": dict(prefix="nl/", depth="../../", months=["Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli", "Augustus", "September", "Oktober", "November", "December"],
               faq="Veelgestelde vragen", summary="In het kort", sources="Bronnen", home="Startpagina", read_blog="Lees", read_home="Lees", locale="nl_BE", in_lang="nl-BE", btn=1),
}
REQUIRED = ["slug", "seo_title", "description", "h1", "hero_sub", "breadcrumb", "category",
            "image_alt", "card_title", "card_excerpt", "summary", "faq", "body"]
SHARED_REQUIRED = ["date", "read_min", "image", "sources"]


def esc(s):
    return html.escape(s, quote=True)


def img_src(image, prefix, width):
    if image.startswith("http"):
        return re.sub(r"w=\d+", f"w={width}", image, count=1)
    return prefix + image


def abs_img(image):
    return image if image.startswith("http") else f"{BASE}/{image}"


def page_path(lang, slug):
    return f"/{LANG[lang]['prefix']}{slug}/"


def normalize(spec):
    """Accept the old FR-only format too."""
    if "fr" not in spec:
        spec = {"date": spec["date"], "read_min": spec["read_min"], "image": spec["image"],
                "fr": {k: v for k, v in spec.items() if k not in ("date", "read_min", "image")}}
    return spec


def render(spec, lang):
    b = spec[lang]
    L = LANG[lang]
    missing = [k for k in REQUIRED if k not in b] + [k for k in SHARED_REQUIRED if k not in spec]
    if missing:
        raise SystemExit(f"[{lang}] missing fields: {missing}")
    if not 3 <= len(b["summary"]) <= 5:
        raise SystemExit(f"[{lang}] summary needs 3-5 points")
    if not 3 <= len(b["faq"]) <= 5:
        raise SystemExit(f"[{lang}] faq needs 3-5 questions")
    if not spec["sources"] or not all(x.get("url", "").startswith("http") for x in spec["sources"]):
        raise SystemExit(f"[{lang}] sources: at least one {{name, url}} with a real URL")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", b["slug"]):
        raise SystemExit(f"[{lang}] bad slug: {b['slug']}")
    y, m, _ = spec["date"].split("-")
    url = BASE + page_path(lang, b["slug"])
    with open(os.path.join(ROOT, b["body"]), encoding="utf-8") as f:
        body = f.read().strip()
    title_plain = b["seo_title"].split(" · Diamant Consult")[0]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": title_plain, "description": b["description"],
         "datePublished": spec["date"], "dateModified": spec["date"], "inLanguage": L["in_lang"],
         "mainEntityOfPage": url, "image": abs_img(spec["image"]),
         "abstract": " ".join(b["summary"]),
         "citation": [{"@type": "CreativeWork", "name": x["name"], "url": x["url"]} for x in spec["sources"]],
         "author": {"@type": "Organization", "name": "Diamant Consult", "url": BASE + "/"},
         "publisher": {"@type": "Organization", "name": "Diamant Consult", "url": BASE + "/",
                       "logo": {"@type": "ImageObject", "url": BASE + "/icon-512.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L["home"], "item": f"{BASE}/{L['prefix']}"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/{L['prefix']}blog/"},
            {"@type": "ListItem", "position": 3, "name": b["breadcrumb"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in b["faq"]]},
    ]}
    faq_html = ""
    if b["faq"]:
        faq_html = f"\n\n      <h2>{L['faq']}</h2>\n" + "\n".join(
            f"      <h3>{esc(q['q'])}</h3>\n      <p>{esc(q['a'])}</p>" for q in b["faq"])
    summary_html = (
        '      <div class="key-points" style="background: var(--bg-soft); border-radius: 1rem; padding: 1.5rem 1.75rem; margin-bottom: 3rem;">\n'
        f'        <h2 style="margin-top: 0;">{L["summary"]}</h2>\n        <ul>\n'
        + "".join(f"          <li>{esc(x)}</li>\n" for x in b["summary"])
        + "        </ul>\n      </div>\n\n")
    sources_html = (f"\n\n      <h2>{L['sources']}</h2>\n      <ul>\n"
        + "".join(f'        <li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["name"])}</a></li>\n'
                  for x in spec["sources"]) + "      </ul>")
    # language switcher buttons: order in the header is FR, NL, EN
    others = []
    for ol in ("fr", "nl", "en"):
        if ol != lang and ol in spec:
            others.append(f"  lb[{LANG[ol]['btn']}].onclick = () => location.href = '{page_path(ol, spec[ol]['slug'])}';")
        elif ol != lang:
            others.append(f"  lb[{LANG[ol]['btn']}].onclick = () => location.href = '/{LANG[ol]['prefix']}blog/';")
    with open(os.path.join(ROOT, "_tools", f"article_template_{lang}.html"), encoding="utf-8") as f:
        tpl = f.read()
    rep = {
        "{{SEO_TITLE}}": esc(b["seo_title"]), "{{DESCRIPTION}}": esc(b["description"]), "{{URL}}": url,
        "{{OG_TITLE}}": esc(title_plain), "{{OG_IMAGE}}": abs_img(spec["image"]), "{{OG_LOCALE}}": L["locale"],
        "{{JSONLD}}": json.dumps(ld, ensure_ascii=False, indent=2), "{{BREADCRUMB}}": esc(b["breadcrumb"]),
        "{{CATEGORY}}": esc(b["category"]), "{{READ_MIN}}": str(spec["read_min"]),
        "{{MONTH}}": f"{L['months'][int(m) - 1]} {y}", "{{H1}}": b["h1"], "{{HERO_SUB}}": esc(b["hero_sub"]),
        "{{IMG}}": img_src(spec["image"], L["depth"], 1200), "{{IMG_ALT}}": esc(b["image_alt"]),
        "{{LANG_JS}}": "\n".join(others), "{{BODY}}": summary_html + body + faq_html + sources_html,
    }
    page = tpl
    for k, v in rep.items():
        page = page.replace(k, v)
    if "{{" in page:
        raise SystemExit(f"[{lang}] unreplaced placeholder: {re.findall(r'{{[A-Z_]+}}', page)}")
    json.loads(re.search(r'ld\+json">\s*(.*?)\s*</script>', page, re.S).group(1))
    return page


def card(spec, lang, prefix, img_prefix, readmore):
    b = spec[lang]
    return f'''      <article class="article reveal">
        <a href="{prefix}{b["slug"]}/">
          <div class="article-img">
            <img src="{img_src(spec["image"], img_prefix, 800)}" alt="{esc(b["image_alt"])}" loading="lazy" />
          </div>
          <div class="article-body">
            <div class="article-meta"><span>{esc(b["category"])}</span><span>{spec["read_min"]} min</span></div>
            <h3>{esc(b["card_title"])}</h3>
            <p>{esc(b["card_excerpt"])}</p>
            <span class="article-readmore">{readmore} {ARR}</span>
          </div>
        </a>
      </article>
'''


def add_cards(spec, lang):
    L = LANG[lang]
    slug = spec[lang]["slug"]
    up = "../" if lang == "fr" else "../../"      # from /xx/blog/ to site root
    # blog index
    p = os.path.join(ROOT, L["prefix"], "blog", "index.html")
    s = open(p, encoding="utf-8").read()
    if f'href="../{slug}/"' not in s:
        s = s.replace("<!-- NEW-ARTICLES -->", "<!-- NEW-ARTICLES -->\n" + card(spec, lang, "../", up, L["read_blog"]), 1)
        open(p, "w", encoding="utf-8").write(s)
    # homepage journal: newest first, keep 3
    p = os.path.join(ROOT, L["prefix"], "index.html")
    s = open(p, encoding="utf-8").read()
    if f'href="{slug}/"' not in s:
        marker = "<!-- JOURNAL-ARTICLES -->"
        start = s.index(marker) + len(marker)
        end = s.index("    </div>\n  </div>\n</section>", start)
        arts = [a + "</article>\n" for a in s[start:end].split("</article>\n") if "<article" in a]
        home_img = "" if lang == "fr" else "../"
        arts = [card(spec, lang, "", home_img, L["read_home"])] + arts
        s = s[:start] + "\n" + "".join(a.strip("\n") + "\n" for a in arts[:3]) + s[end:]
        open(p, "w", encoding="utf-8").write(s)


def main(path):
    spec = normalize(json.load(open(path, encoding="utf-8")))
    langs = [l for l in ("fr", "en", "nl") if l in spec]
    images.check_new(spec["image"], f"{BASE}/{spec['fr']['slug']}/")   # one banner per article, from the bank
    pages = {l: render(spec, l) for l in langs}          # validate everything before writing
    for l in langs:
        d = os.path.join(ROOT, LANG[l]["prefix"], spec[l]["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pages[l])
        add_cards(spec, l)
        print(f"  [{l}] {page_path(l, spec[l]['slug'])}")
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "commune_links.py")], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "seo.py")], check=True,
                   stdout=subprocess.DEVNULL)
    print("  hreflang + sitemap updated")
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "images.py"), "sync"], check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "images.py"), "check"], check=True)


if __name__ == "__main__":
    main(sys.argv[1])
