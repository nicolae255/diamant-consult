# Diamant Consult: how to write and publish a blog article

This is the playbook for the automated twice-weekly article (and for anyone writing by hand).
Folders starting with `_` are not published by GitHub Pages.

## Goal
Each article must bring in **Brussels property owners who might sell** (houses and apartments, all 19
communes). Every article targets one search a seller would type, uses recent news as the hook,
and ends by pointing to a free valuation / the 2% all-inclusive sale.

## 1. Pick the topic
1. Read `_tools/articles/LOG.md` so you never repeat a topic or the same commune twice in a row.
2. Search the news from the **last 14 days** (French and Dutch-language Belgian sources): notaire.be / Fednot
   barometers, Statbel, Bruxelles Logement / be.brussels / loyers.brussels, Brussels Parliament decisions,
   National Bank / mortgage rates, registration fees (droits d'enregistrement), PEB / Renolution,
   urbanism, Biddit, and media (La Libre, Le Soir, L'Echo, RTBF, BX1, Bruzz, Trends, Immoweb news).
3. Choose an angle that answers a seller question. Rotate between these types:
   - **News for sellers**: "<news> : ce que ça change pour les vendeurs à Bruxelles"
   - **Commune guides**: "Vendre sa maison à <commune> en 2026 : prix, acheteurs, délais". Rotate across:
     Anderlecht, Auderghem, Berchem-Sainte-Agathe, Bruxelles-Ville, Etterbeek, Evere, Forest, Ganshoren,
     Ixelles, Jette, Koekelberg, Molenbeek-Saint-Jean, Saint-Gilles, Saint-Josse-ten-Noode, Schaerbeek,
     Uccle, Watermael-Boitsfort, Woluwe-Saint-Lambert, Woluwe-Saint-Pierre (+ Brabant wallon now and then).
     Schaerbeek, Ixelles/Uccle/Etterbeek already have pages: link to them rather than duplicating.
   - **Seller life situations**: succession / inheritance, divorce/separation, selling a rented property,
     selling to buy another home, downsizing for retirees, selling a property needing renovation, joint ownership.
   - **Costs and process**: agency fees 2% vs 3-4%, documents, PEB, soil certificate, timelines, valuation.
4. Prefer topics where a real search exists (people type it into Google): include the commune name
   or "Bruxelles" and the year in the title.

## 2. Write (French, Belgian usage, "vous")
- 900-1,500 words, 4-7 `<h2>` sections, short paragraphs, bullet lists where useful.
- **Never invent figures.** Every number must come from a source you actually read; cite it with a link
  (`target="_blank" rel="noopener"`). If a commune-level price isn't available from a reliable source,
  speak qualitatively. Do not invent client stories, quotes or testimonials.
- Mention Diamant Consult naturally: 2% all-inclusive, free valuation, works with notaire Stephan Borremans,
  based in Schaerbeek (Av. du Diamant 138), covers all Brussels and Brabant wallon. No exaggerated promises.
- Link to 2-4 existing articles (relative links `../slug/`): `vendre-gre-a-gre-bruxelles`,
  `delai-vente-bruxelles-2026`, `certificat-peb-vente-immobiliere`, `vendre-maison-schaerbeek`,
  `vendre-appartement-ixelles-uccle`, `vente-publique-biddit`, `vendre-maison-brabant-wallon`,
  `marche-immobilier-bruxelles-2026`, `grille-loyers-bruxelles-2026`, plus any newer ones in LOG.md.
- 2-4 FAQ entries (plain text answers, 1-3 sentences): they become Google rich results.
- The template already adds a closing call to action and contact block. Don't add another one.

## 3. Files
Create two files in `_tools/articles/`:
- `<slug>.html`: the body fragment only (`<h2>`, `<p>`, `<ul>`, `<a>`), indented 6 spaces.
- `<slug>.json`: the spec (see the header of `_tools/new_article.py`; copy `grille-loyers-bruxelles-2026.json`).
  - slug: lowercase, no accents, hyphens, contains the main keyword (e.g. `vendre-maison-uccle-2026`)
  - seo_title: keyword first, max ~65 characters + ` · Diamant Consult`
  - description: 140-160 characters, contains the keyword + a reason to click
  - date: today's date (ISO)
  - category: `Marché local`, `Guide vendeur`, `Conseils` or `Actualité`
  - image: reuse one that fits: `img/brussels-old-city.webp`, `img/delai-vente-cles.webp`, a real project photo
    from `img/projets/*.webp` (only when the commune matches, and describe it neutrally), or a Pexels URL already
    used on the site (`grep -rho 'images.pexels.com/photos/[0-9]*/[^"]*' --include='*.html' .`). Never hotlink other sites.

## 4. Build, check, publish
```
python3 _tools/new_article.py _tools/articles/<slug>.json
```
This creates `<slug>/index.html`, adds the card to `/blog/` and the homepage (keeps 3), updates the sitemap.
Then check:
- `grep -c '{{' <slug>/index.html` returns 0
- the JSON-LD parses (`python3 -c "import json,re;s=open('<slug>/index.html').read();json.loads(re.search(r'ld\+json\">(.*?)</script>',s,re.S).group(1))"`)
- `git diff --stat` only touches: the new folder, `blog/index.html`, `index.html`, `sitemap.xml`, `_tools/articles/*`
Append a line to `_tools/articles/LOG.md`: `- YYYY-MM-DD · /<slug>/ · <type> · <commune or theme> · <main source>`
Commit (`Article: <title>`) and push to `main`. GitHub Pages deploys automatically.
