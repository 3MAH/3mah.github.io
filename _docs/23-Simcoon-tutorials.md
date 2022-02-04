---
title: "Tutorials"
permalink: /docs/s-tutorials/
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

Elastic properties will be evaluated depending on the volume fraction of reinforcement (up to 50% volume fraction).

The following elastic properties for the matrix is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$. The following elastic properties for the reinforcement is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$

### A: Effective properties of the composite with 20% of reinforcement

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

### B: Effective properties of the composite as a function of the reinforcements

### 02: Cubic symmetry and directional stiffness

In this tutorial we will plot the directional stiffness of a cubic material. Make sure first that you have matplotlib installed: 

{% highlight sh %}

conda install -c conda-forge matplolib

{% endhighlight %}

We shall first import the libraries required, i.e. lumpy, matplotlib and simcoon. We also indicate to use $$\LaTeX$$ into the matplotlib plots:

{% highlight python %}

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from simcoon import simmit as sim

{% endhighlight %}


We explore next the possible direction in the three-dimensional space using a unit vector $$\vec{n}$$, and the result is stored into a numpy array:

\$$ \vec{n} = \left( \begin{array}{c}
      \sin (\theta) \cos (\phi) \\
      \sin (\theta) \sin (\phi) \\
      \cos (\theta)
    \end{array} \right) $$

{% highlight python %}
phi = np.linspace(0,2*np.pi, 128) # the angle of the projection in the xy-plane
theta = np.linspace(0, np.pi, 128).reshape(128,1) # the angle from the polar axis, ie the polar angle

n_1 = np.sin(theta)*np.cos(phi)
n_2 = np.sin(theta)*np.sin(phi)
n_3 = np.cos(theta)*np.ones(128)

n = np.array([n_1*n_1, n_2*n_2, n_3*n_3, n_1*n_2, n_1*n_3, n_2*n_3]).transpose(1,2,0).reshape(128,128,1,6)
{% endhighlight %}

Next we are using *Simcoon* to determine the elastic stiffness matrix $$ \mathcal{L} $$ from the cubic stiffness components $$(C_{11}, C_{12}, C_{44})$$ and to invert it to obtain the compliance matrix $$ \mathcal{M} $$:

{% highlight python %}
C11 = 185000.
C12 = 158000.
C44 = 39700.

L = sim.L_cubic(C11, C12, C44, 'Cii')
M = np.linalg.inv(L)
{% endhighlight %}

We write now a numpy array that performs the operation $$\vec{n} \cdot \mathcal{M} \cdot \vec{n}$$ and invert it to obtain the elastic stiffness for all the directions of the vector $$\vec{n}$$. The last operation is to get the components $$(x,y,z)$$ of this stiffness to be able to plot a surface plot:

{% highlight python %}
S = (n@M@n.reshape(128,128,6,1)).reshape(128,128)

E = (1./S)
x = E*n_1
y = E*n_2
z = E*n_3 
{% endhighlight %}

The last part consist in plotting the results into a surface plot and get the nice following picture:

![alt]({{ site.url }}{{ site.baseurl }}/assets/images/tutorials/Dir_stiffness.png)

{% highlight python %}
fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(x, y, z, cmap='hot',c=E)

norm = colors.Normalize(vmin = np.min(E), vmax = np.max(E), clip = False)
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, norm=norm, facecolors=cm.bone(norm(E)),linewidth=0, antialiased=False, shade=False)

#ax.set_xlim(0,20000)
#ax.set_ylim(0,20000)
#ax.set_zlim(0,20000)
ax.set_xlabel(r'$E_x$')
ax.set_ylabel(r'$E_y$')
ax.set_zlabel(r'$E_z$')

scalarmap = cm.ScalarMappable(cmap=plt.cm.bone, norm=norm)
#m.set_array([])
cbar = plt.colorbar(scalarmap)
#cbar.ax.set_yticklabels(['0','1','2','>3'])
cbar.set_label(r'directional stiffness $E$', rotation=270)

plt.show()
{% endhighlight %}

