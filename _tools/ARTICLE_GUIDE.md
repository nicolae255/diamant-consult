# Diamant Consult: how to write and publish a blog article (FR + EN + NL)

This is the playbook for the automated twice-weekly article (and for anyone writing by hand).
Folders starting with `_` are not published by GitHub Pages.

## Goal
Each article must bring in **Brussels property owners who might sell** (houses and apartments, all 19
communes). Every article targets one search a seller would type, uses recent news as the hook,
and ends by pointing to a free first meeting / the 2% excl. VAT all-inclusive sale. Never promise a free valuation or estimate: it is not a service on its own.
Style: never use em dashes (—) or en dashes (–) anywhere (text, titles, alt, FAQ, sources). The owner finds them
"too AI". Use a comma, a colon, parentheses or two sentences instead; for source names write `notaire.be · Title`.
Write smoothly and simply, like a person talking to a seller, without slogans.
Blog filter categories: `category` must be exactly one of these, so the blog filter buttons work:
FR `Marché local` · `Guide vendeur` · `Frais de vente` · `Conseils` · `Vente publique`;
EN `Local market` · `Seller guide` · `Selling costs` · `Advice` · `Public auction`;
NL `Lokale markt` · `Verkopersgids` · `Verkoopkosten` · `Advies` · `Openbare verkoop`.
Never describe negotiation as part of our service (the notary handles offers); describing the market ("buyers negotiate harder") is fine.


Every article is published in **three languages**: French (main market), English (expats, very present
in Ixelles, Etterbeek, Woluwe, Uccle) and Dutch (Dutch-speaking Brussels owners). Same facts, same
sources, same structure, but each version is **written natively for its readers**, not translated word
for word: use the words people actually type into Google in that language
(FR "vendre sa maison Uccle", EN "sell my house Brussels", NL "huis verkopen Ukkel").

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
     Use the official name in each language (NL: Elsene, Ukkel, Schaarbeek, Watermaal-Bosvoorde,
     Sint-Lambrechts-Woluwe, Sint-Pieters-Woluwe, Oudergem, Vorst, Sint-Gillis, Sint-Joost-ten-Node,
     Sint-Agatha-Berchem, Molenbeek, Brussel-Stad; EN usually keeps the French names).
   - **Seller life situations**: succession / inheritance, divorce/separation, selling a rented property,
     selling to buy another home, downsizing for retirees, selling a property needing renovation, joint ownership.
   - **Costs and process**: agency fees 2% vs 3-4%, documents, PEB, soil certificate, timelines, valuation.
4. Prefer topics where a real search exists: include the commune name or "Bruxelles / Brussels / Brussel"
   and the year in the title of each language.

## 2. Write
- Write the French version first (vous), then the English (you, British spelling) and Dutch (u, Belgian
  Dutch: "EPB-certificaat", "notaris", "onderhandse verkoop", "openbare verkoop", "schatting").
- 900-1,500 words per language, 4-7 `<h2>` sections, short paragraphs, bullet lists where useful.
- **Never invent figures.** Every number must come from a source you actually read; cite it with a link
  (`target="_blank" rel="noopener"`). If a commune-level price isn't available from a reliable source,
  speak qualitatively. Do not invent client stories, quotes or testimonials. All three versions contain the
  same facts and figures (use local number formats: FR 609 227 €, EN €609,227, NL € 609.227).
- **Price rule: the commission is always written with "excluding VAT"**: FR "2% HTVA", EN "2% excl. VAT",
  NL "2% excl. btw" (e.g. "2% HTVA, tout compris"). Never write "2%" alone for the commission.
- Mention Diamant Consult naturally: 2% excl. VAT all-inclusive, free first meeting (where the asking price is set), works with notaire Stephan Borremans,
  based in Schaerbeek (Av. du Diamant 138), covers all Brussels and Brabant wallon. No exaggerated promises.
