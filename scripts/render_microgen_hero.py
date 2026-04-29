"""Render the Microgen hero — graded gyroid with the triangular mesh
visible, in brand-orange.

Used as the headline image in the Microgen showcase block (full-width)
on the homepage. Landscape aspect ratio, no PBR, edges on.
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
OUT = REPO / "assets" / "images" / "index" / "microgen" / "microgen_hero.png"

# Landscape banner aspect, suitable for a full-width showcase block.
WINDOW = (3000, 1500)

MICROGEN_RAMP = LinearSegmentedColormap.from_list(
    "microgen_ramp",
    [
        (0.00, "#fff5e8"),  # palest cream
        (0.35, "#ffd9a8"),  # warm peach
        (0.65, "#ee7d30"),  # microgen brand orange
        (1.00, "#a14114"),  # deep burnt orange
    ],
)


def main():
    mesh = pv.read(INPUTS / "gyroid_graded.vtk")
    if not mesh.is_all_triangles:
        mesh = mesh.triangulate()
    mesh = mesh.clean()

    pts = np.asarray(mesh.points)
    mesh.point_data["x"] = pts[:, 0].astype(np.float32)

    p = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    p.set_background("#ffffff", top="#f1ebe2")
    p.enable_anti_aliasing("ssaa")

    p.add_mesh(
        mesh,
        scalars="x",
        cmap=MICROGEN_RAMP,
        show_scalar_bar=False,
        show_edges=True,
        edge_color=(0.18, 0.12, 0.08),
        line_width=0.35,
        smooth_shading=False,
        ambient=0.40,
        diffuse=0.72,
        specular=0.05,
        specular_power=8,
        opacity=1.0,
    )

    # The graded gyroid extends along +x; view from the front-right slightly
    # above so the grading reads left-to-right across the wide frame.
    bounds = mesh.bounds
    cx = 0.5 * (bounds[0] + bounds[1])
    span = bounds[1] - bounds[0]
    p.camera_position = [(cx + 0.5 * span, -2.4 * span, 1.5 * span),
                          (cx, 0.0, 0.0),
                          (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=bounds)
    p.camera_position = [(cx + 0.5 * span, -2.4 * span, 1.5 * span),
                          (cx, 0.0, 0.0),
                          (0.0, 0.0, 1.0)]
    p.camera.zoom(1.30)

    p.screenshot(str(OUT), return_img=False)
    p.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
