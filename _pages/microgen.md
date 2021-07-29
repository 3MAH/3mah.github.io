---
title: "About"
layout: splash
permalink: /microgen/
excerpt: "Microgen is a simple python libraries that helps to generate and mesh Representative Unit Cells"
intro:
  - image_path: /assets/images/logo_microgen/microgen_logo.png
    excerpt: 'Microgen is a simple python libraries that helps to generate and mesh Representative Unit Cells.'
layouts_gallery:
  - url: /assets/images/about/coupled_cons_models.png
    image_path: /assets/images/about/coupled_cons_models.png
    alt: "Coupled constitutive models"
  - url: /assets/images/about/micromechanics.png
    image_path: /assets/images/about/micromechanics.png
    alt: "micromechanial (Mori-Tanaka) scheme for the analysis of composites response"
  - url: /assets/images/about/DIC_map.png
    image_path: /assets/images/about/DIC_map.png
    alt: "Digital Image Correlation - multiaxial strain field"
last_modified_at: 2018-01-10T11:22:24-05:00
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

Here are the main features:

* microgen is entirely written in Python 3
* It allows to generate simple reinforcement geometries (spheres, cylinder, ellipsoids) to generate virtual composites microstructures
* Three-dimensional Voronoi tessellation rallons to simulate the response granular materials and polycrystalline metals
* Regular mesh and periodic mesh is implemented using gmsh

{% include gallery id="layouts_gallery" caption="Main features of the simcoon library `Constitutive models`, `Multi-scale models`, and `Identification and analyses`." %}