- Link to 2-4 existing articles **in the same language** (relative links `../slug/`):

  | FR | EN | NL |
  |---|---|---|
  | `vendre-maison-bruxelles-2026` | `selling-property-brussels-2026` | `woning-verkopen-brussel-2026` |
  | `delai-vente-bruxelles-2026` | `how-long-to-sell-brussels-2026` | `hoelang-verkopen-brussel-2026` |
  | `certificat-peb-vente-immobiliere` | `epc-certificate-property-sale` | `epc-attest-verkoop` |
  | `vendre-maison-schaerbeek` | `sell-house-schaerbeek-brussels` | `woning-verkopen-schaarbeek` |
  | `vendre-appartement-ixelles-uccle` | `sell-apartment-ixelles-uccle` | `appartement-verkopen-elsene-ukkel` |
  | `vente-publique-biddit` | `public-auction-biddit-belgium` | `openbare-verkoop-biddit` |
  | `vendre-maison-brabant-wallon` | `selling-property-brabant-wallon` | `woning-verkopen-waals-brabant` |
  | `marche-immobilier-bruxelles-2026` | `brussels-property-market-2026` | `vastgoedmarkt-brussel-2026` |
  | `grille-loyers-bruxelles-2026` | `brussels-rent-grid-2026` | `huurprijzenrooster-brussel-2026` |
  | `vendre-gre-a-gre-bruxelles` | (none: use `../#offres`) | (none: use `../#offres`) |

  plus any newer articles listed in LOG.md (each line gives the three slugs).
- **Commune landing pages exist for all 19 Brussels communes**: whenever an article mentions a commune, link its
  page in the same language: FR `../vendre-<commune>/` (e.g. `vendre-uccle`, `vendre-bruxelles-ville`), EN
  `../sell-property-<commune>/` (`sell-property-brussels-city` for the City of Brussels), NL `../verkopen-<nl-name>/`
  (e.g. `verkopen-ukkel`, `verkopen-sint-jans-molenbeek`). Exact slugs: the `slug` fields in `_tools/communes/*.json`.
- The templates already add a closing call to action and contact block. Don't add another one.

### Written for Google AND answer engines (SEO + AEO + GEO)
AI answers (Google AI Overviews, ChatGPT, Perplexity, Copilot) quote pages that answer clearly, with facts
and sources. Every article must therefore have:
- **summary** (3-5 points, required, shown at the top as "En bref / Key points / In het kort"): each point is one
  self-contained sentence that directly answers part of the question, with the key figure and the place/date
  ("In Q3 2026, the average house price in Brussels reached €609,227 (+4.8%)."). No teasers.
- **H2s phrased as the questions people ask** where natural ("Combien vaut une maison à Uccle en 2026 ?",
  "Faut-il vendre maintenant ?"), and the **first sentence under each H2 answers it directly**; details follow.
- **Concrete, dated facts**: numbers with their period and source, named places, named institutions. Avoid vague
  claims ("prices are rising") without a figure. Name the entity often: "Diamant Consult", "Bruxelles / Brussels / Brussel",
  the commune.
- **faq** (3-5 questions, required): the exact questions sellers type, answered in 1-3 self-contained sentences.
  Google no longer shows FAQ rich results for most sites, but answer engines reuse these Q&A pairs heavily.
- **sources** (required, shared by the 3 languages): every source you used, as `{"name": "...", "url": "..."}`.
  They are listed at the bottom of each version and added to the structured data. The same sources must also be
  linked inline where the figures appear.
- A short comparison table (`<table>`) when it genuinely helps (e.g. 2% vs 3.5% commission on a given price).

## 3. Files
In `_tools/articles/`, named after the **French slug**:
- `<fr-slug>.fr.html`, `<fr-slug>.en.html`, `<fr-slug>.nl.html`: body fragments only
  (`<h2>`, `<p>`, `<ul>`, `<a>`), indented 6 spaces.
