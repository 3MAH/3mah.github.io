# Render scripts

Generate every PNG that lives under `assets/images/index/{simcoon,fedoo,microgen}/`.
The scripts are not run by Jekyll — they are run **once** locally, and their
output PNGs are committed alongside the rest of the site.

## Layout

| File | What it produces |
| --- | --- |
| `render_simcoon.py` | All `assets/images/index/simcoon/*.png` (Chaboche EPCHA hysteresis, Mori-Tanaka homogenization, directional stiffness rose, SMA loop, yield surfaces). Pure matplotlib + simcoon. |
| `render_fedoo.py` | All `assets/images/index/fedoo/*.png` (plate with hole, Kelvin RVE periodic homog, IPC indentation, tube-compression triptych, beam lattice, shell pressure, hero square). Uses fedoo + simcoon (EPCHA / EPICP UMATs) + pyvista. |
| `render_microgen.py` | TPMS hero stack: cylinder, sphere, helix sweep, graded gyroid, surfaces grid, warm-cylinder variant. Pure pyvista, reads VTK meshes from `_render_inputs/`. |
| `render_microgen_hero.py` | Mesh-edge close-up of the graded gyroid (`microgen_hero.png`). |
| `render_banner_cylinder.py` | Splash banner image (`tpms_cylinder.png` — light-themed cylindrical gyroid with mesh visible). |
| `render_voronoi.py` | 3D Voronoi polycrystal tile (`voronoi_polycrystal.png`). Pure scipy + pyvista, no mesh input. |

## Inputs

The Microgen and fedoo renders need TPMS / lattice / Kelvin meshes. They are
**not committed** (each is 10 – 200 MB) but expected at:

```
_render_inputs/
├── Kelvin.vtk             # truncated-octahedron RVE for periodic homog
├── cylinder_g5_tpms.vtk   # gyroid wrapped on a cylinder
├── gyroid_graded.vtk      # spatially graded gyroid
├── sphere_g4_tpms.vtk     # gyroid wrapped on a sphere
├── sweep_g7_helix.vtk     # gyroid swept along a helix
└── surfaces_0.vtp … surfaces_8.vtp   # 9 unit-cell TPMS for the surfaces grid
```

These files were generated with [Microgen](https://3mah.github.io/microgen-docs/).
If you need to regenerate them, the recipes are in the Microgen examples
(see `microgen-docs/examples/...`); the on-disk copies in this repo's
`_render_inputs/` are also kept around locally for convenience.

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
