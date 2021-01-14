#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 22:02:40 2020

@author: aaron
"""

import argparse
import os
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import random
from sklearn.cluster import KMeans
import numpy as np

# Read in stand polygons
#STANDS = '/Users/aaron/Desktop/temp/snf_stands_subset.shp'

# Outdata location
#OUTFILE = "/Users/aaron/Desktop"

# Command line args
parser = argparse.ArgumentParser(description='Process command line arguments.')
parser.add_argument("-i", "--input", help = "input filename")
parser.add_argument("-o", "--output", help = "output filename")
args = parser.parse_args()


def plot_size(row):
    """
    -input is a single polygon
    -Determines the number of plots per acre
    -returns the number of plots per acres
    """
    acres = row["geometry"].area  * 0.000247105 # Get area in acres
    
    if acres <= 15:
        return 3
    elif 20 >= acres >15:
        return 4
    elif 25 >= acres > 20:
        return 5       
    elif 35 >= acres > 25:
        return 6     
    elif 45 >= acres > 35:
        return 7     
    elif 55 >= acres > 45:
        return 8     
    elif 65 >= acres > 55:
        return 9     
    elif 75 >= acres > 65:
        return 10                     
    elif 85 >= acres > 75:
        return 11     
    elif 95 >= acres > 85:
        return 12     
    elif 105 >= acres > 95:
        return 13     
    elif 115 >= acres > 105:
        return 14         
    elif acres > 115:
        return 15      

def random_points_in_polygon(number, polygon):

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
    # Negative buffer 
    neg_buffer = row['geometry'].buffer(-20.1168)
    
    # Generate 1000 random points in each polygon
    points = random_points_in_polygon(1000, neg_buffer)
    points_gdf = gpd.GeoDataFrame(points)
    points_gdf.rename(columns = {0:'geometry'}, inplace = True)
    # points_gdf.set_crs(epsg=26915)
    return points_gdf

def cluster_points(points_gdf, size):
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
    # Calculate centroids
    dissolved_clusters = gdf_cluster.dissolve(by='cluster')
    centroids = dissolved_clusters.representative_point() #Make sure centroid is within polygon
    
    # Append centroids to centroids_gdf
    empty_list.append(centroids)
    
def post_process(centroids_l, STANDS, OUTFILE):
    # Flatten list of centroids
    points_flattened = [item for sublist in centroids_l for item in sublist]
    
    # Convert list of centroids to geodataframe and rename geometry column
    centroids_gdf = gpd.GeoDataFrame(points_flattened)
    centroids_gdf.rename(columns = {0:'geometry'}, inplace = True)
    # centroids_gdf.set_crs(epsg=26915, inplace=True)
    
    # Assign polygon ID to centroids
    result = gpd.sjoin(centroids_gdf, STANDS, how = 'inner', op = 'intersects')
    result.set_crs(epsg=26915, inplace=True)
    
    # Write to file
    result.to_file(OUTFILE, layer='plots', driver="GPKG")
        
def main(STANDS, OUTFILE):
    # Read in shapefile as geopandas df
    STANDS = gpd.read_file(STANDS)
    
    # Populate this empty list with cluster centroids
    centroids_l = []
    
    counter = 1
    
    # Loop through each row in the STANDS DF
    for i, row in STANDS.iterrows():
        
        # Determine number of clusters based on polygon area
        size = plot_size(row)
    
        # Generate 1000 random points in negative buffer polygon
        random_points_gdf = random_points(row)
    
        # Cluster points
        clusters = cluster_points(random_points_gdf, size)
      
        # Calculate point cluster centroids
        cluster_centroids(clusters, centroids_l)
        
        counter += 1
        print(f"{counter} of {len(STANDS)}")
        
    # Convert list of cluster centroids to GDF then to geopackage
    post_process(centroids_l, STANDS, OUTFILE)

if __name__ == "__main__":        
        main(args.input, args.output)
            

        
    


