#!/usr/bin/env python3
"""Image bank: img/banque/catalogue.json lists every banner photo the site may use.

Rule: one banner photo = one article. The FR, EN and NL versions of the same article share
their photo; two different articles never do.

Usage:
  python3 _tools/images.py check     # fails (exit 1) if two articles share a banner or a banner is outside the bank
  python3 _tools/images.py free      # lists the bank photos no article uses yet (pick one of these)
  python3 _tools/images.py sync      # rewrites the "used_by" field of catalogue.json from the pages

Adding a photo to the bank: save it as img/banque/<id>.webp (about 1400 px wide, WebP q≈74) and add an
entry to catalogue.json: id, file, tags, alt {fr,en,nl}, source, license, author, source_url, used_by [].
Only CC0 / public domain / Pexels / Unsplash licences (no attribution needed in a banner) or own photos.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(ROOT, "img", "banque", "catalogue.json")
BASE = "https://www.diamantconsult.com/"


def catalogue():
    return json.load(open(CAT, encoding="utf-8"))


def norm(url):
    """Site-relative file path of an image URL ('img/banque/x.webp'), or the URL itself if external."""
    url = url.split("?")[0]
    if url.startswith(BASE):
        url = url[len(BASE):]
    elif url.startswith("http"):
        return url
    path = re.sub(r"^(\.\./)+|^/", "", url)
    webp = re.sub(r"\.(jpe?g|png)$", ".webp", path)      # a .jpg fallback counts as its .webp twin
    return webp if os.path.exists(os.path.join(ROOT, webp)) else path


def article_banners():
    """{article key (FR URL): banner file} for every page with BlogPosting JSON-LD."""
    out = {}
    pages = glob.glob(os.path.join(ROOT, "*", "index.html")) + glob.glob(os.path.join(ROOT, "*", "*", "index.html"))
    for p in pages:
        s = open(p, encoding="utf-8").read()
        if '"BlogPosting"' not in s or 'http-equiv="refresh"' in s:
            continue
        m = re.search(r'"@type":\s*"BlogPosting".*?"image":\s*"([^"]+)"', s, re.S)
        if not m:
            continue
        key = re.search(r'hreflang="fr" href="([^"]+)"', s) or re.search(r'rel="canonical" href="([^"]+)"', s)
        out.setdefault(key.group(1), set()).add(norm(m.group(1)))
    return out


def used_files(exclude_key=None):
    """{file: article key} for every banner in use (optionally ignoring one article)."""
    used = {}
    for key, files in article_banners().items():
        if key != exclude_key:
            for f in files:
                used[f] = key
    return used


def check_new(image, fr_url):
    """Raise SystemExit if `image` is not in the bank or already used by another article."""
    f = norm(image)
    files = {c["file"] for c in catalogue()}
    if f not in files:
        raise SystemExit(f"image {image!r} is not in the image bank (img/banque/catalogue.json). "
                         f"Run `python3 _tools/images.py free` and pick one.")
    other = used_files(exclude_key=fr_url).get(f)
    if other:
        raise SystemExit(f"image {image!r} is already the banner of {other}. "
                         f"Run `python3 _tools/images.py free` and pick an unused one.")


def cmd_check():
    files = {c["file"] for c in catalogue()}
    errors = []
    seen = {}
    for key, imgs in sorted(article_banners().items()):
        if len(imgs) > 1:
            errors.append(f"{key}: the language versions use different banners {sorted(imgs)}")
        for f in imgs:
            if f not in files:
                errors.append(f"{key}: banner {f} is not in the image bank")
            if f in seen and seen[f] != key:
                errors.append(f"{f} is used by two articles: {seen[f]} and {key}")
            seen[f] = key
    if errors:
        print("IMAGE BANK ERRORS:\n  " + "\n  ".join(errors))
        sys.exit(1)
    print(f"image bank OK: {len(seen)} banners, all unique, all in the bank")


def cmd_free():
    used = used_files()
    for c in catalogue():
        if c["file"] not in used:
            print(f'{c["file"]:48} {", ".join(c["tags"])} | {c["alt"]["fr"]}')


def cmd_sync():
    used = used_files()
    cat = catalogue()
    for c in cat:
        k = used.get(c["file"])
        c["used_by"] = [k.replace(BASE, "/")] if k else []
    json.dump(cat, open(CAT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(CAT, "a").write("\n")
    print(f"catalogue synced: {sum(1 for c in cat if c['used_by'])} used, {sum(1 for c in cat if not c['used_by'])} free")


if __name__ == "__main__":
    {"check": cmd_check, "free": cmd_free, "sync": cmd_sync}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
