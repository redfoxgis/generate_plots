# generate_plots
Repository for the USFS plots project.

The purpose of this repository:
- Generates uniform plots (points) in forest stand polygons. 
- Plots are generated based on the size of the forest stand (acres). 

## Environment settings
### Installing anaconda
`anaconda` is a repository containing popular packages. The good thing about `anaconda` is that it is cross-platform.

For installing `anaconda`, please check its [website](https://www.anaconda.com/distribution/).
After installing `anaconda`, we need to create a development environment (if there exists already a development environment, then no need to create a new one). Use the following command to create a new development environment:

`conda create -n yourenvname python=x.x anaconda`

Then we need to activate the environment by using

`conda activate yourenvname`

Having activated the environment, the following dependencies need to be installed:

* geopandas (0.8.1+): `conda install geopandas`
* sklearn (0.24.0+):  `conda install scikit-learn`
* tqdm (4.56.0+):     `conda install tqdm`

Other dependencies such as `gdal`, `shapely`, `pandas`, and `numpy` will be installed during the `geopandas` and `sklearn` installs.

## How to run
Activate the conda environment created above
`conda activate geopandas`

In the command prompt, specify the input polygon data (forest stands) and the output geopackage path and name of the plots
`python ./stand_plots.py -i '/path/to/input_polygon_data.shp' -o '/path/to/plots.gpkg'`
