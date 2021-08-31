---
title: "Installation"
permalink: /docs/installation/
excerpt: "How to install Simcoon within a condo environment."
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


**Please note:** Make sure you activate your environment before running any python code that invoke Simcoon.
{: .notice--info}
