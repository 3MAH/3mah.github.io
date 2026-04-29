"""
Render hero-quality fedoo simulation images for the 3mah.github.io homepage.

Outputs land in assets/images/index/fedoo/ at 1600x1000 (square hero at 1200x1200).
Each render uses SSAA, a 3-light setup, and off-screen rendering.

Notes
-----
* PBR is intentionally avoided for field-colored meshes: metallic shading
  washes out scientific colormaps. We use smooth shading + ambient/diffuse
  control via lighting instead.
* Text shadows are disabled because vtkMatplotlibMathTextUtilities triggers
  spurious math-text fallbacks on titles containing "|".
"""

from __future__ import annotations

import os

# Must be set before any OpenMP/numpy library import that fedoo pulls in.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from pathlib import Path

import numpy as np
import pyvista as pv
from matplotlib.colors import LinearSegmentedColormap

import fedoo as fd

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "assets" / "images" / "index" / "fedoo"
)
OUT_DIR.mkdir(parents=True, exist_ok=True)

WINDOW_LANDSCAPE = (1600, 1000)
WINDOW_SQUARE = (1200, 1200)

# Light theme matching the splash banner: pale blue-grey gradient, dark text.
BG_LIGHT_TOP = "#f6f8fb"
BG_LIGHT_BOT = "#dde4ec"
BG_DEEP = (BG_LIGHT_BOT, BG_LIGHT_TOP)
BG_NIGHT = (BG_LIGHT_BOT, BG_LIGHT_TOP)
TEXT_DARK = "#0e1c30"

# Brand-aware colormaps tuned to the fedoo logo green.
# Sequential map for always-positive fields (von Mises, displacement magnitude).
# Bright end avoids near-white so high values stay visible on a light page.
FEDOO_SEQ = LinearSegmentedColormap.from_list(
    "fedoo_seq",
    [
        (0.00, "#0d3d18"),  # deep forest
        (0.30, "#1f7a1a"),  # dark fedoo green
        (0.60, "#2fa12c"),  # fedoo green
        (0.85, "#7fd35a"),  # bright lime
        (1.00, "#b9e870"),  # warm lime tip
    ],
)
# Diverging map for signed fields (sigma_xx, shear). Soft warm-neutral centre
# (no pure white) so the mid range stays distinguishable from the page bg.
FEDOO_DIV = LinearSegmentedColormap.from_list(
    "fedoo_div",
    [
        (0.00, "#5a1a4a"),  # deep magenta
        (0.25, "#a85a8c"),  # mid magenta
        (0.50, "#e6dfd0"),  # warm light grey centre
        (0.75, "#5fb85b"),  # mid green
        (1.00, "#1f7a1a"),  # deep fedoo green
    ],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ensure_3d_disp(pv_mesh, key="Disp", new_key="Disp3"):
    """Ensure a 3D vector exists for warp_by_vector. Returns the key to use."""
    if key not in pv_mesh.point_data:
        return None
    d = np.asarray(pv_mesh.point_data[key])
    if d.ndim != 2:
        return None
    if d.shape[1] == 2:
        d3 = np.zeros((d.shape[0], 3))
        d3[:, :2] = d
        pv_mesh.point_data[new_key] = d3
        return new_key
    if d.shape[1] == 3:
        return key
    return None


def _expand_stress_components(pv_mesh, key="Stress"):
    """Expand a (N,6) Voigt stress array into named scalar fields and VM."""
    if key not in pv_mesh.point_data:
        return
    S = np.asarray(pv_mesh.point_data[key])
    if S.ndim != 2 or S.shape[1] < 1:
        return
    names = ["XX", "YY", "ZZ", "XY", "XZ", "YZ"]
    for i in range(min(S.shape[1], len(names))):
        pv_mesh.point_data[f"{key}_{names[i]}"] = S[:, i]
    if S.shape[1] >= 4:
        sxx = S[:, 0]
        syy = S[:, 1]
        szz = S[:, 2] if S.shape[1] > 2 else np.zeros_like(sxx)
        sxy = S[:, 3] if S.shape[1] > 3 else np.zeros_like(sxx)
        sxz = S[:, 4] if S.shape[1] > 4 else np.zeros_like(sxx)
        syz = S[:, 5] if S.shape[1] > 5 else np.zeros_like(sxx)
        vm = np.sqrt(
            0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2)
            + 3 * (sxy ** 2 + sxz ** 2 + syz ** 2)
        )
        pv_mesh.point_data[f"{key}_vm"] = vm


def make_plotter(window_size=WINDOW_LANDSCAPE, background=BG_NIGHT):
    """Create an off-screen plotter with a 3-light rig + SSAA.

    `background` may be a single colour or a (bottom, top) tuple for a
    vertical gradient.
    """
    pl = pv.Plotter(off_screen=True, window_size=window_size, lighting="none")
    if isinstance(background, tuple):
        pl.set_background(background[0], top=background[1])
    else:
        pl.set_background(background)
    pl.enable_anti_aliasing("ssaa")
    # 3-light rig: key, fill, rim — neutral white tints to keep colormap honest
    key = pv.Light(
        position=(2.5, 2.5, 3.0), focal_point=(0, 0, 0),
        color="white", intensity=1.05, light_type="scene light",
    )
    fill = pv.Light(
        position=(-2.5, 1.0, 1.5), focal_point=(0, 0, 0),
        color="#d6e0ff", intensity=0.55, light_type="scene light",
    )
    rim = pv.Light(
        position=(0.0, -2.5, 2.0), focal_point=(0, 0, 0),
        color="#ffe4c8", intensity=0.50, light_type="scene light",
    )
    for l in (key, fill, rim):
        pl.add_light(l)
    return pl


