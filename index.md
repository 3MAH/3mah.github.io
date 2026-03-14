---
layout: splash
header:
#  overlay_color: "#000"
#  overlay_filter: "0.5"
  overlay_image: /assets/images/layout_index2.jpg
  cta_label: "Download"
  cta_url: "https://github.com/3MAH/"
excerpt: "A set of scientific tools that render simulation in mechanics of materials and multiphysics easy. Open source, it is perfect to conduct research in the field of mechanics, thermomechanics with a focus on non-linear response, homogeneization of heterogeneous materials, composites and smart materials."
intro:
- excerpt: 'The 3MAH set brings together three complementary tools: **Simcoon**, a C++ library with Python bindings for constitutive modeling and multiphysics simulation; **fedOO**, a Python Finite Element solver with emphasis on model reduction, non-linear analysis and homogenization; and **Microgen**, a Python library for microstructure generation and meshing. Together, they provide a complete workflow from CAD to simulation for mechanics of materials research.'
feature_row:
  - image_path: assets/images/index/constitutive.png
    alt: "Constitutive Models"
    title: "Constitutive Models"
    excerpt: "Develop your own **constitutive model** or use one of the many out-of-the-box models."
    url: "https://3mah.github.io/simcoon-docs/"
    btn_label: "Read More"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/homogenization.png
    alt: "Homogenization"
    title: "Homogenization"
    excerpt: "Obtain **effective properties** using Micromechanics or Periodic Homogenization tools."
    url: "https://3mah.github.io/fedoo-docs/"
    btn_label: "Read More"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/optimization.png
    alt: "Identification"
    title: "Identification"
    excerpt: "Get **material parameters** using optimization algorithms."
    url: "https://3mah.github.io/simcoon-docs/"
    btn_label: "Read More"
    btn_class: "btn--primary"
feature_row2:
  - image_path: /assets/images/index/architectured.png
    alt: "Architectured materials"
    title: "Architectured materials"
    excerpt: 'Get the most out of Architectured materials. Apply periodic boundary conditions to obtain effective properties and non-linear response to loading conditions you define.'
    url: "https://3mah.github.io/fedoo-docs/examples/03-advanced/3D_periodic_BC_off_axis.html"
    btn_label: "See Example"
    btn_class: "btn--primary"
feature_row3:
  - image_path: /assets/images/index/identification.png
    alt: "Parameter identification"
    title: "Parameter identification"
    excerpt: 'Set up a parameter identification workflow, using gradient-based or genetic algorithms.'
    url: "https://3mah.github.io/simcoon-docs/"
    btn_label: "Read More"
    btn_class: "btn--primary"
---

{% include feature_row id="intro" type="center" %}

<a href='https://mybinder.org/v2/gh/3MAH/CSMA2022/HEAD'> <img alt='binder' src='https://mybinder.org/badge_logo.svg' width='200' > </a>

{% include feature_row %}

{% include feature_row id="feature_row2" type="left" %}

{% include feature_row id="feature_row3" type="right" %}
