---
title: "Documentation"
layout: single
permalink: /documentation/
last_modified_at: 2018-01-10T11:22:24-05:00
toc: true
---

## How to install Simcoon

The easiest way to install simcoon is to create a *conda* environnement: You can utilize the Anaconda GUI or type:
(for the installation of an environment called "scientific")

{% highlight sh %}

conda create --name scientific

{% endhighlight %}

To activate the environment: 

{% highlight sh %}

conda activate scientific

{% endhighlight %}

The next step is to install the required packages:

{% highlight sh %}

conda install -c conda-forge armadillo conda install -c conda-forge boost conda install -c conda-forge cgal conda install -c conda-forge numpy

{% endhighlight %}

Next, after downloading the simcoon sources in the github repository of [Simcoon](https://github.com/3MAH/simcoon). Unzip the content in a folder and modify the Install.sh source file to look after you conda environnement path:

anacondaloc=/path/to/anaconda/anaconda3/envs/scientific

The last step is to run the installation script:

{% highlight sh %}

sh Install.sh

{% endhighlight %}

##Simcoon tutorial

Proabbly the first thing you would like to do with Simcoon is to simulate the mechanical response corresponding of a simple tension test, considering an elastic isotropic material:

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
