# Generate Uniformly Distributed Plots
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
After installing `anaconda`, we need to create a development environment (if there is already a development environment, then no need to create a new one). Use the following command to create a new development environment:
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
conda activate ENVNAME
```

In the shell, specify the python script, input polygon data (forest stands) and the output shapefile (.shp) or geopackage (.gpkg) path, name of the output plots, and any flags:
```shell
python ./stand_plots.py -i /path/to/input_polygon_data.shp -o /path/to/plots.gpkg -r 10 20 30 50 100 -p 1 2 3 4 5 10 -u acres -b 10
```
The following flags are available:

`-i` The input forest stand (polygon) data
`-o` The output plot (point) data. Valid output formats include shapefile (.shp) and geopackage (.gpkg)
`-r` A list of range values to help determine how many plots will be assigned for each forest stand polygon. For example `-r 10 20 30 50 100` would translate to:

    Range Values
      0 - 10
    >10 - 20
    >20 - 30
    >30 - 50
    >50 - 100
    >100
    
`-p` A list of the number of plots associated with each range of values. For example, `-p 1 2 3 4 5 10` would translate to:

    Range Values    Plots
      0 - 10          1
    >10 - 20          2
    >20 - 30          3
    >30 - 50          4
    >50 - 100         5
    >100              10
    
`-u` The units used for the range values: acres or hectares. `default = acres`.
`-b` A buffer distance in map units used to ensure plot points are not within a certain distance from the polygon edge. `default = 0`
