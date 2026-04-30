"""Render a TPMS morphing movie for the microgen showcase.

Inspired by microgen's reference ``graded_cell_type_density_movie.py`` —
walks gyroid → schwarzP → schwarzD → neovius → schoenIWP → schoenFRD →
fischerKochS → pmy → honeycomb → lidinoid → split_p → gyroid, blending
neighbours via a tanh weight on a linear superposition of implicit
functions.

Differences from the reference:
- Higher marching-cubes resolution so the TPMS-meets-cube exit curves
  are smooth rather than jagged.
- Vertices within 1e-3 of a cube face are snapped to that face exactly,
  so the box-face cuts are planar to double precision.
- Phong smooth shading with a feature-angle split, so the cube-face
  creases stay sharp while the TPMS interior shades smoothly.
- Brand-orange microgen colormap (matches the logo / showcase styling)
  instead of the default viridis.

Output: assets/images/index/microgen/microgen_morph.mp4
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pyvista as pv
from matplotlib.colors import LinearSegmentedColormap
from microgen import Tpms
from microgen.shape.surface_functions import (
    fischerKochS,
    gyroid,
    honeycomb,
    lidinoid,
    neovius,
    pmy,
    schoenFRD,
    schoenIWP,
    schwarzD,
    schwarzP,
    split_p,
)

pv.OFF_SCREEN = True
pv.global_theme.allow_empty_mesh = True

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "index" / "microgen" / "microgen_morph.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

WINDOW = (1024, 768)  # matches the CSMA reference; even for libx264

MICROGEN_RAMP = LinearSegmentedColormap.from_list(
    "microgen_ramp",
    [
        (0.00, "#fff5e8"),
        (0.35, "#ffd9a8"),
        (0.65, "#ee7d30"),
        (1.00, "#a14114"),
    ],
)

PHI_SEQUENCE = [
    gyroid, schwarzP, schwarzD, neovius, schoenIWP, schoenFRD,
    fischerKochS, pmy, honeycomb, lidinoid, split_p, gyroid,
]


def digraded(x, y, z, phi_pair, frame: float):
    return (1.0 - frame) * phi_pair[0](x, y, z) + frame * phi_pair[1](x, y, z)


def main():
    transition_width = 1.0
    n_frames_per_pair = 20
    tpms_resolution = 45    # 50% above the reference's 30, enough to smooth
                            # the TPMS-cube exit curves without blowing up
                            # render cost (scales as resolution^3).

    pl = pv.Plotter(off_screen=True, window_size=WINDOW)
    pl.set_background("white")
    pl.camera.position = (1.5, 2.5, 2.0)
    pl.camera.Roll(45.0)
    pl.camera.Elevation(60.0)
    pl.camera.Azimuth(30.0)

    pl.open_movie(str(OUT), framerate=24, quality=8)

    for i in range(len(PHI_SEQUENCE) - 1):
        phi = PHI_SEQUENCE[i: i + 2]
        for f in np.linspace(0.0, 1.0, n_frames_per_pair):
            morph = (
                0.5 * np.tanh((2.0 * (f - 0.5)) * np.exp(1) / transition_width)
                + 0.5
            )
            geom = Tpms(
                surface_function=lambda x, y, z, _phi=phi, _m=morph: digraded(
                    x, y, z, _phi, _m
                ),
                density=0.3,
                cell_size=1.0,
                repeat_cell=(1, 1, 1),
                resolution=tpms_resolution,
            )
            shape = geom.generate_vtk(type_part="sheet").extract_surface()

            # Snap vertices within 1e-3 of any cube face onto that face,
            # so the box-face cuts are planar to double precision.
            pts = np.asarray(shape.points).copy()
            for axis in range(3):
                pts[np.abs(pts[:, axis] + 0.5) < 1e-3, axis] = -0.5
                pts[np.abs(pts[:, axis] - 0.5) < 1e-3, axis] =  0.5
            shape.points = pts
            # Sharp Phong creases at the TPMS-meets-cube dihedrals.
            shape = shape.compute_normals(
                cell_normals=False, point_normals=True,
                consistent_normals=True, auto_orient_normals=True,
                split_vertices=True, feature_angle=30.0,
            )

            pl.clear()
            shape["distances"] = np.linalg.norm(np.asarray(shape.points), axis=1)
            pl.add_mesh(
                shape,
                scalars="distances",
                cmap=MICROGEN_RAMP,
                clim=[0.0, 1.0],
                smooth_shading=True,
                specular=0.6,
                show_scalar_bar=False,
            )
            pl.write_frame()
            print(f"   pair {i+1}/{len(PHI_SEQUENCE) - 1}  frame {f:.2f}")

    pl.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
