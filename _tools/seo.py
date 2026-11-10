#!/usr/bin/env python3
"""SEO maintenance for diamantconsult.com (static site on GitHub Pages).

Usage:  python3 _tools/seo.py
  - rewrites the hreflang block of every page listed in GROUPS
  - rebuilds sitemap.xml from every indexable index.html (lastmod = last git commit)

When you add a new article that has translations, add its group to GROUPS.
FR-only articles need nothing here: they get a self-referencing fr + x-default link.
Folders starting with "_" or "." and pages containing "noindex" are skipped.
"""
import os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.diamantconsult.com"

# (fr, en, nl) URL paths; None when that language doesn't exist
GROUPS = [
    ("/", "/en/", "/nl/"),
    ("/projets/", "/en/projects/", "/nl/projecten/"),
    ("/contact/", "/en/contact/", "/nl/contact/"),
    ("/blog/", "/en/blog/", "/nl/blog/"),
    ("/vendre-maison-bruxelles-2026/", "/en/selling-property-brussels-2026/", "/nl/woning-verkopen-brussel-2026/"),
    ("/vendre-maison-schaerbeek/", "/en/sell-house-schaerbeek-brussels/", "/nl/woning-verkopen-schaarbeek/"),
    ("/vendre-appartement-ixelles-uccle/", "/en/sell-apartment-ixelles-uccle/", "/nl/appartement-verkopen-elsene-ukkel/"),
    ("/vente-publique-biddit/", "/en/public-auction-biddit-belgium/", "/nl/openbare-verkoop-biddit/"),
    ("/certificat-peb-vente-immobiliere/", "/en/epc-certificate-property-sale/", "/nl/epc-attest-verkoop/"),
    ("/vendre-maison-brabant-wallon/", "/en/selling-property-brabant-wallon/", "/nl/woning-verkopen-waals-brabant/"),
    ("/delai-vente-bruxelles-2026/", "/en/how-long-to-sell-brussels-2026/", "/nl/hoelang-verkopen-brussel-2026/"),
]

# Old Wix URLs still known to Google -> new page. GitHub Pages can't send 301s, so we
# publish small pages with canonical + meta refresh 0, which Google treats as a permanent redirect.
REDIRECTS = {
    "/post/marche-immobilier-belgique-bruxelles-juin-2025": "/marche-immobilier-bruxelles-2026/",
    "/post/nouvelle-grille-des-loyers-à-bruxelles-juillet-2025-ce-que-tout-propriétaire-doit-savoir": "/grille-loyers-bruxelles-2026/",
    "/post/les-clés-d-une-vente-réussie-à-schaerbeek-critères-vente-schaerbeek": "/vendre-maison-schaerbeek/",
    "/services-2": "/#offres",
    "/services-immobiliers-bruxelles": "/#offres",
    "/visites-vente-publique-notariale-bruxelles": "/vente-publique-biddit/",
    "/properties-1": "/projets/",
    "/projets-immobiliers-vendus": "/projets/",
    "/obtenircertificatpeb": "/certificat-peb-vente-immobiliere/",
    "/blog-1": "/blog/",
}

REDIRECT_TPL = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<title>Page déplacée · Diamant Consult</title>
<link rel="canonical" href="{url}" />
<meta http-equiv="refresh" content="0; url={url}" />
<meta name="robots" content="noindex, follow" />
<script>location.replace("{url}");</script>
</head>
<body>
<p>Cette page a été déplacée : <a href="{url}">{url}</a></p>
</body>
</html>
"""


def write_redirects():
    for old, new in REDIRECTS.items():
        d = os.path.join(ROOT, old.strip("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(REDIRECT_TPL.format(url=BASE + new))
    print(f"  redirects: {len(REDIRECTS)} old URLs")


HREFLANG_RE =re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"\s*/?>\n?')
CANON_RE = re.compile(r'(<link rel="canonical" href="[^"]*"\s*/?>\n)')


def pages():
    out = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")) and d != "post")
        if "index.html" in files:
            rel = os.path.relpath(dirpath, ROOT)
            out.append("/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/")
    return out


def path_file(p):
    return os.path.join(ROOT, p.strip("/"), "index.html")


def indexable(p):
    with open(path_file(p), encoding="utf-8") as f:
        html = f.read()
    return "noindex" not in html and "http-equiv=\"refresh\"" not in html


def hreflang_block(group):
    fr, en, nl = group
    lines = []
    for lang, p in (("fr", fr), ("en", en), ("nl", nl)):
        if p:
            lines.append(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{p}" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}{fr or en or nl}" />')
    return "\n".join(lines) + "\n"


def apply_hreflang():
    grouped = {p: g for g in GROUPS for p in g if p}
    for p in pages():
        if not indexable(p):
            continue
        lang = "en" if p.startswith("/en/") else "nl" if p.startswith("/nl/") else "fr"
        group = grouped.get(p) or ((p, None, None) if lang == "fr" else
                                   (None, p, None) if lang == "en" else (None, None, p))
        fn = path_file(p)
        with open(fn, encoding="utf-8") as f:
            html = f.read()
        new = HREFLANG_RE.sub("", html)
        if not CANON_RE.search(new):
            print("  ! no canonical, skipped:", p)
            continue
        new = CANON_RE.sub(lambda m: m.group(1) + hreflang_block(group), new, count=1)
        if new != html:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(new)
            print("  hreflang updated:", p)


def lastmod(p):
    rel = os.path.relpath(path_file(p), ROOT)
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    except Exception:
        d = ""
    return d or datetime.date.today().isoformat()


def build_sitemap():
    def prio(p):
        if p in ("/", "/en/", "/nl/"):
            return "1.0"
        if p.rstrip("/").count("/") <= 2 and any(p.endswith(x) for x in ("/blog/", "/contact/", "/projets/", "/projects/", "/projecten/")):
            return "0.8"
        if "mentions-legales" in p or "confidentialite" in p:
            return "0.3"
        return "0.7"
    entries = []
    for p in pages():
        if not indexable(p):
            continue
        entries.append(f"  <url>\n    <loc>{BASE}{p}</loc>\n    <lastmod>{lastmod(p)}</lastmod>\n    <priority>{prio(p)}</priority>\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"  sitemap.xml: {len(entries)} URLs")


if __name__ == "__main__":
    write_redirects()
    apply_hreflang()
    build_sitemap()
