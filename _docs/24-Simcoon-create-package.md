---
title: "Create Conda package"
permalink: /docs/s-create-package/
excerpt: "How to create Simcoon conda package."
last_modified_at: 2022-01-27T16:51:00-04:00
---

## How to create Simcoon conda package

To build a conda package, a recipe must be written. It consists in creating a meta.yaml file that will tell the building tool several informations such as the dependencies necessary for the package you want to build. It is also necessary to create a build.sh (for Linux and OSx) and/or a bld.bat (Windows) file to list the commands used to compile and/or install the package. These files have been put in the folder conda.recipe.

When the recipe is ready, it is necessary to install the conda-build package :

`conda install conda-build`

To build the package :

`conda-build conda.recipe -c conda-forge`

The first argument of the conda-build command is the folder where to find the conda recipe, then it is necessary to give the channels where to find all the dependencies. The channel conda-forge is a community channel where a lot of packages are hosted. 

A simcoon package works only with a specific python version, it is necessary to create one package per python version. The conda recipe is written in order to build three packages at the same time with python 3.7, 3.8 and 3.9.

When the package is successfully created, a file path is given such as ~/anaconda/conda-bld/linux-64/simcoon-1.0.0-py39hbdda60e_0.tar.bz2

# Upload

To upload this package to the set3mah channel on Anaconda, the anaconda-client package is required :

`conda install anaconda-client`

You must login with your Anaconda login if you have access permissions to the set3mah channel or with the login of set3mah

`anaconda login`

To upload the package on the set3mah channel, you must copy the package file path to paste it in the anaconda upload command :

`anaconda upload ~/anaconda/conda-bld/linux-64/simcoon-1.0.0-py39hbdda60e_0.tar.bz2`

If a package with this name already exists, you can replace it with the --force option :

`anaconda upload ~/anaconda/conda-bld/linux-64/simcoon-1.0.0-py39hbdda60e_0.tar.bz2 --force`