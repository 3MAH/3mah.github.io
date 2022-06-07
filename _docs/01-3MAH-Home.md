---
title: "Documentation - Home"
permalink: /docs/3-Home/
excerpt: "3MAH documentation"
last_modified_at: 2022-01-26T16:51:00-04:00
---

## Microgen
- [Overview](/docs/m-overview)

- [Installation](/docs/m-installation/)

- [Create conda package](/docs/m-create-package/)


## Simcoon
- [Installation](/docs/s-installation/)

- [Quick-start-guide](/docs/s-quick-start-guide/)

- [Tutorials](/docs/s-tutorials/)

- [Create conda package](/docs/s-create-package/)


## FedOO
- [Tutorials](/docs/f-tutorials/)

- [Create conda package](/docs/f-create-package/)



## How to install these softwares

The fastest way to install the softwares shown above is to use *conda* package management system that is available with [Anaconda](https://docs.continuum.io/anaconda/install/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda is sufficient as it comes with conda package management and environment management systems)

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
