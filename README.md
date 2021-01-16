# generate_plots
Repository for the USFS plots project.

The purpose of this repository:
-Generates uniform plots (points) in forest stand polygons. 
-Plots are generated based on the size of the forest stand (acres). 

## Environment settings
### Installing anaconda
`anaconda` is a repository containing popular packages. The good thing about `anaconda` is that it is cross-platform.

For installing `anaconda`, please check its [website](https://www.anaconda.com/distribution/).
After installing `anaconda`, we need to create a development environment (if there exists already a development environment, then no need to create a new one). Use the following command to create a new development environment:

`conda create -n yourenvname python=x.x anaconda`

Then we need to activate the environment by using

`conda activate yourenvname`

Having activated the environment, the following dependencies need to be installed:
