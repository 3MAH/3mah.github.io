---
layout: splash
header:
  overlay_color: "#0a1428"
  overlay_filter: "0.35"
  overlay_image: /assets/images/index/microgen/tpms_cylinder.png
  og_image: /assets/images/index/microgen/tpms_cylinder.png
  cta_label: "Download"
  cta_url: "https://github.com/3MAH/"
  caption: "Gyroid TPMS rendered with microgen"
title: "3MAH — Mechanics of Heterogeneous & Architectured Materials"
description: "Open-source scientific software for mechanics of materials and multiphysics. simcoon (constitutive modeling, micromechanics, UMAT), fedoo (nonlinear finite element analysis, periodic homogenization, PGD), and microgen (TPMS, lattices, polycrystals and microstructure meshing) in a single coherent workflow."
keywords:
  - mechanics of materials
  - computational mechanics
  - constitutive modeling
  - micromechanics
  - finite element analysis
  - nonlinear FEM
  - periodic homogenization
  - microstructure generation
  - TPMS
  - gyroid
  - lattice structures
  - polycrystal
  - Voronoi tessellation
  - plasticity
  - hyperelasticity
  - shape memory alloys
  - composites
  - Mori-Tanaka
  - simcoon
  - fedoo
  - microgen
  - Python
  - C++
  - UMAT
  - Abaqus
  - open source
excerpt: "Open-source scientific tools for the mechanics of materials and multiphysics: constitutive modeling, finite element analysis, and microstructure generation, in a single coherent workflow."

intro:
  - excerpt: 'The **3MAH** initiative brings together three complementary, interoperable open-source libraries: **simcoon** for constitutive modeling and micromechanics, **fedoo** for nonlinear finite element analysis, and **microgen** for microstructure generation and meshing. Together, they provide a complete pipeline from geometry to simulation for research in mechanics of heterogeneous and architectured materials.'

simcoon_row:
  - image_path: /assets/images/logo_simcoon/simcoon_logo_text.png
    alt: "simcoon"
    title: "simcoon"
    excerpt: "**Constitutive modeling and micromechanics** in C++ with Python bindings. Anisotropic elasticity, plasticity (isotropic, kinematic, Chaboche), viscoelasticity, hyperelasticity and phase transformation, with finite-strain support."
    url: "https://3mah.github.io/simcoon-docs/"
    btn_label: "simcoon docs"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/simcoon/simcoon_homog_mori_tanaka.png
    alt: "Mean-field homogenization"
    title: "Mean-field homogenization"
    excerpt: "Effective properties of composites with **Mori-Tanaka** and self-consistent schemes, framed by Voigt and Reuss bounds and validated against experimental data."
    url: "https://3mah.github.io/simcoon-docs/examples/heterogeneous/homogenization.html"
    btn_label: "See example"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/simcoon/simcoon_directional_stiffness.png
    alt: "Directional stiffness"
    title: "Analysis & identification"
    excerpt: "Analyse **directional stiffness**, yield surfaces and cyclic response, then identify model parameters with hybrid genetic-gradient algorithms."
    url: "https://3mah.github.io/simcoon-docs/examples/analysis/directional_stiffness.html"
    btn_label: "See example"
    btn_class: "btn--primary"

fedoo_row:
  - image_path: /assets/images/logo_fedoo/fedoo_logo.png
    alt: "fedoo"
    title: "fedoo"
    excerpt: "A **Python finite element solver** for nonlinear mechanics, with an emphasis on geometric and material nonlinearity, model reduction (PGD) and multiscale homogenization."
    url: "https://3mah.github.io/fedoo-docs/"
    btn_label: "fedoo docs"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/fedoo/fedoo_periodic_homog.png
    alt: "Periodic homogenization"
    title: "Periodic homogenization"
    excerpt: "Apply **periodic boundary conditions** on representative volume elements to extract full anisotropic effective stiffness and nonlinear macroscopic response."
    url: "https://3mah.github.io/fedoo-docs/examples/03-advanced/3D_periodic_BC_off_axis.html"
    btn_label: "See example"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/fedoo/fedoo_beam_lattice.png
    alt: "Beam and shell elements"
    title: "Beam, shell and solid elements"
    excerpt: "From 2D plates with holes to 3D **beam lattices** and pressurised shells: a unified API for 1D, 2D and 3D structural analysis."
    url: "https://3mah.github.io/fedoo-docs/"
    btn_label: "Read more"
    btn_class: "btn--primary"

fedoo_contact:
  - image_path: /assets/images/index/fedoo/fedoo_ipc_indentation.mp4
    poster: /assets/images/index/fedoo/fedoo_ipc_indentation.png
    alt: "Stiff disk progressively indenting a soft plate, von Mises stress field"
    title: "Contact with IPC"
    excerpt: "Robust **incremental potential contact** (IPC) via the `ipctk` backend — barrier-method, intersection-free, **frictional or frictionless** contact for indentation, self-contact and lattice compression. The disk-on-plate example here is validated against the Hertzian half-space solution."
    url: "https://3mah.github.io/fedoo-docs/"
    btn_label: "Read more"
    btn_class: "btn--primary"

