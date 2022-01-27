---
title: "Quick-Start Guide"
permalink: /docs/s-quick-start-guide/
excerpt: "How to quickly get started with Simcoon."
last_modified_at: 2021-06-07T08:48:05-04:00
redirect_from:
  - /theme-setup/
---

Simcoon has been developed as a API platform to help engineers and researchers in mechanics to develop constitutive models and numerical simulations. You could go the the [**Gallery** page]({{ "/gallery/" | relative_url }}) to see some examples of how Simcoon is utilized.

## Simcoon first steps

We first import *simmit* (the python simulation module of simcoon) and *numpy* 

{% highlight python %}
import numpy as np
from simcoon import simmit as sim
{% endhighlight %}

Then, suppose we would like to compute the stiffness tensor (in the form of a 6x6 matrix) of a linear elastic material, providing the Young's modulus $$ E $$ and the Poisson's ratio $$ \nu $$:

{% highlight python %}
E = 70000.0
nu = 0.3
L = sim.L_iso(E,nu,"Enu")
print np.array_str(L, precision=4, suppress_small=True)
{% endhighlight %}

Conversely, one can ask Simcoon to output he material properties, providing s stiffness tensor:

{% highlight python %}
x = sim.L_iso_props(L)
print(x)
{% endhighlight %}

Simcoon can also check the symetries of a provided stiffness tensor and ouput the set of material parameter, if a specific symmetry has been found:

{% highlight python %}
d = sim.check_symetries(L)
print(d['umat_type'])
print(d['props'])
{% endhighlight %}

## Simcoon tutorial

Probably the first thing you would like to do with Simcoon is to simulate the mechanical response corresponding of a simple tension test, considering an elastic isotropic material:

We first import *simmit* (the python simulation module of simcoon) and *numpy* 

{% highlight python %}
import numpy as np
from simcoon import simmit as sim
{% endhighlight %}

Next we shall define the material constitutive law to be utilized and the associated material properties. We will pass them as a numpy array:

{% highlight python %}

umat_name = 'ELISO' #This is the 5 character code for the elastic-isotropic subroutine
nstatev = 1 #The number of scalar variables required, only the initial temperature is stored here to consider the thermal expansion if temperature changes.

E = 700000. #The Young modulus
nu = 0.2 #The Poisson coefficient
alpha = 1.E-5 #The coefficient of thermal expansion

#Three Euler angles to represent the material orientation with respect to the reference basis (in which the loading is expressed)
psi_rve = 0.
theta_rve = 0.
phi_rve = 0.

#Solver_type define the solver strategy (only a classical newton scheme is actually implemeted for now), and the corate_type define the type of corotational spin rate (0 for Jauman, 1 for Green-Naghdi, 2 for logarithmic)
solver_type = 0
corate_type = 2

props = np.array([E, nu, alpha])
{% endhighlight %}

The last part of the script is to define, if wanted, the location of the data input files (i.e., to define the loading path), and the results outut file and location:

{% highlight python %}
path_data = 'data'
path_results = 'results'
pathfile = 'path.txt'
outputfile = 'results_ELISO.txt'
{% endhighlight %}

The last part is to define the loading path. Further details about this file is given in the <a href="https://simcoon.readthedocs.io/en/latest/">Simcoon documentation</a>, but for instance you could just create a folder 'data' and create a text file named 'path.txt' with the following inside:

{% highlight sh %}
#Initial_temperature
293.5
#Number_of_blocks
1

#Block
1
#Loading_type
1
#Control_type(NLGEOM)
1    
#Repeat
1
#Steps
1

#Mode
1
#Dn_init 1.
#Dn_mini 0.1
#Dn_inc 0.01
#time
30.
#mechanical_state
E 0.01 
S 0 S 0
S 0 S 0 S 0
#temperature_state
T 293.5
{% endhighlight %}

The latter correspond to a pure strain-controlled tension test in the direction *1* up to 1% strain, at the temperature 293.5K.

You can now run your just created python file (you could also create a jupyter notebook, or run the notebook ELISO.ipynb that you can find in the examples). You will now find in the 'results' folder a file named *results_ELISO.txt*. Have a look at the existing notebook or in the documentation to know how to analyse the result file. The documentation of the latest version of simcoon can be found here: 
 <a href="https://simcoon.readthedocs.io/en/latest/">Simcoon documentation</a>.
