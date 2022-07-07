---
title: "About"
layout: splash
permalink: /microgen/
excerpt: "Microgen is a simple python libraries that helps to generate and mesh Representative Unit Cells"
intro:
  - image_path: /assets/images/logo_microgen/microgen_logo.png
    excerpt: 'Microgen is a simple python libraries that helps to generate and mesh Representative Unit Cells.'
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
last_modified_at: 2018-01-10T11:22:24-05:00
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/3MAH/microgen)
[![build-and-test workflow](https://github.com/3MAH/microgen/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/3MAH/microgen)
[![Anaconda-Server Badge](https://anaconda.org/set3mah/microgen/badges/installer/conda.svg)](https://conda.anaconda.org/set3mah)
[![PyPI version](https://badge.fury.io/py/microgen.svg)](https://pypi.org/project/microgen/1.0/)
[![Documentation Status](https://readthedocs.org/projects/microgen/badge/?version=latest)](https://microgen.readthedocs.io/en/latest/?badge=latest)


Here are the main features:

* microgen is entirely written in Python 3 and based on CadQuery and PyVista libraries
* It allows to generate simple reinforcement geometries (spheres, cylinder, ellipsoids, ...) to generate virtual composites microstructures
* Three-dimensional Voronoi tessellation rallons to simulate the response granular materials and polycrystalline metals
* Regular mesh and periodic mesh are implemented using gmsh


<p align="center">
  <img src="/assets/images/about/gyroid.gif" height=250alt="Gyroid"/>
</p>

<p align="center">
  <img src="/assets/images/about/fischerKoch.gif" alt="TPMS"/>
</p>


Microgen is dedicated to parametric geometrical definition of structures applied to mechanical simulations. It has a lot of exciting features! You can see below that triply periodic surfaces and volumes are very easy to represent for FEM simulation or 3D printing
Microgen’s objective is to represent, with an easy-to-learn python scripting approach, any CAD-compatible surface and volume and be able to easy perform parametric analysis.

Also, several geometrical operations are included (repetition, boolean, slicing, etc..). Microgen heavily relies on Cadquery (Python wrapper for Opencascade) and PyVista (python vtk visualisation library).
Microgen facilitates the generation of meshes using GMSH, allowing periodic meshes if the geometry is periodic. It also wraps the very good [MMG remeshing software](https://www.mmgtools.org) developed at INRIA.

This software is totally compatible with our FEA software [FedOO](https://github.com/3MAH/fedoo), to perform non-linear (geometrical and material) homogenization for mechanical, thermal and very soon thermo-mechanical problems. It can also be utilised with other FEA solutions such as Abaqus, Ansys, Salome, Fenics, Zebulon, ...


{% include gallery id="layouts_gallery" caption="Main microstructures obtained using the microgen library `Neovius TPMS`, `Voronoi tessellation of polycristals`, and `Gyroid surfaces`." %}
