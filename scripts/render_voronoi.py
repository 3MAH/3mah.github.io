"""Render a 3D Voronoi polycrystal tile + grain-by-grain animation.

Builds a 3D Voronoi tessellation from random seeds in a unit cube using
scipy, clips the open cells off and writes:
- ``voronoi_polycrystal.png`` — final composition (static)
- ``voronoi_polycrystal.gif`` — same tessellation built up one grain per
  frame, used in the microgen showcase to convey the construction.
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
OUT_VIDEO = OUT / "voronoi_polycrystal.mp4"

WINDOW = (1600, 1600)
# Even dimensions required by the H.264 encoder (libx264/yuv420p)
VIDEO_WINDOW = (960, 960)


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

    palette = [
        "#ee7d30", "#f4a26b", "#c45f1a", "#f8c190",
        "#a14114", "#ffd9b1", "#7a3a14", "#fbe2c8",
        "#d96e1f", "#ffb27a", "#893010", "#ffe4cb",
    ]

    # Pre-build all bounded polyhedra once — used both for the static
    # render and (in the same order) for the grain-by-grain animation.
    polyhedra = []
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
        polyhedra.append(poly)

    def _setup(plotter):
        plotter.set_background("#f6f8fb", top="#dde4ec")
        plotter.enable_anti_aliasing("ssaa")
        plotter.camera_position = [(2.5, -2.5, 2.0), (0.5, 0.5, 0.5), (0, 0, 1)]
        plotter.reset_camera(bounds=(0, 1, 0, 1, 0, 1))
        plotter.camera.zoom(1.10)

    # ----- 1) static composite render --------------------------------------
    plotter = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    _setup(plotter)
    for i, poly in enumerate(polyhedra):
        plotter.add_mesh(
            poly,
            color=palette[i % len(palette)],
            show_edges=True, edge_color="#1f1411", line_width=0.6,
            smooth_shading=False,
            ambient=0.30, diffuse=0.78, specular=0.10, specular_power=12,
        )
    plotter.screenshot(str(OUT_PATH))
    plotter.close()
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.0f} KB)  "
          f"({len(polyhedra)} grains)")

    # ----- 2) grain-by-grain MP4 -------------------------------------------
    movie = pv.Plotter(off_screen=True, window_size=VIDEO_WINDOW, lighting="three lights")
    _setup(movie)
    movie.open_movie(str(OUT_VIDEO), framerate=12, quality=7)
    # Hold the empty unit cube for a beat
    for _ in range(6):
        movie.write_frame()
    for i, poly in enumerate(polyhedra):
        movie.add_mesh(
            poly,
            color=palette[i % len(palette)],
            show_edges=True, edge_color="#1f1411", line_width=0.6,
            smooth_shading=False,
            ambient=0.30, diffuse=0.78, specular=0.10, specular_power=12,
        )
        movie.write_frame()
    # Hold the final filled tessellation
    for _ in range(20):
        movie.write_frame()
    movie.close()
    print(f"wrote {OUT_VIDEO} ({OUT_VIDEO.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