def add_field_mesh(
    pl,
    pv_mesh,
    scalars,
    cmap="viridis",
    show_edges=False,
    edge_color="#1f2440",
    line_width=0.5,
    ambient=0.30,
    diffuse=0.85,
    specular=0.05,
    specular_power=10,
    bar_title=None,
    clim=None,
    clim_percentile=None,
):
    """Add a field-colored mesh with neutral lambertian-ish shading.

    If `clim_percentile` is a (low, high) pair in [0, 100], a robust color
    range is computed from the scalar field — useful when fields have heavy
    near-zero mass that would wash out the colormap.
    """
    if clim is None and clim_percentile is not None:
        arr = np.asarray(pv_mesh.point_data[scalars])
        lo, hi = np.percentile(arr, clim_percentile)
        if lo == hi:
            hi = lo + 1e-12
        # Symmetric range when sign changes (good for coolwarm)
        if lo < 0 < hi:
            m = max(abs(lo), abs(hi))
            clim = [-m, m]
        else:
            clim = [float(lo), float(hi)]

    actor = pl.add_mesh(
        pv_mesh,
        scalars=scalars,
        cmap=cmap,
        show_edges=show_edges,
        edge_color=edge_color,
        line_width=line_width,
        smooth_shading=True,
        ambient=ambient,
        diffuse=diffuse,
        specular=specular,
        specular_power=specular_power,
        clim=clim,
        scalar_bar_args=dict(
            title=bar_title or str(scalars),
            color=TEXT_DARK,
            label_font_size=14,
            title_font_size=18,
            n_labels=4,
            shadow=False,
            italic=False,
            bold=False,
            font_family="arial",
            position_x=0.83,
            position_y=0.12,
            width=0.045,
            height=0.50,
            fmt="%.2g",
            vertical=True,
        ),
    )
    return actor


def add_caption(pl, text, color=TEXT_DARK, font_size=16):
    """Add an upper-left caption without shadow (avoids matplotlib mathtext)."""
    pl.add_text(
        text,
        position="upper_left",
        color=color,
        font_size=font_size,
        shadow=False,
        font="arial",
    )


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def render_plate_with_hole():
    """2D plate with circular hole in tension. Von Mises stress."""
    print(">> render_plate_with_hole")
    fd.ModelingSpace("2Dstress")

    mesh = fd.mesh.hole_plate_mesh(
        nr=21, nt=21, length=100, height=100, radius=20,
        elm_type="quad4", sym=False, name="DomainPlate",
    )
    material = fd.constitutivelaw.ElasticIsotrop(2e5, 0.3, name="ElasticPlate")
    fd.weakform.StressEquilibrium("ElasticPlate", name="WFPlate")
    fd.Assembly.create("WFPlate", mesh, name="APlate")

    pb = fd.problem.Linear("APlate")
    pb.bc.add("Dirichlet", mesh.find_nodes("X", mesh.bounding_box.xmin),
              "DispX", -0.5)
    pb.bc.add("Dirichlet", mesh.find_nodes("X", mesh.bounding_box.xmax),
              "DispX", 0.5)
    pb.bc.add("Dirichlet", [0], "DispY", 0)
    pb.set_solver("CG")
    pb.solve()

    res = pb.get_results("APlate", ["Stress", "Disp"])
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=15.0)
        _expand_stress_components(pv_mesh, "Stress")
    pv_mesh.set_active_scalars("Stress_vm")

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_NIGHT)
    add_field_mesh(
        pl, pv_mesh, "Stress_vm", cmap=FEDOO_SEQ,
        show_edges=True, edge_color="#1c1c33", line_width=0.4,
        bar_title="von Mises (MPa)",
    )
    add_caption(pl, "Plate with hole - tension - von Mises stress")
    pl.view_xy()
    pl.camera.zoom(1.35)
    out = OUT_DIR / "fedoo_plate_hole_vm.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_cantilever_linear():
    """3D cantilever beam, large displacement visualised via warp."""
    print(">> render_cantilever_linear")
    fd.ModelingSpace("3D")
    mesh = fd.mesh.box_mesh(
        nx=51, ny=9, nz=9,
        x_min=0, x_max=1000,
        y_min=0, y_max=100,
        z_min=0, z_max=100,
        elm_type="hex8", name="DomainBeam",
    )
    fd.constitutivelaw.ElasticIsotrop(200e3, 0.3, name="ElasticBeam")
    wf = fd.weakform.StressEquilibrium("ElasticBeam")
    fd.Assembly.create(wf, mesh, "hex8", name="ABeam")

    pb = fd.problem.Linear("ABeam")
    nodes_left = mesh.find_nodes("X", mesh.bounding_box.xmin)
    nodes_load = mesh.find_nodes(
        f"X=={mesh.bounding_box.xmax} and Y=={mesh.bounding_box.ymax}"
    )
    pb.bc.add("Dirichlet", nodes_left, "Disp", 0)
    pb.bc.add("Dirichlet", nodes_load, "DispY", -120)
    pb.solve()

    res = pb.get_results("ABeam", ["Stress", "Disp"])
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=1.0)
        _expand_stress_components(pv_mesh, "Stress")
    pv_mesh.set_active_scalars("Stress_XX")

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_DEEP)
    add_field_mesh(
        pl, pv_mesh, "Stress_XX", cmap=FEDOO_DIV,
        show_edges=False, bar_title="sigma_xx (MPa)",
        clim_percentile=(2, 98),
    )
    add_caption(pl, "Cantilever beam - tip-loaded bending - sigma_xx")
    pl.view_isometric()
    pl.camera.azimuth = 25
    pl.camera.elevation = 18
    pl.camera.zoom(1.50)
    out = OUT_DIR / "fedoo_finite_strain.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def _build_cubic_lattice(n=5, L=100.0):
    """Build a cubic 3D lattice mesh of lin2 beams."""
    coords = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                coords.append([i * L / (n - 1), j * L / (n - 1),
                               k * L / (n - 1)])
    coords = np.asarray(coords)

    def idx(i, j, k):
        return i + n * (j + n * k)

    elements = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i + 1 < n:
                    elements.append([idx(i, j, k), idx(i + 1, j, k)])
                if j + 1 < n:
                    elements.append([idx(i, j, k), idx(i, j + 1, k)])
                if k + 1 < n:
                    elements.append([idx(i, j, k), idx(i, j, k + 1)])
    elements = np.asarray(elements)
    return fd.Mesh(coords, elements, "lin2")