microgen_morph:
  - image_path: /assets/images/index/microgen/microgen_morph.mp4
    alt: "Continuous morphing through eleven TPMS surface families"
    title: "Continuous morphing between TPMS families"
    excerpt: "Blend any two TPMS surface functions with a tanh weight to walk continuously through families: **gyroid → Schwarz P → Schwarz D → Neovius → Schoen IWP → Schoen FRD → Fischer-Koch S → PMY → honeycomb → Lidinoid → split P → gyroid**. The animated transition exposes the underlying surface-function arithmetic of microgen."
    url: "https://3mah.github.io/microgen-docs/"
    btn_label: "Read more"
    btn_class: "btn--primary"

microgen_row:
  - image_path: /assets/images/logo_microgen/microgen_logo.png
    alt: "microgen"
    title: "microgen"
    excerpt: "A **Python library for microstructure generation and meshing**: TPMS, lattices, polycrystals and hybrid architectures, exported to CAD or directly to periodic FE meshes."
    url: "https://3mah.github.io/microgen-docs/"
    btn_label: "microgen docs"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/microgen/gyroid_graded.png
    alt: "Graded TPMS"
    title: "Graded TPMS & lattices"
    excerpt: "Generate **gyroids, Schwarz, Schoen** and other triply periodic minimal surfaces, with spatially graded thickness and mapping onto arbitrary CAD bodies."
    url: "https://3mah.github.io/microgen-docs/"
    btn_label: "See example"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/microgen/examples/voronoi_polycrystal.mp4
    poster: /assets/images/index/microgen/examples/voronoi_polycrystal.png
    alt: "Voronoi polycrystal grains assembling one by one"
    title: "Polycrystals & architectured cells"
    excerpt: "**Voronoi** polycrystals, octet-truss lattices, honeycombs and hybrid architectures, ready for periodic homogenization in fedoo or Abaqus."
    url: "https://3mah.github.io/microgen-docs/"
    btn_label: "Read more"
    btn_class: "btn--primary"

cta_row:
  - title: "Team"
    excerpt: "Meet the researchers and labs behind 3MAH."
    url: "/team/"
    btn_label: "About the team"
    btn_class: "btn--inverse"
  - title: "Gallery"
    excerpt: "Explore simulations and renderings produced with the 3MAH stack."
    url: "/gallery/"
    btn_label: "Open gallery"
    btn_class: "btn--inverse"
---

{% include feature_row id="intro" type="center" %}

## simcoon — Constitutive modeling & micromechanics
{: .brand-simcoon}

{% include feature_row id="simcoon_row" %}

<figure class="showcase showcase--simcoon">
  <p class="showcase__title">Parameter identification from cyclic experiments</p>
  <p class="showcase__lede">
    Identify <strong>seven Chaboche parameters</strong> — initial yield σ_y,
    Voce isotropic hardening (Q, b) and two non-linear Armstrong-Frederick
    backstresses (C₁, D₁, C₂, D₂) — from <strong>three cyclic uniaxial
    tests</strong> at increasing strain amplitudes. simcoon's
    <strong>EPCHA</strong> UMAT is the forward model, driven through
    <code>sim.solver</code>; the new <code>simcoon.identify</code> module
    wraps SciPy's differential evolution with a key-based file-templating
    workflow that generalises to any optimiser or external simulator.
  </p>
  <video class="showcase__video"
         src="/assets/images/index/simcoon/simcoon_chaboche_identification.mp4"
         poster="/assets/images/index/simcoon/simcoon_chaboche_identification.png"
         autoplay loop muted playsinline preload="metadata"
         aria-label="Differential-evolution iterations converging onto three experimental cyclic stress-strain curves"></video>
  <p class="showcase__caption">
    EPCHA UMAT · E = 140 GPa, ν = 0.3 (fixed) · 7 parameters identified ·
    cost = NMSE-per-response, balanced across the three tests · optimiser:
    <code>scipy.optimize.differential_evolution</code> (popsize 15, maxiter 80,
    seed 42) · final cost ≈ 8 × 10⁻³.
  </p>
</figure>

## fedoo — Nonlinear finite element analysis
{: .brand-fedoo}

{% include feature_row id="fedoo_row" %}

