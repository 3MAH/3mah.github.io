"""Re-render the Microgen hero tile so the mesh itself is visible.

Goal: replace the PBR/magma close-up with a high-resolution view that
showcases the actual triangular mesh (edges on, flat shading, no metallic
look). Used for the small hero tile in the Microgen section of index.md.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv

pv.OFF_SCREEN = True
pv.global_theme.allow_empty_mesh = True

REPO = Path(__file__).resolve().parent.parent
INPUTS = REPO / "_render_inputs"
OUT = REPO / "assets" / "images" / "index" / "microgen" / "microgen_hero.png"

WINDOW = (2200, 2200)


def main():
    mesh = pv.read(INPUTS / "gyroid_graded.vtk")
    if not mesh.is_all_triangles:
        mesh = mesh.triangulate()
    mesh = mesh.clean()

    pts = np.asarray(mesh.points)
    mesh.point_data["x"] = pts[:, 0].astype(np.float32)

    p = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    p.set_background("#ffffff", top="#e8edf3")
    p.enable_anti_aliasing("ssaa")

    p.add_mesh(
        mesh,
        scalars="x",
        cmap="Blues",
        show_scalar_bar=False,
        show_edges=True,
        edge_color=(0.18, 0.22, 0.30),
        line_width=0.4,
        smooth_shading=False,
        ambient=0.35,
        diffuse=0.75,
        specular=0.05,
        specular_power=8,
        opacity=1.0,
    )

    p.camera_position = [(4.0, -3.5, 2.6), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(4.0, -3.5, 2.6), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.4)

    p.screenshot(str(OUT), return_img=False)
    p.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
