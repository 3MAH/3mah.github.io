"""Fail the build when the site links to a page of the Sphinx docs that is gone.

Scans the built site (site/) for every link and media URL pointing to
https://3mah.github.io/<lib>-docs/... and checks that each one answers 200.
Run after `zensical build`.

Only a link that is really gone (4xx) fails the build. Server hiccups (5xx,
timeouts, network errors) are retried, then reported as warnings: a temporary
503 from GitHub Pages must not block the deployment.

    python scripts/check_doc_links.py [site_dir]
"""

import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
DOCS_URL = re.compile(r'(?:href|src|poster)="(https://3mah\.github\.io/[a-z]+-docs/[^"#?]*)')
UA = {"User-Agent": "3mah-link-checker"}


def status(url):
    """Status of `url`, retrying the answers that are likely temporary."""
    for attempt in range(4):
        code = status_once(url)
        if code == 200 or is_gone(code):
            return code
        time.sleep(2 * (attempt + 1))
    return code


def is_gone(code):
    return isinstance(code, int) and 400 <= code < 500 and code not in (408, 429)


def status_once(url):
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
    broken = {u: s for u, s in results.items() if is_gone(s)}
    flaky = {u: s for u, s in results.items() if s != 200 and u not in broken}
    print(f"Checked {len(results)} links to the Sphinx docs, {len(broken)} broken, "
          f"{len(flaky)} not reachable right now.")
    for label, group in (("broken", broken), ("warning", flaky)):
        for url, code in sorted(group.items()):
            print(f"  {label} [{code}] {url}\n        used in: {', '.join(sorted(pages[url]))}")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
