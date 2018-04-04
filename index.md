---
layout: splash
header:
#  overlay_color: "#000"
#  overlay_filter: "0.5"
  overlay_image: /assets/images/layout_index.png
  cta_label: "Download"
  cta_url: "https://github.com/simcoon/simcoon/"
excerpt: "A scientific library that render simulation in mechanics of materials and multiphysics easy. Open source, it is perfect to conduct research in the field of mechanics and mechanobiology of materials, composites and smart materials."
intro: 
- excerpt: 'Simcoon expands the possibilities of the simulation in Mechanics of Materials and merge education, research and industrial requirements with a new, interactive approach. Discover some of the simcoon capabilities below'
feature_row:
  - image_path: assets/images/index/constitutive.png
    alt: "Constitutive Models"
    title: "Constitutive Models"
    excerpt: "Develop your own **constitutive mode** or use one of the many out-of-the-box models."
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/homogenization.png
    alt: "Homogenization"
    title: "Homogenization"
    excerpt: "Obtain **effective properties** using Micromechanics or Periodic Homogenization tools."
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
  - image_path: /assets/images/index/optimization.png
    alt: "Identification"
    title: "Identification"
    excerpt: "Get **material parameters** using optimization algorithms."
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
feature_row2:
  - image_path: /assets/images/unsplash-gallery-image-2-th.jpg
    alt: "placeholder image 2"
    title: "Placeholder Image Left Aligned"
    excerpt: 'This is some sample content that goes here with **Markdown** formatting. Left aligned with `type="left"`'
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
feature_row3:
  - image_path: /assets/images/unsplash-gallery-image-2-th.jpg
    alt: "placeholder image 2"
    title: "Placeholder Image Right Aligned"
    excerpt: 'This is some sample content that goes here with **Markdown** formatting. Right aligned with `type="right"`'
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
feature_row4:
  - image_path: /assets/images/unsplash-gallery-image-2-th.jpg
    alt: "placeholder image 2"
    title: "Placeholder Image Center Aligned"
    excerpt: 'This is some sample content that goes here with **Markdown** formatting. Centered with `type="center"`'
    url: "#test-link"
    btn_label: "Read More"
    btn_class: "btn--primary"
---

{% include feature_row id="intro" type="center" %}

{% include feature_row %}

{% include feature_row id="feature_row2" type="left" %}

{% include feature_row id="feature_row3" type="right" %}

{% include feature_row id="feature_row4" type="center" %}