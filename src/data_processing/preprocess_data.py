import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import LineString, MultiLineString
import os

def preprocess_drainage(input_path="data/drainage_raw.gpkg", output_path="data/drainage_clean.gpkg"):
    """
    Cleans and hydrates the raw OSM data.
    """
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return
    
    print(f"Loading {input_path}...")
    gdf = gpd.read_file(input_path)
    
    # 1. Explode MultiLineStrings to LineStrings
    gdf = gdf.explode(index_parts=False)
    
    # Reset index to ensure a clean 1D array of geometries
    gdf = gdf.reset_index(drop=True)
    
    # 2. Keep only relevant columns and add missing ones
    required_cols = ['geometry', 'name', 'waterway', 'man_made']
    existing_cols = [c for c in required_cols if c in gdf.columns]
    gdf = gdf[existing_cols] # GeoPandas keeps geometry automatically if it's the active geometry
    
    # 3. Add default hydrological attributes
    gdf['diameter'] = 0.3 # 300mm default (more sensitive)
    gdf['material'] = 'concrete'
    gdf['status'] = 'active'
    gdf['capacity'] = 0.5 # Lower default capacity
    
    # 4. Filter out very short or invalid segments
    # Use gdf.length directly (GeoPandas property)
    gdf = gdf[gdf.geometry.length > 0.00001] 
    
    # 5. Save cleaned data
    gdf.to_file(output_path, driver="GPKG")
    print(f"Cleaned data saved to {output_path}")
    print(f"Total features: {len(gdf)}")

if __name__ == "__main__":
    preprocess_drainage()
