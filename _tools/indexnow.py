#!/usr/bin/env python3
"""Tell Bing (and Yandex, Seznam, Naver) about new or changed pages via IndexNow.
ChatGPT search and Copilot rely on Bing's index, so this speeds up AI visibility.

Usage:
  python3 _tools/indexnow.py                 # every URL of the sitemap
  python3 _tools/indexnow.py URL [URL ...]   # only these URLs (e.g. a new article in FR/EN/NL)
  python3 _tools/indexnow.py --changed       # URLs of pages changed in the last commit
The key file /39fa79733e404f38b87f5256546f7a28.txt must stay at the site root.
"""
import json, os, re, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "www.diamantconsult.com"
KEY = "39fa79733e404f38b87f5256546f7a28"


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def changed_urls():
    out = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True).stdout
    urls = []
    for f in out.split():
        if f.endswith("index.html") and not f.startswith("_"):
            d = f[: -len("index.html")]
            urls.append(f"https://{HOST}/{d}")
    known = set(sitemap_urls())
    return [u for u in urls if u in known]


def submit(urls):
    if not urls:
        print("IndexNow: nothing to submit")
        return
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: {len(urls)} URL(s) submitted, HTTP {r.status}")
    except urllib.error.HTTPError as e:
        print(f"IndexNow: HTTP {e.code} {e.read()[:200]!r}")     # 202 = accepted, 403 = key not reachable yet


if __name__ == "__main__":
    a = sys.argv[1:]
    submit(changed_urls() if a == ["--changed"] else (a or sitemap_urls()))
