---
permalink: /about/
title: "About"
excerpt: "Simcoon is a scientific library built to facilitate the analysis of mechanics of materials. It is built on the top of Armadillo, a high quality C++ linear algebra library. It integrates several algorithms for the analysis of heterogeneous materials Enjoy!"
intro:
  - image_path: /assets/images/simcoon_logo_small.png
    excerpt: 'Simcoon is a C++ library with emphasis on speed and ease-of-use. Its principle focus is to provide tools to facilitate the implementation of up-to-date constitutive model for materials in Finite Element Analysis Packages. This is done by providing a C++ API to generate user material subroutine based on a library of functions. Also, SMART+ provides tools to analyse the behavior of material, considering loading at the material point level.'
layouts_gallery:
  - url: /assets/images/feature1_index.png
    image_path: /assets/images/feature1_index.png
    alt: "Coupled constitutive models"
  - url: /assets/images/mm-layout-single-meta.png
    image_path: /assets/images/mm-layout-single-meta.png
    alt: "single layout with comments and related posts"
  - url: /assets/images/mm-layout-archive.png
    image_path: /assets/images/DIC_map.png
    alt: "archive layout example"
last_modified_at: 2018-01-10T11:22:24-05:00
toc: true
---

{% include feature_row id="intro" type="left" %}

* Simcoon consists in an Application Programming Interface (API) developped in C++ and exposed in Python. 

* It relies on the high quality linear algebra library C++ library Armadillo. This provides a perfect balance between speed and ease of use 
 
* It can be used as a standalone solver tool for the numerical simulation of material's thermomechanical response, or coupled to Finite Element Analysis (FEA) packages for the simulation of complex structures 

* Provide efficient material constitutive law for anisotropic elasticity, plasticity, viscoélasticity, phase transformation


{% include gallery id="layouts_gallery" caption="Main features of the simcoon library `Constitutive models`, `Multi-scale models`, and `Identification and analyses`." %}
