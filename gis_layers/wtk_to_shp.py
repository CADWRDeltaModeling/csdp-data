# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 16:07:29 2025

@author: smunger
"""

# %%
import pandas as pd
import geopandas as gpd
from shapely import wkt
import os

def wkt_to_shapefile(input_file, output_file, geom_type="line", crs="EPSG:26910"):
    """
    Convert a WKT file to a shapefile.
    
    Parameters
    ----------
    input_file : str
        Path to the WKT input file
    output_file : str
        Path to the output shapefile (.shp)
    geom_type : str
        "line" or "point" (for channels or nodes)
    crs : str
        Coordinate reference system (default EPSG:4326)
    """
    
    # --- Case 1: Node file (id;wkt format) ---
    if geom_type == "point":
        # Read table with id and WKT
        df = pd.read_csv(input_file, sep=";")
        df["geometry"] = df["wkt"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df.drop(columns=["wkt"]), geometry="geometry", crs=crs)
    
    # --- Case 2: Channel file (just a WKT geometry) ---
    elif geom_type == "line":
        df = pd.read_csv(input_file, sep=";")
        df["geometry"] = df["wkt"].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(df.drop(columns=["wkt"]), geometry="geometry", crs=crs)
    
    else:
        raise ValueError("geom_type must be 'line' or 'point'")
    
    # Save shapefile
    gdf.to_file(output_file, driver="ESRI Shapefile")
    print(f"✅ Shapefile saved: {output_file}")

# Example usage
wkt_to_shapefile("channels_SDG_20251001.wkt", "channels_SDG_20251001.shp", geom_type="line", crs="EPSG:26910")
wkt_to_shapefile("nodes_SDG_20251001.wkt", "nodes_SDG_20251001.shp", geom_type="point", crs="EPSG:26910")


