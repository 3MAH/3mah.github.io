# Render scripts

Generate every PNG that lives under `assets/images/index/{simcoon,fedoo,microgen}/`.
The scripts are not run by Jekyll — they are run **once** locally, and their
output PNGs are committed alongside the rest of the site.

## Layout

| File | What it produces |
| --- | --- |
| `render_simcoon.py` | Mori-Tanaka homogenization, directional stiffness rose, SMA loop, yield surfaces. Pure matplotlib + simcoon. Quick (< 10 s). |
| `render_simcoon_identification.py` | Drives the new `EPCHA` Chaboche cyclic identification example merged into simcoon master — fits 7 parameters from 3 cyclic uniaxial tests via differential evolution and saves a brand-styled experiment-vs-fit plot to `simcoon_chaboche_identification.png`. Needs the simcoon source tree (defaults to `~/Documents/GitHub/simcoon`, override with `SIMCOON_REPO=…`); takes 1–2 min. |
| `render_fedoo.py` | All `assets/images/index/fedoo/*.png` (plate with hole, Kelvin RVE periodic homog, IPC indentation, tube-compression triptych, beam lattice, shell pressure, hero square). Uses fedoo + simcoon (EPCHA / EPICP UMATs) + pyvista. |
| `render_microgen.py` | TPMS hero stack: cylinder, sphere, helix sweep, graded gyroid, surfaces grid, warm-cylinder variant. Pure pyvista, reads VTK meshes from `_render_inputs/`. |
| `render_microgen_hero.py` | Mesh-edge close-up of the graded gyroid (`microgen_hero.png`). |
| `render_banner_cylinder.py` | Splash banner image (`tpms_cylinder.png` — light-themed cylindrical gyroid with mesh visible). |
| `render_voronoi.py` | 3D Voronoi polycrystal tile (`voronoi_polycrystal.png`). Pure scipy + pyvista, no mesh input. |

## Inputs

The microgen and fedoo renders need TPMS / lattice / Kelvin meshes — 14
files totalling ~330 MB. They are too large for git and are kept locally
(uncommitted, gitignored) at:

```
_render_inputs/
├── Kelvin.vtk             # truncated-octahedron RVE for periodic homog
├── cylinder_g5_tpms.vtk   # gyroid wrapped on a cylinder
├── gyroid_graded.vtk      # spatially graded gyroid
├── sphere_g4_tpms.vtk     # gyroid wrapped on a sphere
├── sweep_g7_helix.vtk     # gyroid swept along a helix
└── surfaces_0.vtp … surfaces_8.vtp   # 9 unit-cell TPMS for the surfaces grid
```

The meshes were generated with
[microgen](https://3mah.github.io/microgen-docs/); the recipes are in
its example gallery.

If/when these stabilise and become worth archiving, `scripts/fetch_inputs.py`
is ready to download them from a Zenodo deposit (set `ZENODO_RECORD` in
that file once a record is published; the SHA-256 manifest is already
pinned). For now, the file is dormant.

## Running

Each script picks the right conda env from the comment block; in practice the
following works on macOS:

```bash
# the simcoon / matplotlib charts
conda activate 3mah && python scripts/render_simcoon.py
conda activate 3mah && python scripts/render_voronoi.py
conda activate 3mah && python scripts/render_microgen.py
conda activate 3mah && python scripts/render_microgen_hero.py
conda activate 3mah && python scripts/render_banner_cylinder.py

# fedoo simulations need its own env
conda activate fedoo && python scripts/render_fedoo.py
```

`render_fedoo.py:render_tube_compression` writes ~600 MB of intermediate
`.fdz` archives to a `tempfile.mkdtemp(prefix="fedoo_tube_")` directory and
unconditionally wipes them in a `finally` block. Stale `fedoo_tube_*` dirs
from earlier crashed runs are also swept on startup so the disk stays sane.

## After regenerating

1. `bundle exec jekyll build` (in the `jekyll` conda env) to regenerate `_site/`.
2. `git status` — only the changed PNGs and any source edits should appear;
   the `_render_inputs/`, `results/`, `examples/`, `_site/` and `.fdz`
   directories are gitignored and will not show.
