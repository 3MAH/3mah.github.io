---
title: "Documentation"
layout: single
permalink: /documentation/
last_modified_at: 2018-01-10T11:22:24-05:00
toc: true
---

The documentation of the latest version of simcoon can be found here: 
 <a href="https://simcoon.readthedocs.io/en/latest/">Simcoon documentation</a>.

## History of API of simcoon

### v1.9.0
The new version of `simcoon` has been released! It includes many new features, notably:
- New functions for finite strain, especially to define objective stress rates (Jaumann, Green-Naghdi)
- Generation of Periodic boundary conditions for Thermal-Mechanical studies of periodic Unit Cells (boxes)
- Tests for regular contitutive models and identification tools

### v1.8
Added the possibility/examples to develop an Abaqus UMAT with the simcoon API

### v1.7
Added thermomechanical couplings of viscoelastic materials (Prony series or Zener with N branches)

### v1.6
Added thermomechanical couplings for most basic constitutive models, except N-branches viscoelasticity

### v1.5
Added tools for the definition of Abaqus input files automatically: steps, materials and sections

### v1.4
Added tools for the generation of periodic boundary condition for parallelepipedic unit cells, considering non-periodic meshes.

### v1.3
Added tools for the generation of periodic boundary condition for parallelepipedic unit cells

### v1.2
Addition of Finite strain functions the API

### v1.1
Addition of thermomechanical constitutive laws for:
* elasticity, plasticity, phase transformation (shape memory alloys)

### v1.0 
Stable version of simcoon that contained the followinf features: 
* Non-linear solver working with infinitesimal strains
* constitutive equations for elasticity, plasticity, viscoelasticity, phase transformation (shape memory alloys)
* identification tool
* micromechanical algorithms and periodic layers

### v0.9 
First release of simcoon: Basic features from the former 'smartplus' library 
