---
title: "Microgen"
layout: splash
permalink: /microgen/
excerpt: "Microgen is a Python library designed to facilitate microstructure generation and meshing."
intro:
  - image_path: /assets/images/logo_microgen/microgen_logo.png
    excerpt: 'Microgen is a Python library designed to streamline microstructure generation and mesh creation. It leverages Open CASCADE (via CadQuery) and VTK (using PyVista) for geometry generation, Neper for 3D tessellation, GMSH for mesh generation, and MMG for remeshing.'
    url: "https://3mah.github.io/microgen-docs/"
    btn_label: "View Documentation"
    btn_class: "btn--primary"
layouts_gallery:
  - url: /assets/images/about/neovius_sheet.png
    image_path: /assets/images/about/neovius_sheet.png
    alt: "Neovius triply periodic minimal surface (sheet part)"
  - url: /assets/images/about/voronoi500.png
    image_path: /assets/images/about/voronoi500.png
    alt: "Random polycrystalline texture (500 polyhedral grain, Voronoi tesselation)"
  - url: /assets/images/about/gyroid_points.png
    image_path: /assets/images/about/gyroid_points.png
    alt: "Gyroid triply periodic minimal surfaces : definition of surfaces"
last_modified_at: 2026-03-12
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/3MAH/microgen)
[![build-and-test workflow](https://github.com/3MAH/microgen/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/3MAH/microgen)
[![Anaconda-Server Badge](https://anaconda.org/set3mah/microgen/badges/installer/conda.svg)](https://conda.anaconda.org/set3mah)
[![PyPI version](https://badge.fury.io/py/microgen.svg)](https://pypi.org/project/microgen/)
[![Documentation](https://img.shields.io/badge/docs-microgen-blue?style=for-the-badge)](https://3mah.github.io/microgen-docs/)


Here are the main features:

* **Lattice structures**: Generation of lattice structures such as octet trusses and honeycombs through repeated unit cells
* **TPMS**: Triply Periodic Minimal Surfaces (TPMS)-based lattice generation, known for favorable physical (mechanical, thermal) properties like low density and large surface area
* **Virtual composites**: Generation of basic reinforcement geometries, including spheres, cylinders, ellipsoids, and more
* **Voronoi tessellation**: 3D Voronoi tessellation for simulation of granular materials and polycrystalline metals (using Neper)
* **Mesh generation**: Regular and periodic meshing using GMSH, and remeshing using MMG

<p align="center">
  <img src="/assets/images/about/gyroid.gif" alt="Gyroid" width="49%"/>
  <img src="/assets/images/about/fischerKoch.gif" alt="TPMS" width="49%"/>
</p>

<p align="center">
  <img src="/assets/images/about/shell.png" alt="Shell" width="49%"/>
  <img src="/assets/images/about/beams.png" alt="Beams" width="49%"/>
</p>

Microgen is dedicated to parametric geometrical definition of structures applied to mechanical simulations. Triply periodic surfaces and volumes are easy to represent for FEM simulation or 3D printing. Microgen's objective is to represent, with an easy-to-learn Python scripting approach, any CAD-compatible surface and volume and be able to easily perform parametric analysis.

Several geometrical operations are included (repetition, boolean, slicing, etc.). Microgen heavily relies on CadQuery (Python wrapper for Open CASCADE) and PyVista (Python VTK visualisation library). It facilitates the generation of meshes using GMSH, allowing periodic meshes if the geometry is periodic. It also wraps the [MMG remeshing software](https://www.mmgtools.org) developed at INRIA.

This software is compatible with [fedOO](https://3mah.github.io/fedoo-docs/) for non-linear (geometrical and material) homogenization for mechanical, thermal and thermo-mechanical problems. It can also be utilised with other FEA solutions such as Abaqus, Ansys, Salome, FEniCS, Zebulon, etc.

[View full documentation](https://3mah.github.io/microgen-docs/){: .btn .btn--info .btn--large}
[Back to 3MAH](https://3mah.github.io/){: .btn .btn--inverse .btn--large}

{% include gallery id="layouts_gallery" caption="Main microstructures obtained using the Microgen library: `Neovius TPMS`, `Voronoi tessellation of polycrystals`, and `Gyroid surfaces`." %}
