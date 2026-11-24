"""Result images for the two "one script, three imports" examples of the site.

Runs the scripts shown on the pages, with the same parameters:

* home page (docs/index.md): an elasto-plastic gyroid unit cell under
  periodic homogenization, 2 % mean tensile strain, and its tangent modulus;
* Libraries page (docs/libraries/index.md): the effective elastic stiffness
  of a Kelvin cell and its directional Young's modulus.

Two stages, which may run in different environments:

    python scripts/render_libraries.py mesh    # microgen[cad] + gmsh + mmg
    python scripts/render_libraries.py render  # fedoo + simcoon + pyvista

The mesh and the cached solution are written to ``_render_inputs/`` (not
committed); delete ``gyroid_periodic_result.*`` there to solve again.
The PNGs go to ``docs/assets/images/libraries/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MESH = REPO / "_render_inputs" / "gyroid_periodic.vtk"
RESULT = REPO / "_render_inputs" / "gyroid_periodic_result.vtk"
DATA = REPO / "_render_inputs" / "gyroid_periodic_result.npz"
OUT_DIR = REPO / "docs" / "assets" / "images" / "libraries"

KELVIN = REPO / "_render_inputs" / "kelvin_periodic.vtk"
KELVIN_RADIUS = 0.08
KELVIN_SIZE = 0.03
KELVIN_ELASTIC = (70e3, 0.3)  # E (MPa), nu

DENSITY = 0.3
MESH_SIZE = 0.035
MEAN_STRAIN = 0.02
#        E      nu   alpha  sigma_y  k     m
PROPS = [200e3, 0.3, 1e-5, 300.0, 1000.0, 0.3]

MICROGEN_ORANGE = "#ee7d30"
SIMCOON_RED = "#971c20"
INK = "#0e1c30"


def make_mesh():
    import pyvista as pv
    from microgen import Phase, Rve, Tpms, mesh_periodic
    from microgen.remesh import remesh_keeping_boundaries_for_fem
    from microgen.shape.surface_functions import gyroid

    MESH.parent.mkdir(exist_ok=True)
    step = MESH.with_suffix(".step")
    cell = Phase.from_cad(
        Tpms(surface_function=gyroid, density=DENSITY, resolution=30).generate_cad()
    )
    cell.cad.export_step(str(step))
    mesh_periodic(
        mesh_file=str(step),
        rve=Rve(dim=1),
        list_phases=[cell],
        size=MESH_SIZE,
        order=1,
        output_file=str(MESH),
    )
    step.unlink()
    # gmsh follows the facets of the CAD shell and leaves flat tetrahedra:
    # mmg remeshes the cell and keeps the nodes of opposite faces matched
    mesh = remesh_keeping_boundaries_for_fem(
        pv.UnstructuredGrid(str(MESH)), periodic=True, hmax=MESH_SIZE
    )
    quality = mesh.cell_quality("scaled_jacobian")["scaled_jacobian"]
    print(
        f"   {mesh.n_points} nodes, {mesh.n_cells} tetrahedra, scaled Jacobian: "
        f"min {quality.min():.3f}, mean {quality.mean():.3f}"
    )
    mesh.save(str(MESH))
    print(f"wrote {MESH}")


def _view(pl):
    pl.enable_parallel_projection()
    pl.view_vector((1.0, 0.75, 0.55), viewup=(0, 0, 1))
    pl.reset_camera()
    pl.camera.zoom(1.0)


def render():
    import matplotlib as mpl
    import numpy as np
    import pyvista as pv
    import simcoon as sim

    mpl.use("Agg")
    import matplotlib.pyplot as plt

    from render_fedoo import (
        FEDOO_SEQ,
        WINDOW_SQUARE,
        make_plotter,
        shoot_clear,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- microgen: the periodic mesh -------------------------------------
    pl = make_plotter(WINDOW_SQUARE)
    pl.add_mesh(
        pv.read(str(MESH)).extract_surface(algorithm="dataset_surface"),
        color=MICROGEN_ORANGE,
        show_edges=True,
        edge_color=INK,
        line_width=0.4,
        smooth_shading=False,
        ambient=0.45,
        diffuse=0.55,
        specular=0.05,
    )
    _view(pl)
    shoot_clear(pl, OUT_DIR / "gyroid_mesh.png")

    # --- fedoo + simcoon: periodic homogenization -------------------------
    if not (RESULT.exists() and DATA.exists()):
        solve()
    pv_mesh = pv.read(str(RESULT))
    data = np.load(DATA)
    curve, Lt = data["curve"], data["Lt"]

    p = np.asarray(pv_mesh.point_data["P"])
    print(f"   equivalent plastic strain: [{p.min():.4g}, {p.max():.4g}]")
    lo, hi = np.percentile(p, (2, 98))
    pl = make_plotter(WINDOW_SQUARE)
    pl.add_mesh(
        pv_mesh.extract_surface(algorithm="dataset_surface"),
        scalars="P",
        cmap=FEDOO_SEQ,
        clim=[float(lo), float(hi)],
        # the cell is cut by its faces: keep those edges sharp
        smooth_shading=True,
        split_sharp_edges=True,
        feature_angle=40,
        ambient=0.30,
        diffuse=0.85,
        specular=0.05,
        show_scalar_bar=False,
    )
    _view(pl)
    shoot_clear(pl, OUT_DIR / "gyroid_plastic_strain.png", scalars="P")

    # --- simcoon: macroscopic response and tangent modulus ----------------
    tangent = sim.Tensor4.stiffness(Lt)
    Et = 1 / tangent.inverse().voigt[0, 0]
    deps = tangent.inverse() @ sim.Tensor2.stress([10, 0, 0, 0, 0, 0])
    np.set_printoptions(precision=1, suppress=True, linewidth=200)
    print(f"   Lt (MPa):\n{Lt}")
    print(f"   strain increment for dS_xx = 10 MPa (%): {100 * deps.voigt}")
    print(f"   uniaxial tangent modulus: {Et:.0f} MPa")
    print(f"   macroscopic von Mises stress: {curve[-1, 1]:.1f} MPa")

    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 20,
        "axes.edgecolor": INK, "axes.labelcolor": INK, "axes.linewidth": 1.6,
        "axes.labelweight": "semibold", "xtick.color": INK, "ytick.color": INK,
        "axes.grid": True, "grid.alpha": 0.25, "legend.frameon": False,
    })
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.plot(100 * curve[:, 0], curve[:, 1], color=SIMCOON_RED, lw=3.5,
            label="fedoo, periodic cell")
    e1, s1 = curve[-1]
    de = np.array([-0.45, 0.0]) * MEAN_STRAIN
    ax.plot(100 * (e1 + de), s1 + Et * de, color=INK, lw=2.2, ls="--",
            label="tangent modulus $L_t$ (simcoon)")
    ax.plot(100 * e1, s1, "o", color=SIMCOON_RED, ms=11)
    ax.set_xlabel("mean strain $E_{xx}$ (%)")
    ax.set_ylabel("macroscopic von Mises stress (MPa)")
    ax.set_xlim(0, 100 * MEAN_STRAIN * 1.05)
    ax.set_ylim(0, None)
    ax.legend(loc="lower right", fontsize=17)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    out = OUT_DIR / "gyroid_response.png"
    fig.savefig(out, dpi=160, bbox_inches="tight", pad_inches=0.3, facecolor="white")
    print(f"   wrote {out}")


def solve():
    """Run the homogenization and cache the fields, the macroscopic curve and
    the tangent stiffness (the solve takes several minutes)."""
    import fedoo as fd
    import numpy as np
    import simcoon as sim

    fd.ModelingSpace("3D")
    mesh = fd.Mesh.read(str(MESH))
    assert mesh.is_periodic()
    print(f"   {mesh.n_nodes} nodes, {mesh.n_elements} elements")
    material = fd.constitutivelaw.Simcoon("EPICP", np.array(PROPS))
    assembly = fd.Assembly.create(fd.weakform.StressEquilibrium(material), mesh)

    pb = fd.problem.NonLinear(assembly)
    pb.bc.add(fd.constraint.PeriodicBC("small_strain"))
    pb.bc.add("Dirichlet", mesh.nearest_node(mesh.bounding_box.center), "Disp", 0)
    pb.bc.add("Dirichlet", "E_xx", MEAN_STRAIN)

    volume = mesh.bounding_box.volume
    curve = [(0.0, 0.0)]

    def record(pb):
        sigma = np.ravel(pb.get_ext_forces("MeanStrain")) / volume
        strain = np.ravel(pb.get_dof_solution("MeanStrain"))
        curve.append((strain[0], sim.Tensor2.stress(sigma).mises()))

    pb.nlsolve(
        dt=0.025, tmax=1, print_info=1,
        callback=record, exec_callback_at_each_iter=True,
    )
    pb.get_results(assembly, ["Disp", "Stress", "P"]).to_pyvista().save(str(RESULT))
    Lt = fd.homogen.get_tangent_stiffness(pb)
    np.savez(DATA, curve=np.array(curve), Lt=Lt)


def make_kelvin_mesh():
    import pyvista as pv
    from microgen import Phase, Rve, TruncatedOctahedron, mesh_periodic
    from microgen.remesh import remesh_keeping_boundaries_for_fem

    step = KELVIN.with_suffix(".step")
    cell = Phase.from_cad(
        TruncatedOctahedron(strut_radius=KELVIN_RADIUS).generate_cad()
    )
    cell.cad.export_step(str(step))
    mesh_periodic(
        mesh_file=str(step),
        rve=Rve(dim=1),
        list_phases=[cell],
        size=KELVIN_SIZE,
        order=1,
        output_file=str(KELVIN),
    )
    step.unlink()
    mesh = remesh_keeping_boundaries_for_fem(
        pv.UnstructuredGrid(str(KELVIN)), periodic=True, hmax=KELVIN_SIZE
    )
    quality = mesh.cell_quality("scaled_jacobian")["scaled_jacobian"]
    print(
        f"   {mesh.n_points} nodes, {mesh.n_cells} tetrahedra, density "
        f"{mesh.volume:.3f}, scaled Jacobian: min {quality.min():.3f}, "
        f"mean {quality.mean():.3f}"
    )
    mesh.save(str(KELVIN))
    print(f"wrote {KELVIN}")


def render_kelvin():
    """Kelvin cell of the Libraries page: mesh, one of the six load cases of
    the elastic homogenization, directional Young's modulus."""
    import fedoo as fd
    import numpy as np
    import pyvista as pv
    import simcoon as sim

    from render_fedoo import (
        FEDOO_DIV,
        WINDOW_SQUARE,
        _expand_stress_components,
        make_plotter,
        shoot_clear,
    )
    from render_simcoon import CMAP_HEAT

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- microgen: the periodic mesh -------------------------------------
    pl = make_plotter(WINDOW_SQUARE)
    pl.add_mesh(
        pv.read(str(KELVIN)).extract_surface(algorithm="dataset_surface"),
        color=MICROGEN_ORANGE,
        show_edges=True,
        edge_color=INK,
        line_width=0.4,
        smooth_shading=False,
        ambient=0.45,
        diffuse=0.55,
        specular=0.05,
    )
    _view(pl)
    shoot_clear(pl, OUT_DIR / "kelvin_mesh.png")

    # --- fedoo: homogenized stiffness, and the shear load case ------------
    fd.ModelingSpace("3D")
    mesh = fd.Mesh.read(str(KELVIN))
    assert mesh.is_periodic()
    material = fd.constitutivelaw.ElasticIsotrop(*KELVIN_ELASTIC)
    assembly = fd.Assembly.create(fd.weakform.StressEquilibrium(material), mesh)
    L = fd.homogen.get_homogenized_stiffness(assembly)
    np.set_printoptions(precision=1, suppress=True, linewidth=200)
    print(f"   L (MPa):\n{L}")

    fd.ModelingSpace("3D")  # fresh space: the homogenization added its own dofs
    mesh = fd.Mesh.read(str(KELVIN))
    material = fd.constitutivelaw.ElasticIsotrop(*KELVIN_ELASTIC)
    assembly = fd.Assembly.create(fd.weakform.StressEquilibrium(material), mesh)
    pb = fd.problem.Linear(assembly)
    pb.bc.add(fd.constraint.PeriodicBC("small_strain"))
    pb.bc.add("Dirichlet", mesh.nearest_node(mesh.bounding_box.center), "Disp", 0)
    pb.bc.add("Dirichlet", "MeanStrain", [0, 0, 0, 0, 0, 0.01])
    pb.solve()
    pv_mesh = pb.get_results(assembly, ["Stress", "Disp"]).to_pyvista()
    _expand_stress_components(pv_mesh, "Stress")
    lo, hi = np.percentile(np.asarray(pv_mesh.point_data["Stress_YZ"]), (2, 98))
    m = max(abs(lo), abs(hi))
    pl = make_plotter(WINDOW_SQUARE)
    pl.add_mesh(
        pv_mesh.extract_surface(algorithm="dataset_surface"),
        scalars="Stress_YZ",
        cmap=FEDOO_DIV,
        clim=[-m, m],
        smooth_shading=True,
        split_sharp_edges=True,
        feature_angle=40,
        ambient=0.30,
        diffuse=0.85,
        specular=0.05,
        show_scalar_bar=False,
    )
    _view(pl)
    shoot_clear(pl, OUT_DIR / "kelvin_shear.png", scalars="Stress_YZ")

    # --- simcoon: symmetry and directional Young's modulus ----------------
    print(f"   symmetry: {sim.check_symetries(L, 20.0)['umat_type']}")
    E, nu, G = sim.L_cubic_props(L).ravel()
    print(f"   E = {E:.0f} MPa, nu = {nu:.3f}, G = {G:.0f} MPa")
    theta, phi = np.meshgrid(
        np.linspace(0, np.pi, 181), np.linspace(0, 2 * np.pi, 361), indexing="ij"
    )
    n = np.stack(
        [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)],
        axis=-1,
    )
    sigma = sim.Tensor2.stress(np.einsum("ni,nj->nij", *2 * [n.reshape(-1, 3)]))
    eps = sim.Tensor4.stiffness(L).inverse() @ sigma
    E_n = (1 / np.einsum("nij,nij->n", sigma.mat, eps.mat)).reshape(theta.shape)
    print(f"   E(n) from {E_n.min():.0f} to {E_n.max():.0f} MPa")

    # drawn at unit size, so that the light rig of make_plotter stays outside
    surface = pv.StructuredGrid(*(0.5 * E_n[..., None] / E_n.max() * n).transpose(2, 0, 1))
    surface["E"] = E_n.ravel(order="F")
    pl = make_plotter(WINDOW_SQUARE)
    pl.add_mesh(
        surface.extract_surface(algorithm="dataset_surface"),
        scalars="E",
        cmap=CMAP_HEAT,
        smooth_shading=True,
        ambient=0.65,
        diffuse=0.45,
        specular=0.0,
        show_scalar_bar=False,
    )
    _view(pl)
    pl.camera.zoom(1.5)
    shoot_clear(pl, OUT_DIR / "kelvin_modulus.png", scalars="E")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else ""
    if stage == "mesh":
        make_mesh()
        make_kelvin_mesh()
    elif stage == "render":
        render()
        render_kelvin()
    else:
        sys.exit(__doc__)
