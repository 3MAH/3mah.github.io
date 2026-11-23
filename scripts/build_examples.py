"""Build the cross-project example gallery from the published Sphinx docs.

Reads the sphinx-gallery index page of each library (simcoon, fedoo,
microgen), extracts every example (title, thumbnail, link, section) and
writes:

  docs/examples.md                   unified, filterable gallery page
  snippets/examples_<lib>.md         "featured examples" block per library
  docs/assets/data/examples.json     machine-readable index

Thumbnails are not copied: they are served by the Sphinx docs on the same
domain (3mah.github.io). Run before `zensical build`; the CI workflow does
it on every build so the gallery follows the documentation automatically.
A library whose gallery cannot be fetched keeps a "browse the docs" card
instead of failing the build.

    python scripts/build_examples.py
"""

import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent

LIBRARIES = {
    "simcoon": {
        "gallery": "https://3mah.github.io/simcoon-docs/examples/index.html",
        "docs": "https://3mah.github.io/simcoon-docs/",
        "featured": [
            "heterogeneous/homogenization.html",
            "analysis/directional_stiffness.html",
            "identification/chaboche_cyclic_identification.html",
            "mechanical/SMA_T.html",
            "hyperelasticity/GOH2006_tube_inflation.html",
            "mechanical/MODUL.html",
        ],
    },
    "fedoo": {
        "gallery": "https://3mah.github.io/fedoo-docs/stable/examples/index.html",
        "docs": "https://3mah.github.io/fedoo-docs/stable/",
        "featured": [
            "boundary_conditions/periodic_bc_3d_gyroid_off_axis.html",
            "contact/tube_compression.html",
            "contact/ipc_indentation_2d.html",
            "homogenization/periodic_homogenization.html",
            "contact/ipc_gyroid_compression.html",
            "basic/lattice_beam.html",
        ],
    },
    "microgen": {
        "gallery": "https://3mah.github.io/microgen-docs/examples/index.html",
        "docs": "https://3mah.github.io/microgen-docs/",
        "featured": [
            "TPMS/graded_density.html",
            "TPMS/graded_cell_type.html",
            "TPMS/infill_bunny.html",
            "Spinodoids/spinodoid.html",
            "3Doperations/voronoi.html",
            "Mesh/periodic_gyroid_remesh.html",
        ],
    },
}

UA = {"User-Agent": "3mah-site-builder"}
H2 = re.compile(r"<h2>(.*?)<a class=\"headerlink\"", re.S)
THUMB = re.compile(
    r'<div class="sphx-glr-thumbcontainer"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*>'
    r'.*?<a class="reference internal" href="([^"]+)"'
    r'.*?<div class="sphx-glr-thumbnail-title">(.*?)</div>',
    re.S,
)


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_gallery(lib, url):
    page = fetch(url)
    sections = [(m.start(), strip_tags(m.group(1))) for m in H2.finditer(page)]
    examples, seen = [], set()
    for m in THUMB.finditer(page):
        link = urljoin(url, m.group(2))
        if link in seen:
            continue
        seen.add(link)
        section = next((t for pos, t in reversed(sections) if pos < m.start()), "Examples")
        examples.append({
            "library": lib,
            "section": section,
            "title": strip_tags(m.group(3)),
            "url": link,
            "thumbnail": urljoin(url, m.group(1)),
        })
    return examples


LEGACY_SECTION = re.compile(
    r'<section id="([^"]+)">\s*<h2>(.*?)<a class="headerlink".*?<img[^>]*src="([^"]+)"', re.S)
H1 = re.compile(r"<h1>(.*?)<a class=\"headerlink\"", re.S)


def parse_legacy(lib, pages):
    """Older docs without sphinx-gallery: one example per <h2> section with an image."""
    examples = []
    for url in pages:
        page = fetch(url)
        h1 = H1.search(page)
        section = strip_tags(h1.group(1)) if h1 else "Examples"
        for m in LEGACY_SECTION.finditer(page):
            examples.append({
                "library": lib,
                "section": section,
                "title": strip_tags(m.group(2)),
                "url": f"{url}#{m.group(1)}",
                "thumbnail": urljoin(url, m.group(3)),
            })
    return examples


