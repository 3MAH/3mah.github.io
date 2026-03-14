---
title: "Gallery"
layout: single
permalink: /gallery/
toc: false
classes: wide
author_profile: true
author : Yves Chemisky
---

## Physics-Informed Graph Neural Networks for Local Field Reconstruction

A Physics-Informed Graph Neural Network (PIGNN) approach is proposed to reconstruct local displacement and stress fields in heterogeneous materials undergoing finite strain hyperelasticity. By embedding physical constraints directly into the neural network architecture, the method provides accurate full-field predictions while respecting the underlying mechanics. This work demonstrates the potential of combining graph-based learning with continuum mechanics for efficient computational homogenization.

{% include figure image_path="/assets/images/gallery/2025_PIGNN.png" caption="Architecture of the Physics-Informed Graph Neural Network: the physical mesh is encoded into a latent graph via node and edge encoders, message passing steps propagate information across the graph, and the node decoder reconstructs the local output field (stress, displacement)." %}

*M.R. Guevara Garban, Y. Chemisky, M. Clément, É. Prulière — International Journal for Numerical Methods in Engineering, 126(24), e70193, 2025.*

---

## FE-LSTM: Accelerating Multiscale Simulations of Architectured Materials

FE-LSTM is a hybrid approach that combines Recurrent Neural Networks (Long Short-Term Memory networks) with Finite Element Analysis to accelerate multiscale simulations of architectured materials. The trained LSTM surrogate replaces expensive microscale FE computations at each integration point, dramatically reducing computational cost while maintaining accuracy for complex non-linear path-dependent material responses.

{% include figure image_path="/assets/images/gallery/2024_FE_LSTM.png" caption="FE-LSTM hybrid workflow: at each macroscopic time increment, the strain increment is localized to the microscopic RVE. Instead of a full FE resolution, the trained LSTM network predicts the homogenized stress and tangent matrix, which are passed back to the macroscopic solver." %}

*A. Danoun, E. Prulière, Y. Chemisky — Computer Methods in Applied Mechanics and Engineering, 429, 117192, 2024.*

---

## Thermodynamically Consistent Recurrent Neural Networks for Dissipative Materials

This work develops thermodynamically consistent Recurrent Neural Networks capable of predicting the non-linear behavior of dissipative materials under non-proportional loading paths. By embedding thermodynamic principles (such as the Clausius-Duhem inequality) into the network architecture, the model ensures physically meaningful predictions even for complex cyclic and multiaxial loading histories not seen during training.

{% include figure image_path="/assets/images/gallery/2022_TCRNN.png" caption="Comparison of LSTM predictions (dashed red) against reference test data (solid blue) for the tangent moduli components under non-proportional loading. The network accurately captures the evolution of all components of the tangent operator." %}

*A. Danoun, E. Prulière, Y. Chemisky — Mechanics of Materials, 173, 104436, 2022.*

---

## TPMS-Based and Strut-Based Lattices for Biomedical Applications

A numerical investigation of the effective mechanical properties and local stress distributions of Triply Periodic Minimal Surface (TPMS)-based and strut-based lattice structures for biomedical applications. Using Microgen for geometry generation and fedOO for finite element analysis, this study compares different lattice topologies in terms of stiffness, strength and stress concentration, providing guidelines for the design of bone implants and tissue engineering scaffolds.

{% include figure image_path="/assets/images/gallery/2022_TPMS_lattices.png" caption="Workflow of the numerical investigation: TPMS-based and strut-based unit cell designs are generated, periodic homogenization is applied to compute effective elastic properties and local stress distributions, and stress fields are compared at equivalent stiffness across topologies." %}

*C. Chatzigeorgiou, B. Piotrowski, Y. Chemisky, P. Laheurte, F. Meraghni — Journal of the Mechanical Behavior of Biomedical Materials, 126, 105025, 2022.*

---

## Functional Fatigue Analysis of an SMA Actuator

Simcoon has been utilized to develop a three dimensional constitutive model for structural and functional fatigue of shape memory alloy actuators. It describes the behavior of shape memory alloy actuators undergoing a large number of cycles leading to the development of internal damage and eventual catastrophic failure. Physical mechanisms such as transformation strain generation and recovery, transformation-induced plasticity, and fatigue damage associated with martensitic phase transformation occurring during cyclic loading are all considered within a thermodynamically consistent framework. Fatigue damage in particular is described utilizing a continuum theory of damage. The total damage growth rate has been formulated as a function of the current stress state and the rate of martensitic transformation such that the magnitude of recoverable transformation strain and the complete or partial nature of the transformation cycles impact the total cyclic life as per experimental observations. Simulation results from the model developed are compared to uniaxial actuation fatigue tests at different applied stress levels. It is shown that both lifetime and the evolution of irrecoverable strain are accurately predicted by the developed model.

{% include figure image_path="/assets/images/gallery/2018_Fatigue_SMA.png" caption="Comparison between the evolution of irrecoverable strains in NiTiHf actuators under various isobaric loads (experimental data from Wheeler et al. 2015) with the model simulations: a), b), and c) show comparisons of the evolution of TRIP strains for the calibration stress levels of 200, 400, and 600 MPa, respectively; d) shows an example of a simulation of the evolution of the response of an actuator for the first, 100<sup>th</sup>, 200<sup>th</sup>, and the last 309<sup>th</sup> cycle prior to failure. The blue and red dots correspond to the experimentally measured strains at high and low temperature for the considered cycles, respectively." %}

*Y. Chemisky et al. — International Journal of Fatigue, 2018.*
