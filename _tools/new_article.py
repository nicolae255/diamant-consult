#!/usr/bin/env python3
"""Create a new FR blog article from a JSON spec + an HTML body fragment.

Usage:  python3 _tools/new_article.py _tools/articles/<slug>.json

The JSON spec (see _tools/ARTICLE_GUIDE.md for the full rules):
{
  "slug": "marche-immobilier-bruxelles-2026",          # folder name, lowercase, no accents
  "seo_title": "... · Diamant Consult",                 # <title>, max ~65 chars before the brand
  "description": "...",                                 # meta description, 140-160 chars
  "h1": "Ligne 1 :<br><span style=\"color: var(--mute);\">ligne 2.</span>",
  "hero_sub": "...",                                    # 1-2 sentence intro under the H1
  "breadcrumb": "Short label",
  "category": "Marché local",                           # Guide vendeur | Marché local | Conseils | Actualité
  "read_min": 6,
  "date": "2026-11-10",                                 # ISO publish date
  "image": "img/xxx.webp" or "https://images.pexels.com/...",
  "image_alt": "...",
  "card_title": "...", "card_excerpt": "...",
  "faq": [{"q": "...", "a": "..."}],                    # 2-4 questions, plain text answers
  "body": "_tools/articles/<slug>.html"                 # body fragment: <h2>, <p>, <ul>, links
}
It writes <slug>/index.html, adds the card at the top of /blog/ and the homepage journal
(keeping 3 there), then runs seo.py (hreflang + sitemap).
"""
import json, os, sys, html, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.diamantconsult.com"
MONTHS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
          "Septembre", "Octobre", "Novembre", "Décembre"]
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M17 7H9M17 7V15" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def img_src(image, prefix, width):
    if image.startswith("http"):
        return image.replace("w=1200", f"w={width}") if width != 1200 else image
    return prefix + image


def abs_img(image):
    return image if image.startswith("http") else f"{BASE}/{image}"


def build(spec):
    slug = spec["slug"]
    y, m, _ = spec["date"].split("-")
    month_label = f"{MONTHS[int(m) - 1]} {y}"
    url = f"{BASE}/{slug}/"
    with open(os.path.join(ROOT, spec["body"]), encoding="utf-8") as f:
        body = f.read().strip()
    title_plain = spec["seo_title"].split(" · Diamant Consult")[0]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": title_plain,
                "description": spec["description"],
                "datePublished": spec["date"],
                "dateModified": spec["date"],
                "inLanguage": "fr-BE",
                "mainEntityOfPage": url,
                "image": abs_img(spec["image"]),
                "author": {"@type": "Organization", "name": "Diamant Consult", "url": BASE + "/"},
                "publisher": {"@type": "Organization", "name": "Diamant Consult", "url": BASE + "/",
                              "logo": {"@type": "ImageObject", "url": BASE + "/favicon-180.png"}},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q["q"],
                     "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                    for q in spec.get("faq", [])
                ],
            },
        ],
    }
    faq_html = ""
    if spec.get("faq"):
        faq_html = "\n\n      <h2>Questions fréquentes</h2>\n" + "\n".join(
            f"      <h3>{esc(q['q'])}</h3>\n      <p>{esc(q['a'])}</p>" for q in spec["faq"])

    with open(os.path.join(ROOT, "_tools", "article_template.html"), encoding="utf-8") as f:
        tpl = f.read()
    page = (tpl.replace("{{SEO_TITLE}}", esc(spec["seo_title"]))
               .replace("{{DESCRIPTION}}", esc(spec["description"]))
               .replace("{{URL}}", url)
               .replace("{{OG_TITLE}}", esc(title_plain))
               .replace("{{OG_IMAGE}}", abs_img(spec["image"]))
               .replace("{{JSONLD}}", json.dumps(ld, ensure_ascii=False, indent=2))
               .replace("{{BREADCRUMB}}", esc(spec["breadcrumb"]))
               .replace("{{CATEGORY}}", esc(spec["category"]))
               .replace("{{READ_MIN}}", str(spec["read_min"]))
               .replace("{{MONTH}}", month_label)
               .replace("{{H1}}", spec["h1"])
               .replace("{{HERO_SUB}}", esc(spec["hero_sub"]))
               .replace("{{IMG}}", img_src(spec["image"], "../", 1200))
               .replace("{{IMG_ALT}}", esc(spec["image_alt"]))
               .replace("{{BODY}}", body + faq_html))
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    with open(os.path.join(ROOT, slug, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("  page:", f"/{slug}/")

    def card(prefix, long_meta):
        meta = f'<span>{esc(spec["category"])}</span><span>{spec["read_min"]} min</span>'
        return f'''
      <article class="article reveal">
        <a href="{prefix}{slug}/">
          <div class="article-img">
            <img src="{img_src(spec["image"], prefix, 800)}" alt="{esc(spec["image_alt"])}" loading="lazy" />
          </div>
          <div class="article-body">
            <div class="article-meta">{meta}</div>
            <h3>{esc(spec["card_title"])}</h3>
            <p>{esc(spec["card_excerpt"])}</p>
            <span class="article-readmore">{"Lire l'article" if long_meta else "Lire"} {ARR}</span>
          </div>
        </a>
      </article>
'''

    # blog index: newest first, right after the featured article
    p = os.path.join(ROOT, "blog", "index.html")
    s = open(p, encoding="utf-8").read()
    if f'href="../{slug}/"' not in s:
        s = s.replace("<!-- NEW-ARTICLES -->", "<!-- NEW-ARTICLES -->\n" + card("../", True), 1)
        open(p, "w", encoding="utf-8").write(s)
        print("  card added to /blog/")

    # homepage journal: newest first, keep 3
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    if f'href="{slug}/"' not in s:
        marker = "<!-- JOURNAL-ARTICLES -->"
        start = s.index(marker) + len(marker)
        end = s.index("    </div>\n  </div>\n</section>", start)
        block = s[start:end]
        arts = [a + "</article>\n" for a in block.split("</article>\n") if "<article" in a]
        arts = [card("", False)] + arts
        s = s[:start] + "\n" + "".join(a.strip("\n") + "\n" for a in arts[:3]) + s[end:]
        open(p, "w", encoding="utf-8").write(s)
        print("  card added to homepage journal")


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    build(spec)
    subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "seo.py")], check=True)
