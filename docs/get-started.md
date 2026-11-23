---
title: Get started
description: Install simcoon, fedoo and microgen with conda or pip, then follow the documentation, tutorials and examples of each library.
hide:
- navigation
---

# Get started

The three libraries are independent Python packages: install only what you need, or the whole stack.
Each library's documentation is the reference for installation details, tutorials, examples and API.

## Install the whole stack

=== "conda (recommended)"

    ```bash
    conda create -n 3mah -c conda-forge -c set3mah python=3.12 simcoon fedoo microgen
    conda activate 3mah
    ```

=== "pip"

    ```bash
    pip install simcoon "fedoo[all]" microgen
    ```

!!! tip "Which one should I use?"

    conda installs the compiled dependencies (BLAS/LAPACK, sparse solvers, mmg) for you, so it is the
    easiest route. pip wheels are available for Linux, macOS (Apple Silicon) and Windows.
    Platform-specific notes (OpenMP, sparse solvers, CAD backend) are in each installation guide below.

## Pick a library

<div class="lib-grid" markdown>

<div class="lib-card lib-card--simcoon" markdown>

### simcoon

Constitutive laws, micromechanics and parameter identification (C++ with Python bindings).

```bash
conda install -c conda-forge -c set3mah simcoon
# or: pip install simcoon
```

- [:octicons-download-16: Installation guide](https://3mah.github.io/simcoon-docs/installation.html)
- [:octicons-book-16: Material point simulation](https://3mah.github.io/simcoon-docs/simulation/index.html)
- [:octicons-image-16: Examples](https://3mah.github.io/simcoon-docs/examples/index.html)
- [:octicons-code-16: C++ API reference](https://3mah.github.io/simcoon-docs/cpp_api/index.html)

</div>

<div class="lib-card lib-card--fedoo" markdown>

### fedoo

Nonlinear finite element analysis in Python, homogenization, contact and model reduction.

```bash
conda install -c conda-forge -c set3mah fedoo
# or: pip install "fedoo[all]"
```

- [:octicons-download-16: Installation guide](https://3mah.github.io/fedoo-docs/stable/install.html)
- [:octicons-book-16: Quick start](https://3mah.github.io/fedoo-docs/stable/quick_start.html)
- [:octicons-image-16: Examples](https://3mah.github.io/fedoo-docs/stable/examples/index.html)
- [:octicons-code-16: User guide](https://3mah.github.io/fedoo-docs/stable/overview.html)

</div>

<div class="lib-card lib-card--microgen" markdown>

### microgen

Microstructure generation and meshing: TPMS, lattices, polycrystals, periodic meshes.

```bash
conda install -c conda-forge microgen
# or: pip install "microgen[cad]"
```

- [:octicons-download-16: Installation guide](https://3mah.github.io/microgen-docs/Install.html)
- [:octicons-book-16: Quick start](https://3mah.github.io/microgen-docs/quick_start.html)
- [:octicons-image-16: Examples](https://3mah.github.io/microgen-docs/examples/index.html)
- [:octicons-code-16: API reference](https://3mah.github.io/microgen-docs/modules.html)

</div>

</div>

## From geometry to simulation

The libraries are designed to be chained:

1. **microgen** generates the microstructure (TPMS, lattice, Voronoi polycrystal…) and exports a
   conforming, periodic mesh (`.vtk` / `.msh`).
2. **fedoo** reads the mesh, applies periodic boundary conditions and solves the nonlinear
   finite element problem.
3. **simcoon** provides the constitutive laws used at each integration point (elasticity, plasticity,
   viscoelasticity, hyperelasticity, phase transformation), through the same UMAT interface as Abaqus.

[:octicons-image-16: Browse all examples](examples.md){ .md-button .md-button--primary }
[:octicons-mark-github-16: Source code on GitHub](https://github.com/3MAH){ .md-button }
