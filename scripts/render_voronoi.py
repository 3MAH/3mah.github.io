"""Render a 3D Voronoi polycrystal tile for the Microgen section.

Builds a 3D Voronoi tessellation from random seeds in a unit cube using
scipy, clips the open cells off and writes a PyVista PBR-style render
matching the rest of the Microgen tiles. Output:
    assets/images/index/microgen/examples/voronoi_polycrystal.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv
from scipy.spatial import Voronoi

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "index" / "microgen" / "examples"
OUT.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT / "voronoi_polycrystal.png"

WINDOW = (1600, 1600)


def main(n_seeds: int = 80, seed: int = 7):
    rng = np.random.default_rng(seed)

    # Replicate seeds across 26 surrounding cells so that cells of seeds
    # near the central cube boundary become bounded polyhedra.
    seeds = rng.uniform(0.0, 1.0, size=(n_seeds, 3))
    shifts = np.array([(i, j, k) for i in (-1, 0, 1)
                                  for j in (-1, 0, 1)
                                  for k in (-1, 0, 1)])
    repeated = (seeds[None, :, :] + shifts[:, None, :]).reshape(-1, 3)
    # The 'central' seeds occupy indices [13*n_seeds : 14*n_seeds]
    central_offset = 13 * n_seeds

    vor = Voronoi(repeated)

    plotter = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    plotter.set_background("#f6f8fb", top="#dde4ec")
    plotter.enable_anti_aliasing("ssaa")

    palette = [
        "#ee7d30", "#f4a26b", "#c45f1a", "#f8c190",
        "#a14114", "#ffd9b1", "#7a3a14", "#fbe2c8",
        "#d96e1f", "#ffb27a", "#893010", "#ffe4cb",
    ]

    actor_count = 0
    for k in range(n_seeds):
        region_idx = vor.point_region[central_offset + k]
        region = vor.regions[region_idx]
        if not region or -1 in region:
            continue
        verts = vor.vertices[region]
        try:
            poly = pv.PolyData(verts).delaunay_3d().extract_surface()
        except Exception:
            continue
        plotter.add_mesh(
            poly,
            color=palette[actor_count % len(palette)],
            show_edges=True,
            edge_color="#1f1411",
            line_width=0.6,
            smooth_shading=False,
            ambient=0.30, diffuse=0.78, specular=0.10, specular_power=12,
        )
        actor_count += 1

    plotter.camera_position = [(2.5, -2.5, 2.0), (0.5, 0.5, 0.5), (0, 0, 1)]
    plotter.reset_camera(bounds=(0, 1, 0, 1, 0, 1))
    plotter.camera.zoom(1.10)
    plotter.screenshot(str(OUT_PATH))
    plotter.close()
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.0f} KB) with {actor_count} grains")


if __name__ == "__main__":
    main()