<figure class="showcase showcase--fedoo">
  <p class="showcase__title">Nonlinear and finite-strain mechanics</p>
  <p class="showcase__lede">
    Plastic buckling of a thin tube under axial compression — 2D <strong>axisymmetric</strong>
    model with <strong>updated-Lagrangian</strong> finite strain,
    <strong>self-contact</strong>, and a simcoon <strong>EPICP</strong>
    elasto-plastic UMAT. Line-search Newton with adaptive stiffness drives
    the tube from undeformed to fully folded in a single nonlinear solve.
  </p>
  <div class="showcase__grid showcase__grid--cols-3">
    <figure class="showcase__cell">
      <img class="showcase__img"
           src="/assets/images/index/fedoo/fedoo_tube_initial.png"
           alt="Undeformed tube — initial configuration">
      <p class="showcase__subcaption"><strong>Initial</strong></p>
    </figure>
    <figure class="showcase__cell">
      <video class="showcase__video"
             src="/assets/images/index/fedoo/fedoo_tube_evolution.mp4"
             poster="/assets/images/index/fedoo/fedoo_tube_initial.png"
             autoplay loop muted playsinline preload="metadata"
             aria-label="Tube buckling evolution from undeformed to fully folded under axial compression"></video>
      <p class="showcase__subcaption"><strong>Evolution</strong></p>
    </figure>
    <figure class="showcase__cell">
      <a href="https://3mah.github.io/fedoo-docs/examples/03-advanced/tube_compression.html">
        <img class="showcase__img"
             src="/assets/images/index/fedoo/fedoo_tube_final.png"
             alt="Fully folded tube — final accordion-like configuration with equivalent plastic strain field">
      </a>
      <p class="showcase__subcaption"><strong>Final</strong></p>
    </figure>
  </div>
  <p class="showcase__caption">
    E = 200 GPa · σ_y = 300 MPa · power-law isotropic hardening
    <code>σ = σ_y + k·p<sup>m</sup></code> (k = 1000, m = 0.3) ·
    240 axial elements · 3D revolution from the axisymmetric solution ·
    field shown: equivalent plastic strain p.
  </p>
</figure>

{% include feature_row id="fedoo_contact" type="left" %}

## microgen — Microstructure generation & meshing
{: .brand-microgen}

{% include feature_row id="microgen_row" %}

<figure class="showcase showcase--microgen">
  <p class="showcase__title">Graded and periodic meshes</p>
  <p class="showcase__lede">
    microgen drives <strong>Gmsh</strong> and <strong>MMG</strong> from
    Python to deliver two complementary mesh styles for architectured
    materials: <strong>graded</strong> structures with spatially varying
    thickness, and seamlessly <strong>periodic</strong> unit cells ready
    for periodic-homogenisation BCs in fedoo or Abaqus.
  </p>
  <div class="showcase__grid">
    <figure class="showcase__cell">
      <a href="https://3mah.github.io/microgen-docs/">
        <img class="showcase__img"
             src="/assets/images/index/microgen/microgen_hero.png"
             alt="Spatially graded gyroid with the conforming triangular mesh visible across the gradient">
      </a>
      <p class="showcase__subcaption">
        <strong>Graded</strong> — tanh-graded gyroid, thickness varying along x.
      </p>
    </figure>
    <figure class="showcase__cell">
      <a href="https://3mah.github.io/microgen-docs/">
        <img class="showcase__img"
             src="/assets/images/index/microgen/microgen_periodic.png"
             alt="A single TPMS unit cell tiled three by two showing seamless periodicity across cell boundaries">
      </a>
      <p class="showcase__subcaption">
        <strong>Periodic</strong> — unit cell tiled 3 × 2, no seam visible.
      </p>
    </figure>
  </div>
  <p class="showcase__caption">
    Open CASCADE / CadQuery for geometry · Gmsh for the conforming
    triangulation · MMG for adaptive remeshing · exported as <code>.vtk</code>
    /<code>.msh</code> for fedoo, Abaqus and others.
  </p>
</figure>

{% include feature_row id="microgen_morph" type="right" %}

## From microstructure to simulation

The same Kelvin (truncated-octahedron) unit cell is generated and meshed with **microgen**, exported as a conforming periodic mesh, then loaded directly into **fedoo** to run a periodic homogenization with **simcoon** constitutive models. One workflow, three libraries — geometry, mesh and simulation kept in lock-step.

<figure class="half">
  <a href="/microgen/"><img src="/assets/images/index/fedoo/fedoo_kelvin_mesh.png" alt="Kelvin RVE - conforming periodic mesh from microgen"></a>
  <a href="/fedoo/"><img src="/assets/images/index/fedoo/fedoo_periodic_homog.png" alt="Kelvin RVE - periodic homogenization with fedoo"></a>
  <figcaption>Same Kelvin unit cell — left: periodic conforming mesh from microgen; right: periodic homogenization (shear E<sub>YZ</sub>, σ<sub>YZ</sub> field) in fedoo.</figcaption>
</figure>

{% include feature_row id="cta_row" %}
