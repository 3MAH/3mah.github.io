---
title: "About"
layout: splash
permalink: /fedoo/
excerpt: "Simcoon is a scientific library built to facilitate the analysis of mechanics of materials. It is built on the top of Armadillo, a high quality C++ linear algebra library. It integrates several algorithms for the analysis of heterogeneous materials Enjoy!"
intro:
  - image_path: /assets/images/logo_fedoo/fedoo_logo.png
    excerpt: 'fedOO is a Python library for Finite Elements, highy tunable with emphasis on model reduction (PGD, AI-based models). It has a designed balance between speed and ease-of-use. fedOO integrates a non-linear sover, and tools to faciitate integration of homogenization techniques and multiscale modelling.'
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
last_modified_at: 2018-01-10T11:22:24-05:00
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

Here are the main features:

* FEDOO is entirely written in Python 3
* Resolution of problems based on a separated decomposition (PGD, POD, Reduced bases)
Static and Dynamics poblems
* Mesh import/export from msh (GMSH) and vtk format
* Export results in vtk file for easy visualisation with Paraview (https://www.paraview.org/)
* Constitutive equation library including elasto-plastic law, composites law, ...
* Include many type of elements like cohesive elements, 2D, 3D, beam, ...
* Geometrical non linearities
* And many other....

{% include gallery id="layouts_gallery" caption="Main features of the simcoon library `Constitutive models`, `Multi-scale models`, and `Identification and analyses`." %}
