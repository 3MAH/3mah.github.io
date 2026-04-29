"""Render hero-quality PNGs of Microgen TPMS meshes for the 3MAH website.

Uses PyVista off-screen rendering with PBR shaders, SSAA anti-aliasing,
shadows, environment lighting, and tasteful per-image color palettes.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pyvista as pv

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
pv.OFF_SCREEN = True
pv.global_theme.transparent_background = False
pv.global_theme.allow_empty_mesh = True

REPO = Path(__file__).resolve().parent.parent
INPUTS = REPO / "_render_inputs"
OUT = REPO / "assets" / "images" / "index" / "microgen"
OUT.mkdir(parents=True, exist_ok=True)

WIDE = (1600, 1000)
SQUARE = (1200, 1200)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def prep(mesh: pv.PolyData) -> pv.PolyData:
    """Triangulate, clean and compute smooth normals on a PolyData mesh."""
    m = mesh
    if not m.is_all_triangles:
        m = m.triangulate()
    m = m.clean()
    m = m.compute_normals(
        cell_normals=False,
        point_normals=True,
        consistent_normals=True,
        auto_orient_normals=True,
        split_vertices=False,
        flip_normals=False,
        non_manifold_traversal=False,
    )
    return m


def add_scalar(mesh: pv.PolyData, axis: str = "z") -> pv.PolyData:
    """Append a coordinate-based scalar field to drive colormaps."""
    pts = np.asarray(mesh.points)
    idx = {"x": 0, "y": 1, "z": 2}[axis]
    s = pts[:, idx]
    mesh = mesh.copy()
    mesh.point_data["height"] = s.astype(np.float32)
    # also a radial scalar (XY plane radius)
    r = np.sqrt(pts[:, 0] ** 2 + pts[:, 1] ** 2)
    mesh.point_data["radius"] = r.astype(np.float32)
    return mesh


def studio_lighting(plotter: pv.Plotter, intensity: float = 1.0) -> None:
    """Three-point studio rig: key, fill, rim."""
    plotter.remove_all_lights()
    key = pv.Light(
        position=(4, -3, 6),
        focal_point=(0, 0, 0),
        color="white",
        intensity=1.0 * intensity,
        light_type="scene light",
    )
    key.positional = False
    fill = pv.Light(
        position=(-5, -4, 2),
        focal_point=(0, 0, 0),
        color=(0.85, 0.9, 1.0),
        intensity=0.45 * intensity,
        light_type="scene light",
    )
    rim = pv.Light(
        position=(-1, 5, 3),
        focal_point=(0, 0, 0),
        color=(1.0, 0.85, 0.7),
        intensity=0.55 * intensity,
        light_type="scene light",
    )
    head = pv.Light(light_type="headlight", intensity=0.15 * intensity)
    plotter.add_light(key)
    plotter.add_light(fill)
    plotter.add_light(rim)
    plotter.add_light(head)


def make_plotter(window_size, background_top="#f3f6fa", background_bottom="#cfd6e0"):
    p = pv.Plotter(off_screen=True, window_size=window_size, lighting="none")
    p.set_background(background_top, top=background_bottom)
    p.enable_anti_aliasing("ssaa")
    try:
        p.enable_eye_dome_lighting()
        p.disable_eye_dome_lighting()  # we want PBR; just ensure init ok
    except Exception:
        pass
    return p


def safe_pbr_kwargs(metallic=0.35, roughness=0.4):
    return dict(pbr=True, metallic=metallic, roughness=roughness, smooth_shading=True)


def shoot(plotter: pv.Plotter, path: Path, transparent=False):
    img = plotter.screenshot(
        filename=str(path),
        transparent_background=transparent,
        return_img=True,
    )
    plotter.close()
    print(f"  -> wrote {path} ({path.stat().st_size/1024:.0f} KB)")
    return img


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------
def render_cylinder(out: Path, window_size=WIDE, square=False):
    print("[1/6] cylinder TPMS...")
    mesh = pv.read(INPUTS / "cylinder_g5_tpms.vtk")
    mesh = prep(mesh)
    mesh = add_scalar(mesh, axis="z")

    p = make_plotter(window_size, "#11161f", "#1e2a40")
    studio_lighting(p, intensity=1.0)
    p.add_mesh(
        mesh,
        scalars="height",
        cmap="cividis",
        show_scalar_bar=False,
        clim=[mesh.point_data["height"].min(), mesh.point_data["height"].max()],
        **safe_pbr_kwargs(metallic=0.55, roughness=0.32),
    )
    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    # Camera: slight perspective, slightly above
    p.camera_position = [
        (7.5, -8.5, 6.5),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
    ]
    p.camera.view_angle = 24
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(7.5, -8.5, 6.5), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.25)
    shoot(p, out)


def render_sphere(out: Path, window_size=WIDE):
    print("[2/6] sphere TPMS (large file)...")
    mesh = pv.read(INPUTS / "sphere_g4_tpms.vtk")
    # Decimate to keep it snappy; PolyData is huge.
    mesh = prep(mesh)
    if mesh.n_cells > 800_000:
        try:
            mesh = mesh.decimate(0.55)
            mesh = mesh.compute_normals(auto_orient_normals=True, split_vertices=False)
        except Exception as e:
            print(f"  decimate skipped: {e}")
    mesh = add_scalar(mesh, axis="z")

    p = make_plotter(window_size, "#fdf6ec", "#dbb98a")
    studio_lighting(p, intensity=1.4)
    p.add_mesh(
        mesh,
        scalars="height",
        cmap="YlOrBr_r",
        show_scalar_bar=False,
        clim=[mesh.point_data["height"].min(), mesh.point_data["height"].max()],
        **safe_pbr_kwargs(metallic=0.4, roughness=0.5),
    )
    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    p.camera_position = [(9.0, -10.0, 7.5), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(9.0, -10.0, 7.5), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.18)
    shoot(p, out)


def render_graded(out: Path, window_size=WIDE, square_path: Path | None = None):
    print("[3/6] graded gyroid...")
    mesh = pv.read(INPUTS / "gyroid_graded.vtk")
    mesh = prep(mesh)
    mesh = add_scalar(mesh, axis="x")  # grading runs along X

    p = make_plotter(window_size, "#f7f9fc", "#c8d2e0")
    studio_lighting(p, intensity=1.0)
    p.add_mesh(
        mesh,
        scalars="height",
        cmap="viridis",
        show_scalar_bar=False,
        **safe_pbr_kwargs(metallic=0.25, roughness=0.45),
    )
    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    # graded structure runs along x; view it from a 3/4 angle
    p.camera_position = [(4.5, -3.5, 2.8), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(4.5, -3.5, 2.8), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.35)
    shoot(p, out)

    # Optional second pass for the square hero
    if square_path is not None:
        print("    -> hero square render...")
        p2 = make_plotter(SQUARE, "#0f1322", "#2d3a5e")
        studio_lighting(p2, intensity=1.1)
        p2.add_mesh(
            mesh,
            scalars="height",
            cmap="magma",
            show_scalar_bar=False,
            **safe_pbr_kwargs(metallic=0.5, roughness=0.32),
        )
        try:
            p2.add_environment_lighting()
        except Exception:
            pass
        p2.enable_shadows()
        p2.camera_position = [(4.0, -3.5, 2.6), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        p2.reset_camera(bounds=mesh.bounds)
        p2.camera_position = [(4.0, -3.5, 2.6), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
        p2.camera.zoom(1.4)
        shoot(p2, square_path)


def render_helix(out: Path, window_size=WIDE):
    print("[4/6] helix sweep TPMS...")
    mesh = pv.read(INPUTS / "sweep_g7_helix.vtk")
    mesh = prep(mesh)
    mesh = add_scalar(mesh, axis="z")

    p = make_plotter(window_size, "#0c0f17", "#26314a")
    studio_lighting(p, intensity=1.0)
    p.add_mesh(
        mesh,
        scalars="height",
        cmap="plasma",
        show_scalar_bar=False,
        **safe_pbr_kwargs(metallic=0.45, roughness=0.35),
    )
    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    p.camera_position = [(8.5, -9.5, 5.5), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(8.5, -9.5, 5.5), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.22)
    shoot(p, out)


def render_surfaces(out: Path, window_size=WIDE):
    print("[5/6] surfaces stack (3x3 unit cells)...")
    p = make_plotter(window_size, "#fafbfd", "#cfd6e0")
    studio_lighting(p, intensity=1.05)

    cmaps = [
        "viridis", "plasma", "magma",
        "cividis", "inferno", "viridis",
        "magma", "plasma", "cividis",
    ]
    for i in range(9):
        m = pv.read(INPUTS / f"surfaces_{i}.vtp")
        m = prep(m)
        m = add_scalar(m, axis="z")
        p.add_mesh(
            m,
            scalars="height",
            cmap=cmaps[i],
            show_scalar_bar=False,
            **safe_pbr_kwargs(metallic=0.3, roughness=0.42),
        )

    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    # Look at the 3x3 grid (X spans roughly -1.7..1.7, Y -1.7..1.7, Z -0.5..0.5)
    p.camera_position = [(4.5, -5.5, 4.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=(-1.8, 1.8, -1.8, 1.8, -0.6, 0.6))
    p.camera_position = [(4.5, -5.5, 4.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.4)
    shoot(p, out)


def render_cylinder_warm(out: Path, window_size=WIDE):
    """Alternate cylinder render with a warm rim-lit look — gives variety."""
    print("[6/6] cylinder TPMS (warm)...")
    mesh = pv.read(INPUTS / "cylinder_g5_tpms.vtk")
    mesh = prep(mesh)
    mesh = add_scalar(mesh, axis="z")

    p = make_plotter(window_size, "#fff4e0", "#f0c080")
    studio_lighting(p, intensity=1.4)
    p.add_mesh(
        mesh,
        scalars="height",
        cmap="inferno",
        show_scalar_bar=False,
        clim=[mesh.point_data["height"].min(), mesh.point_data["height"].max()],
        **safe_pbr_kwargs(metallic=0.35, roughness=0.45),
    )
    try:
        p.add_environment_lighting()
    except Exception:
        pass
    p.enable_shadows()

    p.camera_position = [(2.5, -9.5, 1.8), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.reset_camera(bounds=mesh.bounds)
    p.camera_position = [(2.5, -9.5, 1.8), (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    p.camera.zoom(1.4)
    shoot(p, out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"Output dir: {OUT}")
    render_cylinder(OUT / "tpms_cylinder.png")
    render_graded(OUT / "gyroid_graded.png", square_path=OUT / "microgen_hero.png")
    render_helix(OUT / "tpms_helix.png")
    render_surfaces(OUT / "surfaces_stack.png")
    render_cylinder_warm(OUT / "tpms_cylinder_warm.png")
    # Sphere is biggest — render last so the rest are safe even if it OOMs.
    try:
        render_sphere(OUT / "tpms_sphere.png")
    except Exception as e:
        print(f"  sphere render failed: {e}")

    print("\nDone. Files written:")
    for f in sorted(OUT.glob("*.png")):
        print(f"  {f.name}  ({f.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
