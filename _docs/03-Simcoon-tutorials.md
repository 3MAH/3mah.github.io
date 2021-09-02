---
title: "Tutorials"
permalink: /docs/tutorials/
excerpt: "Tutorials for the main Simcoon features."
last_modified_at: 2019-08-20T21:36:18-04:00
---

**Please note:** Make sure you activate your environment before running any python code that invoke Simcoon.
{: .notice--info}

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

In this tutorial we will study the evolution of the mechanical properties of a composite material considering spherical reinforcement. 
Elastic prperties will be evaluated depending on the volume fraction of reinforcement (up to 50% volume fraction).

The following elastic properties for the matrix is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$
The following elastic properties for the reinforcement is considered: $$E = 2250$$ MPa, $$\nu = 0.19$$

The first thing we want to do is to add a file in a 'data' folder, named 'Nellipsoids0.dat'. This file can be downloaded here:

| Number | Coatingof | umat | save | c | psi_mat | theta_mat | phi_mat | a1 | a2 | a3 | psi_geom | theta_geom | phi_geom | nprops | nstatev | props
|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|---------|-------|--------|
| 0 | 0  | ELISO | 1 | 0.8 | 0. | 0. | 0. | 1 | 1 | 1 | 0. | 0. | 0. | 3 | 1 | 2250 | 0.19 | 0. |
| 1 | 0  | ELISO | 1 | 0.2 | 0. | 0. | 0. | 1 | 1 | 1 | 0. | 0. | 0. | 3 | 1 | 73000 | 0.19 | 0. |

{% highlight python %}

import pandas as pd
import matplotlib.pyplot as plt
from simcoon import simmit as sim
import os

{% endhighlight %}
