---
title: "Installation"
permalink: /docs/m-installation/
excerpt: "How to install Microgen within a conda environment."
last_modified_at: 2022-01-27T16:51:00-04:00
---

## How to install Microgen

The easiest way to install Microgen is to create a *conda* environnement (for the installation of an environment called "3MAH"):

{% highlight sh %}

conda create -n 3MAH

{% endhighlight %}

To activate the environment: 

{% highlight sh %}

conda activate 3MAH

{% endhighlight %}

The next step is to install Microgen:

{% highlight sh %}

conda install -c conda-forge -c cadquery -c set3mah microgen

{% endhighlight %}

Microgen is now installed.