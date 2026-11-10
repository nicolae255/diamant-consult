#!/usr/bin/env python3
"""Check every internal link and local image on the site. Exit code 1 if anything is broken.

Usage:  python3 _tools/check_links.py
"""
import os, re, sys
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "www.diamantconsult.com"
broken = []

for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith((".", "_"))]
    for fn in files:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dirpath, fn)
        html = open(path, encoding="utf-8").read()
        if 'http-equiv="refresh"' in html:
            continue
        for attr, url in re.findall(r'(href|src|srcset)="([^"]+)"', html):
            u = urlparse(url)
            if u.scheme in ("mailto", "tel", "javascript", "data"):
                continue
            if u.netloc and u.netloc != SITE:
                continue
            p = unquote(u.path)
            if not p:
                continue
            target = os.path.join(ROOT, p.lstrip("/")) if (p.startswith("/") or u.netloc) else os.path.normpath(os.path.join(dirpath, p))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                broken.append(f"{os.path.relpath(path, ROOT)} -> {url}")

if broken:
    print("BROKEN LINKS:")
    print("\n".join("  " + b for b in sorted(set(broken))))
    sys.exit(1)
print("all internal links OK")
