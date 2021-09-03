---
title: "Tutorials"
permalink: /docs/tutorials/
excerpt: "Tutorials for the main Simcoon features."
last_modified_at: 2019-08-20T21:36:18-04:00
---

**Please note:** Make sure you activate your environment before running any python code that invoke Simcoon.
{: .notice--info}

The python script and input files for this tutoial can be found [here]():

{% highlight sh %}

conda activate scientific

{% endhighlight %}

To be able to follow these tutorials it is much better to install the ipython environment and a few more libraries:

{% highlight sh %}

conda install ipython
conda install ipykernel
python -m ipykernel install --user --name=scientific
conda install -c conda-forge matplolib matplotlib-inline pandas

{% endhighlight %}

## Composite simulation with mean field methods

**Please note:** Be careful with the data type while you pass numpy arrays. Make sure you define them as dtype='float' unless specified, since they will be interpreted as float by Simcoon, i.e.:
x = np.array([1, 2, 3, 4, 5],  dtype='float')
{: .notice--info}

In this tutorial we will study the evolution of the mechanical properties of a composite material considering spherical reinforcement (sew figure below)

![alt]({{ site.url }}{{ site.baseurl }}/assets/images/tutorials/composite_spheres.png)

Elastic prperties will be evaluated depending on the volume fraction of reinforcement (up to 50% volume fraction).

The following elastic properties for the matrix is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$. The following elastic properties for the reinforcement is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$

The first thing we want to do is to add a file in a 'data' folder, named 'Nellipsoids0.dat'. This file can be downloaded [here](https://raw.githubusercontent.com/3MAH/simcoon/master/tutorials/01A-Composites/data/Nellipsoids0.dat):

| Number | Coatingof | umat | save | c | psi_mat | theta_mat | phi_mat | a1 | a2 | a3 | psi_geom | theta_geom | phi_geom | nprops | nstatev | props
|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|
| 0 | 0  | ELISO | 1 | 0.8 | 0. | 0. | 0. | 1 | 1 | 1 | 0. | 0. | 0. | 3 | 1 | 2250 | 0.19 | 0. |
| 1 | 0  | ELISO | 1 | 0.2 | 0. | 0. | 0. | 1 | 1 | 1 | 0. | 0. | 0. | 3 | 1 | 73000 | 0.19 | 0. |

{% highlight python %}

import numpy as np
from simcoon import simmit as sim

{% endhighlight %}

Next we shall inform the number of internal state variables (if any) at the macroscopic level and the material properties:

{% highlight python %}

nstatev = 0 #None here

nphases = 2 #The number of phases
num_file = 0 #The num of the file that contains the subphases
int1 = 50 #Number of integration points in the long axis
int2 = 50 #Number of integration points in the lat axis
n_matrix = 0 #phase number for the matrix

props = np.array([nphases, num_file, int1, int2, n_matrix],  dtype='float')

{% endhighlight %}

There is a possibility to consider a misorientation between the test frame of reference and the composite material orientation, considering Euler angles with the z-x-z. The stiffness tensor will be returned in the test frame of reference. Also, we shall inform which micrmechanical scheme will be used. Enter umat_name = 'MIMTN' for a Mori-Tanaka scheme and umat_name = 'MISCN' for a self-consistent scheme

{% highlight python %}

psi_rve = 0.
theta_rve = 0.
phi_rve = 0.

umat_name = 'MIMTN'

{% endhighlight %}

We are now ready to run the simulation, get the effective isotropic elastic properties (since both phases are isotropic and the reinforcements are spherical) and print them:

{% highlight python %}

L = sim.L_eff(umat_name, props, nstatev, psi_rve, theta_rve, phi_rve)
p = sim.L_iso_props(L)
print(p)

{% endhighlight %}

The result is a python numpy array containing the material parameters (here two, the Young's modulus and the Poisson ratio):

{% highlight sh %}

[3.29316019e+03 1.91800053e-01]

{% endhighlight %}

**Notice:** Note that despite the Poisson ratio is the same between the two materials, the stiffness mismatch between the two phases lead to a different effective Poisson ratio.
{: .notice--info}




