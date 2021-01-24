# generate_plots
Repository for the USFS plots project.

The purpose of this repository:
- Generate uniformly distributed plots (points) in forest stand polygons. 
- Plots are generated based on the size of the forest stand (acres). 
- No plot can be within 66 ft (1 chain) of a polygon boundary.

![alt text](https://github.com/redfoxgis/generate_plots/blob/main/plots_screenshot.png)

## Environment settings
### Installing anaconda
`anaconda` is a repository containing popular packages. The good thing about `anaconda` is that it is cross-platform.

For installing `anaconda`, please check its [website](https://www.anaconda.com/distribution/).
After installing `anaconda`, we need to create a development environment (if there exists already a development environment, then no need to create a new one). Use the following command to create a new development environment:
```shell
conda create --name ENVNAME python=x.x
```
Then we need to activate the environment by using
```shell
conda activate yourenvname
```
Having activated the environment, the following dependencies need to be installed:

* geopandas (0.8.1+): `conda install geopandas`
* sklearn (0.24.0+):  `conda install scikit-learn`
* tqdm (4.56.0+):     `conda install tqdm`

Other dependencies such as `gdal`, `shapely`, `pandas`, and `numpy` will be installed during the `geopandas` and `sklearn` installs.

## How to run
If not already done, activate the conda environment created above
```shell
conda activate geopandas
```

In the shell, specify the python script, input polygon data (forest stands) and the output shapefile (.shp) or geopackage (.gpkg) path and name of the plots
```shell
python ./stand_plots.py -i '/path/to/input_polygon_data.shp' -o '/path/to/plots.gpkg'
```
