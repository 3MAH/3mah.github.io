"""Re-render the splash banner: cylindrical gyroid in the same light/edges
style as the Microgen hero tile (white-to-blue, mesh visible, no PBR).

Replaces assets/images/index/microgen/tpms_cylinder.png. The splash header
in index.md uses this as `overlay_image` (and also as the site-wide
og_image), so it doubles as the social-card preview.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv

pv.OFF_SCREEN = True
pv.global_theme.allow_empty_mesh = True

REPO = Path(__file__).resolve().parent.parent
INPUTS = REPO / "_render_inputs"
OUT = REPO / "assets" / "images" / "index" / "microgen" / "tpms_cylinder.png"

WINDOW = (2600, 1300)  # wide landscape for splash header


def main():
    mesh = pv.read(INPUTS / "cylinder_g5_tpms.vtk")
    if not mesh.is_all_triangles:
        mesh = mesh.triangulate()
    mesh = mesh.clean()

    pts = np.asarray(mesh.points)
    # Drive the colormap with z (cylinder axis) so the white-to-blue gradient
    # runs along the cylinder length.
    mesh.point_data["axis"] = pts[:, 2].astype(np.float32)

    p = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    p.set_background("#ffffff", top="#dde6f1")
    p.enable_anti_aliasing("ssaa")

    p.add_mesh(
        mesh,
        scalars="axis",
        cmap="Blues",
        show_scalar_bar=False,
        show_edges=True,
        edge_color=(0.18, 0.24, 0.34),
        line_width=0.35,
        smooth_shading=False,
        ambient=0.40,
        diffuse=0.70,
        specular=0.05,
        specular_power=8,
        opacity=1.0,
    )

    # Camera: bring the cylinder roughly horizontal across the wide frame.
    # Cylinder axis is +Z in source; we tilt it down so it sweeps across.
    p.camera_position = [(8.5, -7.0, 4.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(8.5, -7.0, 4.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.30)

    p.screenshot(str(OUT), return_img=False)
    p.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
