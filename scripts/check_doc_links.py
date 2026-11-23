"""Fail the build when the site links to a page of the Sphinx docs that is gone.

Scans the built site (site/) for every link and media URL pointing to
https://3mah.github.io/<lib>-docs/... and checks that each one answers 200.
Run after `zensical build`.

    python scripts/check_doc_links.py [site_dir]
"""

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
DOCS_URL = re.compile(r'(?:href|src|poster)="(https://3mah\.github\.io/[a-z]+-docs/[^"#?]*)')
UA = {"User-Agent": "3mah-link-checker"}


def status(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if e.code != 405:
                return e.code
        except (urllib.error.URLError, TimeoutError) as e:
            return f"error: {e}"
    return "error"


def main():
    pages = {}
    for f in SITE.rglob("*.html"):
        for url in DOCS_URL.findall(f.read_text(encoding="utf-8")):
            pages.setdefault(url, set()).add(str(f.relative_to(SITE)))
    with ThreadPoolExecutor(16) as pool:
        results = dict(zip(pages, pool.map(status, pages)))
    broken = {u: s for u, s in results.items() if s != 200}
    print(f"Checked {len(results)} links to the Sphinx docs, {len(broken)} broken.")
    for url, code in sorted(broken.items()):
        print(f"  [{code}] {url}\n        used in: {', '.join(sorted(pages[url]))}")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
