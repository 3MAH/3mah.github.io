---
title: "Simcoon"
layout: splash
permalink: /simcoon/
excerpt: "Simcoon is a free, open-source C++ library for simulating multiphysics systems, with emphasis on constitutive modeling for heterogeneous materials."
intro:
  - image_path: /assets/images/logo_simcoon/simcoon_logo_text.png
    excerpt: 'Simcoon is a scientific library built to facilitate the analysis of mechanics of materials. It provides a C++ API with Python bindings, designed to help researchers implement modern material behavior models for Finite Element Analysis packages. Built on Armadillo and FTensor for high-performance tensor operations.'
    url: "https://simcoon.readthedocs.io/"
    btn_label: "View Documentation"
    btn_class: "btn--primary"
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
last_modified_at: 2026-03-12
toc: false
classes: wide
---

{% include feature_row id="intro" type="left" %}

Here are the main features:

* Simcoon provides both a C++ and a Python API for flexibility and accessibility
* Built on the Armadillo linear algebra library and FTensor for advanced tensor operations, providing a balance between speed and ease of use
* Thermomechanical solver for material point analysis and composite effective property prediction
* Constitutive models for anisotropic elasticity, plasticity, viscoelasticity, and phase transformation
* Handles geometric non-linearities with multiple strain measures (Lagrangian, Eulerian, cumulative strains) and spin options (Jaumann, Green-Naghdi, logarithmic)
* Extensive libraries for continuum mechanics functions, homogenization techniques, and micromechanics schemes
* Built-in identification software using hybrid genetic-gradient algorithms
* Can be used as a standalone solver or coupled to FEA packages (Abaqus, Ansys, etc.)

[View full documentation](https://simcoon.readthedocs.io/){: .btn .btn--info .btn--large}
[Back to 3MAH](https://3mah.github.io/){: .btn .btn--inverse .btn--large}

{% include gallery id="layouts_gallery" caption="Main features of the Simcoon library: `Constitutive models`, `Multi-scale models`, and `Identification and analyses`." %}
