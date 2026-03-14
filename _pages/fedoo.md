---
title: "fedOO"
layout: splash
permalink: /fedoo/
excerpt: "fedOO is a free open source Finite Element library developed in Python, designed for mechanical and thermal simulations of heterogeneous materials."
intro:
  - image_path: /assets/images/logo_fedoo/fedoo_logo.png
    excerpt: 'fedOO is a Python Finite Element library, highly tunable with emphasis on model reduction (PGD, AI-based models). It balances speed and ease-of-use, and integrates a non-linear solver with tools to facilitate homogenization techniques and multiscale modelling.'
    url: "https://3mah.github.io/fedoo-docs/"
    btn_label: "View Documentation"
    btn_class: "btn--primary"
layouts_gallery:
  - url: /assets/images/about/fedooBeams.png
    image_path: /assets/images/about/fedooBeams.png
    alt: "Simulation of an assembly of beams"
  - url: /assets/images/about/sigxyyarns.png
    image_path: /assets/images/about/sigxyyarns.png
    alt: "Simulation of damage in composite materials (yarns shown) using Periodic boundary conditions and PGD model reduction"
  - url: /assets/images/about/shearPerio.png
    image_path: /assets/images/about/shearPerio.png
    alt: "Simulation of periodic architectured materials response using Periodic boundary conditions"
last_modified_at: 2026-03-12
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

Here are the main features:

* Entirely written in Python 3 with an emphasis on readable, maintainable code
* Implicit Finite Element solver for static and dynamic problems
* Resolution of problems based on separated decomposition (PGD, POD, Reduced bases)
* Integration with the Simcoon library for finite strain constitutive laws
* Supports 2D, 3D, beam, plate, and cohesive elements
* Contact analysis in 2D and 3D, including self-contact
* Geometric non-linearities
* Periodic boundary conditions and automatic tangent matrix extraction for homogenization
* Multi-point constraint support for complex boundary conditions
* Embedded results visualization using the PyVista library
* Mesh import/export from msh (GMSH) and vtk formats
* Export results in vtk format for easy visualisation with [Paraview](https://www.paraview.org/)

[View full documentation](https://3mah.github.io/fedoo-docs/){: .btn .btn--info .btn--large}
[Back to 3MAH](https://3mah.github.io/){: .btn .btn--inverse .btn--large}

{% include gallery id="layouts_gallery" caption="Examples of Finite Element simulations using fedOO: `Beam network`, `damage in composites`, and `architectured materials`." %}