def render_lattice_beam():
    """3D cubic lattice of beams under nonlinear bending."""
    print(">> render_lattice_beam")
    fd.ModelingSpace("3D")
    mesh = _build_cubic_lattice(n=5, L=100.0)

    material = fd.constitutivelaw.ElasticIsotrop(1e5, 0.3)
    beam_props = fd.constitutivelaw.BeamCircular(material, 1.5, k=0.9)

    nodes_left = mesh.find_nodes("X", mesh.bounding_box.xmin)
    nodes_right = mesh.find_nodes("X", mesh.bounding_box.xmax)

    wf = fd.weakform.BeamEquilibrium(beam_props)
    assembly = fd.Assembly.create(wf, mesh)

    pb = fd.problem.NonLinear(assembly, nlgeom=True)
    pb.bc.add("Dirichlet", nodes_left, ["Disp", "Rot"], 0)
    pb.bc.add("Dirichlet", nodes_right, "DispY", -25)
    pb.set_nr_criterion("Displacement", tol=5e-3, max_subiter=10)
    pb.nlsolve(dt=0.1, update_dt=True, print_info=0)

    res = pb.get_results(assembly, ["Disp", "Rot", "BeamStress"])
    pv_mesh = res.to_pyvista()

    # Pick a usable scalar — prefer displacement magnitude for visibility
    if "Disp" in pv_mesh.point_data:
        d = np.asarray(pv_mesh.point_data["Disp"])
        if d.ndim == 2:
            if d.shape[1] == 2:
                d3 = np.zeros((d.shape[0], 3))
                d3[:, :2] = d
                pv_mesh.point_data["Disp3"] = d3
                pv_mesh.point_data["DispMag"] = np.linalg.norm(d3, axis=1)
            else:
                pv_mesh.point_data["DispMag"] = np.linalg.norm(d, axis=1)
    cand = "DispMag" if "DispMag" in pv_mesh.point_data else (
        "BeamStress_0" if "BeamStress_0" in pv_mesh.point_data
        else list(pv_mesh.point_data.keys())[0]
    )

    # Convert UnstructuredGrid to PolyData (lines) for tube filtering
    poly = pv_mesh.extract_surface()
    if not poly.n_lines and pv_mesh.n_cells:
        # Fallback: rebuild a PolyData from cells if extract_surface lost lines
        poly = pv.PolyData(pv_mesh.points)
        lines = []
        for c in range(pv_mesh.n_cells):
            cell = pv_mesh.get_cell(c)
            ids = list(cell.point_ids)
            if len(ids) == 2:
                lines.extend([2, ids[0], ids[1]])
        if lines:
            poly.lines = np.asarray(lines)
            for k in pv_mesh.point_data:
                poly.point_data[k] = pv_mesh.point_data[k]

    tubes = poly.tube(radius=1.4, n_sides=18)

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_NIGHT)
    pl.add_mesh(
        tubes,
        scalars=cand,
        cmap=FEDOO_SEQ,
        smooth_shading=True,
        ambient=0.30,
        diffuse=0.85,
        specular=0.10,
        specular_power=15,
        scalar_bar_args=dict(
            title=str(cand), color=TEXT_DARK, label_font_size=14,
            title_font_size=18, n_labels=4, shadow=False, font_family="arial",
            position_x=0.83, position_y=0.10, width=0.04, height=0.55,
            fmt="%.1e",
        ),
    )
    add_caption(pl, "Beam lattice - nonlinear geometric bending")
    pl.view_isometric()
    pl.camera.azimuth = 30
    pl.camera.elevation = 18
    pl.camera.zoom(1.10)
    out = OUT_DIR / "fedoo_beam_lattice.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_periodic_homog():
    """Periodic BC homogenization on a Kelvin (truncated octahedron) RVE
    under shear EYZ."""
    print(">> render_periodic_homog")
    fd.ModelingSpace("3D")

    repo = Path(__file__).resolve().parent.parent
    mesh = fd.Mesh.read(str(repo / "_render_inputs" / "Kelvin.vtk"))
    assert mesh.is_periodic(tol=1e-3), "Kelvin.vtk is not periodic at 1e-3 tol"

    material = fd.constitutivelaw.ElasticIsotrop(1e5, 0.3)
    wf = fd.weakform.StressEquilibrium(material)
    assembly = fd.Assembly.create(wf, mesh)

    pb = fd.problem.Linear(assembly)
    pb.bc.add(fd.constraint.PeriodicBC("small_strain", tol=1e-3))
    # Pin one node near the centre to remove rigid-body motion
    pb.bc.add(
        "Dirichlet", mesh.nearest_node(mesh.bounding_box.center), "Disp", 0
    )
    # Drive a pure shear strain E_yz on the global mean-strain DOF
    pb.bc.add("Dirichlet", "E_yz", 0.06)

    pb.solve()
    res = pb.get_results(assembly, ["Stress", "Disp"])
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=2.5)
        _expand_stress_components(pv_mesh, "Stress")

    scalar = (
        "Stress_YZ" if "Stress_YZ" in pv_mesh.point_data
        else ("Stress_vm" if "Stress_vm" in pv_mesh.point_data
              else list(pv_mesh.point_data.keys())[0])
    )
    pv_mesh.set_active_scalars(scalar)

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_DEEP)
    add_field_mesh(
        pl, pv_mesh, scalar, cmap=FEDOO_DIV,
        show_edges=True, edge_color="#23304a", line_width=0.3,
        bar_title="sigma_yz (MPa)",
        clim_percentile=(2, 98),
    )
    add_caption(pl, "Periodic homogenization - Kelvin RVE under shear EYZ")
    pl.view_isometric()
    pl.camera.azimuth = 30
    pl.camera.elevation = 22
    pl.camera.zoom(1.25)
    out = OUT_DIR / "fedoo_periodic_homog.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_ishape_bending():
    """3D I-shape beam under 3-point bending."""
    print(">> render_ishape_bending")
    profil = fd.mesh.structured_mesh.I_shape_mesh(10, 10, 2, 2, 1, "tri3")
    mesh = fd.mesh.extrude(profil, 100, 21)
    mesh.nodes = mesh.nodes[:, [2, 1, 0]]

    fd.ModelingSpace("3D")
    fd.constitutivelaw.ElasticIsotrop(200e3, 0.3, name="ElasticI")
    wf = fd.weakform.StressEquilibrium("ElasticI", name="WFI")
    assembly = fd.Assembly.create(wf, mesh, name="AI")
    pb = fd.problem.Linear(assembly)

    bottom = mesh.find_nodes("Y", mesh.bounding_box.ymin)
    top = mesh.find_nodes("Y", mesh.bounding_box.ymax)
    left_bottom = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.xmin), bottom)
    right_bottom = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.xmax), bottom)
    center_top = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.center[0]), top)

    pb.bc.add("Dirichlet", left_bottom, "Disp", 0)
    pb.bc.add("Dirichlet", right_bottom, "DispY", 0)
    pb.bc.add("Dirichlet", center_top, "DispY", -8)
    pb.solve()

    res = pb.get_results(assembly, ["Stress", "Disp"])
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=2.5)
        _expand_stress_components(pv_mesh, "Stress")

    pv_mesh.set_active_scalars("Stress_XX")

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_NIGHT)
    add_field_mesh(
        pl, pv_mesh, "Stress_XX", cmap=FEDOO_DIV,
        show_edges=False, bar_title="sigma_xx (MPa)",
    )
    add_caption(pl, "I-beam - 3-point bending - sigma_xx")
    pl.view_isometric()
    pl.camera.azimuth = 25
    pl.camera.elevation = 18
    pl.camera.zoom(1.30)
    out = OUT_DIR / "fedoo_ibeam_bending.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_pingpong_shell():
    """Plate / shell elements - pressure on a sphere."""
    print(">> render_pingpong_shell")
    fd.ModelingSpace("3D")
    radius = 20
    sphere = pv.Sphere(radius, theta_resolution=64, phi_resolution=64)
    mesh = fd.Mesh.from_pyvista(sphere)

    fd.constitutivelaw.ElasticIsotrop(2e3, 0.37, name="MatShell")
    shell_section = fd.constitutivelaw.ShellHomogeneous("MatShell", 0.45)

    wf = fd.weakform.PlateEquilibrium(shell_section)
    solid_assembly = fd.Assembly.create(wf, mesh)

    boundaries = mesh.find_elements(
        f"Z>{mesh.bounding_box.zmax-3} or Z<{mesh.bounding_box.zmin+3}"
    )
    pressure_assembly = fd.constraint.Pressure(
        mesh.extract_elements(boundaries), 10
    )
    assembly = solid_assembly + pressure_assembly

    pb = fd.problem.Linear(assembly)
    pb.solve()

    res = pb.get_results(solid_assembly, ["Disp", "Stress"], position=1)
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=1.0)
        _expand_stress_components(pv_mesh, "Stress")

    scalar = (
        "Stress_vm" if "Stress_vm" in pv_mesh.point_data
        else ("Stress_XX" if "Stress_XX" in pv_mesh.point_data
              else list(pv_mesh.point_data.keys())[0])
    )
    pv_mesh.set_active_scalars(scalar)

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_DEEP)
    add_field_mesh(
        pl, pv_mesh, scalar, cmap=FEDOO_SEQ,
        show_edges=False, bar_title="von Mises (MPa)",
    )
    add_caption(pl, "Shell elements - pressure on a sphere")
    pl.view_isometric()
    pl.camera.zoom(1.30)
    out = OUT_DIR / "fedoo_shell_pressure.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_hero_square():
    """Square hero render: I-beam composition at 1200x1200."""
    print(">> render_hero_square")
    profil = fd.mesh.structured_mesh.I_shape_mesh(10, 10, 2, 2, 1, "tri3")
    mesh = fd.mesh.extrude(profil, 100, 25)
    mesh.nodes = mesh.nodes[:, [2, 1, 0]]

    fd.ModelingSpace("3D")
    fd.constitutivelaw.ElasticIsotrop(200e3, 0.3, name="ElasticHero")
    wf = fd.weakform.StressEquilibrium("ElasticHero", name="WFHero")
    assembly = fd.Assembly.create(wf, mesh, name="AHero")
    pb = fd.problem.Linear(assembly)

    bottom = mesh.find_nodes("Y", mesh.bounding_box.ymin)
    top = mesh.find_nodes("Y", mesh.bounding_box.ymax)
    left_bottom = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.xmin), bottom)
    right_bottom = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.xmax), bottom)
    center_top = np.intersect1d(
        mesh.find_nodes("X", mesh.bounding_box.center[0]), top)
    pb.bc.add("Dirichlet", left_bottom, "Disp", 0)
    pb.bc.add("Dirichlet", right_bottom, "DispY", 0)
    pb.bc.add("Dirichlet", center_top, "DispY", -10)
    pb.solve()

    res = pb.get_results(assembly, ["Stress", "Disp"])
    pv_mesh = res.to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    disp_key = _ensure_3d_disp(pv_mesh)
    if disp_key:
        pv_mesh = pv_mesh.warp_by_vector(disp_key, factor=3.0)
        _expand_stress_components(pv_mesh, "Stress")
    pv_mesh.set_active_scalars("Stress_XX")

    pl = make_plotter(WINDOW_SQUARE, background=BG_DEEP)
    add_field_mesh(
        pl, pv_mesh, "Stress_XX", cmap=FEDOO_DIV,
        show_edges=False, bar_title="sigma_xx (MPa)",
        ambient=0.32, diffuse=0.90, specular=0.05,
        clim_percentile=(2, 98),
    )
    pl.add_text(
        "fedoo", position="lower_left", color=TEXT_DARK,
        font_size=32, shadow=False, font="arial",
    )
    pl.view_isometric()
    pl.camera.azimuth = 28
    pl.camera.elevation = 20
    pl.camera.zoom(1.05)
    out = OUT_DIR / "fedoo_hero.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


