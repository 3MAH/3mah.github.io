"""Render a TPMS morphing movie for the microgen showcase.

Adapted from microgen's ``graded_cell_type_density_movie.py``: walks
through eleven different TPMS surface families (gyroid → schwarzP →
schwarzD → neovius → schoenIWP → schoenFRD → fischerKochS → pmy →
honeycomb → lidinoid → split_p → gyroid), interpolating between
neighbours via a tanh weight. The result is a continuous loop of TPMS
shapes for the homepage.

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

WINDOW = (1080, 1080)  # even dimensions for libx264

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
    n_frames_per_pair = 16
    tpms_resolution = 70    # marching-cubes resolution. Sharp box-face cuts
                            # come from split-vertex normals (below), not
                            # from cranking this — 70 is plenty.

    pl = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="three lights")
    pl.set_background("#ffffff", top="#f1ebe2")
    pl.enable_anti_aliasing("ssaa")
    pl.camera.position = (1.5, 2.5, 2.0)
    pl.camera.Roll(45.0)
    pl.camera.Elevation(60.0)
    pl.camera.Azimuth(30.0)

    pl.open_movie(str(OUT), framerate=12, quality=7)

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
            shape = geom.generateVtk(type_part="sheet").extract_surface()
            # Split vertices at sharp feature edges (TPMS-meets-cube
            # dihedrals): keeps Phong shading smooth across the curved
            # TPMS surface while preserving sharp creases at the box cuts.
            shape = shape.compute_normals(
                cell_normals=False, point_normals=True,
                consistent_normals=True, auto_orient_normals=True,
                split_vertices=True,
                feature_angle=30.0,
            )

            pl.clear_actors()
            pts = np.asarray(shape.points)
            shape["dist"] = np.linalg.norm(pts, axis=1).astype(np.float32)
            pl.add_mesh(
                shape,
                scalars="dist",
                cmap=MICROGEN_RAMP,
                show_scalar_bar=False,
                smooth_shading=True,
                ambient=0.40, diffuse=0.72, specular=0.06, specular_power=10,
            )
            pl.write_frame()
            print(f"   pair {i+1}/{len(PHI_SEQUENCE) - 1}  frame {f:.2f}")

    pl.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