def card(ex):
    title = html.escape(ex["title"])
    return (
        f'<a class="example-card" href="{ex["url"]}" data-library="{ex["library"]}">'
        f'<img src="{ex["thumbnail"]}" alt="" loading="lazy">'
        f'<span class="example-card__lib example-card__lib--{ex["library"]}">{ex["library"]}</span>'
        f'<span class="example-card__title">{title}</span>'
        f'<span class="example-card__section">{html.escape(ex["section"])}</span></a>'
    )


def fallback_card(lib, cfg):
    return (
        f'<a class="example-card example-card--fallback" href="{cfg["docs"]}" data-library="{lib}">'
        f'<span class="example-card__lib example-card__lib--{lib}">{lib}</span>'
        f'<span class="example-card__title">Browse the {lib} documentation</span>'
        f'<span class="example-card__section">The example gallery is being republished</span></a>'
    )


def main():
    all_examples, status = [], {}
    for lib, cfg in LIBRARIES.items():
        try:
            found = parse_gallery(lib, cfg["gallery"])
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"[warn] {lib}: gallery unavailable ({e})", file=sys.stderr)
            found = []
        if not found and cfg.get("legacy_pages"):
            try:
                found = parse_legacy(lib, cfg["legacy_pages"])
                print(f"[info] {lib}: using {len(found)} examples from the legacy example pages",
                      file=sys.stderr)
            except (urllib.error.URLError, TimeoutError) as e:
                print(f"[warn] {lib}: legacy pages unavailable ({e})", file=sys.stderr)
        status[lib] = len(found)
        all_examples.extend(found)
        print(f"{lib}: {len(found)} examples")

    # Unified gallery page
    chips = ['<button class="example-filter is-active" data-filter="all">All '
             f'<span>{len(all_examples)}</span></button>']
    chips += [f'<button class="example-filter" data-filter="{lib}">{lib}'
              + (f' <span>{n}</span>' if n else "") + "</button>"
              for lib, n in status.items()]
    cards = [card(e) for e in all_examples]
    cards += [fallback_card(lib, cfg) for lib, cfg in LIBRARIES.items() if not status[lib]]
    page = (
        "---\n"
        "title: Examples\n"
        "description: Every example of simcoon, fedoo and microgen in one place — "
        "constitutive laws, finite element analyses, homogenization, TPMS and lattice generation.\n"
        "hide:\n- navigation\n- toc\n"
        "---\n\n"
        "<!-- Generated by scripts/build_examples.py — do not edit by hand. -->\n\n"
        "# Examples\n\n"
        "All the runnable examples of the three libraries, gathered from their documentation. "
        "Each card opens the example — code, figures and explanations — in the library's documentation.\n\n"
        f'<div class="example-filters">\n{"".join(chips)}\n</div>\n\n'
        f'<div class="example-grid">\n' + "\n".join(cards) + "\n</div>\n"
    )
    (ROOT / "docs" / "examples.md").write_text(page, encoding="utf-8")

    # Featured examples per library (included in the library pages)
    snip = ROOT / "snippets"
    snip.mkdir(exist_ok=True)
    for lib, cfg in LIBRARIES.items():
        mine = [e for e in all_examples if e["library"] == lib]
        # Hand-picked examples (matched on the end of their URL), else the first six
        picked = [e for key in cfg["featured"] for e in mine if e["url"].endswith("/" + key)]
        mine = picked or mine[:6]
        body = "\n".join(card(e) for e in mine) if mine else fallback_card(lib, cfg)
        (snip / f"examples_{lib}.md").write_text(
            "<!-- Generated by scripts/build_examples.py -->\n"
            f'<div class="example-grid example-grid--compact">\n{body}\n</div>\n',
            encoding="utf-8",
        )

    data = ROOT / "docs" / "assets" / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "examples.json").write_text(json.dumps(all_examples, indent=1, ensure_ascii=False),
                                        encoding="utf-8")


if __name__ == "__main__":
    main()
