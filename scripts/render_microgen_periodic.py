"""Render a periodic-mesh demonstration: a single TPMS unit cell tiled
across space so the seamless periodicity reads visually.

Used as the "periodic" half of the Microgen showcase block on the
homepage (the "graded" half stays as the graded gyroid).
Output: assets/images/index/microgen/microgen_periodic.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv
from matplotlib.colors import LinearSegmentedColormap

pv.OFF_SCREEN = True
pv.global_theme.allow_empty_mesh = True

REPO = Path(__file__).resolve().parent.parent
INPUTS = REPO / "_render_inputs"
OUT = REPO / "assets" / "images" / "index" / "microgen" / "microgen_periodic.png"

WINDOW = (3000, 1500)

MICROGEN_RAMP = LinearSegmentedColormap.from_list(
    "microgen_ramp",
    [
        (0.00, "#fff5e8"),
        (0.35, "#ffd9a8"),
        (0.65, "#ee7d30"),
        (1.00, "#a14114"),
    ],
)


def main():
    # Use the centered unit cell (bounds ~ [-0.5, 0.5]³); the periodic mesh
    # should stitch seamlessly when translated by integer multiples of the
    # cell extent.
    cell = pv.read(INPUTS / "surfaces_4.vtp")
    if not cell.is_all_triangles:
        cell = cell.triangulate()
    cell = cell.clean()

    bounds = np.array(cell.bounds)
    extent = bounds[1::2] - bounds[0::2]   # (Lx, Ly, Lz)

    # Tile 3 × 2 × 1 — wide aspect to fit the banner. All tiles share a
    # single solid colour so that periodicity reads as identical units
    # repeating, with no spurious colour gradient hinting at variation.
    tiles = []
    for ix in range(3):
        for iy in range(2):
            t = cell.copy()
            t.translate((ix * extent[0], iy * extent[1], 0.0), inplace=True)
            tiles.append(t)
    tiled = pv.MultiBlock(tiles).combine()

    p = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    p.set_background("#ffffff", top="#f1ebe2")
    p.enable_anti_aliasing("ssaa")

    # Mid-range warm orange sampled from MICROGEN_RAMP (~50 % into the
    # ramp). Single solid colour, just shading + edges to give depth.
    SOLID = MICROGEN_RAMP(0.55)

    p.add_mesh(
        tiled,
        color=SOLID,
        show_edges=True,
        edge_color=(0.18, 0.12, 0.08),
        line_width=0.30,
        smooth_shading=False,
        ambient=0.40,
        diffuse=0.72,
        specular=0.05,
        specular_power=8,
        opacity=1.0,
    )

    # Frame the 3×2 array, slight 3/4 perspective.
    bounds_all = tiled.bounds
    cx = 0.5 * (bounds_all[0] + bounds_all[1])
    cy = 0.5 * (bounds_all[2] + bounds_all[3])
    span = max(bounds_all[1] - bounds_all[0], bounds_all[3] - bounds_all[2])
    p.camera_position = [
        (cx + 0.20 * span, cy - 1.6 * span, 1.1 * span),
        (cx, cy, 0.0),
        (0.0, 0.0, 1.0),
    ]
    p.reset_camera(bounds=bounds_all)
    p.camera_position = [
        (cx + 0.20 * span, cy - 1.6 * span, 1.1 * span),
        (cx, cy, 0.0),
        (0.0, 0.0, 1.0),
    ]
    p.camera.zoom(1.30)

    p.screenshot(str(OUT), return_img=False)
    p.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