- `<fr-slug>.json`: the spec. Copy `marche-immobilier-bruxelles-2026.json` and replace everything.
  Shared fields: `date` (today, ISO), `read_min`, `image`, `sources`. Then one block per language (`fr`, `en`, `nl`) with:
  - slug: lowercase, no accents, hyphens, main keyword **in that language** (e.g. `vendre-maison-uccle-2026`,
    `sell-house-uccle-2026`, `huis-verkopen-ukkel-2026`). Must not already exist.
  - seo_title: keyword first, max ~65 characters + ` · Diamant Consult`
  - description: 140-160 characters, keyword + a reason to click
  - category: one of the blog filter categories listed at the top of this guide (news goes under `Marché local` / `Local market` / `Lokale markt`)
  - h1, hero_sub, breadcrumb, image_alt, card_title, card_excerpt, summary (3-5), faq (3-5),
    body (path to that language's fragment)
  The builder refuses to build if summary, faq or sources are missing or have the wrong count.
- image: every article gets its OWN banner from the image bank (`img/banque/`, catalogue in
  `img/banque/catalogue.json`). Run `python3 _tools/images.py free` to list the unused photos with their tags and
  pick the one that fits the topic best; put its `file` (e.g. `"img/banque/signature-stylo.webp"`) in `image`. Use the
  catalogue's `alt` as a starting point for each language's `image_alt` (adapt it to the article). The FR, EN and NL
  versions share the photo; two articles never do: new_article.py refuses an image already used by another article.
  If no free photo fits (or fewer than 5 remain), add new ones: only CC0 / public-domain images (e.g. Openverse
  `https://api.openverse.org/v1/images/?q=...&license=cc0,pdm`), Pexels or Unsplash, about 1400 px wide, saved as
  `img/banque/<descriptive-id>.webp`, with a catalogue entry (id, file, tags, alt fr/en/nl, source, license, author,
  source_url, used_by []). No photos of identifiable people's private homes, no foreign skylines, no black-and-white
  archive pictures. Never hotlink other sites. `python3 _tools/images.py check` must pass before you push.

## 4. Build, check, publish
```
python3 _tools/images.py free          # pick an unused banner first
python3 _tools/new_article.py _tools/articles/<fr-slug>.json
python3 _tools/check_links.py
python3 _tools/images.py check
```
The builder validates all three languages before writing anything, then creates `/<fr-slug>/`,
`/en/<en-slug>/` and `/nl/<nl-slug>/`, adds the cards to the three blogs and three homepages (keeps 3 there),
links the versions together (hreflang + language buttons), updates the sitemap and `llms.txt`.
Then check:
- `check_links.py` prints "all internal links OK" (fix any broken link and rebuild)
- `images.py check` prints "image bank OK" (every banner unique)
- `git status` only shows: the three new article folders, `blog/index.html`, `en/blog/index.html`,
  `nl/blog/index.html`, `index.html`, `en/index.html`, `nl/index.html`, `sitemap.xml`, `llms.txt`, `img/banque/catalogue.json` (and any new `img/banque/*.webp`), and files in `_tools/articles/`
After the push, notify Bing (used by ChatGPT search and Copilot) once the page is live:
```
for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}" https://www.diamantconsult.com/<fr-slug>/ | grep -q 200 && break; sleep 15; done
python3 _tools/indexnow.py https://www.diamantconsult.com/<fr-slug>/ https://www.diamantconsult.com/en/<en-slug>/ https://www.diamantconsult.com/nl/<nl-slug>/ https://www.diamantconsult.com/blog/ https://www.diamantconsult.com/en/blog/ https://www.diamantconsult.com/nl/blog/
```
HTTP 200 or 202 = accepted. If the network call fails, just mention it in the final message (do not retry endlessly).
Append a line to `_tools/articles/LOG.md`:
`- YYYY-MM-DD · /<fr-slug>/ · /en/<en-slug>/ · /nl/<nl-slug>/ · <type> · <commune or theme> · <main source>`
Commit (`Article: <French title>`) and push to `main`. GitHub Pages deploys automatically.
If any language fails, publish nothing: do not push a partial article.