def render_tube_compression():
    """2D axisymmetric tube compression with self-contact, finite strain
    and the Simcoon ``EPICP`` plastic UMAT — buckling / folding tube.

    Mirrors fedoo-docs/examples/03-advanced/tube_compression.html. The
    deformed configuration is reconstructed in 3D and rendered with the
    equivalent plastic strain field on the brand sequential colormap.
    """
    print(">> render_tube_compression")
    fd.ModelingSpace("2Daxi")
    mesh = fd.mesh.rectangle_mesh(5, 240, 23, 25, 0, 180)

    # EPICP power-law isotropic-hardening plasticity (Simcoon UMAT)
    sigma_y, k, m = 300.0, 1000.0, 0.3
    E, nu = 200.0e3, 0.3
    props = np.array([E, nu, 1e-5, sigma_y, k, m])
    material = fd.constitutivelaw.Simcoon("EPICP", props)

    wf = fd.weakform.StressEquilibrium(material)
    assembly = fd.Assembly.create(wf, mesh)

    surf = fd.mesh.extract_surface(mesh)
    contact = fd.constraint.contact.SelfContact(surf)
    contact.contact_search_once = True
    contact.eps_n = 1e4
    contact.max_dist = 1.0

    pb = fd.problem.NonLinear(assembly + contact, nlgeom="UL")
    pb.set_nr_criterion(
        "Displacement", tol=1e-2, max_subiter=20, adaptive_stiffness=True,
    )

    # Tube-compression generates large .fdz archives (~600 MB for the 3D
    # reconstruction). Write them to a per-process temp dir, *and* sweep
    # any stragglers from earlier failed runs so the disk stays sane.
    import glob, shutil, tempfile
    for stale in glob.glob(
        str(Path(tempfile.gettempdir()) / "fedoo_tube_*")
    ):
        shutil.rmtree(stale, ignore_errors=True)
    out_dir = Path(tempfile.mkdtemp(prefix="fedoo_tube_"))

    try:
        res = pb.add_output(
            str(out_dir / "tube_compression"),
            assembly, ["Disp", "Stress", "Strain", "P"],
        )

        bottom = mesh.node_sets["bottom"]
        top = mesh.node_sets["top"]
        pb.bc.add("Dirichlet", bottom, "Disp", 0)
        pb.bc.add("Dirichlet", top, "Disp", [0, -150])
        pb.add_line_search()
        pb.nlsolve(dt=0.01, tmax=1, update_dt=True, print_info=0, dt_min=1e-8)

        # 3D reconstruction (revolve axisymmetric mesh + fields around z).
        # Pass `filename` so the full 3D dataset is materialised on disk and
        # the per-frame fields (Stress, P, Strain) are written out — the
        # in-memory lightweight wrapper only exposes Disp.
        full_3d_path = out_dir / "tube_compression_3d"
        data_3d = fd.post_processing.axi_to_3d(res, filename=str(full_3d_path))
        n_iter = data_3d.n_iter

        # Three snapshots: undeformed, mid-deformed, fully deformed.
        frame_idx = [0, n_iter // 2, n_iter - 1]
        frame_labels = ["Undeformed", "Mid-deformed", "Fully deformed"]

        def warped_mesh(idx):
            data_3d.load(idx)
            m = data_3d.to_pyvista()
            d = _ensure_3d_disp(m)
            return m.warp_by_vector(d, factor=1.0) if d else m

        meshes = [warped_mesh(i) for i in frame_idx]

        # Shared colour scale built from the final (most strained) frame.
        p_final = np.asarray(meshes[-1].point_data["P"])
        clim = [0.0, float(np.percentile(p_final, 98))]
        # Shared camera bounds = union of all frame bounds (all xy-radii are
        # the same after the radial bulge dominates; z shrinks with compression).
        union_bounds = np.array(meshes[0].bounds, dtype=float)
        for m in meshes[1:]:
            b = np.array(m.bounds)
            union_bounds[0::2] = np.minimum(union_bounds[0::2], b[0::2])
            union_bounds[1::2] = np.maximum(union_bounds[1::2], b[1::2])
        span_xy = max(union_bounds[1] - union_bounds[0],
                      union_bounds[3] - union_bounds[2])
        span_z = union_bounds[5] - union_bounds[4]
        cam_target = (
            0.5 * (union_bounds[0] + union_bounds[1]),
            0.5 * (union_bounds[2] + union_bounds[3]),
            0.5 * (union_bounds[4] + union_bounds[5]),
        )
        cam_pos = (
            cam_target[0] + 2.6 * span_xy,
            cam_target[1] - 0.6 * span_xy,
            cam_target[2] + 0.4 * span_z,
        )

        # Three independent panels — initial (static PNG), evolution
        # (MP4), final (static PNG). H.264 needs even dimensions.
        panel_w = 1000
        panel_h = 1200
        # Even dimensions for libx264 / yuv420p
        movie_w = panel_w if panel_w % 2 == 0 else panel_w + 1
        movie_h = panel_h if panel_h % 2 == 0 else panel_h + 1

        def _frame_plotter(window_size, with_label=None, with_bar=False):
            pl = make_plotter(window_size=window_size, background=BG_NIGHT)
            if with_label is not None:
                pl.add_text(
                    with_label, position="upper_left",
                    color=TEXT_DARK, font_size=22, shadow=False, font="arial",
                )
            return pl

        bar_kwargs = dict(
            title="equivalent plastic strain  p",
            color=TEXT_DARK,
            label_font_size=24, title_font_size=30,
            n_labels=4, shadow=False, italic=False, bold=False,
            font_family="arial",
            position_x=0.78, position_y=0.10,
            width=0.08, height=0.65, fmt="%.2g", vertical=True,
        )

        def _add_tube(pl, mesh, show_bar=False):
            pl.add_mesh(
                mesh, scalars="P", cmap=FEDOO_SEQ, clim=clim,
                show_edges=False, smooth_shading=True,
                ambient=0.30, diffuse=0.85, specular=0.05, specular_power=10,
                show_scalar_bar=show_bar,
                scalar_bar_args=bar_kwargs if show_bar else None,
            )
            pl.camera_position = [cam_pos, cam_target, (0, 0, 1)]
            pl.reset_camera(bounds=tuple(union_bounds))
            pl.camera.elevation = -10
            pl.camera.zoom(1.05)

        # ----- 1) static initial frame (PNG) -------------------------------
        pl = _frame_plotter((panel_w, panel_h), with_label="Undeformed")
        _add_tube(pl, meshes[0])
        out_initial = OUT_DIR / "fedoo_tube_initial.png"
        pl.screenshot(str(out_initial))
        pl.close()
        print(f"   wrote {out_initial}")

        # ----- 2) static final frame (PNG, with colorbar) ------------------
        pl = _frame_plotter((panel_w, panel_h), with_label="Fully deformed")
        _add_tube(pl, meshes[-1], show_bar=True)
        out_final = OUT_DIR / "fedoo_tube_final.png"
        pl.screenshot(str(out_final))
        pl.close()
        print(f"   wrote {out_final}")

        # ----- 3) evolution MP4 --------------------------------------------
        # Sample ~50 frames evenly over the simulation history.
        n_frames = min(60, n_iter)
        frame_indices = np.linspace(0, n_iter - 1, n_frames).astype(int)

        movie_pl = _frame_plotter((movie_w, movie_h), with_label=None)
        out_movie = OUT_DIR / "fedoo_tube_evolution.mp4"
        movie_pl.open_movie(str(out_movie), framerate=15, quality=7)
        # Tiny intro hold on the undeformed shape
        for _ in range(8):
            movie_pl.clear_actors()
            _add_tube(movie_pl, meshes[0])
            movie_pl.write_frame()
        for fi in frame_indices:
            data_3d.load(int(fi))
            m = data_3d.to_pyvista()
            d = _ensure_3d_disp(m)
            warped = m.warp_by_vector(d, factor=1.0) if d else m
            movie_pl.clear_actors()
            _add_tube(movie_pl, warped)
            movie_pl.write_frame()
        # Hold on the folded final state
        for _ in range(20):
            movie_pl.clear_actors()
            _add_tube(movie_pl, meshes[-1])
            movie_pl.write_frame()
        movie_pl.close()
        print(f"   wrote {out_movie}  ({out_movie.stat().st_size / 1024:.0f} KB)")
        return out_initial
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def render_ipc_indentation():
    """2D plane-strain disk indentation with IPC barrier-method contact.

    A stiff disk (E_disk) is pressed vertically into a softer plate
    (E_plate) — classical Hertzian contact, here driven through fedoo's
    ipctk-backed `IPCContact` constraint. Renders the deformed shape with
    the von Mises stress field (sequential brand colormap).
    """
    print(">> render_ipc_indentation")
    fd.ModelingSpace("2D")

    E_plate, E_disk, nu = 1.0e3, 1.0e5, 0.3
    R = 5.0
    plate_half, plate_h = 15.0, 12.0
    gap = 0.1
    imposed_disp = -1.5

    mesh_plate = fd.mesh.rectangle_mesh(
        nx=121, ny=51,
        x_min=-plate_half, x_max=plate_half,
        y_min=0, y_max=plate_h,
        elm_type="tri3",
    )
    mesh_plate.element_sets["plate"] = np.arange(mesh_plate.n_elements)

    mesh_disk = fd.mesh.disk_mesh(radius=R, nr=14, nt=36, elm_type="tri3")
    mesh_disk.nodes += np.array([0.0, plate_h + R + gap])
    mesh_disk.element_sets["disk"] = np.arange(mesh_disk.n_elements)

    mesh = fd.Mesh.stack(mesh_plate, mesh_disk)

    surf = fd.mesh.extract_surface(mesh)
    ipc_contact = fd.constraint.IPCContact(
        mesh, surface_mesh=surf,
        dhat=0.05, dhat_is_relative=False, use_ccd=True,
    )

    mat_plate = fd.constitutivelaw.ElasticIsotrop(E_plate, nu)
    mat_disk = fd.constitutivelaw.ElasticIsotrop(E_disk, nu)
    material = fd.constitutivelaw.Heterogeneous(
        (mat_plate, mat_disk), ("plate", "disk"),
    )
    wf = fd.weakform.StressEquilibrium(material, nlgeom=False)
    solid = fd.Assembly.create(wf, mesh)
    assembly = fd.Assembly.sum(solid, ipc_contact)

    import shutil, tempfile
    out_dir = Path(tempfile.mkdtemp(prefix="fedoo_ipc_"))
    try:
        pb = fd.problem.NonLinear(assembly)
        # Multi-frame results — one frame per converged step
        ipc_res = pb.add_output(
            str(out_dir / "ipc_indentation"),
            solid, ["Stress", "Disp"],
        )

        nodes_bottom = mesh.find_nodes("Y", 0)
        nodes_disk_top = mesh.find_nodes("Y", mesh.bounding_box.ymax)
        pb.bc.add("Dirichlet", nodes_bottom, "Disp", 0)
        pb.bc.add("Dirichlet", nodes_disk_top, "Disp", [0, imposed_disp])
        pb.set_nr_criterion("Force", tol=5e-3, max_subiter=10)
        pb.nlsolve(dt=0.1, tmax=1, update_dt=True, print_info=0)

        n_iter = ipc_res.n_iter

        def warped_frame(idx):
            ipc_res.load(idx)
            m = ipc_res.to_pyvista()
            _expand_stress_components(m, "Stress")
            d = _ensure_3d_disp(m)
            if d:
                m = m.warp_by_vector(d, factor=1.0)
                _expand_stress_components(m, "Stress")
            m.set_active_scalars("Stress_vm")
            return m

        # Final frame drives the colour scaling so all frames share the
        # same plate-vm percentile cap.
        final = warped_frame(n_iter - 1)
        plate_vm = np.asarray(final.point_data["Stress_vm"])[:mesh_plate.n_nodes]
        cap = float(np.percentile(plate_vm, 95))
        clim = [0.0, cap]

        # ----- 1) static final-state PNG (kept as poster for the video) ----
        pl = make_plotter(WINDOW_LANDSCAPE, background=BG_NIGHT)
        add_field_mesh(
            pl, final, "Stress_vm", cmap=FEDOO_SEQ,
            show_edges=False, bar_title="von Mises (MPa)", clim=clim,
        )
        add_caption(pl, "IPC contact - disk indentation - von Mises stress")
        pl.view_xy()
        pl.camera.zoom(1.45)
        out_png = OUT_DIR / "fedoo_ipc_indentation.png"
        pl.screenshot(str(out_png))
        pl.close()
        print(f"   wrote {out_png}")

        # ----- 2) evolution MP4 -------------------------------------------
        # Even dimensions for libx264
        movie_size = (
            WINDOW_LANDSCAPE[0] - (WINDOW_LANDSCAPE[0] % 2),
            WINDOW_LANDSCAPE[1] - (WINDOW_LANDSCAPE[1] % 2),
        )
        n_frames = min(50, n_iter)
        frame_indices = np.linspace(0, n_iter - 1, n_frames).astype(int)

        # Camera bounds = union of initial + final frame so the plate's
        # fixed bottom and lateral edges stay anchored throughout the loop.
        first = warped_frame(0)
        b0 = np.array(first.bounds)
        bF = np.array(final.bounds)
        fixed_bounds = (
            min(b0[0], bF[0]), max(b0[1], bF[1]),
            min(b0[2], bF[2]), max(b0[3], bF[3]),
            min(b0[4], bF[4]), max(b0[5], bF[5]),
        )

        movie_pl = make_plotter(window_size=movie_size, background=BG_NIGHT)
        out_movie = OUT_DIR / "fedoo_ipc_indentation.mp4"
        movie_pl.open_movie(str(out_movie), framerate=15, quality=7)

        # ---- Stable caption + camera ----
        add_caption(
            movie_pl,
            "IPC contact - disk indentation - von Mises stress",
        )
        movie_pl.view_xy()
        movie_pl.reset_camera(bounds=fixed_bounds)
        movie_pl.camera.zoom(1.45)

        # Persistent scalar bar args, used only on the FIRST add_mesh call
        # so we get exactly one bar (not flickering across frames).
        bar_kwargs = dict(
            title="von Mises (MPa)", color="#0e1c30",
            label_font_size=14, title_font_size=18,
            n_labels=4, shadow=False, italic=False, bold=False,
            font_family="arial",
            position_x=0.83, position_y=0.12,
            width=0.045, height=0.50, fmt="%.2g", vertical=True,
        )

        def _show_frame(mesh, *, with_bar):
            """Replace the named 'ipc' actor; keep scalar bar persistent."""
            movie_pl.add_mesh(
                mesh, name="ipc",                   # replace-in-place
                scalars="Stress_vm", cmap=FEDOO_SEQ, clim=clim,
                show_edges=False, smooth_shading=True,
                ambient=0.30, diffuse=0.85, specular=0.05, specular_power=10,
                show_scalar_bar=with_bar,
                scalar_bar_args=bar_kwargs if with_bar else None,
            )

        # First frame creates the scalar bar; every subsequent frame just
        # swaps the mesh actor with the same name — no bar churn.
        _show_frame(first, with_bar=True)
        for _ in range(8):
            movie_pl.write_frame()
        for fi in frame_indices:
            _show_frame(warped_frame(int(fi)), with_bar=False)
            movie_pl.write_frame()
        _show_frame(final, with_bar=False)
        for _ in range(20):
            movie_pl.write_frame()
        movie_pl.close()
        print(f"   wrote {out_movie}  ({out_movie.stat().st_size / 1024:.0f} KB)")
        return out_png
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def render_kelvin_raw():
    """Raw mesh view of the Kelvin RVE — same geometry as the homogenization
    render, used as the 'before' image in the microstructure-to-simulation
    pipeline section. No PBR, no field, just the conforming triangulation.
    """
    print(">> render_kelvin_raw")
    repo = Path(__file__).resolve().parent.parent
    pv_mesh = pv.read(str(repo / "_render_inputs" / "Kelvin.vtk"))
    surf = pv_mesh.extract_surface()

    pl = make_plotter(WINDOW_LANDSCAPE, background=BG_NIGHT)
    pl.add_mesh(
        surf,
        color="#cfd6df",
        show_edges=True,
        edge_color="#0e1c30",
        line_width=0.4,
        smooth_shading=False,
        ambient=0.45,
        diffuse=0.55,
        specular=0.05,
        opacity=1.0,
    )
    add_caption(pl, "Kelvin RVE - conforming periodic mesh from Microgen")
    pl.view_isometric()
    pl.camera.azimuth = 30
    pl.camera.elevation = 22
    pl.camera.zoom(1.25)
    out = OUT_DIR / "fedoo_kelvin_mesh.png"
    pl.screenshot(str(out))
    pl.close()
    print(f"   wrote {out}")
    return out


# Each renderer creates its own ModelingSpace and runs sequentially.
ALL = [
    render_plate_with_hole,
    render_kelvin_raw,
    render_periodic_homog,
    render_ipc_indentation,
    render_tube_compression,
    render_ishape_bending,
    render_cantilever_linear,
    render_lattice_beam,
    render_pingpong_shell,
    render_hero_square,
]


def main():
    pv.OFF_SCREEN = True
    successes, failures = [], []
    for fn in ALL:
        try:
            fn()
            successes.append(fn.__name__)
        except Exception as e:
            import traceback
            print(f"!! {fn.__name__} FAILED: {e}")
            traceback.print_exc()
            failures.append(fn.__name__)
    print()
    print(f"DONE - ok={len(successes)} fail={len(failures)}")
    if failures:
        print("failures:", failures)


if __name__ == "__main__":
    main()
