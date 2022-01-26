---
title: "Documentation - Home"
permalink: /docs/3-Home/
excerpt: "3MAH documentation"
last_modified_at: 2022-01-26T16:51:00-04:00
---

## Microgen


## Simcoon
[[Installation|01-Simcoon-installation.md]]
[[Quick start guide|02-Simcoon-quick-start-guid.md]]
[[Tutorials|03-Simcoon-tutorials.md]]


## FedOO
[[Tutorials|04-fedOO-tutorials.md]]



## How to install these softwares

The fastest way to install the softwares shown above is to use *conda* package management system that is available with [[Anaconda|https://docs.continuum.io/anaconda/install/]] or [[Miniconda|https://docs.conda.io/en/latest/miniconda.html]] (Miniconda is sufficient as it comes with conda package management and environment management systems)

To avoid any conflicts between package dependencies it is safer to create a new conda environment:

{% highlight sh %}

conda create -n 3MAH

{% endhighlight %}

To work inside this environment, it has to be activated: 

{% highlight sh %}

conda activate 3MAH

{% endhighlight %}

The next step is to install the desired package. If you want to install the three softwares of 3MAH team:

{% highlight sh %}

conda install -c conda-forge -c cadquery -c set3mah microgen simcoon fedoo

{% endhighlight %}

For Microgen only:

{% highlight sh %}

conda install -c conda-forge -c cadquery -c set3mah microgen

{% endhighlight %}

For Simcoon only:

{% highlight sh %}

conda install -c conda-forge -c set3mah simcoon

{% endhighlight %}

For fedOO only:

{% highlight sh %}

conda install -c conda-forge -c set3mah fedoo

{% endhighlight %}
