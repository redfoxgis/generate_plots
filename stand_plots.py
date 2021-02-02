#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:02:40 2020

This program generates uniformly distributed plots within forest stand polygons. 
The number of plots in each forest stand is determined by the size (acres) of the forest stand.

USAGE: 
    python ./stand_plots.py -i '/path/to/input_polygon_data.shp' -o '/path/to/plots.gpkg'

@author: Aaron @ RedFox GIS & Remote Sensing
"""

import argparse
import os
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import random
from sklearn.cluster import KMeans
import numpy as np
from bisect import bisect_left
from tqdm import tqdm

def parse_args():
    # Shell args
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument("-i", "--input", help = "input filename")
    parser.add_argument("-o", "--output", help = "output filename")
    parser.add_argument("-b", "--break_list", nargs='+', type=int, help = "break_list")
    parser.add_argument("-p", "--plot_list", nargs='+', type=int, help = "plot_list")
    args = parser.parse_args()
    return args

def check_data(sr):
    """
    Check the input data for a projected coordinate system and meter units

    Parameters
    ----------
    sr : pyproj.crs.crs.CRS
        spatial reference object

    Raises
    ------
    ValueError
        The tools raises an error of the spatial reference is not projected and units are not in meters

    Returns
    -------
    None.

    """
    if sr.is_projected == False:
        raise ValueError("This tool only allows data in a projected coordinate system")
    if sr.axis_info[0].unit_name != 'metre':
        raise ValueError("This tool only allows data in a projected coordinate system with units as meters")

def plot_size(row, break_values, plot_values):
    """
    Finds the number of plots for a particular stand based off the area.
    Note the area units are based off the input crs

    Parameters
    ----------
    area : float or int
        The value to test (area of a stand polygon)
    break_values : list
        [x,...]
        example:
            [15,20,25,35,45]
            
        translates to:
            
              0-15
            >15-20
            >20-25
            >25-35
            >35-45
            >45
            
    plot_values : list
        [x,...]
        Note there should be 1 more value than the break_values to
        account for the last break range: >x

    Raises
    ------
    ValueError
        The plot_values list should contain 1 more value than the break_values.

    Returns
    -------
    TYPE
        The number of plots for a particular stand.

    """
    
    acres = row["geometry"].area  * 0.000247105 # Get area in acres

    if len(break_values) + 1 == len(plot_values):
    
        i = bisect_left(break_values,int(acres))
        return plot_values[i]
    
    else:
        raise ValueError("The plot_values list should contain 1 more value than the break_values")
        
def random_points_in_polygon(number, polygon):
    """
    Parameters
    ----------
    number : int
        The number of points to be generated in the polygon
    polygon : TYPE
        shapely polygon geometry.

    Returns
    -------
    List
        List of shapely geometries

    """

    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    i= 0
    while i < number:
        point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(point):
            points.append(point)
            i += 1
    return points  # returns list of shapely point

def random_points(row):
    """
    Parameters
    ----------
    row : shapely geometry
        shapely geometry of stand polygon.

    Returns
    -------
    points_gdf : Geodataframe
        A geodataframe of random points in a forest stand polygon

    """
    # Negative buffer 
    neg_buffer = row['geometry'].buffer(-20.1168)
    
    # Generate 1000 random points in each polygon
    points = random_points_in_polygon(1000, neg_buffer)
    points_gdf = gpd.GeoDataFrame(points)
    points_gdf.rename(columns = {0:'geometry'}, inplace = True)
    # points_gdf.set_crs(epsg=26915)
    return points_gdf

def cluster_points(points_gdf, size):
    """
    Parameters
    ----------
    points_gdf : geodataframe
        A geodataframe of random points within a polygon
    size : int
        The number of clusters

    Returns
    -------
    gdf_cluster : geodataframe
        A geodataframe containing clusters of points

    """
    
    # Cluster points
    # https://samdotson1992.github.io/SuperGIS/blog/k-means-clustering/
    x=pd.Series(points_gdf['geometry'].apply(lambda p: p.x))
    y=pd.Series(points_gdf['geometry'].apply(lambda p: p.y))
    xy=np.column_stack((x,y))
    
    kmeans = KMeans(n_clusters = size, init = 'k-means++', random_state = 5,  max_iter=400)
    y_kmeans = kmeans.fit_predict(xy)
    k=pd.DataFrame(y_kmeans, columns=['cluster'])
    gdf_cluster=points_gdf.join(k) #Add the cluster id to points_gdf 
    return gdf_cluster

def cluster_centroids(gdf_cluster, empty_list):
    """
    Parameters
    ----------
    gdf_cluster : geodataframe
        A geodataframe of point clusters
    empty_list : list
        An empty list to append centroids to

    Returns
    -------
    None.

    """
    
    # Calculate centroids
    dissolved_clusters = gdf_cluster.dissolve(by='cluster')
    centroids = dissolved_clusters.representative_point() #Make sure centroid is within polygon
    
    # Append centroids to centroids_gdf
    empty_list.append(centroids)
    
def post_process(centroids_l, STANDS, sr, OUTFILE):
    """
    Clean up centroids list, spatially join attributes from original STANDS polys and write to file

    Parameters
    ----------
    centroids_l : list
        A list of centroids
    STANDS : geodataframe
        A polygon geodatabase of forest stand polygons
    OUTFILE : Geopackage
        The output file in geopackage format

    Returns
    -------
    None.

    """
    
    # Flatten list of centroids
    points_flattened = [item for sublist in centroids_l for item in sublist]
    
    # Convert list of centroids to geodataframe and rename geometry column
    centroids_gdf = gpd.GeoDataFrame(points_flattened)
    centroids_gdf.rename(columns = {0:'geometry'}, inplace = True) # Create (rename) a geometry column
    centroids_gdf.crs = sr # Set crs to utm 15N
    
    # Assign polygon ID to centroids
    result = gpd.sjoin(centroids_gdf, STANDS, how = 'inner', op = 'intersects')
    result.crs = sr
    
    # Write to file
    if os.path.splitext(OUTFILE)[1] == '.gpkg':
        result.to_file(OUTFILE, layer='plots', driver="GPKG")
    elif os.path.splitext(OUTFILE)[1] == '.shp':
        result.to_file(OUTFILE)
    else:
        raise ValueError("This tool only allows Geopackage (.gpkg) and Shapefile (.shp) output")
        
def main(STANDS, OUTFILE, break_values, plot_values):
    # Read in shapefile as geopandas df
    STANDS = gpd.read_file(STANDS)
    sr = STANDS.crs
    
    check_data(sr) # Check to make sure data is projected and units are meters
    
    # Populate this empty list with cluster centroids
    centroids_l = []
    
    # Loop through each row in the STANDS DF
    for i, row in tqdm(STANDS.iterrows(), total=len(STANDS)):
        
        # Determine number of clusters based on polygon area
        size = plot_size(row, break_values, plot_values)
    
        # Generate 1000 random points in negative buffer polygon
        random_points_gdf = random_points(row)
    
        # Cluster points
        clusters = cluster_points(random_points_gdf, size)
      
        # Calculate point cluster centroids
        cluster_centroids(clusters, centroids_l)
        
    # Convert list of cluster centroids to GDF then to geopackage
    post_process(centroids_l, STANDS, sr, OUTFILE)

if __name__ == "__main__":      
    args = parse_args()
    main(args.input, args.output, args.break_list, args.plot_list)