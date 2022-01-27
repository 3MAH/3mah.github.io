---
title: "Installation"
permalink: /docs/s-installation/
excerpt: "How to install Simcoon within a conda environment."
last_modified_at: 2021-08-31T16:51:00-04:00
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

The next step is to install simcoon:

{% highlight sh %}

conda install -c conda-forge -c set3mah simcoon

{% endhighlight %}

Simcoon is now installed.

## To build Simcoon locally

If you need to compile Simcoon on your system, first you need to install the required packages:

{% highlight sh %}

conda install -c conda-forge armadillo boost cgal numpy

{% endhighlight %}

Next, after downloading the simcoon sources in the github repository of [Simcoon](https://github.com/3MAH/simcoon). Unzip the content in a folder.

**Please note:** If you have installed *matplotlib* you shall delete the file
/path/to/anaconda/anaconda3/envs/scientific/lib/python3.7/site-packages/matplotlib-3.4.3-py3.7-nspkg.pth
{: .notice--info}


The last step is to run the installation script:

{% highlight sh %}

sh Install.sh # Linux or OSx
.\Install.bat # Windows (requires Visual Studio 2022)

{% endhighlight %}


**Please note:** Make sure you activate your environment before running any python code that invoke Simcoon.
{: .notice--info}
